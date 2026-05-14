# Prompt Toolkit — Lucas Mota Ferreira RM566670

Toolkit de Prompt Engineering em Python que aplica automaticamente as 4 técnicas de prompting (Zero-Shot, Few-Shot, Chain-of-Thought e Role Prompting) a tarefas de e-commerce, compara resultados e recomenda a melhor abordagem.

## Domínio
Análise de mensagens de clientes de e-commerce: classificação de sentimento, classificação de urgência e extração de dados estruturados.

## Técnicas implementadas
- **Zero-Shot** — instrução direta sem exemplos
- **Few-Shot** — instrução com 2-3 exemplos de referência
- **Chain-of-Thought** — raciocínio explícito passo a passo
- **Role Prompting** — persona especializada via system prompt

## Estrutura do projeto
```
CP02_LucasRM566670/
├── main.py                  # Ponto de entrada
├── requirements.txt
├── .env.example
├── src/
│   ├── llm_client.py        # Conexão com Ollama API
│   ├── prompt_builder.py    # Montagem de prompts
│   ├── techniques.py        # 4 técnicas de prompting
│   ├── tasks.py             # Definição das tarefas
│   ├── evaluator.py         # Métricas e avaliação
│   └── report.py            # Geração de tabelas e gráficos
├── data/
│   ├── inputs.json          # 5+ inputs reais por tarefa
│   └── examples.json        # Exemplos para few-shot
├── prompts/
│   ├── system_prompts.json  # Personas para role prompting
│   └── templates.json       # Templates por tipo de tarefa
└── output/
    ├── resultados.csv
    └── graficos/
```

## Requisitos
- Python 3.10+
- [Ollama](https://ollama.com) instalado e rodando localmente com o modelo `gpt-oss:120b`

## Instalação e configuração

### 1. Clone o repositório e crie o ambiente virtual
```bash
git clone <url-do-repo>
cd prompt-toolkit
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o arquivo `.env`
Copie o `.env.example` e ajuste se necessário:
```bash
cp .env.example .env
```
Conteúdo padrão (não precisa alterar se usar Ollama local):
```
OLLAMA_HOST=http://localhost:11434
MODEL=gpt-oss:120b
```

### 4. Certifique-se de que o Ollama está rodando
```bash
ollama serve
ollama pull gpt-oss:120b
```

## Execução
```bash
python main.py
```

O sistema irá:
1. Aplicar as 4 técnicas em 3 tarefas × 5 inputs cada
2. Medir acurácia, tokens e tempo de cada resposta
3. Salvar `output/resultados.csv`
4. Gerar 3 gráficos em `output/graficos/`
5. Exibir recomendação automática da melhor técnica por tarefa
6. Testar consistência com 3 temperaturas diferentes (0.1, 0.5, 1.0)

## Saídas geradas
| Arquivo | Descrição |
|---|---|
| `output/resultados.csv` | Tabela completa com todas as execuções |
| `output/graficos/acuracia.png` | Acurácia média por técnica e tarefa |
| `output/graficos/custo_tokens.png` | Tokens médios por técnica |
| `output/graficos/temperatura.png` | Consistência por temperatura |
