from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
import os
import pandas as pd
# IMPORTANDO O PIPELINE
from crawler.scraper.downloader import download_base
from pipelines.etl.bronze_to_silver.main import main as run_bronze_to_silver
from pipelines.etl.silver_to_gold.main import main as run_silver_to_gold

data_bp = Blueprint("data", __name__)
GOLD_LAYER_PATH = "data/gold-layer"

@data_bp.route("/<categoria>/<subcategoria>", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Consulta de Dados'],
    'summary': 'Consulta dados atualizados por categoria e subcategoria',
    'description': '''
Este endpoint consulta dados tratados da **camada Gold** após executar automaticamente o pipeline de ingestão (crawler + ETL).

As categorias representam as seções do site da Embrapa (como Produção ou Exportação), e as subcategorias representam tipos de produto ou agrupamentos internos (como Suco ou Vinhos).

**Categorias disponíveis:**
- `exportacao`
- `importacao`
- `processamento`
- `comercializacao`
- `producao`

**Subcategorias variam por categoria. Exemplo:**
- `/exportacao/suco`
- `/importacao/espumantes`
- `/producao/default`
''',
    'parameters': [
        {
            'name': 'categoria',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Categoria da aba (ex: exportacao, importacao, processamento, comercializacao, producao)'
        },
        {
            'name': 'subcategoria',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Tipo de dado dentro da categoria (ex: suco, vinhos, espumantes, default)'
        }
    ],
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Consulta realizada com sucesso',
            'content': {
                'application/json': {
                    'example': {
                        "mensagem": "Dados de exportacao/suco carregados com sucesso!",
                        "usuario": "user",
                        "dados": [
                            {
                                "pais": "brasil",
                                "ano": 1970,
                                "kilograms": 1000,
                                "dollars": 5000
                            },
                            {
                                "pais": "alemanha",
                                "ano": 1970,
                                "kilograms": 0,
                                "dollars": 0
                            }
                        ]
                    }
                }
            }
        },
        400: {
            'description': 'Categoria ou subcategoria inválida',
            'content': {
                'application/json': {
                    'example': {
                        "erro": "Categoria ou subcategoria inválida."
                    }
                }
            }
        },
        404: {
            'description': 'Arquivo da camada gold não encontrado',
            'content': {
                'application/json': {
                    'example': {
                        "erro": "Arquivo 'ExpSuco.csv' não encontrado."
                    }
                }
            }
        },
        500: {
            'description': 'Erro interno inesperado',
            'content': {
                'application/json': {
                    'example': {
                        "erro": "Erro interno: File not found or pipeline error"
                    }
                }
            }
        }
    }
})

def consulta_categoria_subcategoria(categoria, subcategoria):
    """
    Consulta dados da api por categora e subcategoria.
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
        download_base()
        run_bronze_to_silver()
        run_silver_to_gold()
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
