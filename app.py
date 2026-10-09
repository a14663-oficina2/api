from flask import Flask
from flask_restful import Resource, Api, reqparse
from resources.hotel import Hoteis, Hotel


# NOTA IMPORTANTE: antes de correr o programa temos de entrar no ambiente virtual(se ainda não estivermos) ". venv/bin/activate"
# depois podemos iniciar o servidor "python app.py"

app = Flask(__name__)
api = Api(app)  # variavel para dizer que estou a trabalhar na minha API


api.add_resource(Hoteis,"/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")  # como a class Hotel recebe o parametro "hotel_id" entao temos de dizer que vai receber uma String

if __name__ == "__main__":
    app.run(debug=True)  # debug=true para aparecer oque retorna, como ainda estamos a testar a api vamos deixar o debug ativo


# PARA TESTAR A API DENTRO DO CODESPACE (recomendado testar no Postman)
# Cntrl + Shift + P | abre a lista de comandos do VSCode
# Instalamos a extensão Bruno, e nessa lista pesquisamos Bruno, vai aparecer Bruno Create Collection (bruno.openCreateCollection)
# E finalmente dá-mos um nome, uma pasta para ele usar, e nas opções escolhemos (.bru)
#
# Clicamos com botão direito na pasta embaixo do Explorer na aba "Bruno Collections", e escolhemos "New Request", e neste caso escolhemos HTTPRequest, e dá-mos um nome
