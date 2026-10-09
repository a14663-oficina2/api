# Este "hotel.py" serve para os Gets, Posts...
from flask_restful import Resource, reqparse
from models.hotel import HotelModel  # importar a classe HotelModel do hotel.py em "models/"


hoteis = [
    {"hotel_id": "paraiso", "nome": "Hotel Paraíso", "estrelas": 4.8, "diaria": 125.75, "cidade": "Porto"},
    {"hotel_id": "fukui", "nome": "Hotel Fukui", "estrelas": 4.9, "diaria": 225.75, "cidade": "Lisboa"},
    {"hotel_id": "saint", "nome": "Hotel Saint", "estrelas": 4.6, "diaraia": 165.75, "cidade": "Braga"}
]


# cada rota/endpoint(link, o get, o post...) vai ter de estar associado a uma classe
class Hoteis(Resource):
    # Buscar
    def get(self):
        # API retorna sempre u, JSON(dicionário)
        return {"hoteis": hoteis}  # vai devolver cada dicionario


# API
class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome", type=str, required=True, help="O nome do hotel é obrigatório")
    argumentos.add_argument("estrelas", type=str, required=True, help="O nome do hotel é obrigatório")
    argumentos.add_argument("diaria", type=str, required=True, help="O nome do hotel é obrigatório")
    argumentos.add_argument("cidade", type=str, required=True, help="O nome do hotel é obrigatório")


    def encontrar_hotel(self,hotel_id):
        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                return hotel
            return None


    # Buscar
    def get(self, hotel_id):
        hotel = self.encontrar_hotel(hotel_id)
        if hotel is not None:
            return hotel, 200
        return  {"mensagem": "Hotel não foi encontrado."}


    # Apagar
    def delete(self, hotel_id):
        global hoteis  # se formos usar uma lista de fora da class temos de dizer que é uma classe do "global"
        hoteis = [hotel for hoteis in hotel["hotel_id"] if hotel["hotel_id"] != hotel_id]
        return {"mensagem": f"O hotel com hotel id {hotel_id} foi removido com sucesso."}, 200


    # Criar
    # NOTA para não achar estranho: enquanto não estamos a lidar com bases de dados os Posts não vão inserir os dados na lista para sempre, só enquanto o server estiver ligado.
    def post(self, hotel_id):  # o hotel_id vai no URL (endpoint), porque vai ser o identificador de cada hotel
        dados = Hotel.argumentos.parse_args()  # cria um dicionário com as quatro variáveis (dados)

        hotel = self.encontrar_hotel(hotel_id)
        # verifica cada hotel se já tem um hotel_id dentro da base de dados, se existir, retorna um JSON(dicionário) com uma mensagem a avisar que o hotel já existe
        for hotel in hoteis:
                    if hotel["hotel_id"] == hotel_id:
                        return {"mensagem": f"O hotel com id {hotel_id} já existe."}  # HTTP Requests recebem e retornam sempre JSONs(que são dicionários, logo temos de retornar um dicionário)
        
        novo_hotel = {"hotel_id": hotel_id, **dados}  # dois "**" chama um dicionário
        hoteis.append(novo_hotel)
        return novo_hotel, 200  # "200" é o RESPONSE CODE


    # Atualizar
    def put(self, hotel_id):
        novos_dados = Hotel.argumentos.parse_args()  # cria um dicionário com as quatro variáveis (dados)  || Dados é um dicionario
        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                hotel.update(novos_dados)
                return hoteis, 201  # devolve RESPONSE CODE 201 (Created)
