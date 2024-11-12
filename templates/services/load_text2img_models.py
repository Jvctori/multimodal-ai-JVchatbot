
def load_models(txt: str) -> list[str]:
    """
    Carrega os modelos de imagem do arquivo de configuração.
    """
    try:

        with open(txt, "r") as file:
            models = [model.strip().replace('"', '') for model in file.readlines()]

        return models

    except Exception as e:

        raise Exception(f"Erro ao carregar modelos de imagem: {str(e)}")
