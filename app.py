from pathlib import Path
from uuid import uuid4

from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from ultralytics import YOLO, YOLOWorld


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

UPLOAD_FOLDER.mkdir(exist_ok=True)

# Carrega o modelo uma única vez
model = YOLO("yolo11n.pt")

world_model = YOLOWorld("yolov8s-world.pt")
WORLD_CLASSES = [
    "eyeglasses",
    "glasses",
    "watch",
    "headphones",
    "hat",
    "cap",
    "helmet",
]

world_model.set_classes(WORLD_CLASSES)


def allowed_file(filename: str) -> bool:
    """Validate image extensions accepted by this first version."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def translate_label(label: str) -> str:
    translations = {
        "person": "Pessoa",

        "bicycle": "Bicicleta",
        "car": "Carro",
        "motorcycle": "Moto",
        "bus": "Ônibus",
        "truck": "Caminhão",

        "chair": "Cadeira",
        "couch": "Sofá",
        "dining table": "Mesa",

        "laptop": "Notebook",
        "cell phone": "Celular",
        "tv": "Televisão",
        "mouse": "Mouse",

        "bottle": "Garrafa",
        "cup": "Copo",

        "dog": "Cachorro",
        "cat": "Gato",
        "horse": "Cavalo",
        "bird": "Pássaro",

        "backpack": "Mochila",
        "book": "Livro",
        "eyeglasses": "Óculos",
        "glasses": "Óculos",
        "watch": "Relógio",
        "headphones": "Fone de ouvido",

        "hat": "Chapéu",
        "cap": "Boné",
        "helmet": "Capacete",
    }
    return translations.get(label, label.capitalize())

def classify_objects(label: str) -> str: 
    categoria = {
        # Humano
        "person": "Humano",

        # Transportes
        "bicycle": "Transporte",
        "car": "Transporte",
        "motorcycle": "Transporte",
        "bus": "Transporte",
        "truck": "Transporte",
        "train": "Transporte",
        "airplane": "Transporte",
        "boat": "Transporte",

        # Animais
        "dog": "Animal",
        "cat": "Animal",
        "bird": "Animal",
        "horse": "Animal",
        "cow": "Animal",
        "sheep": "Animal",
        "elephant": "Animal",

        # Eletrônicos
        "laptop": "Eletrônico",
        "cell phone": "Eletrônico",
        "tv": "Eletrônico",
        "keyboard": "Eletrônico",
        "mouse": "Eletrônico",
        "headphones": "Eletrônico",

        # Móveis
        "chair": "Móvel",
        "couch": "Móvel",
        "bed": "Móvel",
        "dining table": "Móvel",

        # Acessórios
        "eyeglasses": "Acessório",
        "glasses": "Acessório",
        "watch": "Acessório",
        "hat": "Acessório",
        "cap": "Acessório",
        "helmet": "Acessório",

        # Objetos gerais
        "bottle": "Objeto",
        "cup": "Objeto",
        "book": "Objeto",
        "backpack": "Objeto",
        "umbrella": "Objeto",
    }

    return categoria.get(label, "Objeto")


def extract_detections(results) -> list:
    detections = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls.item())
            confidence = float(box.conf.item())

            label_en = result.names[class_id]
            label_pt = translate_label(label_en)
            category = classify_objects(label_en)

            detections.append(
                {
                    "label_en": label_en,
                    "label_pt": label_pt,
                    "category": category,
                    "confidence": round(confidence * 100, 1),
                }
            )

    return detections


def analyze_image_with_yolo(image_path: Path) -> dict:
    """
    Analisa a imagem utilizando:

    YOLO11:
    - Pessoas
    - Veículos
    - Animais
    - Eletrônicos
    - Móveis
    - Objetos comuns

    YOLO-World:
    - Óculos
    - Relógios
    - Fones
    - Bonés
    - Capacetes
    - Outros acessórios
    """

    # YOLO11 - detector principal
    main_results = model.predict(
        source=str(image_path),
        conf=0.25,
        verbose=False,
    )

    # YOLO-World - detector complementar
    world_results = world_model.predict(
        source=str(image_path),
        conf=0.30,
        verbose=False,
    )

    main_detections = extract_detections(main_results)
    world_detections = extract_detections(world_results)

    detected_items = []

    # Adiciona tudo que o YOLO11 encontrou
    detected_items.extend(main_detections)

    # Adiciona resultados extras do YOLO-World
    detected_items.extend(world_detections)

    tags = set()

    human_count = 0
    other_count = 0

    for item in detected_items:
        category = item["category"]

        tags.add(category.lower())

        if category == "Humano":
            human_count += 1
        else:
            other_count += 1

    if detected_items:

        objects = [
            (
                f'{item["label_pt"]} '
                f'({item["category"]}) - '
                f'{item["confidence"]}%'
            )
            for item in detected_items
        ]

        description = (
            f"Foram detectados {len(detected_items)} elemento(s): "
            f"{human_count} humano(s) e "
            f"{other_count} outro(s)."
        )

    else:

        objects = [
            "Nenhum elemento reconhecido com confiança suficiente."
        ]

        description = (
            "Não foi possível identificar elementos relevantes na imagem."
        )

    return {
        "description": description,
        "tags": sorted(list(tags)) if tags else ["sem deteccoes"],
        "objects": objects,
        "file_size_kb": round(
            image_path.stat().st_size / 1024,
            2
        ),
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

    analysis = analyze_image_with_yolo(destination)

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