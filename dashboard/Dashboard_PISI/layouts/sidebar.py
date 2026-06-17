from dash import html, dcc

from callbacks.theme import CLUSTER_NAMES


TOP_TAGS = [
    'Indie',
    'Action',
    'Adventure',
    'Casual',
    'Singleplayer',
    'Strategy',
    'Simulation',
    'RPG',
    'Atmospheric',
    '2D',
]


CLUSTER_EMOJI = {
    0: '🔴',
    1: '🟡',
    2: '🟢',
    3: '🔵',
}


CLUSTER_OPTIONS = [
    {
        'label': f'{CLUSTER_EMOJI.get(cid, "⚪")}  {name}',
        'value': cid,
    }
    for cid, name in CLUSTER_NAMES.items()
]


def create_sidebar():
    return html.Div(
        id='sidebar-container',
        className='sidebar',
        children=[
            html.Div(
                'FILTROS',
                className='filter-section-title',
            ),

            # Tags
            html.Label(
                'Tag',
                className='filter-label',
            ),

            dcc.Dropdown(
                id='filter-tags',
                options=[
                    {
                        'label': tag,
                        'value': tag,
                    }
                    for tag in TOP_TAGS
                ],
                value=[],
                multi=True,
                placeholder='Todas as tags...',
                style={
                    'fontSize': '12px',
                },
            ),

            # Faixa de preço
            html.Div(
                'Preço (USD)',
                className='filter-section-title',
            ),

            dcc.RangeSlider(
                id='filter-price-range',
                min=0,
                max=250,
                step=5,
                value=[0, 250],
                marks={
                    0: '0',
                    60: '60',
                    120: '120',
                    250: '250',
                },
                tooltip={
                    'placement': 'bottom',
                    'always_visible': False,
                },
            ),

            # Aprovação mínima
            html.Div(
                'Avaliação Mínima',
                className='filter-section-title',
            ),

            html.Label(
                id='filter-ratio-label',
                children='≥ 0%',
                className='filter-label',
            ),

            dcc.Slider(
                id='filter-positive-ratio',
                min=0,
                max=100,
                step=5,
                value=0,
                marks={
                    0: '0%',
                    50: '50%',
                    80: '80%',
                    100: '100%',
                },
                tooltip={
                    'placement': 'bottom',
                    'always_visible': False,
                },
            ),

            # Intervalo de anos
            html.Div(
                'Ano de Lançamento',
                className='filter-section-title',
            ),

            dcc.RangeSlider(
                id='filter-year-range',
                min=2003,
                max=2024,
                step=1,
                value=[2003, 2024],
                marks={
                    2003: '03',
                    2010: '10',
                    2017: '17',
                    2024: '24',
                },
                tooltip={
                    'placement': 'bottom',
                    'always_visible': False,
                },
            ),

            # Clusters
            html.Div(
                'Clusters',
                className='filter-section-title',
            ),

            dcc.Checklist(
                id='filter-clusters',
                options=CLUSTER_OPTIONS,
                value=[0, 1, 2, 3],
                labelStyle={
                    'display': 'block',
                },
            ),

            # Steam Deck
            html.Div(
                'Steam Deck',
                className='filter-section-title',
            ),

            dcc.RadioItems(
                id='filter-steam-deck',
                options=[
                    {
                        'label': 'Todos',
                        'value': 'all',
                    },
                    {
                        'label': 'Compatível',
                        'value': 'yes',
                    },
                    {
                        'label': 'Incompatível',
                        'value': 'no',
                    },
                ],
                value='all',
                labelStyle={
                    'display': 'block',
                },
            ),

            # Botão para resetar os filtros
            html.Button(
                '↺  Resetar Filtros',
                id='btn-reset-filters',
                className='sidebar-reset-btn',
            ),

            # Quantidade de jogos após os filtros
            html.Div(
                id='filter-count-display',
                style={
                    'marginTop': '14px',
                    'textAlign': 'center',
                    'fontSize': '11px',
                    'color': 'var(--text-muted)',
                },
            ),
        ],
    )