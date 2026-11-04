# Este "hotel.py" serve para os pedidos Gets, Posts...
from flask_restful import Resource, reqparse
from models.hotel import HotelModel  # importar a classe HotelModel do hotel.py em "models/"
from flask_jwt_extended import jwt_required


# cada rota/endpoint(link, o get, o post...) vai ter de estar associado a uma classe
class Hoteis(Resource):
    parametros = reqparse.RequestParser() # Selecionar dados passados na URL
    parametros.add_argument("cidade", type=str, default=" ", location="args") # Está na chave cidade "cidade" | "args" permite buscar oque está na URL
    parametros.add_argument("estrelas_min", type=float, default=0, location="args")
    parametros.add_argument("estrelas_max", type=float, default=0, location="args")
    parametros.add_argument("diaria_min", type=float, default=0, location="args")
    parametros.add_argument("diaria_max", type=float, default=0, location="args")
    parametros.add_argument("items", type=int, default=5, location="args") # Quantos hoteis queremos que mostre por página
    parametros.add_argument("pagina", type=int, default=1, location="args") 
    
    def get(self):
        meus_filtros = Hoteis.parametros.parse_args()
        query = HotelModel.query # Pesquisar por ...(qualquer coisa) na tabela que HotelModel representa

        if meus_filtros["cidade"]: # http://127.0.0.1/hoteis?cidade=Porto
            query = query.filter(HotelModel.cidade == meus_filtros["cidade"])

        if meus_filtros["estrelas_min"]: # http://127.0.0.1/hoteis?cidade=Porto&estrelas=...
            query = query.filter(HotelModel.estrelas >= meus_filtros["estrelas_min"])

        if meus_filtros["estrelas_max"]:
            query = query.filter(HotelModel.estrelas <= meus_filtros["estrelas_max"])

        if meus_filtros["diaria_min"]:
            query = query.filter(HotelModel.diaria >= meus_filtros["diaria_min"])
        
        if meus_filtros["diaria_max"]:
                    query = query.filter(HotelModel.diaria <= meus_filtros["diaria_max"])

        pagina = meus_filtros["pagina"]
        num_hoteis_por_pagina = meus_filtros["items"]
        pagination = query.paginate(page=pagina,error_out=False)

        resultado_hotel = [hotel.json() for hotel in pagination.items]

        return { "hoteis": resultado_hotel }


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
        hotel = HotelModel.find_hotel(hotel_id) # Devolve o hotel ou None caso não encontre nenhum hotel
        if hotel is not None:
            return hotel.json(), 200
        return  {"mensagem": "Hotel não foi encontrado."}


    # Criar
    # NOTA para não achar estranho: enquanto não estamos a lidar com bases de dados os Posts não vão inserir os dados na lista para sempre, só enquanto o server estiver ligado.
    @jwt_required() # Significa que é obrigatório estar autenticado
    def post(self, hotel_id):  # o hotel_id vai no URL (endpoint), porque vai ser o identificador de cada hotel
        dados = Hotel.argumentos.parse_args()  # cria um dicionário com as quatro variáveis (dados)
        hotel = HotelModel.find_hotel(hotel_id)
        # verifica cada hotel se já tem um hotel_id dentro da base de dados, se existir, retorna um JSON(dicionário) com uma mensagem a avisar que o hotel já existe
        if hotel is not None:
            return {"mensagem": f"O hotel com id {hotel_id} já existe."}  # HTTP Requests recebem e retornam sempre JSONs(que são dicionários, logo temos de retornar um dicionário)
        
        novo_hotel = HotelModel(hotel_id, **dados)  # dois "**" chama um dicionário

        try:  # Tenta fazer isto...
            novo_hotel.save_hotel()
            return novo_hotel.json(), 200  # "200" é o RESPONSE CODE
        except:  # Senão...
            return{ "mensagem": "Um erro interno do servidor aconteceu..."}, 500 # RESPONSE ERROR 500 - erro na base de dados


    # Atualizar
    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()  # cria um dicionário com as quatro variáveis (dados)  || "dados" é um dicionario

        # Se o hotel_id existe
        hotel = HotelModel.find_hotel(hotel_id)    
        if hotel is not None:
            try:
                hotel.update_hotel(*dados) # um asterisco "*" serve para ir buscar os valores | (se passarmos sem nenhum "*" ele devolve o dicionário todo)
                hotel.save_hotel()
                return hoteis, 200  # devolve RESPONSE CODE 201 (Created)
            except:  # Senão...
                return{ "mensagem": "Um erro interno do servidor aconteceu..."}, 500 # RESPONSE ERROR 500 - erro na base de dados
        
        # Se o hotel_id não existir, cria o hotel
        novo_hotel = HotelModel(hotel_id, **dados)  # dois "**" chama um dicionário, dois asteriscord "**" serve para is buscar as chaves/keys | (se passarmos sem nenhum "*" ele devolve o dicionário todo)
        hoteis.save_hotel()
        return novo_hotel.json(), 201  # "200" é o RESPONSE CODE


    # Apagar
    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None: 
            try:
                hotel.delete_hotel()
                return {"mensagem": "Hotel removido com sucesso"}, 200
            except:  # Senão...
                        return{ "mensagem": "Um erro interno do servidor aconteceu..."}, 500 # RESPONSE ERROR 500 - erro na base de dados
        return {"mensagem": "Hotel não encontrado."}

    
