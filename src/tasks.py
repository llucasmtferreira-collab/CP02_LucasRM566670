tarefas = [
    {
        "nome": "classificacao_sentimento",
        "tipo": "classificacao",
        "instrucao": "Classifique o sentimento da mensagem do cliente como POSITIVO, NEGATIVO, NEUTRO ou MISTO.",
        "contexto": "Você está analisando avaliações e mensagens de clientes de um e-commerce.",
        "formato_output": "Responda APENAS com uma das opções: POSITIVO, NEGATIVO, NEUTRO ou MISTO.",
        "exemplos_fewshot": [
            {"input": "Produto chegou antes do prazo, qualidade excelente!", "output": "POSITIVO"},
            {"input": "Veio com defeito e o suporte demorou 10 dias para responder.", "output": "NEGATIVO"},
            {"input": "Entrega no prazo, mas a embalagem estava amassada.", "output": "MISTO"},
        ],
        "passos_cot": [
            "Identifique palavras ou expressões com carga positiva na mensagem",
            "Identifique palavras ou expressões com carga negativa na mensagem",
            "Verifique se há elementos neutros ou factuais sem carga emocional",
            "Compare o peso dos aspectos positivos e negativos",
            "Classifique como POSITIVO, NEGATIVO, NEUTRO ou MISTO conforme predominância",
        ],
        "persona": "analista_cx",
    },
    {
        "nome": "classificacao_urgencia",
        "tipo": "classificacao",
        "instrucao": "Classifique o nível de urgência da mensagem do cliente como ALTA, MEDIA ou BAIXA.",
        "contexto": "Você está triando tickets de suporte de um e-commerce para priorizar atendimento.",
        "formato_output": "Responda APENAS com uma das opções: ALTA, MEDIA ou BAIXA.",
        "exemplos_fewshot": [
            {"input": "Meu cartão foi cobrado duas vezes e preciso do estorno urgente!", "output": "ALTA"},
            {"input": "Gostaria de saber se vocês têm esse produto em outras cores.", "output": "BAIXA"},
            {"input": "Meu pedido foi enviado há 5 dias e ainda não chegou.", "output": "MEDIA"},
        ],
        "passos_cot": [
            "Verifique se há impacto financeiro direto mencionado (cobrança indevida, fraude, estorno)",
            "Verifique se há prazo crítico ou evento dependente da entrega",
            "Avalie o tom emocional — há sinais de desespero ou frustração intensa?",
            "Considere se o problema cresce com o tempo sem resposta",
            "Classifique: ALTA se impacto imediato, MEDIA se crescente, BAIXA se informacional",
        ],
        "persona": "especialista_suporte",
    },
    {
        "nome": "extracao_dados",
        "tipo": "extracao",
        "instrucao": "Extraia as informações estruturadas da mensagem do cliente e retorne em formato JSON.",
        "contexto": "Você está extraindo dados de reclamações de clientes de um e-commerce para alimentar um sistema de CRM.",
        "formato_output": 'Retorne APENAS um JSON com os campos: {"produto": "", "problema": "", "prazo_mencionado": "", "valor": ""}. Use null para campos não mencionados.',
        "exemplos_fewshot": [
            {
                "input": "Comprei um Notebook Dell por R$3.800 há 3 dias e ele chegou com a tela trincada.",
                "output": '{"produto": "Notebook Dell", "problema": "tela trincada", "prazo_mencionado": "3 dias", "valor": "R$3.800"}'
            },
            {
                "input": "O fone de ouvido Sony que pedi parou de funcionar depois de uma semana.",
                "output": '{"produto": "Fone de ouvido Sony", "problema": "parou de funcionar", "prazo_mencionado": "uma semana", "valor": null}'
            },
        ],
        "passos_cot": [
            "Identifique o produto mencionado na mensagem",
            "Identifique o problema ou defeito relatado",
            "Procure por menção de prazo ou data (ex: 'há 3 dias', 'semana passada')",
            "Procure por valor monetário mencionado",
            "Monte o JSON com os campos encontrados, usando null para ausentes",
        ],
        "persona": "analista_cx",
    },
]
