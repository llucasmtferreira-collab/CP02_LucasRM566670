import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT = Path("output")
GRAFICOS = OUTPUT / "graficos"


def gerar_tabela(resultados):
    """Gera DataFrame, imprime no terminal e salva CSV."""
    df = pd.DataFrame(resultados)
    OUTPUT.mkdir(exist_ok=True)
    df.to_csv(OUTPUT / "resultados.csv", index=False)
    print("\n=== TABELA COMPARATIVA ===")
    print(df.to_string(index=False))
    return df


def grafico_acuracia(resultados):
    """Barras agrupadas: acurácia média por técnica e por tarefa."""
    df = pd.DataFrame(resultados)
    GRAFICOS.mkdir(parents=True, exist_ok=True)

    pivot = df.groupby(["tarefa", "tecnica"])["acuracia"].mean().unstack()
    ax = pivot.plot(kind="bar", figsize=(10, 6))
    ax.set_title("Acurácia Média por Técnica e Tarefa")
    ax.set_ylabel("Acurácia (%)")
    ax.set_xlabel("Tarefa")
    plt.xticks(rotation=30, ha="right")
    plt.legend(title="Técnica")
    plt.tight_layout()
    plt.savefig(GRAFICOS / "acuracia.png")
    plt.close()
    print("Gráfico salvo: output/graficos/acuracia.png")


def grafico_custo(resultados):
    """Barras: tokens médios por técnica (custo estimado)."""
    df = pd.DataFrame(resultados)
    GRAFICOS.mkdir(parents=True, exist_ok=True)

    media_tokens = df.groupby("tecnica")["tokens_total"].mean().sort_values()
    ax = media_tokens.plot(kind="bar", figsize=(8, 5), color="steelblue")
    ax.set_title("Custo Médio por Técnica (tokens)")
    ax.set_ylabel("Tokens Médios")
    ax.set_xlabel("Técnica")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(GRAFICOS / "custo_tokens.png")
    plt.close()
    print("Gráfico salvo: output/graficos/custo_tokens.png")


def grafico_temperatura(resultados_temp):
    """Linha: consistência por temperatura."""
    GRAFICOS.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(resultados_temp)
    plt.figure(figsize=(7, 4))
    plt.plot(df["temperatura"], df["consistencia"] * 100, marker="o", linewidth=2)
    plt.title("Consistência por Temperatura")
    plt.xlabel("Temperatura")
    plt.ylabel("Consistência (%)")
    plt.xticks(df["temperatura"])
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(GRAFICOS / "temperatura.png")
    plt.close()
    print("Gráfico salvo: output/graficos/temperatura.png")


def recomendar(resultados):
    """Recomenda a melhor técnica por tarefa com justificativa."""
    df = pd.DataFrame(resultados)
    print("\n=== RECOMENDAÇÃO POR TAREFA ===")
    recomendacoes = []

    for tarefa in df["tarefa"].unique():
        sub = df[df["tarefa"] == tarefa]
        media = sub.groupby("tecnica").agg(
            acuracia_media=("acuracia", "mean"),
            tokens_medio=("tokens_total", "mean")
        )

        melhor = media["acuracia_media"].idxmax()
        acc = media.loc[melhor, "acuracia_media"]
        tok = media.loc[melhor, "tokens_medio"]

        print(f"\nTarefa: {tarefa}")
        print(f"  Melhor técnica : {melhor}")
        print(f"  Acurácia média : {acc:.1f}%")
        print(f"  Tokens médios  : {tok:.0f}")
        print(f"  Justificativa  : Maior acurácia entre as 4 técnicas testadas.")

        recomendacoes.append({
            "tarefa": tarefa,
            "melhor_tecnica": melhor,
            "acuracia_media": round(acc, 2),
            "tokens_medio": round(tok)
        })

    return recomendacoes
