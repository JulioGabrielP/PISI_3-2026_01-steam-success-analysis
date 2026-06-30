from dash import html, dcc


def create_clusters_layout():
    return html.Div([
        html.Div(
            '🔬  KMeans K=4 — Clusters identificados com base em engajamento, aprovação, faturamento e desconto.',
            className='page-subtitle',
        ),

        # Card explicativo do método KMeans
        html.Div(className='card', style={'marginBottom': '16px'}, children=[
            html.Div('📖  Como o KMeans foi aplicado', className='card-title'),
            html.P(
                'O algoritmo K-Means foi aplicado sobre quatro variáveis: média de horas jogadas, '
                'taxa de aprovação, faturamento estimado (proxy) e desconto. As variáveis de horas '
                'e faturamento receberam transformação logarítmica para reduzir assimetria, e todos '
                'os atributos foram padronizados antes da clusterização. O número de clusters foi '
                'definido como K=4 com base no método do cotovelo e no coeficiente de silhueta '
                '(score = 0,3226), indicando separação moderada entre os perfis. A projeção 2D via '
                'PCA preservou aproximadamente 59,7% da variância dos dados.',
                style={
                    'color': 'var(--text-muted)',
                    'fontSize': '12px',
                    'lineHeight': '1.6',
                    'margin': 0,
                },
            ),
        ]),

        # Row 1: PCA scatter (big) + Cluster size donut
        html.Div(className='chart-grid-21', children=[
            html.Div(className='card', children=[
                html.Div('Projeção PCA 2D dos Clusters (PC1=35.8%, PC2=25.9%)', className='card-title'),
                dcc.Graph(id='chart-pca-scatter', config={'displayModeBar': False},
                          style={'height': '460px'}),
            ]),
            html.Div(children=[
                html.Div(className='card', children=[
                    html.Div('Distribuição dos Clusters', className='card-title'),
                    dcc.Graph(id='chart-cluster-donut', config={'displayModeBar': False},
                              style={'height': '200px'}),
                ]),
                html.Div(className='card', children=[
                    html.Div('Perfil dos Clusters', className='card-title'),
                    html.Div(id='cluster-profile-badges'),
                ]),
            ]),
        ]),

        # Row 2: Radar chart + Bar comparison
        html.Div(className='chart-grid-2', children=[
            html.Div(className='card', children=[
                html.Div('Radar — Comparação de Atributos por Cluster', className='card-title'),
                dcc.Graph(id='chart-cluster-radar', config={'displayModeBar': False}),
            ]),
            html.Div(className='card', children=[
                html.Div('Métricas Médias por Cluster', className='card-title'),
                dcc.Dropdown(
                    id='cluster-metric-selector',
                    options=[
                        {'label': 'Média de Horas Jogadas', 'value': 'avg_hours_mean'},
                        {'label': 'Taxa de Aprovação Média', 'value': 'positive_ratio_mean'},
                        {'label': 'Faturamento Estimado Médio', 'value': 'est_revenue_proxy_mean'},
                        {'label': 'Desconto Médio (%)', 'value': 'discount_mean'},
                        {'label': 'Taxa de Sucesso Comercial', 'value': 'commercial_success_rate'},
                    ],
                    value='avg_hours_mean',
                    clearable=False,
                    style={'marginBottom': '10px', 'fontSize': '12px'},
                ),
                dcc.Graph(id='chart-cluster-bars', config={'displayModeBar': False}),
            ]),
        ]),

        # Row 3: Sucesso comercial por cluster + tag distribution
        html.Div(className='chart-grid-2', children=[
            html.Div(className='card', children=[
                html.Div('Taxa de Sucesso Comercial por Cluster', className='card-title'),
                dcc.Graph(id='chart-cluster-success-rate', config={'displayModeBar': False}),
            ]),
            html.Div(className='card', children=[
                html.Div('Tags Mais Frequentes por Cluster', className='card-title'),
                dcc.Dropdown(
                    id='cluster-tag-selector',
                    options=[
                        {'label': 'Cluster 0 — Alto Faturamento', 'value': 0},
                        {'label': 'Cluster 1 — Boa Avaliação', 'value': 1},
                        {'label': 'Cluster 2 — Alto Engajamento', 'value': 2},
                        {'label': 'Cluster 3 — Estratégia Promocional', 'value': 3},
                    ],
                    value=2,
                    clearable=False,
                    style={'marginBottom': '10px', 'fontSize': '12px'},
                ),
                dcc.Graph(id='chart-cluster-tags', config={'displayModeBar': False}),
            ]),
        ]),
    ])
