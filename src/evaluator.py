import tiktoken
import json


def contar_tokens(texto, modelo="cl100k_base"):
    """Conta tokens do texto via tiktoken."""
    enc = tiktoken.get_encoding(modelo)
    return len(enc.encode(texto))


def medir_acuracia(resposta, esperado):
    """
    Mede acurácia por match exato ou por keywords.
    Retorna 1.0 (acerto), 0.5 (parcial) ou 0.0 (erro).
    """
    resposta_norm = resposta.strip().upper()

    if isinstance(esperado, dict):
        # Para extração: verifica quantos campos batem
        try:
            resp_json = json.loads(resposta.strip())
            acertos = sum(
                1 for k, v in esperado.items()
                if str(resp_json.get(k, "")).strip().upper() == str(v).strip().upper()
            )
            return round(acertos / len(esperado), 2)
        except (json.JSONDecodeError, AttributeError):
            return 0.0
    else:
        esperado_norm = str(esperado).strip().upper()
        if resposta_norm == esperado_norm:
            return 1.0
        if esperado_norm in resposta_norm:
            return 0.5
        return 0.0


def medir_consistencia(respostas):
    """
    Recebe lista de respostas para o mesmo prompt.
    Retorna % de respostas iguais à moda.
    """
    if not respostas:
        return 0.0
    from collections import Counter
    norm = [r.strip().upper() for r in respostas]
    mais_comum = Counter(norm).most_common(1)[0][1]
    return round(mais_comum / len(norm), 2)


def testar_temperatura(prompt, llm_client, temps=None, n_repeticoes=3):
    """
    Testa o mesmo prompt com diferentes temperaturas.
    Retorna lista de dicts com temperatura, consistência e tokens médios.
    """
    if temps is None:
        temps = [0.1, 0.5, 1.0]

    resultados = []
    for temp in temps:
        respostas = []
        tokens_lista = []
        for _ in range(n_repeticoes):
            resultado = llm_client.chat(prompt=prompt, temp=temp)
            respostas.append(resultado["resposta"])
            tokens_lista.append(resultado["tokens_prompt"] + resultado["tokens_resposta"])

        consistencia = medir_consistencia(respostas)
        tokens_medio = round(sum(tokens_lista) / len(tokens_lista))
        resultados.append({
            "temperatura": temp,
            "consistencia": consistencia,
            "tokens_medio": tokens_medio,
            "respostas": respostas
        })

    return resultados
