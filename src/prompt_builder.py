def montar_prompt(instrucao, contexto, input_dados, formato_output):
    if not instrucao:
        raise ValueError("instrucao não pode ser vazia")
    if not input_dados:
        raise ValueError("input_dados não pode ser vazio")
    if not formato_output:
        raise ValueError("formato_output não pode ser vazio")

    partes = [f"INSTRUÇÃO:\n{instrucao}"]
    if contexto:
        partes.append(f"CONTEXTO:\n{contexto}")
    partes.append(f"ENTRADA:\n{input_dados}")
    partes.append(f"FORMATO DE SAÍDA:\n{formato_output}")

    return "\n\n".join(partes)


def adicionar_exemplos(prompt, exemplos):
    """Adiciona exemplos few-shot ao prompt."""
    if not exemplos:
        return prompt
    linhas = ["EXEMPLOS:"]
    for ex in exemplos:
        linhas.append(f'Input: "{ex["input"]}" → Output: "{ex["output"]}"')
    bloco = "\n".join(linhas)
    return bloco + "\n\n" + prompt


def adicionar_cot(prompt, passos):
    """Adiciona instrução de raciocínio passo a passo ao prompt."""
    if not passos:
        return prompt
    numerados = "\n".join(f"{i+1}. {p}" for i, p in enumerate(passos))
    cot = f"Analise passo a passo antes de responder:\n{numerados}"
    return prompt + "\n\n" + cot
