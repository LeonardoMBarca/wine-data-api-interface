import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import os
from functools import wraps
from .auth_config import DASHBOARD_USER, DASHBOARD_PASSWORD
from crawler.scraper.downloader import download_base
from pipelines.etl.bronze_to_silver.main import main as run_bronze_to_silver
from pipelines.etl.silver_to_gold.main import main as run_silver_to_gold

dashboard_bp = Blueprint(
    'dashboard',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/dashboard/static'
)

# Decorator para verificar se o usuário está logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('dashboard.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

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

@dashboard_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == DASHBOARD_USER and password == DASHBOARD_PASSWORD:
            session['logged_in'] = True
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Credenciais inválidas. Tente novamente.')
    
    return render_template('login.html')

@dashboard_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('dashboard.login'))

@dashboard_bp.route('/atualizar-dados', methods=['POST'])
@login_required
def atualizar_dados():
    try:
        # Executa o crawler para baixar os dados
        if download_base():
            # Se o crawler for bem-sucedido, executa os pipelines ETL
            run_bronze_to_silver()
            run_silver_to_gold()
            return jsonify({"status": "success", "message": "Dados atualizados com sucesso!"})
        else:
            # Se o crawler falhar
            return jsonify({"status": "error", "message": "Site da Embrapa se encontra indisponível no momento."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao atualizar dados: {str(e)}"})

@dashboard_bp.route('/')
@login_required
def index():
    dados, colunas, filtros = carregar_dados('comercio.csv')
    return render_template('index.html', dados=dados, colunas=colunas, filtros=filtros)

@dashboard_bp.route('/exportacao')
@login_required
def exportacao():
    dados, colunas, filtros = carregar_dados('exportacao.csv')
    return render_template('exportacao.html', dados=dados, colunas=colunas, filtros=filtros)

@dashboard_bp.route('/importacao')
@login_required
def importacao():
    dados, colunas, filtros = carregar_dados('importacao.csv')
    return render_template('importacao.html', dados=dados, colunas=colunas, filtros=filtros)

@dashboard_bp.route('/processamento')
@login_required
def processamento():
    dados, colunas, filtros = carregar_dados('processamento.csv')
    return render_template('processamento.html', dados=dados, colunas=colunas, filtros=filtros)

@dashboard_bp.route('/producao')
@login_required
def producao():
    dados, colunas, filtros = carregar_dados('producao.csv')
    return render_template('producao.html', dados=dados, colunas=colunas, filtros=filtros)