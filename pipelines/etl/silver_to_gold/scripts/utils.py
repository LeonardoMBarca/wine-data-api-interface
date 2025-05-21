import pandas as pd
import re
import logging

def split_column_value(df, column_name):
    list_column_value = []

    logging.info("Iniciando split_column_value na coluna '%s'", column_name)
    
    try:
        unique_values = df[column_name].unique()
        logging.info("Foram encontrados %d valores únicos na coluna '%s'", len(unique_values), column_name)

        for idx, original_value in enumerate(unique_values):
            try:
                # Substituir NaNs e valores vazios por uma string padrão
                if pd.isna(original_value) or str(original_value).strip().lower() in ["", "nan", "none"]:
                    logging.warning("Valor nulo encontrado no índice %d — substituindo por 'outros_produtos_comercializados'", idx)
                    original_value = "outros_produtos_comercializados"
                    tokens = ["nao_consta"]
                    list_column_value.append([original_value, tokens])
                    
                    logging.debug("Valor processado com sucesso no índice %d: '%s' -> %s", idx, original_value, tokens)
                
                elif str(original_value).strip().lower() in ["nao_consta_na_tabela", "nao_declarados"]:
                    tokens = ["nao_consta"]
                    list_column_value.append([original_value, tokens])
                    
                    logging.debug("Valor processado com sucesso no índice %d: '%s' -> %s", idx, original_value, tokens)

                elif str(original_value).strip().lower() in ["outros_outros_vinhos_sem_informdetalhada"]:
                    original_value = "outros_vinhos_sem_informacao"
                    tokens = ["nao_consta"]
                    list_column_value.append([original_value, tokens])
                    
                    logging.debug("Valor processado com sucesso no índice %d: '%s' -> %s", idx, original_value, tokens)
                
                else:
                    # 1. Limpeza
                    clean_value = original_value.lower()
                    clean_value = clean_value.replace("(", "").replace(")", "").strip("_")
                    clean_value = clean_value.replace("_", " ")
                    clean_value = re.sub(r'\b(de|da|do|com)\b', '_', clean_value)
                    clean_value = re.sub(r'\s+', ' ', clean_value).strip()
                    clean_value = clean_value.replace(" ", "_")
                    clean_value = re.sub(r'_+', '_', clean_value).strip("_")

                    # 2. Tokenização
                    tokens = clean_value.split("_")

                    # 3. Armazenar [original, [tokens]]
                    list_column_value.append([original_value, tokens])
                    logging.debug("Valor processado com sucesso no índice %d: '%s' -> %s", idx, original_value, tokens)

            except Exception as inner_e:
                logging.error("Erro ao processar valor no índice %d: %s | Erro: %s", idx, original_value, inner_e)
                continue

    except Exception as e:
        logging.critical("Erro fatal ao obter valores únicos da coluna '%s': %s", column_name, e)
        raise RuntimeError(f"Erro ao processar coluna '{column_name}'") from e

    logging.info("split_column_value finalizado com %d entradas processadas com sucesso", len(list_column_value))
    return list_column_value
