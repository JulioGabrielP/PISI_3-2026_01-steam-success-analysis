from dash import html, dcc
import plotly.graph_objects as go
from callbacks.theme import base_layout, ACCENT, TEXT, TEXT_MUT, GRID

def create_shap_layout():
    # ── 3. Distribuição das classes chart ──────────────────────────────────────
    x_vals = [124021, 282590]
    y_vals = ['Not Recommended', 'Recommended']
    text_vals = ['124.021 (30,5%)', '282.590 (69,5%)']
    colors = ['#e07b40', ACCENT] # orange and blue

    fig_dist = go.Figure(go.Bar(
        x=x_vals,
        y=y_vals,
        orientation='h',
        marker_color=colors,
        text=text_vals,
        textposition='inside',
        textfont=dict(color='#ffffff', size=12, family='Source Sans 3, sans-serif'),
        hovertemplate='<b>%{y}</b><br>Quantidade: %{x:,}<extra></extra>'
    ))

    layout_dist = base_layout(height=180)
    layout_dist['showlegend'] = False
    layout_dist['xaxis']['visible'] = False
    layout_dist['yaxis']['tickfont'] = dict(size=12, family='Source Sans 3, sans-serif')
    layout_dist['margin'] = dict(l=120, r=20, t=10, b=10)
    fig_dist.update_layout(**layout_dist)

    # ── 4. Comparação dos modelos chart ───────────────────────────────────────
    y_models = ['Gradient Boosting', 'Random Forest', 'SVM', 'Regressão Logística']
    x_f1 = [0.8602, 0.8649, 0.8849, 0.8902]
    text_f1 = ['0,8602', '0,8649', '0,8849', '0,8902 (Melhor)']
    colors_f1 = ['#2a475e', '#2a475e', '#2a475e', ACCENT]

    fig_models = go.Figure(go.Bar(
        x=x_f1,
        y=y_models,
        orientation='h',
        marker_color=colors_f1,
        text=text_f1,
        textposition='inside',
        textfont=dict(color='#ffffff', size=11, family='Source Sans 3, sans-serif'),
        hovertemplate='<b>%{y}</b><br>F1-Score: %{x:.4f}<extra></extra>'
    ))

    layout_models = base_layout(height=180)
    layout_models['showlegend'] = False
    layout_models['xaxis']['range'] = [0.78, 0.90]
    layout_models['xaxis']['dtick'] = 0.02
    layout_models['yaxis']['tickfont'] = dict(size=12, family='Source Sans 3, sans-serif')
    layout_models['margin'] = dict(l=130, r=20, t=10, b=10)
    fig_models.update_layout(**layout_models)

    # ── 5. Tabela de métricas ─────────────────────────────────────────────────
    table_rows = [
        # Header
        html.Tr([
            html.Th("Modelo", style={'padding': '8px', 'textAlign': 'left', 'borderBottom': '1px solid var(--border)'}),
            html.Th("Acurácia", style={'padding': '8px', 'textAlign': 'center', 'borderBottom': '1px solid var(--border)'}),
            html.Th("Precisão", style={'padding': '8px', 'textAlign': 'center', 'borderBottom': '1px solid var(--border)'}),
            html.Th("Recall", style={'padding': '8px', 'textAlign': 'center', 'borderBottom': '1px solid var(--border)'}),
            html.Th("F1-Score", style={'padding': '8px', 'textAlign': 'center', 'borderBottom': '1px solid var(--border)'}),
        ], style={'backgroundColor': 'var(--bg-secondary)', 'color': 'var(--accent)', 'fontFamily': 'Rajdhani', 'fontWeight': '600'}),
        
        # Body
        html.Tr([
            html.Td("Regressão Logística", style={'padding': '8px', 'fontWeight': 'bold'}),
            html.Td("0,8527", style={'padding': '8px', 'textAlign': 'center', 'fontWeight': 'bold'}),
            html.Td("0,9230", style={'padding': '8px', 'textAlign': 'center', 'fontWeight': 'bold'}),
            html.Td("0,8598", style={'padding': '8px', 'textAlign': 'center', 'fontWeight': 'bold'}),
            html.Td("0,8902", style={'padding': '8px', 'textAlign': 'center', 'fontWeight': 'bold'}),
        ], style={'backgroundColor': 'rgba(102, 192, 244, 0.15)', 'borderLeft': '3px solid var(--accent)', 'color': 'var(--text-primary)'}),
        
        html.Tr([
            html.Td("SVM", style={'padding': '8px'}),
            html.Td("0,8456", style={'padding': '8px', 'textAlign': 'center'}),
            html.Td("0,9177", style={'padding': '8px', 'textAlign': 'center'}),
            html.Td("0,8543", style={'padding': '8px', 'textAlign': 'center'}),
            html.Td("0,8849", style={'padding': '8px', 'textAlign': 'center'}),
        ], style={'borderBottom': '1px solid var(--border-light)', 'color': 'var(--text-secondary)'}),
        
        html.Tr([
            html.Td("Random Forest", style={'padding': '8px'}),
            html.Td("0,8224", style={'padding': '8px', 'textAlign': 'center'}),
            html.Td("0,9175", style={'padding': '8px', 'textAlign': 'center'}),
            html.Td("0,8181", style={'padding': '8px', 'textAlign': 'center'}),
            html.Td("0,8649", style={'padding': '8px', 'textAlign': 'center'}),
        ], style={'borderBottom': '1px solid var(--border-light)', 'color': 'var(--text-secondary)'}),
        
        html.Tr([
            html.Td("Gradient Boosting", style={'padding': '8px'}),
            html.Td("0,8050", style={'padding': '8px', 'textAlign': 'center'}),
            html.Td("0,8568", style={'padding': '8px', 'textAlign': 'center'}),
            html.Td("0,8638", style={'padding': '8px', 'textAlign': 'center'}),
            html.Td("0,8602", style={'padding': '8px', 'textAlign': 'center'}),
        ], style={'borderBottom': '1px solid var(--border-light)', 'color': 'var(--text-secondary)'}),
    ]

    # ── 6. Matriz de confusão ─────────────────────────────────────────────────
    cm = [[20748, 4056],
          [7926, 48593]]
    labels = ['Not Recommended', 'Recommended']

    fig_cm = go.Figure(go.Heatmap(
        z=cm,
        x=labels,
        y=labels,
        colorscale=[[0, '#16202d'], [1.0, ACCENT]],
        text=[[f"{cm[i][j]:,}".replace(',', '.') for j in range(2)] for i in range(2)],
        texttemplate="%{text}",
        textfont=dict(size=14, color='#ffffff', family='Source Sans 3, sans-serif'),
        showscale=False,
        hovertemplate='Real: %{y}<br>Previsto: %{x}<br>Contagem: %{z:,}<extra></extra>'
    ))

    layout_cm = base_layout(height=280)
    layout_cm['xaxis']['title'] = 'Classe prevista'
    layout_cm['yaxis']['title'] = 'Classe real'
    layout_cm['yaxis']['autorange'] = 'reversed'
    layout_cm['margin'] = dict(l=150, r=40, t=10, b=50)
    fig_cm.update_layout(**layout_cm)

    # ── Master Layout ──────────────────────────────────────────────────────────
    return html.Div([
        # 1. Introdução
        html.H1("Classificação da recomendação expressa nas reviews", 
                style={'fontFamily': 'Rajdhani', 'fontSize': '28px', 'fontWeight': '700', 'color': 'var(--accent)', 'marginBottom': '10px'}),
        
        html.P("Após a identificação das limitações da previsão comercial, foi analisado um conjunto independente de reviews. O objetivo desta etapa foi classificar cada avaliação como Recommended ou Not Recommended a partir de seu conteúdo textual.", 
               style={'marginBottom': '16px', 'color': 'var(--text-primary)', 'lineHeight': '1.5'}),
        
        html.Div("Esta página utiliza uma base textual independente. Os filtros laterais aplicados aos jogos estruturados não alteram estes resultados.", 
                 className='page-subtitle'),

        # 2. KPIs
        html.Div(className='kpi-grid', children=[
            html.Div(className='kpi-card', children=[
                html.Div("Reviews analisadas", className='kpi-label'),
                html.Div("406.611", className='kpi-value'),
            ]),
            html.Div(className='kpi-card', children=[
                html.Div("Recommended", className='kpi-label'),
                html.Div("69,5%", className='kpi-value'),
            ]),
            html.Div(className='kpi-card', children=[
                html.Div("Not Recommended", className='kpi-label'),
                html.Div("30,5%", className='kpi-value'),
            ]),
            html.Div(className='kpi-card', children=[
                html.Div("Melhor modelo", className='kpi-label'),
                html.Div("Regressão Logística", className='kpi-value', style={'fontSize': '20px', 'marginTop': '4px'}),
                html.Div("F1-Score: 0,8902", className='kpi-sub')
            ]),
        ]),

        # 3. Distribuição das classes & 4. Comparação dos modelos
        html.Div(className='chart-grid-2', children=[
            html.Div(className='card', children=[
                html.Div("Distribuição das reviews após a limpeza", className='card-title'),
                dcc.Graph(id='chart-class-distribution', figure=fig_dist, config={'displayModeBar': False}),
                html.P("A classe Not Recommended representa a menor parcela do conjunto e permaneceu mais difícil de classificar.", 
                       style={'color': 'var(--text-secondary)', 'marginTop': '12px', 'fontSize': '12px'})
            ]),
            html.Div(className='card', children=[
                html.Div("A Regressão Logística apresentou o melhor F1-Score", className='card-title'),
                dcc.Graph(id='chart-model-comparison', figure=fig_models, config={'displayModeBar': False}),
                html.P("Eixo ampliado a partir de 0,78 para facilitar a comparação entre os modelos.", 
                       style={'color': 'var(--text-secondary)', 'marginTop': '12px', 'fontSize': '12px'}),
            ]),
        ]),

        # 5. Tabela de métricas & 6. Matriz de confusão
        html.Div(className='chart-grid-2', children=[
            html.Div(className='card', children=[
                html.Div("Comparação de Modelos Supervisionados", className='card-title'),
                html.Table(
                    table_rows,
                    style={'width': '100%', 'borderCollapse': 'collapse', 'fontSize': '13px', 'marginTop': '10px'}
                ),
                html.P("Precisão, recall e F1-Score referem-se à classe Recommended.", 
                       style={'fontSize': '11px', 'color': 'var(--text-secondary)', 'marginTop': '12px'}),
                html.P("Na Regressão Logística, o F1-Score da classe Not Recommended foi aproximadamente 0,78, com Macro F1 próximo de 0,83.", 
                       style={'fontSize': '11px', 'color': 'var(--text-secondary)', 'marginTop': '4px'}),
            ]),
            html.Div(className='card', children=[
                html.Div("Matriz de confusão da Regressão Logística", className='card-title'),
                dcc.Graph(id='chart-confusion-matrix', figure=fig_cm, config={'displayModeBar': False}),
                html.P("O modelo classificou corretamente 20.748 reviews não recomendadas e 48.593 recomendadas. A classe minoritária apresentou maior dificuldade relativa.", 
                       style={'color': 'var(--text-secondary)', 'marginTop': '12px', 'fontSize': '12px'})
            ]),
        ]),

        # 7. SHAP
        html.Div(className='card', children=[
            html.Div("Termos que mais influenciaram a classificação", className='card-title'),
            html.Div(
                html.Img(
                    src='/assets/shap_summary.png',
                    style={
                        'width': '100%',
                        'maxWidth': '70%',
                        'height': 'auto',
                        'display': 'block',
                        'margin': '0 auto',
                        'borderRadius': '8px',
                        'border': '1px solid var(--border-light)',
                    }
                ),
                style={'padding': '10px 0'}
            ),
            html.P("Termos como “good”, “best”, “great”, “amazing” e “love” contribuíram para classificações positivas. Palavras como “hackers”, “money” e “worse” apareceram associadas à classe negativa.", 
                   style={'color': 'var(--text-primary)', 'marginTop': '12px', 'lineHeight': '1.5'}),
            html.P("As contribuições representam associações aprendidas pelo modelo e não relações causais.", 
                   className='kpi-sub', style={'color': 'var(--text-muted)', 'marginTop': '8px', 'fontStyle': 'italic'})
        ]),

        # 8. Conclusão e limitações
        html.Div(className='card', children=[
            html.Div("Leitura dos resultados", className='card-title'),
            html.P("A classificação textual apresentou resultados superiores ao baseline comercial, mas responde a uma pergunta diferente. O modelo identifica a recomendação expressa nas reviews e não prevê vendas ou sucesso comercial.", 
                   style={'color': 'var(--text-primary)', 'marginBottom': '12px', 'lineHeight': '1.5'}),
            html.P("A base textual contém avaliações de dez jogos, e a divisão aleatória permite que reviews dos mesmos títulos apareçam no treino e no teste. Por isso, os resultados não comprovam generalização para jogos nunca vistos.", 
                   style={'color': 'var(--text-primary)', 'lineHeight': '1.5'}),
        ]),
    ])