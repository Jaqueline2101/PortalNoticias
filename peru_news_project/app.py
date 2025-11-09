from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Ruta donde se guardan las noticias
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

@app.route('/')
def home():
    """Página principal: muestra las noticias más recientes"""
    files = sorted(
        [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')],
        reverse=True
    )
    if not files:
        return "No hay noticias disponibles aún."

    latest_file = os.path.join(DATA_DIR, files[0])
    df = pd.read_csv(latest_file)

    news = df.to_dict(orient='records')
    return render_template('index.html', news=news)


@app.route('/api/news')
def api_news():
    """Devuelve las noticias en formato JSON"""
    files = sorted(
        [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')],
        reverse=True
    )
    if not files:
        return jsonify([])

    latest_file = os.path.join(DATA_DIR, files[0])
    df = pd.read_csv(latest_file)
    return df.to_json(orient='records', force_ascii=False)


if __name__ == '__main__':
    app.run(debug=True)
