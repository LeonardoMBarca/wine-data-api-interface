from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from crawler.scraper.downloader import download_base
from pipelines.etl.bronze_to_silver.main import main as run_bronze_to_silver
from pipelines.etl.silver_to_gold.main import main as run_silver_to_gold   

crawler_bp = Blueprint("crawler", __name__)

@crawler_bp.route("/executar", methods=["POST"])
@jwt_required()
def executar():
    try:
        download_base()
        run_bronze_to_silver() 
        run_silver_to_gold()
        return jsonify({"mensagem": "Crawler executado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao executar o crawler: {str(e)}"}), 500