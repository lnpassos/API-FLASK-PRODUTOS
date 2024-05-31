# API Flask

### Auxílio inicial para iniciar projeto

### Ferramentas utilizadas

- `Flask` - Framework para API
- `MongoDB` - Banco de Dados
- `Docker` - Ferramente de auxílio para inicializar MongoDB
- `Swagger` - Documentação da API

### Requisitos

- Python 3
- pip
- Docker

### Como usar
- Instale as 3 dependências do projeto:
    `pip install flask`
    `pip install pymongo`
    `pip install flasgger`
- Caso ainda tenha algum erro com o Bson: `pip install bson`
- Caso necessário: `pip install -r requirements.txt`

- Rode o comando `docker compose up`

- Inicie com o comando `flask run`

- Acesse a documentação da API com o Swagger no seguinte endpoint:
`http://127.0.0.1:5000/apidocs/`