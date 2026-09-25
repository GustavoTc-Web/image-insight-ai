from pathlib import Path

from ultralytics import YOLO


IMAGE_PATH = Path("teste.jpg")

if not IMAGE_PATH.exists():
    raise FileNotFoundError("A imagem teste.jpg nao foi encontrada.")

# Carrega um modelo YOLO pré-treinado
model = YOLO("yolo11n.pt")

# Analisa a imagem
results = model.predict(
    source=str(IMAGE_PATH),
    conf=0.25,
    verbose=False,
)

for result in results:
    if len(result.boxes) == 0:
        print("Nenhum objeto foi detectado.")
        continue

    for box in result.boxes:
        class_id = int(box.cls.item())
        confidence = float(box.conf.item())

        name = result.names[class_id]

        if name == "person":
            category = "Humano"
        else:
            category = "Objeto"

        print(
            f"{category} | {name} | "
            f"Confianca: {confidence * 100:.1f}%"
        )