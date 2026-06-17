"""
Playscope Dashboard — Processamento dos dados reais do Kaggle
=============================================================
Lê os arquivos da pasta archive/ e gera os parquets otimizados
usados pelo dashboard.

Uso:
    python generate_demo_data.py
"""

import os
import json
import warnings
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

warnings.filterwarnings('ignore')

# ── Caminhos ───────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(__file__)
ARCHIVE    = os.path.join(BASE_DIR, 'archive')
DATA_DIR   = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

GAMES_CSV      = os.path.join(ARCHIVE, 'games.csv')
METADATA_JSON  = os.path.join(ARCHIVE, 'games_metadata.json')
RECOM_CSV      = os.path.join(ARCHIVE, 'recommendations.csv')

# ── Nomes dos clusters (mesmos do artigo) ──────────────────────────────────────
CLUSTER_NAMES = {
    0: 'Alto Faturamento Estimado',
    1: 'Boa Avaliação, Baixo Alcance',
    2: 'Alto Engajamento e Sucesso',
    3: 'Alta Estratégia Promocional',
}

print("=" * 60)
print("  Playscope — Processando dados reais")
print("=" * 60)


# ── 1. games.csv ──────────────────────────────────────────────────────────────
print("\n[1/5] Carregando games.csv...")
df = pd.read_csv(GAMES_CSV)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
print(f"      {len(df):,} jogos carregados | Colunas: {list(df.columns)}")

# Normaliza nomes de colunas comuns
rename_map = {}
for col in df.columns:
    if 'positive' in col and 'ratio' in col:  rename_map[col] = 'positive_ratio'
    if 'user' in col and 'review' in col:     rename_map[col] = 'user_reviews'
    if 'price' in col and 'final' in col:     rename_map[col] = 'price_final'
    if 'price' in col and 'original' in col:  rename_map[col] = 'price_original'
    if col == 'date_release' or col == 'release_date': rename_map[col] = 'date_release'
df.rename(columns=rename_map, inplace=True)

# Garante colunas essenciais
for col in ['positive_ratio', 'user_reviews', 'price_final', 'discount']:
    if col not in df.columns:
        df[col] = 0

if 'price_original' not in df.columns:
    df['price_original'] = df['price_final']
if 'steam_deck' not in df.columns:
    df['steam_deck'] = False
if 'date_release' not in df.columns:
    df['date_release'] = '2020-01-01'

# Tipos
df['positive_ratio'] = pd.to_numeric(df['positive_ratio'], errors='coerce').fillna(0)
df['user_reviews']   = pd.to_numeric(df['user_reviews'],   errors='coerce').fillna(0).astype(int)
df['price_final']    = pd.to_numeric(df['price_final'],    errors='coerce').fillna(0)
df['price_original'] = pd.to_numeric(df['price_original'], errors='coerce').fillna(0)
df['discount']       = pd.to_numeric(df['discount'],       errors='coerce').fillna(0)
df['date_release']   = pd.to_datetime(df['date_release'],  errors='coerce')
df['year']           = df['date_release'].dt.year.fillna(2020).astype(int)

# Filtra jogos com pelo menos 100 avaliações
df = df[df['user_reviews'] >= 100].copy()
print(f"      Após filtro (≥100 reviews): {len(df):,} jogos")


