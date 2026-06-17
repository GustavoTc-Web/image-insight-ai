# Image Insight AI

Image Insight AI e uma aplicacao web de Visao Computacional criada com Python, Flask e preparada para integracao com Azure AI Vision. Nesta primeira versao, o sistema permite enviar uma imagem, salva o arquivo localmente e exibe uma tela de resultado com dados simulados.

## Objetivo

Desenvolver uma base profissional e evolutiva para analise de imagens, com separacao clara entre interface, backend e documentacao. O projeto foi estruturado para receber futuramente recursos como descricao automatica, tags, deteccao de objetos e outras capacidades de IA visual.

## Tecnologias Utilizadas

- Python 3.12+
- Flask
- HTML5
- CSS3
- Azure AI Vision (integracao futura)

## Estrutura de Pastas

```text
image-insight-ai/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── static/
│   ├── css/
│   │   └── style.css
│   └── img/
├── templates/
│   ├── index.html
│   └── result.html
├── uploads/
└── docs/
    └── architecture.md
```

## Como Executar Localmente

1. Clone o repositorio:

```bash
git clone https://github.com/seu-usuario/image-insight-ai.git
cd image-insight-ai
```

2. Crie e ative um ambiente virtual:

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

3. Instale as dependencias:

```bash
pip install -r requirements.txt
```

4. Execute a aplicacao:

```bash
python app.py
```

5. Acesse no navegador:

```text
http://127.0.0.1:5000
```

## Integracao Futura com Azure AI Vision

A funcao `analyze_image_with_mock_data` em `app.py` concentra o ponto de evolucao para a integracao com Azure AI Vision. Futuramente, essa funcao devera:

- Ler endpoint e chave da Azure por variaveis de ambiente.
- Enviar a imagem carregada para a API do Azure AI Vision.
- Processar a resposta da API.
- Retornar descricoes, tags e objetos detectados reais.

## Roadmap

- [x] Estrutura inicial do projeto
- [ ] Upload de imagens
- [ ] Integracao com Azure AI Vision
- [ ] Deteccao de objetos
- [ ] Geracao de descricoes automaticas
- [ ] Melhorias de interface

## Status

Projeto em desenvolvimento, com estrutura inicial pronta para publicacao no GitHub e evolucao incremental.
