# Playscope Dashboard 🎮

Dashboard interativo desenvolvido para o projeto acadêmico **Steam Success Analysis**, da disciplina de Projeto Interdisciplinar para Sistemas de Informação III.

A aplicação organiza e apresenta as etapas da pesquisa realizada sobre jogos da Steam, reunindo análise exploratória, clusterização, discussão dos limites da previsão comercial e classificação textual de reviews.

O dashboard foi construído com **Dash**, **Plotly**, **Pandas** e **Scikit-learn**.

---

## Páginas

| Página                       | Conteúdo                                                   |
| ---------------------------- | ---------------------------------------------------------- |
| **Percurso da Pesquisa**     | Apresentação das etapas, perguntas e decisões do projeto   |
| **Análise Exploratória**     | Visualizações interativas dos dados estruturados dos jogos |
| **Perfis de Jogos**          | Resultados da clusterização com K-Means                    |
| **Limites da Previsão**      | Revisão metodológica do experimento de previsão comercial  |
| **Classificação de Reviews** | Resultados da classificação textual de avaliações da Steam |

Os filtros laterais são utilizados nas páginas baseadas nos dados estruturados. As páginas **Limites da Previsão** e **Classificação de Reviews** apresentam resultados e discussões próprias, sem utilizar esses filtros.

Os detalhes metodológicos e os resultados completos estão disponíveis no artigo acadêmico do projeto.

---

## Estrutura da aplicação

```text
Dashboard_PISI/
├── assets/
│   └── arquivos de estilo
├── callbacks/
│   └── lógica das visualizações interativas
├── layouts/
│   └── estrutura das páginas
├── utils/
│   └── carregamento e filtragem dos dados
├── dashboard.py
├── generate_demo_data.py
├── requirements.txt
└── README.md
```

Na primeira configuração, também serão utilizadas estas pastas locais:

```text
Dashboard_PISI/
├── archive/    # arquivos originais baixados do Kaggle
└── data/       # arquivos processados gerados pelo script
```

Essas pastas não são fornecidas integralmente pelo GitHub por causa do tamanho dos dados.

---

# Como executar pela primeira vez

## Pré-requisitos

Antes de começar, tenha instalado:

* Git;
* Python 3.10 ou superior;
* pip.

Python 3.10 ou 3.11 é recomendado para maior compatibilidade com as versões registradas no projeto.

---

## 1. Clone o repositório

```bash
git clone https://github.com/JulioGabrielP/PISI_3-2026_01-steam-success-analysis.git
```

Entre na pasta da aplicação:

```bash
cd PISI_3-2026_01-steam-success-analysis/dashboard/Dashboard_PISI
```

Todos os próximos comandos devem ser executados dentro dessa pasta.

---

## 2. Crie um ambiente virtual

### Windows — PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a ativação, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### Windows — Prompt de Comando

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### Linux ou macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instale as dependências

Com o ambiente virtual ativado, execute:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 4. Baixe o dataset

O projeto utiliza o dataset público:

[Game Recommendations on Steam — Kaggle](https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam)

Faça o download do dataset e extraia o arquivo compactado.

Para preparar o dashboard, são necessários estes três arquivos:

```text
games.csv
games_metadata.json
recommendations.csv
```

O arquivo `users.csv`, caso esteja presente no download, não é utilizado pelo script atual do dashboard.

---

## 5. Crie a pasta `archive`

Dentro de `dashboard/Dashboard_PISI`, crie uma pasta chamada:

```text
archive
```

Coloque dentro dela os três arquivos extraídos do Kaggle.

A estrutura deverá ficar exatamente assim:

```text
Dashboard_PISI/
├── archive/
│   ├── games.csv
│   ├── games_metadata.json
│   └── recommendations.csv
├── assets/
├── callbacks/
├── layouts/
├── utils/
├── dashboard.py
├── generate_demo_data.py
├── requirements.txt
└── README.md
```

É importante manter os nomes originais dos arquivos.

---

## 6. Processe os dados

Execute:

```bash
python generate_demo_data.py
```

O script realiza a preparação necessária para o dashboard, incluindo:

* leitura dos jogos;
* associação das tags;
* cálculo da média de horas jogadas;
* criação das variáveis utilizadas nas visualizações;
* clusterização com K-Means;
* projeção bidimensional com PCA;
* geração dos arquivos Parquet.

O arquivo `recommendations.csv` é grande. Por isso, essa etapa pode levar vários minutos e consumir uma quantidade considerável de memória.

Ela precisa ser executada apenas na primeira configuração ou quando os dados precisarem ser gerados novamente.

---

## 7. Verifique os arquivos gerados

Após o processamento, deverá existir uma pasta `data` com estes arquivos:

```text
Dashboard_PISI/
└── data/
    ├── steam_dashboard.parquet
    ├── cluster_profile.parquet
    ├── shap_importance.parquet
    └── model_results.parquet
```

O dashboard depende desses arquivos para carregar seus dados.

Não execute `dashboard.py` antes de concluir essa etapa.

---

## 8. Inicie o dashboard

Execute:

```bash
python dashboard.py
```

Quando o servidor iniciar, abra no navegador:

```text
http://127.0.0.1:8050
```

Para encerrar a aplicação, pressione:

```text
Ctrl + C
```

---

# Execuções posteriores

Depois que a pasta `data` já tiver sido gerada, não será necessário processar novamente o dataset.

Nas próximas execuções, entre na pasta do dashboard, ative o ambiente virtual e execute:

### Windows — PowerShell

```powershell
cd PISI_3-2026_01-steam-success-analysis\dashboard\Dashboard_PISI
.\venv\Scripts\Activate.ps1
python dashboard.py
```

### Linux ou macOS

```bash
cd PISI_3-2026_01-steam-success-analysis/dashboard/Dashboard_PISI
source venv/bin/activate
python dashboard.py
```

---

## Problemas comuns

### O dashboard informa que um arquivo Parquet não foi encontrado

Confirme se você executou:

```bash
python generate_demo_data.py
```

Depois, verifique se os quatro arquivos foram criados dentro de `data/`.

---

### O script informa que `games.csv` não foi encontrado

Confirme se a estrutura está assim:

```text
Dashboard_PISI/archive/games.csv
```

O mesmo vale para:

```text
Dashboard_PISI/archive/games_metadata.json
Dashboard_PISI/archive/recommendations.csv
```

---

### Uma biblioteca não foi encontrada

Ative novamente o ambiente virtual e reinstale as dependências:

```bash
python -m pip install -r requirements.txt
```

---

### O comando `python` não foi reconhecido

No Windows, tente usar:

```powershell
py dashboard.py
```

Para processar os dados:

```powershell
py generate_demo_data.py
```

No Linux ou macOS, tente:

```bash
python3 dashboard.py
```

---

## Tecnologias

* Python
* Dash
* Dash Bootstrap Components
* Plotly
* Pandas
* NumPy
* Scikit-learn
* PyArrow

As versões utilizadas estão registradas no arquivo `requirements.txt`.

---

## Dataset

**Game Recommendations on Steam**
Autor: Anton Kozyriev
Plataforma: Kaggle

Os arquivos originais não são armazenados no repositório devido ao seu tamanho. Cada usuário que configurar o projeto pela primeira vez deverá baixar o dataset e executar o script de processamento.

---

## Contexto acadêmico

O Playscope faz parte do projeto **Steam Success Analysis**, desenvolvido pelo Grupo 6 para a disciplina de Projeto Interdisciplinar para Sistemas de Informação III, no curso de Sistemas de Informação da Universidade Federal Rural de Pernambuco — UFRPE, durante o período 2026.1.
