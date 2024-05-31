from bson import ObjectId
from flask import request, jsonify
from app.models import Produto
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity - Biblioteca para JWT que tentei usar

def configure_routes(app, db):

    # Index
    @app.route('/', methods=['GET'])
    def index():
        """
        Rota para alguns esclarecimentos!
        Tentei autenticar com JWT, porém houve alguns problemas com o Header do Flasgger
        Gerei o Bearer Token, porém o Header estava aceitando qualquer coisa como autenticação
        Impossibilitando de acessar as rotas com `@JWT_REQUIRED`

        Todas requisições estão funcionando com suas respectivas validações (Apenas validações básicas!)

        Deixo aqui um exemplo de código JWT que testei com o Swagger:

        # Configuração do Swagger
        `SWAGGER_TEMPLATE = {"securityDefinitions": {"APIKeyHeader": {"type": "apiKey", "name": "x-access-token", "in": "header"}}}`

        `swagger = Swagger(app, template=SWAGGER_TEMPLATE)`

        # Configuração do JWT
        `app.config['JWT_SECRET_KEY'] = 'teste_python_backend'  # chave para rodar a API`
        
        `jwt = JWTManager(app)`

        OBS: Deixei o código de exemplo comentatado na função `LOGIN`
        

        ---
        responses:
          200:
            description: Retorna uma mensagem de boas-vindas
        """
        return "API Flask"
    

    '''  CÓDIGO DE AUTENTICAÇÃO DE USUARIO JWT (NÃO CONSEGUI FAZER FUNCIONAR COM O SWAGGER)

    # Login JWT
    @app.route('/login', methods=['POST'])
    def login():
        """
        Rota de login para obter o token JWT
        ---
        parameters:
          - in: body
            name: user
            description: Credenciais do usuário
            schema:
              type: object
              required:
                - username
                - password
              properties:
                username:
                  type: string
                password:
                  type: string
        responses:
          200:
            description: Login bem-sucedido
            schema:
              type: object
              properties:
                access_token:
                  type: string
          401:
            description: Credenciais inválidas
        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Verifique as credenciais do usuário (isso deve ser feito de forma segura)
        if username == 'admin' and password == 'admin':  # Substitua por uma verificação real
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Credenciais inválidas"}), 401

    '''



    # Rota para puxar todos produtos
    @app.route('/produtos', methods=['GET'])
    def get_produtos():
        """
        Retorna todos os produtos
        ---
        responses:
          200:
            description: Lista de produtos
            schema:
              type: array
              items:
                type: object
                properties:
                  _id:
                    type: string
                    description: ID do produto
                  nome:
                    type: string
                    description: Nome do produto
                  preco:
                    type: number
                    description: Preço do produto
                  descricao:
                    type: string
                    description: Descrição do produto
        """
        produtos = db.produtos.find()
        produtos_json = []
        for produto in produtos:
            produto['_id'] = str(produto['_id'])  # Converta o ObjectId para uma string
            produtos_json.append(produto)
        return jsonify(produtos_json), 200



    # Rota para criar novo produto
    @app.route('/produto', methods=['POST'])
    def create_produto():
        """
        Cria um novo produto
        ---
        parameters:
          - in: body
            name: produto
            description: O produto a ser criado
            schema:
              type: object
              required:
                - nome
                - preco
                - descricao
              properties:
                nome:
                  type: string
                preco:
                  type: number
                descricao:
                  type: string
        responses:
          201:
            description: Produto criado com sucesso
          400:
            description: Falha na validação dos dados
        """
        data = request.get_json()

        if not data.get('nome') or not data.get('preco') or not data.get('descricao'):
            return jsonify({"mensagem": "Preencha todos os campos!"}), 400

        try:
            preco = float(data['preco'])
        except (ValueError, TypeError):
            return jsonify({"mensagem": "Preencha o valor com valores numéricos"}), 400

        produto = Produto(data['nome'], preco, data['descricao'])
        produto.save()
        return jsonify({"mensagem": "Produto criado com sucesso!"}), 201



    # Rota para puxar produto especifico
    @app.route('/produto/<string:id>', methods=['GET'])
    def get_produto(id):
        """
        Retorna um produto por ID
        ---
        parameters:
          - name: id
            in: path
            type: string
            required: true
            description: ID do produto
        responses:
          200:
            description: Produto encontrado
            schema:
              type: object
              properties:
                _id:
                  type: string
                  description: ID do produto
                nome:
                  type: string
                  description: Nome do produto
                preco:
                  type: number
                  description: Preço do produto
                descricao:
                  type: string
                  description: Descrição do produto
          404:
            description: Produto não encontrado
        """
        produto = db.produtos.find_one({"_id": ObjectId(id)})
        if produto:
            produto['_id'] = str(produto['_id'])  # Converta o ObjectId para uma string
            return jsonify(produto), 200
        else:
            return jsonify({"mensagem": "Produto não encontrado"}), 404



    # Rota para atualizar produto especifico
    @app.route('/produto/<string:id>', methods=['PUT'])
    def update_produto(id):
        """
        Atualiza um produto por ID
        ---
        parameters:
          - name: id
            in: path
            type: string
            required: true
            description: ID do produto
          - in: body
            name: produto
            description: Dados do produto a ser atualizado
            schema:
              type: object
              required:
                - nome
                - preco
                - descricao
              properties:
                nome:
                  type: string
                preco:
                  type: number
                descricao:
                  type: string
        responses:
          200:
            description: Produto atualizado com sucesso
          400:
            description: Falha na validação dos dados
          404:
            description: Produto não encontrado
        """
        data = request.get_json()

        if not data.get('nome') or not data.get('preco') or not data.get('descricao'):
            return jsonify({"mensagem": "Preencha todos os campos!"}), 400

        try:
            preco = float(data['preco'])
        except (ValueError, TypeError):
            return jsonify({"mensagem": "Preencha o valor com valores numéricos"}), 400

        produto = db.produtos.find_one({"_id": ObjectId(id)})
        if produto:
            db.produtos.update_one({"_id": ObjectId(id)}, {"$set": {"nome": data['nome'], "preco": preco, "descricao": data['descricao']}})
            return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 200
        else:
            return jsonify({"mensagem": "Produto não encontrado"}), 404



    # Rota para deletar produto especifico
    @app.route('/produto/<string:id>', methods=['DELETE'])
    def delete_produto(id):
        """
        Deleta um produto por ID
        ---
        parameters:
          - name: id
            in: path
            type: string
            required: true
            description: ID do produto
        responses:
          204:
            description: Produto deletado com sucesso
          404:
            description: Produto não encontrado
        """
        produto = db.produtos.find_one({"_id": ObjectId(id)})
        if produto:
            db.produtos.delete_one({"_id": ObjectId(id)})
            return jsonify({"mensagem": "Produto deletado com sucesso!"}), 204
        else:
            return jsonify({"mensagem": "Produto não encontrado"}), 404
