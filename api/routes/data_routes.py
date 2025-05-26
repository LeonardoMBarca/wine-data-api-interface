from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
import os
import pandas as pd

data_bp = Blueprint("data", __name__)
GOLD_LAYER_PATH = "data/gold-layer"

@data_bp.route("/<categoria>/<subcategoria>", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Consulta de Dados'],
    'summary': 'Consulta dados tratados por categoria e subcategoria',
    'description': 'Esse endpoint retorna os dados de uma tabela CSV localizada na camada gold, categorizada por aba (ex: exportação, importação, processamento, etc).',
    'parameters': [
        {
            'name': 'categoria',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Categoria da informação: exportacao, importacao, processamento, comercializacao, producao.'
        },
        {
            'name': 'subcategoria',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Subcategoria da informação: exemplo - espumantes, suco, vinhos, etc.'
        }
    ],
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Consulta realizada com sucesso',
            'examples': {
                'application/json': {
                    "mensagem": "Dados de exportacao/suco carregados com sucesso!",
                    "usuario": "usuario_exemplo",
                    "dados": [{"coluna1": "valor1"}, {"coluna1": "valor2"}]
                }
            }
        },
        400: {
            'description': 'Categoria ou subcategoria inválida'
        },
        404: {
            'description': 'Arquivo não encontrado'
        },
        500: {
            'description': 'Erro interno'
        }
    }
})
def consulta_categoria_subcategoria(categoria, subcategoria):
    """
    Consulta dados da camada gold por categoria/subcategoria
    ---
    """
    current_user = get_jwt_identity()

    arquivos = {
        "exportacao": {
            "espumantes": "ExpEspumantes.csv",
            "suco": "ExpSuco.csv",
            "uva": "ExpUva.csv",
            "vinho": "ExpVinho.csv"
        },
        "importacao": {
            "espumantes": "ImpEspumantes.csv",
            "frescas": "ImpFrescas.csv",
            "passas": "ImpPassas.csv",
            "suco": "ImpSuco.csv",
            "vinhos": "ImpVinhos.csv"
        },
        "processamento": {
            "americanas": "ProcessaAmericanas.csv",
            "mesa": "ProcessaMesa.csv",
            "semclass": "ProcessaSemclass.csv",
            "viniferas": "ProcessaViniferas.csv"
        },
        "comercializacao": {
            "default": "comercio.csv"
        },
        "producao": {
            "default": "producao.csv"
        }
    }

    try:
        arquivo_csv = arquivos[categoria].get(subcategoria) or arquivos[categoria]["default"]
        caminho = os.path.join(GOLD_LAYER_PATH, arquivo_csv)

        if not os.path.exists(caminho):
            return jsonify({"erro": f"Arquivo '{arquivo_csv}' não encontrado."}), 404

        df = pd.read_csv(caminho)
        dados = df.to_dict(orient="records")

        return jsonify({
            "mensagem": f"Dados de {categoria}/{subcategoria} carregados com sucesso!",
            "usuario": current_user,
            "dados": dados
        }), 200

    except KeyError:
        return jsonify({"erro": "Categoria ou subcategoria inválida."}), 400
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500
