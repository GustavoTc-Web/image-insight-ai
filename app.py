from pathlib import Path
from uuid import uuid4

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename

from services.vision import analyze_image_with_yolo


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp",
}


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

UPLOAD_FOLDER.mkdir(exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Valida as extensões de imagem aceitas."""

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def is_valid_image(image_path: Path) -> bool:
    """Verifica se o arquivo é realmente uma imagem válida."""

    try:
        with Image.open(image_path) as image:
            image.verify()

        return True

    except (UnidentifiedImageError, OSError):
        return False


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    uploaded_file = request.files.get("image")

    if not uploaded_file or uploaded_file.filename == "":
        return redirect(url_for("index"))

    if not allowed_file(uploaded_file.filename):
        return render_template(
            "index.html",
            error=(
                "Formato inválido. "
                "Envie uma imagem PNG, JPG, JPEG ou WEBP."
            ),
        )

    original_name = secure_filename(
        uploaded_file.filename
    )

    extension = original_name.rsplit(
        ".",
        1,
    )[1].lower()

    filename = f"{uuid4().hex}.{extension}"

    destination = (
        app.config["UPLOAD_FOLDER"]
        / filename
    )

    uploaded_file.save(destination)

    # Valida o conteúdo real da imagem.
    if not is_valid_image(destination):
        destination.unlink(missing_ok=True)

        return render_template(
            "index.html",
            error=(
                "O arquivo enviado não é uma imagem válida "
                "ou está corrompido."
            ),
        )

    # Executa a análise com YOLO.
    try:
        analysis = analyze_image_with_yolo(
            destination
        )

    except Exception as error:
        destination.unlink(missing_ok=True)

        app.logger.exception(
            "Erro durante a análise da imagem: %s",
            error,
        )

        return render_template(
            "index.html",
            error=(
                "Não foi possível analisar esta imagem. "
                "Tente novamente com outro arquivo."
            ),
        ), 500

    return render_template(
        "result.html",
        image_url=url_for(
            "uploaded_file",
            filename=filename,
        ),
        filename=original_name,
        analysis=analysis,
    )


@app.route(
    "/uploads/<path:filename>",
    methods=["GET"],
)
def uploaded_file(filename: str):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
    )


@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "index.html",
        error=(
            "A imagem é muito grande. "
            "O tamanho máximo permitido é 8 MB."
        ),
    ), 413


if __name__ == "__main__":
    app.run(debug=True)