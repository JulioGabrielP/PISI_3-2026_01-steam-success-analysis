from dash import html, dcc


def create_experiment_layout():
    return html.Div([
        html.Div(
            '🤖  Regressão Logística — Digite uma review e veja a predição de recomendação.',
            className='page-subtitle',
        ),

        html.Div(className='card', style={'maxWidth': '720px', 'margin': '0 auto'}, children=[
            html.Div('Experimente o Modelo', className='card-title'),

            html.Label(
                'Cole ou escreva uma review de jogo (em inglês):',
                style={
                    'color': 'var(--text-muted)',
                    'fontSize': '12px',
                    'marginBottom': '6px',
                    'display': 'block',
                },
            ),

            dcc.Textarea(
                id='experiment-input-text',
                placeholder='Ex: This game is absolutely fantastic! Great graphics and gameplay...',
                style={
                    'width': '100%',
                    'height': '120px',
                    'background': '#16202d',
                    'color': '#c7d5e0',
                    'border': '1px solid #2a475e',
                    'borderRadius': '4px',
                    'padding': '8px',
                    'fontSize': '13px',
                    'resize': 'vertical',
                    'boxSizing': 'border-box',
                },
            ),

            html.Button(
                '🔍  Prever',
                id='experiment-predict-btn',
                style={
                    'marginTop': '12px',
                    'padding': '8px 20px',
                    'background': 'var(--accent)',
                    'color': '#fff',
                    'border': 'none',
                    'borderRadius': '4px',
                    'cursor': 'pointer',
                    'fontSize': '13px',
                    'fontFamily': 'Rajdhani, sans-serif',
                    'fontWeight': '700',
                },
            ),

            html.Div(id='experiment-output', style={'marginTop': '20px'}),
        ]),
    ])
