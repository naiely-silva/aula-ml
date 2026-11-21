
# Atividade Prática 07 — Versionamento de Dados e Modelos

## Pré-requisitos

- Git instalado.
- Python instalado.
- DVC instalado.
- Repositório GitHub do projeto.
- Armazenamento local configurado para os arquivos DVC.

## Configuração do ambiente

Instale o DVC:

```powershell
python -m pip install dvc
```

Configure o armazenamento local:

```powershell
python -m dvc remote add -d armazenamento "C:\Users\naiel\Downloads\ativ07\dvc-storage"
```

Caso o armazenamento já esteja configurado, ajuste o caminho com:

```powershell
python -m dvc remote modify armazenamento url "C:\Users\naiel\Downloads\ativ07\dvc-storage"
```

## Restaurar uma versão do projeto

Clone o repositório:

```powershell
git clone https://github.com/naiely-silva/aula-ml.git
cd aula-ml
git fetch --all --tags
```

Selecione a versão desejada:

```powershell
git checkout modelo-r1-corrigido-final
```

Configure o armazenamento DVC, caso necessário, e restaure os arquivos:

```powershell
python -m dvc pull
```

Para restaurar a segunda versão corrigida:

```powershell
git checkout modelo-r2-corrigido
python -m dvc pull
```

## Versões corrigidas

- dados-v1-corrigido
- modelo-r1-corrigido-final
- dados-v2-corrigido
- modelo-r2-corrigido


## Observação

O caminho do armazenamento DVC é específico da máquina. Em outro computador, configure o caminho correspondente ao armazenamento disponível.
