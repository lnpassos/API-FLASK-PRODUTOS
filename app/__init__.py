from flask import Flask
from flasgger import Swagger
from app.routes import configure_routes
from config import Config
from pymongo import MongoClient

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Swagger 
    swagger = Swagger(app)

    # Conectar-se ao banco de dados MongoDB usando a URI definida em config.py
    client = MongoClient(app.config["MONGO_URI"])
    db = client.get_default_database()  # Instanciando o Banco de Dados

    # Passando o banco de dados para as rotas
    configure_routes(app, db)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
