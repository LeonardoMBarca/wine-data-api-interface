from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import pandas as pd

data_bp = Blueprint("data", __name__)

GOLD_LAYER_PATH = "data/gold-layer"

@data_bp.route("/consulta/<tabela>", methods=["GET"])
@jwt_required()
def consulta_tabela(tabela):
    current_user = get_jwt_identity()

    # Caminho completo do arquivo CSV
    tabela_path = os.path.join(GOLD_LAYER_PATH, f"{tabela}.csv")

    if not os.path.exists(tabela_path):
        return jsonify({"erro": f"Tabela '{tabela}' não encontrada na camada gold."}), 404

    try:
        df = pd.read_csv(tabela_path)

        dados = df.to_dict(orient="records")

        return jsonify({
            "mensagem": f"Tabela '{tabela}' acessada com sucesso!",
            "usuario": current_user,
            "dados": dados
        }), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao acessar a tabela '{tabela}': {str(e)}"}), 500