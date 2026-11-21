
# Comparação dos modelos r1 e r2

## 1. Alteração realizada

Na versão r2, foi corrigido o rótulo do chamado de ID 006.

- Antes: `006,bloqueio de acesso,comum`
- Depois: `006,bloqueio de acesso,urgente`

O manifesto passou a identificar o conjunto como `chamados-v2`.

## 2. Comparação das métricas

| Métrica | Modelo r1 | Modelo r2 |
|---|---:|---:|
| Acurácia | 0.75 (75%) | 1.00 (100%) |
| Recall comum | 1.00 (100%) | 1.00 (100%) |
| Recall urgente | 0.50 (50%) | 1.00 (100%) |

Os dois modelos foram avaliados utilizando a mesma partição fixa de teste.

Hash SHA-256 da partição:

`d5007d67b4b969f16e268c00c6c1fc90ee452d1b5646410be6ae0c229c4d43dd`

## 3. Evidência de restauração

Foi realizado um clone limpo do repositório e restaurada a versão r1 utilizando DVC.

Tag restaurada: `modelo-r1-corrigido-final`

Commit restaurado:

`3cc80b144e1c3db97f3fd6a80356cd6a7904707f`

Hashes SHA-256 verificados na restauração:

| Arquivo | SHA-256 |
|---|---|
| data/chamados.csv | `bc3fd86a3a5f598841a58839a9726d901fa7e8361ffe79c5b43873ad8a1328ac` |
| data/split.csv | `d5007d67b4b969f16e268c00c6c1fc90ee452d1b5646410be6ae0c229c4d43dd` |
| models/model.json | `72a3a67936139a3473838a6dcfa7aae1acb4c23467be1ef1056d51d485b94840` |

## 4. Hashes da versão r2

| Arquivo | SHA-256 |
|---|---|
| data/chamados.csv | `d65ff38c0aa30a00f087112dbcef5bbda8abe1391bdd01a5afbfa547d165fe17` |
| data/split.csv | `d5007d67b4b969f16e268c00c6c1fc90ee452d1b5646410be6ae0c229c4d43dd` |
| models/model.json | `7f9d94ca8dd86ccc8ad90b0839613c61a33e2168bd23bf083a4bbe1375f908ac` |

## 5. Decisão

**Decisão: aceitar o modelo r2 para este exercício.**

A versão r2 melhorou o recall da classe urgente de 50% para 100%, sem reduzir o recall da classe comum, que permaneceu em 100%.
A acurácia também aumentou de 75% para 100%.
Como a partição de teste foi mantida, a comparação permite observar o efeito da correção do rótulo neste conjunto de dados.
Os resultados são favoráveis à versão r2, considerando o critério estabelecido na atividade.

## 6. Conclusão

O versionamento com Git e DVC permitiu registrar as versões dos dados e modelos, comparar os resultados e restaurar uma versão anterior em um clone limpo.
As tags originais do professor foram preservadas. Para identificar a reconstrução corrigida, foram utilizadas tags alternativas.
