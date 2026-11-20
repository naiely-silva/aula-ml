
import csv
import json
import hashlib
import platform
import sys
import uuid
import subprocess
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path):
    """Calcula o hash SHA256 de um arquivo."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path):
    """Lê um arquivo CSV e retorna uma lista de dicionários."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Uso: python src/train.py <run_id>")

    run_id = sys.argv[1]

    # Lê os parâmetros do projeto.
    with open(ROOT / "params.json", encoding="utf-8") as f:
        params = json.load(f)

    lowercase = params["tokenizer"]["lowercase"]
    strategy = params["tokenizer"]["strategy"]

    # Lê os dados e a divisão treino/teste.
    chamados = read_csv(ROOT / "data" / "chamados.csv")
    split = read_csv(ROOT / "data" / "split.csv")

    particoes = {row["id"]: row["particao"] for row in split}

    treino = [row for row in chamados if particoes[row["id"]] == "train"]
    teste = [row for row in chamados if particoes[row["id"]] == "test"]

    if not treino or not teste:
        raise ValueError("Treino ou teste vazio.")

    # Aprende a classe mais frequente para cada primeira palavra.
    palavras = {}
    todas_classes = Counter(row["classe"] for row in treino)

    for row in treino:
        texto = row["descricao"]
        if lowercase:
            texto = texto.lower()

        if strategy == "first_word":
            palavra = texto.split()[0]
        else:
            raise ValueError("Estrategia de tokenizacao desconhecida.")

        palavras.setdefault(palavra, Counter())
        palavras[palavra][row["classe"]] += 1

    # Treina o classificador.
    modelo = {
        palavra: contador.most_common(1)[0][0]
        for palavra, contador in palavras.items()
    }

    classe_padrao = todas_classes.most_common(1)[0][0]

    def prever(descricao):
        texto = descricao.lower() if lowercase else descricao
        palavra = texto.split()[0]
        return modelo.get(palavra, classe_padrao)

    # Avalia o modelo nos dados de teste.
    corretos = 0
    resultados = []

    for row in teste:
        previsto = prever(row["descricao"])
        real = row["classe"]

        if previsto == real:
            corretos += 1

        resultados.append({
            "id": row["id"],
            "real": real,
            "previsto": previsto,
            "correto": previsto == real
        })

    acuracia = corretos / len(teste)

    # Calcula recall para a classe urgente.
    verdadeiros_positivos = sum(
        1 for r in resultados
        if r["real"] == "urgente" and r["previsto"] == "urgente"
    )

    falsos_negativos = sum(
        1 for r in resultados
        if r["real"] == "urgente" and r["previsto"] != "urgente"
    )

    total_urgentes = verdadeiros_positivos + falsos_negativos
    recall_urgente = (
        verdadeiros_positivos / total_urgentes
        if total_urgentes else 0
    )

    # Salva o modelo.
    (ROOT / "models").mkdir(exist_ok=True)
    with open(ROOT / "models" / "model.json", "w", encoding="utf-8") as f:
        json.dump({
            "palavras": modelo,
            "classe_padrao": classe_padrao,
            "params": params
        }, f, indent=2, ensure_ascii=False)

    # Salva as métricas.
    (ROOT / "reports").mkdir(exist_ok=True)
    metrics = {
        "run_id": run_id,
        "acuracia": acuracia,
        "recall_urgente": recall_urgente,
        "total_teste": len(teste),
        "resultados": resultados
    }

    with open(ROOT / "reports" / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    # Identifica a versão do Git.
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True
    ).strip()

    # Identifica os dados utilizados.
    dataset_id = json.loads(
        (ROOT / "data" / "manifesto.json").read_text(encoding="utf-8")
    )["dataset_id"]

    # Cria o manifesto do modelo.
    model_path = ROOT / "models" / "model.json"
    metrics_path = ROOT / "reports" / "metrics.json"

    manifesto_modelo = {
        "run_id": run_id,
        "dataset_id": dataset_id,
        "git_commit": commit,
        "data_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "sha256_modelo": sha256_file(model_path),
        "sha256_metricas": sha256_file(metrics_path)
    }

    with open(ROOT / "reports" / "modelo.json", "w", encoding="utf-8") as f:
        json.dump(manifesto_modelo, f, indent=2, ensure_ascii=False)

    print("Treinamento concluido!")
    print(f"Run ID: {run_id}")
    print(f"Dataset: {dataset_id}")
    print(f"Acuracia: {acuracia:.2%}")
    print(f"Recall urgente: {recall_urgente:.2%}")


if __name__ == "__main__":
    main()
