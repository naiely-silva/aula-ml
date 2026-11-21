# Atividade Prática 07 — Versionamento de Dados e Modelos

Este repositório apresenta a atividade prática de versionamento de dados e modelos utilizando Git, GitHub e DVC.

## Pré-requisitos

- Git instalado.
- Python instalado.
- DVC instalado.
- Acesso ao repositório GitHub.
- Armazenamento dos arquivos DVC disponível.

## 1. Configuração do ambiente

Instale o DVC:

```powershell
python -m pip install dvc
```

Configure o armazenamento local do DVC:

```powershell
python -m dvc remote add -d armazenamento "C:\Users\naiel\Downloads\ativ07\dvc-storage"
```

Caso o armazenamento já esteja cadastrado, atualize o caminho:

```powershell
python -m dvc remote modify armazenamento url "C:\Users\naiel\Downloads\ativ07\dvc-storage"
```

**Observação:** o caminho do armazenamento é específico da máquina. Em outro computador, substitua-o pelo caminho correspondente.

## 2. Clonando o repositório

Clone o projeto:

```powershell
git clone https://github.com/naiely-silva/aula-ml.git
```

Entre na pasta:

```powershell
cd aula-ml
```

Busque as branches e tags:

```powershell
git fetch --all --tags
```

## 3. Restaurando uma versão

Para restaurar a versão do modelo r1 corrigido:

```powershell
git checkout modelo-r1-corrigido-final
```

Configure o armazenamento DVC, caso necessário, e execute:

```powershell
python -m dvc pull
```

Para restaurar a versão do modelo r2 corrigido:

```powershell
git checkout modelo-r2-corrigido
```

Em seguida:

```powershell
python -m dvc pull
```

## 4. Versões corrigidas

As versões corrigidas foram identificadas pelas seguintes tags:

- `dados-v1-corrigido`
- `modelo-r1-corrigido-final`
- `dados-v2-corrigido`
- `modelo-r2-corrigido`

## 5. Organização do projeto

- `data/`: dados e descritores DVC.
- `models/`: modelo treinado e seu descritor DVC.
- `reports/`: métricas, manifesto do modelo e relatório de comparação.
- `src/`: código de treinamento.
- `params.json`: parâmetros utilizados no treinamento.

## 6. Comparação dos modelos

A versão r2 corrigiu o rótulo do chamado de ID 006, alterando sua classificação de `comum` para `urgente`.
Os modelos foram avaliados utilizando a mesma partição fixa de teste.
Os resultados estão documentados em `reports/comparacao.md`.

## 7. Conclusão

O uso de Git e DVC permitiu versionar os dados e modelos, registrar as avaliações, comparar diferentes versões e restaurar uma versão anterior do projeto.