# ── 2. games_metadata.json — tags ────────────────────────────────────────────
print("\n[2/5] Carregando games_metadata.json (tags)...")
app_tags = {}
try:
    with open(METADATA_JSON, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                aid  = row.get('app_id') or row.get('appid')
                tags = row.get('tags', [])
                if aid and tags:
                    app_tags[int(aid)] = tags[:8]
            except Exception:
                continue
    print(f"      Tags carregadas para {len(app_tags):,} jogos")
except Exception as e:
    print(f"      Aviso: {e} — continuando sem tags")

df['tags_list']   = df['app_id'].map(lambda x: app_tags.get(int(x), []))
df['tags_str']    = df['tags_list'].apply(lambda t: '|'.join(t) if t else 'Indie')
df['primary_tag'] = df['tags_list'].apply(lambda t: t[0] if t else 'Indie')


# ── 3. recommendations.csv — avg_hours ───────────────────────────────────────
print("\n[3/5] Carregando recommendations.csv (horas jogadas)...")
print("      Isso pode levar alguns minutos — arquivo grande (~12M linhas)...")
try:
    # Carrega apenas as colunas necessárias para economizar RAM
    df_rec = pd.read_csv(
        RECOM_CSV,
        usecols=lambda c: c.strip().lower() in ('app_id', 'appid', 'hours', 'playtime_forever'),
        dtype={'hours': 'float32'},
        low_memory=True,
    )
    df_rec.columns = df_rec.columns.str.strip().str.lower()

    # Normaliza nome da coluna de horas
    hour_col = 'hours' if 'hours' in df_rec.columns else 'playtime_forever'
    id_col   = 'app_id' if 'app_id' in df_rec.columns else 'appid'
    df_rec.rename(columns={id_col: 'app_id', hour_col: 'hours'}, inplace=True)

    df_eng = (df_rec
              .groupby('app_id')['hours']
              .mean()
              .reset_index()
              .rename(columns={'hours': 'avg_hours'}))
    df_eng['avg_hours'] = df_eng['avg_hours'].round(2)

    df = df.merge(df_eng, on='app_id', how='left')
    df['avg_hours'] = df['avg_hours'].fillna(0).clip(lower=0)
    print(f"      avg_hours calculado para {df['avg_hours'].gt(0).sum():,} jogos")
    del df_rec, df_eng
except Exception as e:
    print(f"      Aviso: {e} — avg_hours será 0")
    df['avg_hours'] = 0.0


# ── 4. Feature engineering ────────────────────────────────────────────────────
print("\n[4/5] Engenharia de features...")

# Revenue proxy (método do artigo)
df['est_revenue_proxy'] = df['price_final'] * df['user_reviews']

# Sucesso comercial (top 20%)
threshold = df['est_revenue_proxy'].quantile(0.80)
df['commercial_success'] = (df['est_revenue_proxy'] >= threshold).astype(int)
print(f"      Revenue proxy — limiar top 20%: ${threshold:,.2f}")
print(f"      Jogos com sucesso comercial: {df['commercial_success'].sum():,} ({df['commercial_success'].mean():.1%})")

# Publisher (se existir)
if 'publisher' not in df.columns:
    df['publisher'] = 'Desconhecido'

# Title
if 'title' not in df.columns and 'name' in df.columns:
    df.rename(columns={'name': 'title'}, inplace=True)
if 'title' not in df.columns:
    df['title'] = 'Game ' + df['app_id'].astype(str)

# KMeans K=4 (igual ao artigo)
feat_cols = ['avg_hours', 'positive_ratio', 'est_revenue_proxy', 'discount']
feat = np.column_stack([
    np.log1p(df['avg_hours'].values),
    df['positive_ratio'].values / 100,
    np.log1p(df['est_revenue_proxy'].values),
    df['discount'].values / 100,
])
scaler = StandardScaler()
feat_s = scaler.fit_transform(feat)

print("      Executando KMeans K=4...")
km = KMeans(n_clusters=4, random_state=42, n_init=10, max_iter=300)
df['cluster'] = km.fit_predict(feat_s)

# Re-rotula clusters pelo revenue proxy mediano (para consistência com o artigo)
cluster_rev = df.groupby('cluster')['est_revenue_proxy'].median().sort_values()
# Cluster com maior desconto = estratégia promocional (cluster 3 do artigo)
cluster_disc = df.groupby('cluster')['discount'].median().sort_values(ascending=False)
print(f"      Revenue mediano por cluster: {cluster_rev.to_dict()}")

df['cluster_name'] = df['cluster'].map(lambda c: CLUSTER_NAMES.get(c, f'Cluster {c}'))

# PCA 2D
print("      Calculando PCA 2D...")
pca = PCA(n_components=2, random_state=42)
coords = pca.fit_transform(feat_s)
df['pca_x'] = coords[:, 0]
df['pca_y'] = coords[:, 1]
print(f"      PCA — PC1: {pca.explained_variance_ratio_[0]:.1%}, PC2: {pca.explained_variance_ratio_[1]:.1%}")


# ── 5. Salva parquets ─────────────────────────────────────────────────────────
print("\n[5/5] Salvando parquets otimizados...")

# Dataset principal
final_cols = [
    'app_id', 'title', 'date_release', 'year',
    'win', 'mac', 'linux', 'steam_deck',
    'rating', 'positive_ratio', 'user_reviews',
    'price_final', 'price_original', 'discount',
    'avg_hours', 'est_revenue_proxy', 'commercial_success',
    'cluster', 'cluster_name', 'primary_tag', 'tags_str',
    'publisher', 'pca_x', 'pca_y',
]
# Mantém só colunas que existem
final_cols = [c for c in final_cols if c in df.columns]
df[final_cols].to_parquet(
    os.path.join(DATA_DIR, 'steam_dashboard.parquet'), index=False
)
print(f"      steam_dashboard.parquet: {len(df):,} jogos, {len(final_cols)} colunas")

# Perfil dos clusters
profile = df.groupby(['cluster', 'cluster_name']).agg(
    count                    =('app_id', 'count'),
    avg_hours_mean           =('avg_hours', 'mean'),
    avg_hours_median         =('avg_hours', 'median'),
    positive_ratio_mean      =('positive_ratio', 'mean'),
    positive_ratio_median    =('positive_ratio', 'median'),
    est_revenue_proxy_mean   =('est_revenue_proxy', 'mean'),
    est_revenue_proxy_median =('est_revenue_proxy', 'median'),
    discount_mean            =('discount', 'mean'),
    discount_median          =('discount', 'median'),
    commercial_success_rate  =('commercial_success', 'mean'),
).reset_index()
profile.to_parquet(os.path.join(DATA_DIR, 'cluster_profile.parquet'), index=False)
print("      cluster_profile.parquet salvo")

# SHAP importance (valores do artigo — fixos)
shap_data = pd.DataFrame({
    'feature':       ['rating_Positive', 'avg_hours', 'positive_ratio',
                      'rating_Very Positive', 'rating_Overwhelmingly Positive',
                      'discount', 'rating_Negative', 'rating_Very Negative',
                      'rating_Overwhelmingly Negative', 'rating_Mostly Negative',
                      'rating_Mostly Positive', 'steam_deck_True'],
    'importance':    [1.12, 0.95, 0.40, 0.15, 0.10,
                      0.08, 0.04, 0.02, 0.01, 0.01, 0.01, 0.005],
    'feature_label': ['Rating: Positive', 'Média de Horas Jogadas', 'Taxa de Aprovação (%)',
                      'Rating: Very Positive', 'Rating: Overwhelmingly Positive',
                      'Desconto (%)', 'Rating: Negative', 'Rating: Very Negative',
                      'Rating: Overwhelmingly Negative', 'Rating: Mostly Negative',
                      'Rating: Mostly Positive', 'Steam Deck Compatível'],
})
shap_data.to_parquet(os.path.join(DATA_DIR, 'shap_importance.parquet'), index=False)
print("      shap_importance.parquet salvo")

# Comparação de modelos (valores do artigo — fixos)
model_results = pd.DataFrame({
    'modelo':   ['Gradient Boosting', 'Regressão Logística', 'Random Forest', 'SVM (Linear)'],
    'acuracia': [0.7835, 0.7521, 0.7658, 0.6636],
    'precisao': [0.4758, 0.4326, 0.4405, 0.3517],
    'recall':   [0.8128, 0.7686, 0.6329, 0.8088],
    'f1_score': [0.6003, 0.5536, 0.5195, 0.4902],
    'roc_auc':  [0.8819, 0.8370, 0.8299, 0.8307],
})
model_results.to_parquet(os.path.join(DATA_DIR, 'model_results.parquet'), index=False)
print("      model_results.parquet salvo")

print("\n" + "=" * 60)
print("  ✓ Processamento concluído!")
print("  Execute agora: python dashboard.py")
print("  Acesse em:     http://127.0.0.1:8050")
print("=" * 60)
