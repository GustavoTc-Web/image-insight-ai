from pathlib import Path

from ultralytics import YOLO, YOLOWorld

from config import (
    DEFAULT_MAIN_CONFIDENCE,
    DEFAULT_WORLD_CONFIDENCE,
    MAIN_CONFIDENCE,
    WORLD_CLASSES,
    WORLD_CONFIDENCE,
)
from utils.labels import classify_objects, normalize_label, translate_label


# Carrega os modelos uma única vez, durante a importação do serviço.
model = YOLO("yolo11n.pt")
world_model = YOLOWorld("yolov8s-world.pt")
world_model.set_classes(WORLD_CLASSES)


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
