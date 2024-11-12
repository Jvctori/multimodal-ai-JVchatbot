from flask import Flask, render_template, request, redirect, url_for, flash
from services.prompt_processor import PromptProcessor
from services.ai_services import AiServices
from services.load_text2img_models import load_models
from services.load_dotenv_keys import load_dotenv_keys

app = Flask(__name__)

try:
    app.secret_key, HUGGING_FACE_APIKEY = load_dotenv_keys()
    ai_services = AiServices(api_token=HUGGING_FACE_APIKEY)
    prompt_processor = PromptProcessor(ai_services)

except Exception as e:

    print(f"Erro na inicialização: {str(e)}")


@app.route("/")
def index():
    """
    Rota principal que renderiza a página inicial.
    """
    try:
        modelos_imagem = load_models("text2img_models.txt")
        result = request.args.get("result")
        result_type = request.args.get("result_type")
        image_name = request.args.get("image_name")

        return render_template(
            "index.html",
            modelos_imagem=modelos_imagem,
            result=result,
            result_type=result_type,
            image_name=image_name,
        )
    except Exception as e:
        flash(f"Erro ao carregar modelos de imagem: {str(e)}")
        return render_template("index.html")


@app.route("/process_prompt", methods=["POST"])
def process_prompt():
    """
    Processa o prompt enviado pelo usuário.
    """
    try:
        unified_prompt = request.form.get("unified_prompt", "").strip()
        modelo_imagem = request.form.get("image_model", "").strip()

        if not unified_prompt or not modelo_imagem:
            flash("Erro: Todos os campos são obrigatórios")
            return redirect(url_for("index"))

        result_type, result = prompt_processor.process_prompt(
            unified_prompt, modelo_imagem
        )

        if result_type == "image":
            return redirect(
                url_for(
                    "index", result=result, result_type=result_type, image_name=result
                )
            )
        else:
            return redirect(url_for("index", result=result, result_type=result_type))

    except ValueError as e:
        flash(f"Erro de validação: {str(e)}")
        return redirect(url_for("index"))
    except Exception as e:
        flash(f"Erro inesperado: {str(e)}")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
