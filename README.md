# PISI_3-2026_01-steam-success-analysis
Data analysis and machine learning project for Steam games success prediction and clustering.

---

## Visão Geral

O projeto é composto por três frentes complementares:

| Etapa | Notebook | Descrição |
|---|---|---|
| **EDA** | `notebooks/EDA/steam_eda.ipynb` | Exploração, limpeza e visualização do dataset Steam |
| **Modelagem Supervisionada** | `notebooks/ML/steam_ml.ipynb` | Classificação de sucesso comercial com Random Forest, Gradient Boosting, Logistic Regression, SVM e SHAP para interpretabilidade |
| **Baseline Pré-lançamento** | `notebooks/ml/prelaunch_success_baseline.ipynb` | Predição de sucesso usando apenas features disponíveis antes do lançamento do jogo |

---

## Estrutura do Repositório

```
PISI_3-2026_01-steam-success-analysis/
│
├── notebooks/
│   ├── EDA/
│   │   └── steam_eda.ipynb              # Análise exploratória
│   └── ML/
│       ├── steam_ml.ipynb               # Pipeline completo de ML
│       └── prelaunch_success_baseline.ipynb  # Modelo de baseline pré-lançamento
│
├── data/
│   ├── raw/                             # Dados brutos (não versionados no Git)
│   └── processed/                       # Dados processados / features engineered
│
├── models/                              # Modelos treinados exportados (.pkl / .joblib)
│
├── reports/
│   └── figures/                         # Gráficos e visualizações gerados
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Tecnologias e Bibliotecas

- **Linguagem:** Python 3.10+
- **Manipulação de dados:** `pandas`, `numpy`, `pyarrow`
- **Visualização:** `plotly`, `matplotlib`
- **Machine Learning:** `scikit-learn`
- **Balanceamento de classes:** `imbalanced-learn` (SMOTE, RandomOverSampler)
- **Interpretabilidade:** `shap`
- **NLP:** `nltk`
- **Persistência de modelos:** `joblib`
- **Download de datasets:** `gdown`

---

## Instalação e Como Executar

> Siga os passos abaixo **na ordem exata**. O uso de ambiente virtual é obrigatório para garantir reprodutibilidade.

### 1. Clone o repositório

```bash
git clone https://github.com/JulioGabrielP/PISI_3-2026_01-steam-success-analysis.git
cd PISI_3-2026_01-steam-success-analysis
```

### 2. Crie o ambiente virtual (VENV)

```bash
# Windows
python -m venv venv

# Linux / macOS
python3 -m venv venv
```

### 3. Ative o ambiente virtual

```bash
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# Linux / macOS
source venv/bin/activate
```

> Após a ativação, o terminal exibirá `(venv)` no início da linha.

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Inicie o Jupyter e abra os notebooks

```bash
jupyter notebook
```

Acesse a pasta `notebooks/` e execute os notebooks **na seguinte ordem recomendada:**

1. `EDA/steam_eda.ipynb`
2. `ML/steam_ml.ipynb`
3. `ml/prelaunch_success_baseline.ipynb`

---

## Pipeline do Projeto

```
Coleta de Dados (Steam API / Kaggle)
        │
        ▼
    EDA & Limpeza
  (steam_eda.ipynb)
        │
        ▼
Feature Engineering
        │
        ├──► Modelagem Supervisionada ──► SHAP Explainability
        │    (steam_ml.ipynb)
        │
        └──► Baseline Pré-lançamento
             (prelaunch_success_baseline.ipynb)
```

---
