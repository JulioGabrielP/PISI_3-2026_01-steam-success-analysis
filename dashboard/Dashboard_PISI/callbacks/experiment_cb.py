import joblib
import os
from dash import Input, Output, State, html

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')


def register_callbacks(app):

    @app.callback(
        Output('experiment-output', 'children'),
        Input('experiment-predict-btn', 'n_clicks'),
        State('experiment-input-text', 'value'),
        prevent_initial_call=True,
    )
    def predict_review(n_clicks, text):
        if not text or not text.strip():
            return html.Div(
                '⚠️  Digite uma review antes de prever.',
                style={'color': '#f4a460', 'fontSize': '13px'},
            )

        try:
            model = joblib.load(os.path.join(DATA_DIR, 'modelo_classificacao_reviews.pkl'))
            vectorizer = joblib.load(os.path.join(DATA_DIR, 'tfidf_vectorizer.pkl'))
        except FileNotFoundError:
            return html.Div(
                '❌  Arquivos do modelo não encontrados em data/. Verifique se logistic_model.pkl e tfidf_vectorizer.pkl estão na pasta data/.',
                style={'color': '#c94f4f', 'fontSize': '13px'},
            )

        X = vectorizer.transform([text])
        pred = model.predict(X)[0]
        prob = model.predict_proba(X)[0]

        is_success = pred == 1
        label = '✅  Recommended' if is_success else '❌  Not Recommended'
        color = '#5ba85f' if is_success else '#c94f4f'
        conf = prob[1] if is_success else prob[0]

        return html.Div([
            html.Div(
                label,
                style={
                    'fontSize': '22px',
                    'fontWeight': '700',
                    'color': color,
                    'fontFamily': 'Rajdhani, sans-serif',
                    'marginBottom': '8px',
                },
            ),
            html.Div(
                f'Confiança do modelo: {conf:.1%}',
                style={
                    'fontSize': '13px',
                    'color': 'var(--text-muted)',
                },
            ),
        ])
