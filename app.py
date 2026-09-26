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
    # Acessórios
    "eyeglasses",
    "glasses",
    "sunglasses",
    "watch",
    "headphones",
    "hat",
    "cap",
    "helmet",

    #Elementos automotivos
    "steering wheel",
    "dashboard",
]

world_model.set_classes(WORLD_CLASSES)

MAIN_CONFIDENCE = {
    "person": 0.45,
    "bicycle": 0.50,
    "car": 0.55,
    "motorcycle": 0.55,
    "bus": 0.50,
    "truck": 0.50,

    "chair": 0.55,
    "couch": 0.50,
    "dining table": 0.50,

    "laptop": 0.45,
    "cell phone": 0.40,
    "tv": 0.45,

    "dog": 0.45,
    "cat": 0.45,
}

WORLD_CONFIDENCE = {
    "eyeglasses": 0.30,
    "glasses": 0.30,
    "watch": 0.35,
    "headphones": 0.35,
    "hat": 0.35,
    "cap": 0.35,
    "helmet": 0.40,
}

DEFAULT_MAIN_CONFIDENCE = 0.50
DEFAULT_WORLD_CONFIDENCE = 0.35


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


def normalize_label(label: str) -> str:
    aliases = {
        "glasses": "eyeglasses",
        "sunglasses": "eyeglasses",
        "cap": "hat",
    }

    return aliases.get(label, label)


def extract_detections(results, source_model: str) -> list:
    detections = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls.item())
            confidence = float(box.conf.item())

            original_label = result.names[class_id]
            label_en = normalize_label(original_label)

            if source_model == "YOLO11":
                minimum_confidence = MAIN_CONFIDENCE.get(
                    label_en,
                    DEFAULT_MAIN_CONFIDENCE,
                )
            else:
                minimum_confidence = WORLD_CONFIDENCE.get(
                    label_en,
                    DEFAULT_WORLD_CONFIDENCE,
                )

            # Ignora detecções abaixo da confiança mínima
            if confidence < minimum_confidence:
                continue

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append(
                {
                    "label_en": label_en,
                    "label_pt": translate_label(label_en),
                    "category": classify_objects(label_en),
                    "confidence": round(confidence * 100, 1),
                    "source": source_model,
                    "box": {
                        "x1": float(x1),
                        "y1": float(y1),
                        "x2": float(x2),
                        "y2": float(y2),
                    },
                }
            )

    return detections

def calculate_iou(box_a: dict, box_b: dict) -> float:
    x1 = max(box_a["x1"], box_b["x1"])
    y1 = max(box_a["y1"], box_b["y1"])
    x2 = min(box_a["x2"], box_b["x2"])
    y2 = min(box_a["y2"], box_b["y2"])

    if x2 <= x1 or y2 <= y1:
        return 0.0

    intersection = (x2 - x1) * (y2 - y1)

    area_a = (
        (box_a["x2"] - box_a["x1"])
        * (box_a["y2"] - box_a["y1"])
    )

    area_b = (
        (box_b["x2"] - box_b["x1"])
        * (box_b["y2"] - box_b["y1"])
    )

    union = area_a + area_b - intersection

    if union <= 0:
        return 0.0

    return intersection / union

def calculate_containment(box_a: dict, box_b: dict) -> float:
    x1 = max(box_a["x1"], box_b["x1"])
    y1 = max(box_a["y1"], box_b["y1"])
    x2 = min(box_a["x2"], box_b["x2"])
    y2 = min(box_a["y2"], box_b["y2"])

    if x2 <= x1 or y2 <= y1:
        return 0.0

    intersection = (x2 - x1) * (y2 - y1)

    area_a = (
        (box_a["x2"] - box_a["x1"])
        * (box_a["y2"] - box_a["y1"])
    )

    area_b = (
        (box_b["x2"] - box_b["x1"])
        * (box_b["y2"] - box_b["y1"])
    )

    smaller_area = min(area_a, area_b)

    if smaller_area <= 0:
        return 0.0

    return intersection / smaller_area

def remove_duplicate_detections(detections: list) -> list:
    detections = sorted(
        detections,
        key=lambda item: item["confidence"],
        reverse=True,
    )

    filtered = []

    for candidate in detections:
        is_duplicate = False

        for accepted in filtered:
            if candidate["label_en"] != accepted["label_en"]:
                continue

            iou = calculate_iou(
                candidate["box"],
                accepted["box"],
            )

            containment = calculate_containment(
                candidate["box"],
                accepted["box"],
            )

            if iou >= 0.40 or containment >= 0.70:
                is_duplicate = True
                break

        if not is_duplicate:
            filtered.append(candidate)

    return filtered


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

    main_detections = extract_detections(
        main_results,
        source_model="YOLO11",
        )
    world_detections = extract_detections(
        world_results,
        source_model="YOLO-World",
        )

    detected_items = []

    # Adiciona tudo que o YOLO11 encontrou
    detected_items.extend(main_detections)

    # Adiciona resultados extras do YOLO-World
    detected_items.extend(world_detections)

    detected_items = remove_duplicate_detections(detected_items)

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