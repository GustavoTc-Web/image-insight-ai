# Arquitetura do Image Insight AI

## Visao Geral

O Image Insight AI segue uma arquitetura web simples baseada em Flask. A primeira versao nao utiliza banco de dados e mantem os arquivos enviados em armazenamento local, dentro da pasta `uploads/`.

## Componentes

- `app.py`: ponto de entrada da aplicacao Flask, responsavel pelas rotas, validacao de upload e chamada da camada de analise.
- `templates/`: paginas HTML renderizadas pelo Flask.
- `static/css/`: estilos da interface.
- `static/img/`: pasta reservada para imagens estaticas futuras.
- `uploads/`: destino local das imagens enviadas pelos usuarios.
- `docs/`: documentacao tecnica e arquitetural.

## Fluxo Atual

1. O usuario acessa a rota `/`.
2. A pagina inicial renderiza um formulario de upload.
3. O usuario envia uma imagem para `/analyze`.
4. O backend valida a extensao do arquivo.
5. A imagem e salva em `uploads/`.
6. A aplicacao retorna uma tela de resultado com dados simulados.

## Integracao Futura com Azure AI Vision

A funcao `analyze_image_with_mock_data` em `app.py` devera evoluir para uma camada de servico dedicada, por exemplo `services/vision_service.py`.

Responsabilidades futuras dessa camada:

- Ler credenciais da Azure por variaveis de ambiente.
- Enviar a imagem para Azure AI Vision.
- Normalizar a resposta da API.
- Retornar dados estruturados para os templates.
- Tratar erros de rede, autenticacao e limites da API.

## Evolucao Recomendada

- Criar uma pasta `services/` para integrar provedores externos.
- Criar uma pasta `config/` para centralizar configuracoes.
- Adicionar testes automatizados.
- Adicionar validacao de MIME type.
- Implementar limpeza periodica de arquivos enviados.
- Avaliar armazenamento em Azure Blob Storage para ambientes de producao.
