# Playscope — Steam Games Analysis

Projeto acadêmico de análise de dados, aprendizado de máquina e processamento de linguagem natural aplicado a jogos e avaliações da plataforma Steam.

O repositório reúne notebooks de exploração e modelagem, arquivos processados e o Dashboard interativo **Playscope**, desenvolvido com Dash e Plotly.

Para conhecer a metodologia, os experimentos, os resultados e as limitações da pesquisa, consulte o artigo do projeto.

---

## Componentes do projeto

O projeto está organizado nas seguintes frentes:

| Componente                   | Descrição                                                                   |
| ---------------------------- | --------------------------------------------------------------------------- |
| **Análise Exploratória**     | Limpeza, transformação e visualização dos dados da Steam                    |
| **Clusterização**            | Identificação de perfis de jogos com K-Means                                |
| **Modelagem Supervisionada** | Experimentos de classificação com dados estruturados                        |
| **Classificação de Reviews** | Classificação textual de avaliações como `Recommended` ou `Not Recommended` |
| **Dashboard Playscope**      | Aplicação interativa para apresentação das etapas da pesquisa               |

---

## Estrutura do repositório

```text
PISI_3-2026_01-steam-success-analysis/
│
├── notebooks/
│   ├── EDA/
│   │   └── steam_eda.ipynb
│   │
│   └── ML/
│       ├── steam_ml.ipynb
│       ├── prelaunch_success_baseline.ipynb
│       └── notebooks de classificação textual
│
├── Dashboard_PISI/
│   ├── assets/
│   ├── callbacks/
│   ├── data/
│   ├── layouts/
│   ├── dashboard.py
│   ├── README.md
│   └── requirements.txt
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
├── reports/
│   └── figures/
│
├── .gitignore
├── README.md
└── requirements.txt
```

A estrutura pode variar ligeiramente conforme a versão final dos notebooks e artefatos gerados.

---

## Tecnologias utilizadas

* Python
* Pandas
* NumPy
* Scikit-learn
* Imbalanced-learn
* NLTK
* SHAP
* Matplotlib
* Plotly
* Dash
* Jupyter Notebook
* Joblib
* PyArrow

---

## Requisitos

* Python 3.10 ou superior
* Git
* Ambiente virtual Python
* Jupyter Notebook ou JupyterLab

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/JulioGabrielP/PISI_3-2026_01-steam-success-analysis.git
cd PISI_3-2026_01-steam-success-analysis
```

### 2. Crie um ambiente virtual

No Windows:

```bash
python -m venv venv
```

No Linux ou macOS:

```bash
python3 -m venv venv
```

### 3. Ative o ambiente virtual

PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Prompt de Comando do Windows:

```cmd
venv\Scripts\activate.bat
```

Linux ou macOS:

```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

Caso o Dashboard possua um arquivo de dependências próprio, execute também:

```bash
pip install -r Dashboard_PISI/requirements.txt
```

---

## Dados

Os conjuntos de dados originais não são mantidos integralmente no repositório devido ao tamanho dos arquivos.

Os principais arquivos utilizados no projeto incluem:

```text
games.csv
recommendations.csv
games_metadata.json
```

Após obter os datasets, coloque-os nos diretórios esperados pelos notebooks, normalmente em:

```text
data/raw/
```

Arquivos processados utilizados pelo Dashboard podem estar localizados em:

```text
Dashboard_PISI/data/
```

Consulte as células iniciais dos notebooks para confirmar os caminhos utilizados em cada etapa.

---

## Execução dos notebooks

Com o ambiente virtual ativado, inicie o Jupyter:

```bash
jupyter notebook
```

Depois, abra a pasta:

```text
notebooks/
```

A ordem geral recomendada é:

1. análise exploratória;
2. modelagem com dados estruturados;
3. baseline reformulado;
4. classificação textual de reviews.

Alguns notebooks podem depender de arquivos processados produzidos por etapas anteriores.

---

## Execução do Dashboard

Acesse a pasta da aplicação:

```bash
cd Dashboard_PISI
```

Execute:

```bash
python dashboard.py
```

Depois, abra no navegador:

```text
http://127.0.0.1:8050
```

O Dashboard contém as seguintes páginas:

| Página                       | Conteúdo                                   |
| ---------------------------- | ------------------------------------------ |
| **Percurso da Pesquisa**     | Visão geral das etapas do projeto          |
| **Análise Exploratória**     | Visualizações dos dados estruturados       |
| **Perfis de Jogos**          | Resultados da clusterização                |
| **Limites da Previsão**      | Discussão metodológica da tarefa comercial |
| **Classificação de Reviews** | Resultados da classificação textual        |

Os filtros laterais são aplicados somente às páginas baseadas nos dados estruturados.

---

## Artigo

A descrição completa da pesquisa, incluindo metodologia, experimentos, resultados e limitações, está disponível no artigo desenvolvido pelo grupo.

Adicione aqui o link ou caminho do documento final:

```text
docs/artigo.pdf
```

---

## Contexto acadêmico

Projeto desenvolvido pelo **Grupo 6** para a disciplina de **Projeto Interdisciplinar para Sistemas de Informação III — PISI III**, no curso de Sistemas de Informação da Universidade Federal Rural de Pernambuco — UFRPE, durante o período 2026.1.
