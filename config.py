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

    # Automotivo
    "steering wheel",
    "dashboard",
    "gear shift",
    "rearview mirror",
    "seat belt",
]


MAIN_CONFIDENCE = {
    "person": 0.45,

    "bicycle": 0.50,
    "car": 0.45,
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
    # Acessórios
    "eyeglasses": 0.22,
    "glasses": 0.22,
    "sunglasses": 0.22,

    "watch": 0.35,
    "headphones": 0.35,
    "hat": 0.35,
    "cap": 0.35,
    "helmet": 0.40,

    # Automotivo
    "steering wheel": 0.22,
    "dashboard": 0.25,
    "gear shift": 0.25,
    "rearview mirror": 0.25,
    "seat belt": 0.25,
}


DEFAULT_MAIN_CONFIDENCE = 0.50
DEFAULT_WORLD_CONFIDENCE = 0.35