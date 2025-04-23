from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from crawler.scraper.downloader import download_base

crawler_bp = Blueprint("crawler", __name__)

@crawler_bp.route("/executar", methods=["POST"])
@jwt_required()
def executar():
    try:
        download_base()
        return jsonify({"mensagem": "Crawler executado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao executar o crawler: {str(e)}"}), 500