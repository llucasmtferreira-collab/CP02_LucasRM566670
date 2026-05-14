import json
from pathlib import Path
from dotenv import load_dotenv

from src.llm_client import LLMClient
from src.techniques import zero_shot, few_shot, chain_of_thought, role_prompting
from src.evaluator import contar_tokens, medir_acuracia, testar_temperatura
from src.report import gerar_tabela, grafico_acuracia, grafico_custo, grafico_temperatura, recomendar
from src.tasks import tarefas

load_dotenv()

# ── Carregar dados ──────────────────────────────────────────────
with open("data/inputs.json", encoding="utf-8") as f:
    inputs_data = json.load(f)

with open("data/examples.json", encoding="utf-8") as f:
    examples_data = json.load(f)

with open("prompts/system_prompts.json", encoding="utf-8") as f:
    personas = json.load(f)

llm = LLMClient()
resultados = []

# ── Loop principal: tarefa × técnica × input ────────────────────
for tarefa in tarefas:
    nome = tarefa["nome"]
    inputs = inputs_data.get(nome, [])
    exemplos = examples_data.get(nome, [])
    persona = personas.get(tarefa["persona"], {})

    print(f"\n{'='*50}")
    print(f"TAREFA: {nome}")
    print(f"{'='*50}")

    for item in inputs:
        input_texto = item["input"]
        esperado = item["esperado"]

        tecnicas_resultados = {}

        # Zero-Shot
        prompt_zs = zero_shot(tarefa, input_texto)
        res_zs = llm.chat(prompt=prompt_zs)
        tecnicas_resultados["Zero-Shot"] = res_zs

        # Few-Shot
        prompt_fs = few_shot(tarefa, input_texto, exemplos or tarefa.get("exemplos_fewshot", []))
        res_fs = llm.chat(prompt=prompt_fs)
        tecnicas_resultados["Few-Shot"] = res_fs

        # Chain-of-Thought
        prompt_cot = chain_of_thought(tarefa, input_texto, tarefa.get("passos_cot", []))
        res_cot = llm.chat(prompt=prompt_cot)
        tecnicas_resultados["Chain-of-Thought"] = res_cot

        # Role Prompting
        system_rp, user_rp = role_prompting(tarefa, input_texto, persona)
        res_rp = llm.chat(prompt=user_rp, system=system_rp)
        tecnicas_resultados["Role Prompting"] = res_rp

        for tecnica, res in tecnicas_resultados.items():
            acuracia = medir_acuracia(res["resposta"], esperado)
            tokens_total = res["tokens_prompt"] + res["tokens_resposta"]

            print(f"  [{tecnica}] resposta='{res['resposta'].strip()[:60]}' | acc={acuracia} | tokens={tokens_total}")

            resultados.append({
                "tarefa": nome,
                "tecnica": tecnica,
                "input": input_texto[:60],
                "resposta": res["resposta"].strip()[:80],
                "esperado": str(esperado)[:60],
                "acuracia": round(acuracia * 100, 2),
                "tokens_total": tokens_total,
                "tokens_prompt": res["tokens_prompt"],
                "tokens_resposta": res["tokens_resposta"],
                "tempo_ms": res["tempo_ms"],
            })

# ── Relatório ───────────────────────────────────────────────────
print("\n\nGerando relatório...")
df = gerar_tabela(resultados)
grafico_acuracia(resultados)
grafico_custo(resultados)
recomendar(resultados)

# ── Teste de temperatura (melhor técnica da 1ª tarefa) ──────────
print("\n\nTestando temperaturas no melhor prompt...")
primeira_tarefa = tarefas[0]
primeiro_input = inputs_data.get(primeira_tarefa["nome"], [{}])[0].get("input", "")
prompt_teste = zero_shot(primeira_tarefa, primeiro_input)

resultados_temp = testar_temperatura(prompt_teste, llm, temps=[0.1, 0.5, 1.0])
grafico_temperatura(resultados_temp)

print("\n✅ Projeto executado com sucesso!")
print("CSV e gráficos salvos em output/")
