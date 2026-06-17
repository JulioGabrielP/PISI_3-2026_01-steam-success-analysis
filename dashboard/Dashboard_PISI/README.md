# Playscope Dashboard 🎮

Plataforma analítica interativa do mercado Steam, desenvolvida como parte de um projeto acadêmico de Ciência de Dados. Construída com **Dash + Plotly + Pandas**, permite explorar livremente um dataset de ~50 mil jogos da Steam por meio de filtros dinâmicos, visualizações interativas e análises de machine learning.

---

## Visão Geral

O dashboard funciona como um mini Business Intelligence do mercado de jogos digitais. Em vez de apresentar análises estáticas, ele oferece uma ferramenta onde o usuário faz suas próprias perguntas sobre os dados e obtém respostas visuais em tempo real — todos os gráficos respondem simultaneamente aos filtros da barra lateral.

O projeto é baseado em um dataset público da Steam disponível no Kaggle e integra as etapas de análise exploratória, clusterização com KMeans e interpretabilidade via SHAP desenvolvidas no trabalho acadêmico original.

---

## Páginas

| Página | O que explora |
|--------|---------------|
| 📊 **Visão Geral** | KPIs do mercado, distribuição de preços, ratings, faturamento por gênero, scatter de reviews e heatmap de correlação de Spearman |
| 🎮 **Engajamento** | Horas jogadas vs. faturamento estimado, engajamento por gênero, preço vs. horas, comparativo Steam Deck, lançamentos por ano |
| 🔬 **Clusterização** | Visualização PCA 2D dos 4 clusters KMeans, radar chart comparativo, perfis, taxa de sucesso e tags por cluster |
| 💰 **Mercado & Preços** | Preço vs. volume de reviews, faturamento por faixa de preço, desconto vs. revenue, distribuição de descontos, top 20 jogos |
| 🧠 **Interpretabilidade** | Importância SHAP das features, comparação dos modelos supervisionados, SHAP summary plot, dependence plots e matriz de confusão |

---

## Filtros Globais

A barra lateral controla todos os gráficos ao mesmo tempo:

- **Gênero / Tag** — filtra por categoria do jogo
- **Faixa de preço** — slider de $0 a $250
- **Avaliação mínima** — positive ratio mínimo
- **Ano de lançamento** — range de 2003 a 2024
- **Clusters** — seleciona quais dos 4 grupos exibir
- **Steam Deck** — compatível / incompatível / todos
- **Sucesso Comercial** — top 20% de faturamento / restante / todos

---

## Estrutura do Projeto

```
playscope_dashboard/
├── dashboard.py                   ← ponto de entrada
├── generate_demo_data.py          ← processa os dados e gera os parquets
├── requirements.txt
├── data/
│   ├── steam_dashboard.parquet    ← dataset principal (~50k jogos)
│   ├── cluster_profile.parquet    ← perfil médio dos 4 clusters
│   ├── shap_importance.parquet    ← importância SHAP das features
│   └── model_results.parquet      ← comparação dos modelos
├── assets/
│   └── style.css                  ← tema dark Steam
├── layouts/                       ← estrutura de cada página (sem lógica)
│   ├── sidebar.py
│   ├── overview.py
│   ├── engagement.py
│   ├── clusters.py
│   ├── pricing.py
│   └── shap_page.py
├── callbacks/                     ← lógica interativa de todos os gráficos
│   ├── theme.py
│   ├── overview_cb.py
│   ├── engagement_cb.py
│   ├── cluster_cb.py
│   ├── pricing_cb.py
│   ├── shap_cb.py
│   └── reset_cb.py
└── utils/
    └── data_loader.py             ← carregamento com cache (lru_cache)
```

---

## Como Rodar

### Pré-requisitos

- Python **3.10** ou superior
- pip atualizado
- Dataset do Kaggle: [Game Recommendations on Steam](https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam)

---

### 1. Clone o repositório

```bash
git clone https://github.com/IgordevBR/Dashboard_PISI.git
cd Dashboard_PISI
```

---

### 2. Crie e ative um ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

Dependências utilizadas:

```
dash==2.17.1
dash-bootstrap-components==1.6.0
plotly==5.22.0
pandas==2.2.2
numpy==1.26.4
pyarrow==16.0.0
scikit-learn==1.5.0
```

---

### 4. Baixe e configure o dataset

O dataset não está incluído neste repositório devido ao tamanho dos arquivos. Você precisa baixá-lo manualmente no Kaggle pelo link indicado nos pré-requisitos.

Após baixar e extrair o `.zip`, você terá uma pasta chamada `archive` com os seguintes arquivos:

```
archive/
├── games.csv
├── games_metadata.json
├── recommendations.csv
└── users.csv
```

Mova essa pasta `archive` para dentro de `playscope_dashboard`, ficando assim:

```
playscope_dashboard/
├── archive/
│   ├── games.csv
│   ├── games_metadata.json
│   ├── recommendations.csv
│   └── users.csv
├── dashboard.py
├── generate_demo_data.py
└── ...
```

---

### 5. Processe os dados

Execute o script de pré-processamento. Ele lê os arquivos da pasta `archive`, aplica a engenharia de features, roda o KMeans K=4 e o PCA, e gera os parquets otimizados na pasta `data/`.

```bash
python generate_demo_data.py
```

> ⚠️ **Atenção:** o arquivo `recommendations.csv` tem cerca de 12 milhões de linhas. O processamento pode levar entre 2 e 5 minutos dependendo da sua máquina. Isso só precisa ser feito uma vez.

Ao terminar, você verá:

```
============================================================
  ✓ Processamento concluído!
  Execute agora: python dashboard.py
  Acesse em:     http://127.0.0.1:8050
============================================================
```

---

### 6. Inicie o dashboard

```bash
python dashboard.py
```

Abra o navegador e acesse:

```
http://127.0.0.1:8050
```

---

## Tecnologias

- [Dash](https://dash.plotly.com/) — framework de aplicações analíticas em Python
- [Plotly](https://plotly.com/python/) — visualizações interativas
- [Pandas](https://pandas.pydata.org/) — manipulação e análise de dados
- [Scikit-learn](https://scikit-learn.org/) — KMeans e PCA
- [PyArrow](https://arrow.apache.org/docs/python/) — formato Parquet para alta performance

---

## Dataset

**Game Recommendations on Steam** — disponível publicamente no Kaggle.

> Kozyriev, Anton. *Game Recommendations on Steam*. Kaggle, 2023.
> https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam

O dataset não está incluído neste repositório devido às limitações de tamanho de arquivo do GitHub. Siga as instruções da seção **Como Rodar** para obtê-lo e configurá-lo localmente.
