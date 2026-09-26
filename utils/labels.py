def translate_label(label: str) -> str:
    translations = {
        # Humano
        "person": "Pessoa",

        # Transportes
        "bicycle": "Bicicleta",
        "car": "Carro",
        "motorcycle": "Moto",
        "bus": "Ônibus",
        "truck": "Caminhão",
        "train": "Trem",
        "airplane": "Avião",
        "boat": "Barco",

        # Móveis
        "chair": "Cadeira",
        "couch": "Sofá",
        "bed": "Cama",
        "dining table": "Mesa",

        # Eletrônicos
        "laptop": "Notebook",
        "cell phone": "Celular",
        "tv": "Televisão",
        "keyboard": "Teclado",
        "mouse": "Mouse",
        "headphones": "Fone de ouvido",

        # Objetos gerais
        "bottle": "Garrafa",
        "cup": "Copo",
        "book": "Livro",
        "backpack": "Mochila",
        "umbrella": "Guarda-chuva",

        # Animais
        "dog": "Cachorro",
        "cat": "Gato",
        "horse": "Cavalo",
        "bird": "Pássaro",
        "cow": "Vaca",
        "sheep": "Ovelha",
        "elephant": "Elefante",

        # Acessórios
        "eyeglasses": "Óculos",
        "glasses": "Óculos",
        "sunglasses": "Óculos",
        "watch": "Relógio",
        "hat": "Chapéu",
        "cap": "Boné",
        "helmet": "Capacete",

        # Automotivo
        "steering wheel": "Volante",
        "dashboard": "Painel do carro",
        "gear shift": "Câmbio",
        "rearview mirror": "Retrovisor",
        "seat belt": "Cinto de segurança",
    }

    return translations.get(label, label.capitalize())


def classify_objects(label: str) -> str:
    categories = {
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
        "sunglasses": "Acessório",
        "watch": "Acessório",
        "hat": "Acessório",
        "cap": "Acessório",
        "helmet": "Acessório",

        # Automotivo
        "steering wheel": "Automotivo",
        "dashboard": "Automotivo",
        "gear shift": "Automotivo",
        "rearview mirror": "Automotivo",
        "seat belt": "Automotivo",

        # Objetos gerais
        "bottle": "Objeto",
        "cup": "Objeto",
        "book": "Objeto",
        "backpack": "Objeto",
        "umbrella": "Objeto",
    }

    return categories.get(label, "Objeto")


def normalize_label(label: str) -> str:
    aliases = {
        "glasses": "eyeglasses",
        "sunglasses": "eyeglasses",
        "cap": "hat",
    }

    return aliases.get(label, label)