from dash import html, dcc


def create_overview_layout():
    return html.Div([
        # Apresentação da pesquisa
        html.Div(className='card narrative-card', children=[
            html.Div('Do desempenho comercial à análise das reviews',
                     className='card-title'),

            html.P(
                'A pesquisa começou investigando padrões associados ao '
                'desempenho de jogos da Steam. Durante a modelagem, foi '
                'identificado que as variáveis mais informativas eram '
                'produzidas após o lançamento, limitando seu uso para '
                'previsões de novos títulos.',
                className='page-subtitle'
            ),

            html.P(
                'A partir desse resultado, o estudo foi organizado em duas '
                'frentes complementares: a identificação de perfis de jogos '
                'já lançados e a classificação da recomendação expressa no '
                'texto das reviews.',
                className='page-subtitle'
            ),
        ]),

        # Etapas principais
        html.Div(className='chart-grid-3', children=[
            html.Div(className='card', children=[
                html.Div('1', className='kpi-value'),
                html.Div('Dados estruturados', className='card-title'),
                html.P(
                    'Preços, avaliações, engajamento, descontos e tags.',
                    className='page-subtitle'
                ),
            ]),

            html.Div(className='card', children=[
                html.Div('2', className='kpi-value'),
                html.Div('Perfis de jogos', className='card-title'),
                html.P(
                    'Clusterização de títulos com características semelhantes.',
                    className='page-subtitle'
                ),
            ]),

            html.Div(className='card', children=[
                html.Div('3', className='kpi-value'),
                html.Div('Reviews textuais', className='card-title'),
                html.P(
                    'Classificação das avaliações como recomendadas ou não.',
                    className='page-subtitle'
                ),
            ]),
        ]),

        # Indicadores gerais
        html.Div(id='overview-kpis', className='kpi-grid'),

        # Contexto visual da base estruturada
        html.Div(className='section-heading', children=[
            html.H3('Ponto de partida da análise'),
            html.P(
                'Os gráficos abaixo apresentam duas relações observadas '
                'na base estruturada. As análises completas estão organizadas '
                'nas páginas seguintes.',
                className='page-subtitle'
            ),
        ]),

        html.Div(className='chart-grid-21', children=[
            html.Div(className='card', children=[
                html.Div(
                    'Alta aprovação não implica grande alcance',
                    className='card-title'
                ),
                dcc.Graph(
                    id='chart-scatter-reviews',
                    config={'displayModeBar': False}
                ),
                html.P(
                    'Há jogos muito bem avaliados que permanecem com baixo '
                    'volume de reviews.',
                    className='chart-insight'
                ),
            ]),

            html.Div(className='card', children=[
                html.Div(
                    'Associações entre os indicadores',
                    className='card-title'
                ),
                dcc.Graph(
                    id='chart-heatmap',
                    config={'displayModeBar': False}
                ),
                html.P(
                    'As associações descrevem a base, mas não representam '
                    'relações de causa e efeito.',
                    className='chart-insight'
                ),
            ]),
        ]),

        # Direcionamento para as demais páginas
        html.Div(className='card narrative-card', children=[
            html.Div('Como explorar o dashboard', className='card-title'),
            html.P(
                'A página Análise Exploratória apresenta os padrões iniciais. '
                'Perfis de Jogos mostra os agrupamentos gerados pelo K-Means. '
                'Limites da Previsão descreve a tentativa de classificação '
                'comercial, enquanto Classificação de Reviews apresenta os '
                'resultados da análise textual.',
                className='page-subtitle'
            ),
        ]),
    ])