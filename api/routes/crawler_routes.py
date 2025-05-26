from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from crawler.scraper.downloader import download_base
from pipelines.etl.bronze_to_silver.main import main as run_bronze_to_silver
from pipelines.etl.silver_to_gold.main import main as run_silver_to_gold   

crawler_bp = Blueprint("crawler", __name__)

@crawler_bp.route("/executar", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Crawler'],
    'summary': 'Executar pipeline de dados se caso necessário',
    'description': 'Executa as etapas do processo de ingestão: download da base, bronze → silver, silver → gold.',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Crawler executado com sucesso',
            'examples': {
                'application/json': {
                    "mensagem": "Crawler executado com sucesso!"
                }
            }
        },
        500: {
            'description': 'Erro durante a execução do pipeline'
        }
    }
})
def executar():
    try:
        download_base()
        run_bronze_to_silver() 
        run_silver_to_gold()
        return jsonify({"mensagem": "Crawler executado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao executar o crawler: {str(e)}"}), 500
