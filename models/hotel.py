# Este contrutor vai servir para qunado eu quiser criar uma class sem adicionar a base de dados
class HotelModel:
    # Construtor
    def __init__(self,hotel_id,nome,estrelas,diaria,cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    # Quando quisermos transformar em json é so fazer por exemplo: "x = x.json"
    def json(self):
        return {"hotel_id": self.hotel_id, "nome": self.nome, "estrelas": self.estrelas, "diaria": self.diaria, "cidade": self.cidade}


x = HotelModel("oficina","Oficina Hotel",4.1,120.99,"Santo Tirso")