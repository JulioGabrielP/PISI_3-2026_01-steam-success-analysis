import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, html
from utils.data_loader import load_main_data, apply_filters
from callbacks.theme import (base_layout, empty_fig, BG_CARD, ACCENT, TEXT,
                              TEXT_MUT, GRID, CLUSTER_COLORS, RATING_COLORS)


def register_callbacks(app):

    # ── Filter count display ───────────────────────────────────────────────────
    @app.callback(
        Output('filter-count-display', 'children'),
        Output('filter-ratio-label', 'children'),
        Input('filter-tags', 'value'),
        Input('filter-price-range', 'value'),
        Input('filter-positive-ratio', 'value'),
        Input('filter-clusters', 'value'),
        Input('filter-steam-deck', 'value'),
        Input('filter-year-range', 'value'),
    )
    def update_count(tags, price_range, ratio_min, clusters, steam_deck, year_range):
        df = load_main_data()
        filtered = apply_filters(df, tags, price_range, ratio_min, clusters,
                                 steam_deck, year_range)
        pct = len(filtered) / len(df) * 100
        return (f'{len(filtered):,} jogos ({pct:.1f}%)',
                f'≥ {ratio_min or 0}%')

    # ── KPIs ──────────────────────────────────────────────────────────────────
    @app.callback(
        Output('overview-kpis', 'children'),
        Input('filter-tags', 'value'),
        Input('filter-price-range', 'value'),
        Input('filter-positive-ratio', 'value'),
        Input('filter-clusters', 'value'),
        Input('filter-steam-deck', 'value'),
        Input('filter-year-range', 'value'),
    )
    def update_kpis(tags, price_range, ratio_min, clusters, steam_deck, year_range):
        df = load_main_data()
        d = apply_filters(df, tags, price_range, ratio_min, clusters, steam_deck, year_range)
        if d.empty:
            return []
        kpis = [
            (
                'JOGOS',
                f'{len(d):,}',
                f'{len(d) / len(df) * 100:.1f}% do conjunto'
            ),
            (
                'REVIEWS REGISTRADAS',
                f'{d["user_reviews"].sum():,.0f}',
                'indicador acumulado de alcance'
            ),
            (
                'APROVAÇÃO MEDIANA',
                f'{d["positive_ratio"].median():.0f}%',
                f'média de {d["positive_ratio"].mean():.1f}%'
            ),
            (
                'HORAS JOGADAS',
                f'{d["avg_hours"].median():.1f} h',
                'mediana por jogo'
            ),
]
        return [html.Div(className='kpi-card', children=[
            html.Div(label, className='kpi-label'),
            html.Div(val, className='kpi-value'),
            html.Div(sub, className='kpi-sub'),
        ]) for label, val, sub in kpis]

    # ── Tag revenue bar ───────────────────────────────────────────────────────
    @app.callback(
        Output('chart-tag-revenue', 'figure'),
        Input('filter-tags', 'value'),
        Input('filter-price-range', 'value'),
        Input('filter-positive-ratio', 'value'),
        Input('filter-clusters', 'value'),
        Input('filter-steam-deck', 'value'),
        Input('filter-year-range', 'value'),
    )

    # ── Rating donut ──────────────────────────────────────────────────────────
    @app.callback(
        Output('chart-rating-pie', 'figure'),
        Input('filter-tags', 'value'),
        Input('filter-price-range', 'value'),
        Input('filter-positive-ratio', 'value'),
        Input('filter-clusters', 'value'),
        Input('filter-steam-deck', 'value'),
        Input('filter-year-range', 'value'),
    )

    # ── Price histogram ───────────────────────────────────────────────────────
    @app.callback(
        Output('chart-price-dist', 'figure'),
        Input('filter-tags', 'value'),
        Input('filter-price-range', 'value'),
        Input('filter-positive-ratio', 'value'),
        Input('filter-clusters', 'value'),
        Input('filter-steam-deck', 'value'),
        Input('filter-year-range', 'value'),
    )

    # ── Positive ratio histogram ──────────────────────────────────────────────
    @app.callback(
        Output('chart-ratio-dist', 'figure'),
        Input('filter-tags', 'value'),
        Input('filter-price-range', 'value'),
        Input('filter-positive-ratio', 'value'),
        Input('filter-clusters', 'value'),
        Input('filter-steam-deck', 'value'),
        Input('filter-year-range', 'value'),
    )
    # ── Scatter reviews vs positive ratio ─────────────────────────────────────
    @app.callback(
        Output('chart-scatter-reviews', 'figure'),
        Input('filter-tags', 'value'),
        Input('filter-price-range', 'value'),
        Input('filter-positive-ratio', 'value'),
        Input('filter-clusters', 'value'),
        Input('filter-steam-deck', 'value'),
        Input('filter-year-range', 'value'),
    )
    def update_scatter_reviews(tags, price_range, ratio_min, clusters, steam_deck, year_range):
        df = load_main_data()
        d = apply_filters(df, tags, price_range, ratio_min, clusters, steam_deck, year_range)
        if d.empty:
            return empty_fig()

        sample = d.sample(min(4000, len(d)), random_state=42)
        sample = sample[sample['user_reviews'] > 0]

        fig = go.Figure(go.Scatter(
            x=sample['positive_ratio'],
            y=sample['user_reviews'],
            mode='markers',
            marker=dict(color=ACCENT, size=4, opacity=0.5),
            hovertemplate='<b>%{text}</b><br>Aprovação: %{x:.0f}%<br>Reviews: %{y:,}<extra></extra>',
            text=sample['title'],
        ))

        layout = base_layout(height=340)
        layout['xaxis']['title'] = 'Taxa de aprovação (%)'
        layout['yaxis']['title'] = 'Volume de reviews'
        layout['yaxis']['type'] = 'log'
        layout['showlegend'] = False
        fig.update_layout(**layout)
        return fig

    # ── Spearman heatmap ──────────────────────────────────────────────────────
    @app.callback(
        Output('chart-heatmap', 'figure'),
        Input('filter-tags', 'value'),
        Input('filter-price-range', 'value'),
        Input('filter-positive-ratio', 'value'),
        Input('filter-clusters', 'value'),
        Input('filter-steam-deck', 'value'),
        Input('filter-year-range', 'value'),
    )
    def update_heatmap(tags, price_range, ratio_min, clusters, steam_deck, year_range):
        df = load_main_data()
        d = apply_filters(df, tags, price_range, ratio_min, clusters, steam_deck, year_range)
        if len(d) < 10:
            return empty_fig()

        cols = ['positive_ratio', 'user_reviews', 'price_final',
                'discount', 'est_revenue_proxy', 'avg_hours']
        labels = [
            'Aprovação',
            'Reviews',
            'Preço',
            'Desconto',
            'Desempenho estimado',
            'Horas jogadas'
        ]
        corr = d[cols].corr(method='spearman').values

        fig = go.Figure(go.Heatmap(
            z=corr, x=labels, y=labels,
            colorscale=[[0, '#8b2020'], [0.5, '#16202d'], [1, '#4a9a6a']],
            zmin=-1, zmax=1,
            text=[[f'{v:.2f}' for v in row] for row in corr],
            texttemplate='%{text}',
            textfont=dict(size=10),
            showscale=True,
            colorbar=dict(tickfont=dict(color=TEXT_MUT, size=9)),
            hovertemplate='%{y} × %{x}: %{z:.3f}<extra></extra>',
        ))
        layout = base_layout(height=380)
        layout['xaxis']['tickfont'] = dict(size=9)
        layout['xaxis']['tickangle'] = -25
        layout['xaxis']['automargin'] = True
        layout['yaxis']['tickfont'] = dict(size=9)
        layout['yaxis']['automargin'] = True
        layout['yaxis']['autorange'] = 'reversed'
        layout['margin'] = dict(l=110, r=20, t=10, b=90)
        fig.update_layout(**layout)
        return fig
