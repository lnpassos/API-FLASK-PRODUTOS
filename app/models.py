import os
from pymongo import MongoClient
from config import Config


# Conectando-se ao banco de dados MongoDB usando a URI definida em config.py
client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()  # Instanciando o banco de dados

# Model único para o Produto
class Produto:
    def __init__(self, nome, preco, descricao):
        self.nome = nome
        self.preco = preco
        self.descricao = descricao

    def save(self):
        produto_data = {
            "nome": self.nome,
            "preco": self.preco,
            "descricao": self.descricao
        }
        return db.produtos.insert_one(produto_data)
