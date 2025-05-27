import pandas as pd
from flask import Blueprint, render_template
import os

dashboard_bp = Blueprint(
    'dashboard',                  # ← nome precisa ser 'dashboard'
    __name__,
    template_folder='templates',
    static_folder='static',       # ← onde estão seus CSS/JS
    static_url_path='/dashboard/static'  # ← TRUQUE CHAVE para resolver
)

@dashboard_bp.route('/')
def index():
    caminho_csv = os.path.join('data', 'gold-layer', 'comercio.csv')
    df = pd.read_csv(caminho_csv)

    df.columns = [col.strip().lower() for col in df.columns]

    df = df.fillna('')

    dados = df.to_dict(orient='records')
    colunas = df.columns.tolist()

    filtros = {
        "ano": sorted(df['ano'].unique()),
        "categoria": sorted(df['categoria'].unique()),
        "subcategoria": sorted(df['subcategoria'].unique()),
        "tipo_estilo": sorted(df['tipo_estilo'].unique()),
        "processamento": sorted(df['processamento'].unique())
    }

    return render_template('index.html', dados=dados, colunas=colunas, filtros=filtros)