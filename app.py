from pathlib import Path
from uuid import uuid4

from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

UPLOAD_FOLDER.mkdir(exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Validate image extensions accepted by this first version."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def analyze_image_with_mock_data(image_path: Path) -> dict:
    """
    Return temporary analysis data while Azure AI Vision is not connected.

    Future Azure AI Vision integration:
    - Configure endpoint and key through environment variables.
    - Send the uploaded image to Azure AI Vision.
    - Replace the mocked description, tags, and objects below with the API response.
    """
    return {
        "description": "Imagem recebida com sucesso. A descricao automatica sera gerada pelo Azure AI Vision em uma etapa futura.",
        "tags": ["imagem", "upload", "analise visual", "azure-ready"],
        "objects": ["area reservada para objetos detectados"],
        "file_size_kb": round(image_path.stat().st_size / 1024, 2),
    }


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
            error="Formato invalido. Envie uma imagem PNG, JPG, JPEG ou WEBP.",
        )

    original_name = secure_filename(uploaded_file.filename)
    extension = original_name.rsplit(".", 1)[1].lower()
    filename = f"{uuid4().hex}.{extension}"
    destination = app.config["UPLOAD_FOLDER"] / filename
    uploaded_file.save(destination)

    analysis = analyze_image_with_mock_data(destination)

    return render_template(
        "result.html",
        image_url=url_for("uploaded_file", filename=filename),
        filename=original_name,
        analysis=analysis,
    )


@app.route("/uploads/<path:filename>", methods=["GET"])
def uploaded_file(filename: str):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
