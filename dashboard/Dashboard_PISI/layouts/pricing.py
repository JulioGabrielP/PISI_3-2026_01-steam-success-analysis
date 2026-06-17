from dash import html, dcc
import plotly.graph_objects as go
from callbacks.theme import base_layout


def create_pricing_layout():
    # ── Graph 1: SHAP Horizontal Bar Chart ──
    fig_shap = go.Figure()
    fig_shap.add_trace(go.Bar(
        x=[3.63, 5.23, 13.05, 33.69, 40.91],
        y=[
            "Classificação Overwhelmingly Positive",
            "Classificação Very Positive",
            "Taxa de aprovação",
            "Média de horas jogadas",
            "Classificação Positive"
        ],
        orientation='h',
        marker_color='#e07b40',  # Alert orange
        text=['3,63%', '5,23%', '13,05%', '33,69%', '40,91%'],
        textposition='outside',
        textfont=dict(color='#c6d4df', size=11),
        hovertemplate='<b>%{y}</b><br>Contribuição: %{x:.2f}%<extra></extra>'
    ))

    # long category names need a generous left margin
    layout_shap = base_layout(height=280)
    layout_shap['margin'] = dict(l=240, r=45, t=15, b=40)
    layout_shap['xaxis']['title'] = 'Contribuição Percentual (%)'
    layout_shap['xaxis']['range'] = [0, 48]
    layout_shap['showlegend'] = False
    fig_shap.update_layout(**layout_shap)

    # ── Graph 2: F1-Score Baseline Comparison Chart ──
    f1_vals = [0.3909, 0.4202, 0.4204, 0.4733]
    models = ["Random Forest", "Regressão Logística", "SVM", "Gradient Boosting"]
    bar_colors = ['#1e3144', '#1e3144', '#1e3144', '#e07b40']  # Neutral dark gray/blue for others, orange highlight for GB

    fig_baseline = go.Figure()
    fig_baseline.add_trace(go.Bar(
        x=f1_vals,
        y=models,
        orientation='h',
        marker_color=bar_colors,
        text=[f"{v:.4f}" for v in f1_vals],
        textposition='outside',
        textfont=dict(color='#c6d4df', size=11),
        hovertemplate='<b>%{y}</b><br>F1-Score: %{x:.4f}<extra></extra>'
    ))

    layout_base = base_layout(height=240)
    layout_base['margin'] = dict(l=140, r=45, t=15, b=40)
    layout_base['xaxis']['title'] = 'F1-Score (Eixo Ampliado: 0.35 a 0.50)'
    layout_base['xaxis']['range'] = [0.35, 0.50]
    layout_base['showlegend'] = False
    fig_baseline.update_layout(**layout_base)

    # ── Table Styling ──
    header_style = {
        'background': '#1e3144',
        'color': '#66c0f4',
        'fontFamily': 'Rajdhani, sans-serif',
        'fontWeight': '700',
        'fontSize': '12px',
        'letterSpacing': '0.8px',
        'textTransform': 'uppercase',
        'padding': '10px 12px',
        'textAlign': 'left',
        'borderBottom': '1px solid #2a475e',
    }

    cell_style_normal = {
        'padding': '10px 12px',
        'fontSize': '13px',
        'color': '#c6d4df',
        'borderBottom': '1px solid #1e3144',
    }

    cell_style_highlight = {
        'padding': '10px 12px',
        'fontSize': '13px',
        'color': '#66c0f4',
        'borderBottom': '1px solid #2a475e',
        'fontWeight': '600',
        'background': 'rgba(102, 192, 244, 0.08)',
    }

    return html.Div([
        # 1. Cabeçalho
        html.Div([
            html.H1(
                "Por que a previsão comercial foi limitada?",
                style={
                    'fontFamily': 'Rajdhani, sans-serif',
                    'fontWeight': '700',
                    'fontSize': '28px',
                    'color': '#66c0f4',
                    'marginBottom': '8px'
                }
            ),
            html.Div(
                "A interpretação do primeiro experimento mostrou que boas métricas não significavam, necessariamente, capacidade de prever o desempenho de um jogo antes de seu lançamento.",
                style={'fontSize': '15px', 'color': '#8f98a0', 'marginBottom': '16px', 'lineHeight': '1.5'}
            ),
            html.Div(
                "Esta página apresenta uma revisão metodológica do experimento supervisionado e não um novo modelo de previsão.",
                className="page-subtitle",
                style={
                    'borderLeft': '3px solid #e07b40',
                    'background': '#1b2838',
                    'padding': '10px 16px',
                    'fontSize': '13px',
                    'color': '#e07b40',
                }
            ),
        ], style={'marginBottom': '24px'}),

        # 2. Resultado inicial
        html.Div([
            html.Div("O primeiro resultado parecia promissor", className="card-title"),
            html.Div(
                "Na formulação inicial, o Gradient Boosting apresentou o melhor desempenho entre os modelos avaliados. Entretanto, a interpretação das variáveis revelou uma limitação importante para o uso pretendido.",
                style={'marginBottom': '16px', 'color': '#c6d4df', 'lineHeight': '1.5', 'fontSize': '14px'}
            ),

            # KPI Grid
            html.Div(className='kpi-grid', children=[
                html.Div(className='kpi-card', children=[
                    html.Div("Melhor modelo", className="kpi-label"),
                    html.Div("Gradient Boosting", className="kpi-value", style={'fontSize': '20px', 'whiteSpace': 'nowrap'}),
                    html.Div("Experimento inicial (pós-lançamento)", className="kpi-sub")
                ]),
                html.Div(className='kpi-card', children=[
                    html.Div("ROC-AUC", className="kpi-label"),
                    html.Div("0,8819", className="kpi-value"),
                    html.Div("Experimento inicial (pós-lançamento)", className="kpi-sub")
                ]),
                html.Div(className='kpi-card', children=[
                    html.Div("Recall da classe de sucesso", className="kpi-label"),
                    html.Div("0,8128", className="kpi-value"),
                    html.Div("Experimento inicial (pós-lançamento)", className="kpi-sub")
                ]),
                html.Div(className='kpi-card', children=[
                    html.Div("F1-Score da classe de sucesso", className="kpi-label"),
                    html.Div("0,6003", className="kpi-value"),
                    html.Div("Experimento inicial (pós-lançamento)", className="kpi-sub")
                ]),
            ]),
        ], className="card"),

        # 3. Variáveis mais influentes no experimento inicial
        html.Div([
            html.Div("O modelo inicial dependia principalmente de informações pós-lançamento", className="card-title"),

            dcc.Graph(
                id='chart-shap-influential',
                figure=fig_shap,
                config={'displayModeBar': False}
            ),

            html.Div(
                "As cinco variáveis concentraram 96,51% do ranking percentual das contribuições apresentadas.",
                style={'fontWeight': 'bold', 'color': '#e07b40', 'marginTop': '12px', 'marginBottom': '12px', 'fontSize': '13px'}
            ),

            html.Div(
                "Avaliações, taxa de aprovação e horas jogadas são informações formadas após a publicação do jogo. Por isso, embora fossem úteis para explicar retrospectivamente o desempenho observado, elas não estariam disponíveis em um cenário real de previsão anterior ao lançamento, o que demonstra uma clara dependência de variáveis pós-lançamento.",
                style={'color': '#c6d4df', 'lineHeight': '1.5', 'fontSize': '13px'}
            ),
        ], className="card"),

        # 4. Explicação metodológica
        html.Div([
            html.Div("Explicação Metodológica", className="card-title"),
            html.Div(className='chart-grid-3', children=[
                # Card 1: Pergunta pretendida
                html.Div(className='card', style={'background': '#1b2838', 'borderColor': '#2a475e', 'marginBottom': '0'}, children=[
                    html.Div("Pergunta pretendida", style={'fontFamily': 'Rajdhani, sans-serif', 'fontWeight': '600', 'color': '#66c0f4', 'fontSize': '14px', 'marginBottom': '8px', 'textTransform': 'uppercase'}),
                    html.Div("Quais jogos apresentam maior chance de alcançar sucesso comercial?", style={'fontSize': '12px', 'color': '#c6d4df', 'lineHeight': '1.4'})
                ]),
                # Card 2: Informações utilizadas
                html.Div(className='card', style={'background': '#1b2838', 'borderColor': '#2a475e', 'marginBottom': '0'}, children=[
                    html.Div("Informações utilizadas", style={'fontFamily': 'Rajdhani, sans-serif', 'fontWeight': '600', 'color': '#66c0f4', 'fontSize': '14px', 'marginBottom': '8px', 'textTransform': 'uppercase'}),
                    html.Div("Parte das variáveis mais importantes somente é conhecida depois que o jogo já acumulou avaliações e horas jogadas.", style={'fontSize': '12px', 'color': '#c6d4df', 'lineHeight': '1.4'})
                ]),
                # Card 3: Limitação
                html.Div(className='card', style={'background': '#1b2838', 'borderColor': '#e07b40', 'marginBottom': '0'}, children=[
                    html.Div("Limitação", style={'fontFamily': 'Rajdhani, sans-serif', 'fontWeight': '600', 'color': '#e07b40', 'fontSize': '14px', 'marginBottom': '8px', 'textTransform': 'uppercase'}),
                    html.Div("O modelo funcionava melhor como explicação retrospectiva do que como previsão antecipada para jogos ainda não lançados.", style={'fontSize': '12px', 'color': '#c6d4df', 'lineHeight': '1.4'})
                ]),
            ]),
        ], className="card", style={'border': '1px solid #2a475e'}),

        # 5. Baseline reformulado & 6. Tabela de métricas
        html.Div(className='chart-grid-2', children=[
            # Coluna 1: Gráfico F1-Score
            html.Div([
                html.Div("F1-Score no baseline reformulado", className="card-title"),
                html.Div(
                    "Para avaliar um cenário mais restritivo, o experimento foi reformulado com menor dependência de informações posteriores ao lançamento. A redução das métricas indicou que as variáveis estruturadas disponíveis possuíam poder preditivo limitado para a tarefa comercial.",
                    style={'fontSize': '12px', 'color': '#8f98a0', 'marginBottom': '12px', 'lineHeight': '1.4'}
                ),
                dcc.Graph(
                    id='chart-baseline-f1',
                    figure=fig_baseline,
                    config={'displayModeBar': False}
                ),
                html.Div(
                    "Eixo ampliado para facilitar a comparação entre os modelos.",
                    style={'fontSize': '11px', 'color': '#8f98a0', 'marginTop': '4px', 'textAlign': 'center'}
                ),
            ], className="card"),

            # Coluna 2: Tabela de métricas
            html.Div([
                html.Div("Métricas Detalhadas do Baseline Reformulado", className="card-title"),
                html.Div(style={'overflowX': 'auto'}, children=[
                    html.Table([
                        # Cabeçalho da tabela
                        html.Tr([
                            html.Th('Modelo', style=header_style),
                            html.Th('Acurácia', style=header_style),
                            html.Th('Precisão', style=header_style),
                            html.Th('Recall', style=header_style),
                            html.Th('F1-Score', style=header_style),
                        ]),
                        # Linha 1: Gradient Boosting (destacado)
                        html.Tr([
                            html.Td('Gradient Boosting', style=cell_style_highlight),
                            html.Td('0,7241', style=cell_style_highlight),
                            html.Td('0,3829', style=cell_style_highlight),
                            html.Td('0,6194', style=cell_style_highlight),
                            html.Td('0,4733', style=cell_style_highlight),
                        ], style={'background': 'rgba(102, 192, 244, 0.04)'}),
                        # Linha 2: SVM
                        html.Tr([
                            html.Td('SVM', style=cell_style_normal),
                            html.Td('0,6854', style=cell_style_normal),
                            html.Td('0,3330', style=cell_style_normal),
                            html.Td('0,5702', style=cell_style_normal),
                            html.Td('0,4204', style=cell_style_normal),
                        ]),
                        # Linha 3: Regressão Logística
                        html.Tr([
                            html.Td('Regressão Logística', style=cell_style_normal),
                            html.Td('0,6657', style=cell_style_normal),
                            html.Td('0,3218', style=cell_style_normal),
                            html.Td('0,6056', style=cell_style_normal),
                            html.Td('0,4202', style=cell_style_normal),
                        ]),
                        # Linha 4: Random Forest
                        html.Tr([
                            html.Td('Random Forest', style=cell_style_normal),
                            html.Td('0,7400', style=cell_style_normal),
                            html.Td('0,3679', style=cell_style_normal),
                            html.Td('0,4170', style=cell_style_normal),
                            html.Td('0,3909', style=cell_style_normal),
                        ]),
                    ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '10px'})
                ]),
                # Avisos sob a tabela
                html.Div([
                    html.Div(
                        "Precisão, recall e F1-Score referem-se à classe positiva de sucesso comercial.",
                        style={'fontSize': '11px', 'color': '#8f98a0', 'marginTop': '12px'}
                    ),
                    html.Div(
                        "A acurácia isolada não foi considerada suficiente, pois a tarefa apresentava desbalanceamento entre as classes.",
                        style={'fontSize': '11px', 'color': '#8f98a0', 'marginTop': '4px'}
                    ),
                ]),
            ], className="card"),
        ]),

        # 7. Leitura dos resultados
        html.Div([
            html.Div("O que foi aprendido com a reformulação?", className="card-title"),
            html.Div(className='chart-grid-3', children=[
                html.Div([
                    html.Div("📌 Insight 1", style={'fontFamily': 'Rajdhani, sans-serif', 'fontWeight': '600', 'color': '#fafafa', 'fontSize': '13px', 'marginBottom': '6px'}),
                    html.Div("As métricas iniciais eram fortemente favorecidas por informações produzidas após o lançamento.", style={'fontSize': '12px', 'color': '#8f98a0', 'lineHeight': '1.4'})
                ], style={'background': '#1b2838', 'padding': '12px', 'borderRadius': '4px', 'borderLeft': '3px solid #66c0f4'}),
                html.Div([
                    html.Div("📌 Insight 2", style={'fontFamily': 'Rajdhani, sans-serif', 'fontWeight': '600', 'color': '#fafafa', 'fontSize': '13px', 'marginBottom': '6px'}),
                    html.Div("Sem essas informações, os modelos apresentaram dificuldade para identificar jogos comercialmente bem-sucedidos.", style={'fontSize': '12px', 'color': '#8f98a0', 'lineHeight': '1.4'})
                ], style={'background': '#1b2838', 'padding': '12px', 'borderRadius': '4px', 'borderLeft': '3px solid #e07b40'}),
                html.Div([
                    html.Div("📌 Insight 3", style={'fontFamily': 'Rajdhani, sans-serif', 'fontWeight': '600', 'color': '#fafafa', 'fontSize': '13px', 'marginBottom': '6px'}),
                    html.Div("Os dados estruturados permaneceram adequados para análise exploratória e identificação de perfis por clusterização.", style={'fontSize': '12px', 'color': '#8f98a0', 'lineHeight': '1.4'})
                ], style={'background': '#1b2838', 'padding': '12px', 'borderRadius': '4px', 'borderLeft': '3px solid #5cb85c'}),
            ]),
        ], className="card"),

        # 8. Conclusão e transição
        html.Div([
            html.Div("Redirecionamento da etapa supervisionada", className="card-title", style={'color': '#f4b942', 'fontSize': '15px'}),
            html.Div([
                html.Div(
                    "A redução do desempenho mostrou que os dados estruturados disponíveis não sustentavam uma previsão comercial antecipada suficientemente confiável. Por esse motivo, a etapa supervisionada foi redirecionada para uma tarefa compatível com os dados disponíveis: classificar a recomendação expressa no texto das reviews.",
                    style={'fontWeight': '500', 'color': '#c6d4df', 'marginBottom': '12px', 'lineHeight': '1.5', 'fontSize': '14px'}
                ),
                html.Div(
                    "Essa nova tarefa não substitui a análise comercial e não prevê vendas. Ela responde a uma pergunta independente sobre a opinião registrada pelos usuários.",
                    style={'color': '#8f98a0', 'lineHeight': '1.5', 'fontSize': '13px', 'marginBottom': '16px'}
                ),
                html.Div([
                    html.Span("Próxima etapa: Classificação de Reviews", style={
                        'fontFamily': 'Rajdhani, sans-serif',
                        'fontWeight': '700',
                        'fontSize': '13px',
                        'color': '#66c0f4',
                        'textTransform': 'uppercase',
                        'letterSpacing': '1px'
                    })
                ], style={'textAlign': 'right', 'marginTop': '8px'})
            ])
        ], className="card", style={'borderColor': '#f4b942', 'background': 'rgba(244,185,66,0.03)'}),
    ])
