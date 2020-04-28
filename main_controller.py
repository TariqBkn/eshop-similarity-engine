from flask import Flask, request
from flask_restful import Resource, Api
import similarity_engine

app = Flask(__name__)
api = Api(app)

class Similarity(Resource):
    def __init__(self):
        self.se = similarity_engine.Similarity_engine()
    def get(self, productId):
        return self.se.get_similar_products_of(productId)

api.add_resource(Similarity,'/products/<int:productId>/similar')

if __name__=='__main__':
    app.run(debug=True)
