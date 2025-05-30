import pandas as pd
from flask import Blueprint, render_template
import os

dashboard_bp = Blueprint(
    'dashboard',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/dashboard/static'
)

colunas_filtro_por_arquivo = {
    'comercio.csv': ["ano", "categoria", "subcategoria", "tipo_estilo", "processamento"],
    'exportacao.csv': ["ano", "categoria", "pais"],
    'importacao.csv': ["ano", "categoria", "pais"],
    'processamento.csv': ["ano", "categoria", "subcategoria", "tipo_estilo", "origem", "classificacao"],
    'producao.csv': ["ano", "categoria", "subcategoria", "tipo_estilo", "processamento"]
}

def carregar_dados(nome_arquivo_csv):
    caminho_csv = os.path.join('data', 'analytics', nome_arquivo_csv)
    df = pd.read_csv(caminho_csv)
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.fillna('')

    col_filtros = colunas_filtro_por_arquivo.get(nome_arquivo_csv, [])

    filtros = {}
    for col in col_filtros:
        if col in df.columns:
            filtros[col] = sorted(df[col].unique())

    dados = df.to_dict(orient='records')
    colunas = df.columns.tolist()

    return dados, colunas, filtros

@dashboard_bp.route('/')
def index():
    dados, colunas, filtros = carregar_dados('comercio.csv')
    return render_template('index.html', dados=dados, colunas=colunas, filtros=filtros)

@dashboard_bp.route('/exportacao')
def exportacao():
    dados, colunas, filtros = carregar_dados('exportacao.csv')
    return render_template('exportacao.html', dados=dados, colunas=colunas, filtros=filtros)

@dashboard_bp.route('/importacao')
def importacao():
    dados, colunas, filtros = carregar_dados('importacao.csv')
    return render_template('importacao.html', dados=dados, colunas=colunas, filtros=filtros)

@dashboard_bp.route('/processamento')
def processamento():
    dados, colunas, filtros = carregar_dados('processamento.csv')
    return render_template('processamento.html', dados=dados, colunas=colunas, filtros=filtros)

@dashboard_bp.route('/producao')
def producao():
    dados, colunas, filtros = carregar_dados('producao.csv')
    return render_template('producao.html', dados=dados, colunas=colunas, filtros=filtros)