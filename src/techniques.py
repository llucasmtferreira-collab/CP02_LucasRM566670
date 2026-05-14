from src.prompt_builder import montar_prompt, adicionar_exemplos, adicionar_cot


def zero_shot(tarefa, input_texto):
    """Monta prompt direto, sem exemplos. Instrução clara + formato de output."""
    prompt = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=tarefa.get("contexto", ""),
        input_dados=input_texto,
        formato_output=tarefa["formato_output"]
    )
    return prompt


def few_shot(tarefa, input_texto, exemplos):
    """Monta prompt com 2-3 exemplos do data/examples.json."""
    prompt_base = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=tarefa.get("contexto", ""),
        input_dados=input_texto,
        formato_output=tarefa["formato_output"]
    )
    return adicionar_exemplos(prompt_base, exemplos)


def chain_of_thought(tarefa, input_texto, passos):
    """Monta prompt com raciocínio explícito passo a passo."""
    prompt_base = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=tarefa.get("contexto", ""),
        input_dados=input_texto,
        formato_output=tarefa["formato_output"]
    )
    return adicionar_cot(prompt_base, passos)


def role_prompting(tarefa, input_texto, persona):
    """
    Usa system prompt com persona detalhada.
    Retorna tupla (system_prompt, user_prompt).
    """
    system_prompt = (
        f"Você é {persona['titulo']}. "
        f"Experiência: {persona['experiencia']}. "
        f"Especialidade: {persona['especialidade']}. "
        f"Tom de voz: {persona['tom']}. "
        f"Limitações: {persona['limitacoes']}."
    )
    user_prompt = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=tarefa.get("contexto", ""),
        input_dados=input_texto,
        formato_output=tarefa["formato_output"]
    )
    return (system_prompt, user_prompt)
