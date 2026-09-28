# TeceVision

**TeceVision** é uma aplicação web de Visão Computacional desenvolvida em Python e Flask para análise de imagens utilizando modelos YOLO.

A aplicação permite enviar uma imagem pelo navegador e identificar automaticamente pessoas, animais, veículos, objetos e acessórios, exibindo os elementos encontrados com nível de confiança e caixas delimitadoras diretamente sobre a imagem.

Todo o processamento de Inteligência Artificial é realizado localmente, sem necessidade de enviar as imagens para serviços externos.

---

## Funcionalidades

- Upload de imagens pelo navegador
- Suporte a PNG, JPG, JPEG e WEBP
- Limite de upload de 8 MB
- Detecção de pessoas e objetos
- Identificação de animais e veículos
- Detecção complementar de acessórios
- Bounding boxes sobre os elementos identificados
- Exibição do nível de confiança de cada detecção
- Classificação dos elementos por categoria
- Remoção de detecções duplicadas
- Filtros de confiança específicos por classe
- Validação de imagens inválidas ou corrompidas
- Tratamento de erros durante o processamento
- Interface responsiva em tema escuro

---

## Modelos de Inteligência Artificial

O TeceVision utiliza dois modelos de Visão Computacional de forma complementar.

### YOLO11s

Utilizado como modelo principal para identificar elementos gerais da imagem, como:

- Pessoas
- Carros
- Bicicletas
- Motos
- Cachorros
- Gatos
- Cadeiras
- Sofás
- Notebooks
- Celulares
- Livros
- Outros objetos

### YOLO-World

Utilizado como modelo complementar para detectar classes mais específicas, principalmente acessórios, como:

- Óculos
- Relógios
- Fones de ouvido
- Chapéus
- Bonés
- Capacetes

O projeto utiliza filtros de confiança específicos para reduzir falsos positivos e melhorar a qualidade dos resultados.

---

## Tecnologias Utilizadas

### Backend

- Python
- Flask
- Ultralytics
- YOLO11
- YOLO-World
- Pillow

### Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2

### Ferramentas

- Git
- GitHub
- Visual Studio Code

---

## Arquitetura

O projeto foi organizado separando as responsabilidades da aplicação.

```text
image-insight-ai/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── services/
│   ├── __init__.py
│   └── vision.py
│
├── utils/
│   ├── __init__.py
│   └── labels.py
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── result.css
│   │
│   └── js/
│       └── upload.js
│
└── uploads/
```

### Responsabilidades

**`app.py`**

Responsável pelas rotas Flask, upload dos arquivos, validações e tratamento de erros.

**`config.py`**

Centraliza configurações relacionadas aos modelos e limites de confiança utilizados nas detecções.

**`services/vision.py`**

Contém a lógica de Visão Computacional, execução dos modelos YOLO, processamento das detecções e remoção de duplicidades.

**`utils/labels.py`**

Responsável pela tradução, normalização e categorização das classes detectadas.

---

## Como Funciona

O fluxo de análise do TeceVision segue estas etapas:

```text
Usuário envia uma imagem
        ↓
Flask recebe o arquivo
        ↓
Validação da extensão e conteúdo
        ↓
YOLO11s realiza a detecção principal
        ↓
YOLO-World realiza a detecção complementar
        ↓
Aplicação aplica filtros de confiança
        ↓
Detecções duplicadas são removidas
        ↓
Resultados são classificados e traduzidos
        ↓
Bounding boxes são calculadas
        ↓
Resultado é exibido na interface
```

---

## Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/GustavoTc-Web/image-insight-ai.git
cd image-insight-ai
```

### 2. Crie o ambiente virtual

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
python app.py
```

### 5. Acesse no navegador

```text
http://127.0.0.1:5000
```

Na primeira execução, os pesos necessários dos modelos podem ser baixados automaticamente pelo Ultralytics.

---

## Dependências Principais

```text
Flask==3.0.3
Werkzeug==3.0.3
ultralytics==8.4.163
Pillow==12.3.0
```

Os arquivos de pesos dos modelos (`.pt`) não são armazenados no repositório.

---

## Validação e Tratamento de Erros

A aplicação possui tratamento para diferentes situações durante o upload e processamento:

- Arquivo não selecionado
- Extensão não suportada
- Arquivo que não representa uma imagem válida
- Imagem corrompida
- Arquivo maior que 8 MB
- Falhas inesperadas durante a análise
- Imagens sem elementos detectados com confiança suficiente

---

## Detecção e Confiança

Cada classe possui um nível mínimo de confiança antes de ser exibida ao usuário.

Essa abordagem permite configurar classes individualmente, evitando depender de um único limite global.

Além disso, o TeceVision aplica técnicas de comparação entre bounding boxes para reduzir detecções duplicadas sem eliminar objetos diferentes que estejam próximos ou sobrepostos.

---

## Limitações

Modelos de Visão Computacional não possuem precisão absoluta.

Dependendo de fatores como:

- Iluminação
- Resolução
- Ângulo da imagem
- Tamanho do objeto
- Oclusão
- Semelhança visual entre objetos

podem ocorrer falsos positivos ou elementos não serem reconhecidos.

O projeto utiliza filtros e modelos complementares para reduzir esses casos.

---

## Roadmap

- [x] Estrutura inicial da aplicação
- [x] Sistema de upload de imagens
- [x] Integração com YOLO11
- [x] Integração com YOLO-World
- [x] Detecção real de objetos
- [x] Detecção de acessórios
- [x] Filtros de confiança por classe
- [x] Remoção de detecções duplicadas
- [x] Bounding boxes
- [x] Validação de arquivos
- [x] Tratamento de erros
- [x] Refatoração do backend
- [x] Interface do TeceVision
- [ ] Publicação da aplicação
- [ ] Ampliação da bateria de testes
- [ ] Novas classes e melhorias de precisão

---

## Objetivo do Projeto

O TeceVision foi desenvolvido como projeto de portfólio com o objetivo de aplicar conceitos de:

- Desenvolvimento Backend com Python
- Flask
- Visão Computacional
- Inteligência Artificial
- Integração de modelos de Machine Learning
- Processamento e validação de arquivos
- Organização e arquitetura de software
- Desenvolvimento de interfaces web

O projeto também busca demonstrar a evolução de uma aplicação desde um protótipo inicial até uma solução funcional utilizando modelos reais de Inteligência Artificial.

---

## Autor

**Gustavo Tecedora Candido**

Desenvolvedor Back-End / Full Stack em formação.

GitHub: [GustavoTc-Web](https://github.com/GustavoTc-Web)