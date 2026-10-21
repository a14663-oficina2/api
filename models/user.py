# Tudo oque têm aver com utilizadores na base de dados#
# Este contrutor vai servir para qunado eu quiser criar uma class sem adicionar a base de dados
from con_sql_alchemy import bd

class UserModel(bd.Model):
    __tablename__ = "utlizadores"  # nome da tabela que vai ser criada na base de dados
    user_id = bd.Column(bd.String, primary_key=True)
    username = bd.Column(bd.String(80))
    password = bd.Column(bd.Float(precision=1))

    # Construtor
    def __init__(self, username, password):
        self.username = username
        self.password = password


    # Quando quisermos transformar em json é so fazer por exemplo: "x = x.json"
    def json(self):
        return {
            "hotel_id": self.user_id,
            "nome": self.username
        }


    @classmethod  # Decorador  || diz que é um método da classe, porque não esta associado a um hotel em especifico (neste caso ele vai procurar um hotel qualquer)
    def find_user(cls, user_id):
        user = cls.query.filter_by(username = user_id).first() # hotel_id da tabela da base de dados = hotel_id deste método  || first() retorna uma lista dos hoteis, que neste caso vai ser só 1
        # no SQL seria: SELECT * FROM hoteis WHERE hotel_id = hotel_id LIMIT 1
        # lembrando que o SQLAlchemy transforma o codigo em SQL e executa na base de dados direta
        if user:
            return user
        return None


    def save_user(self):
        bd.session.add(self)
        bd.session.commit()  # commit para a base de dados para enviar os dados
        # Problema deste código: numa base de dados normal os dados sao enviados todos ou não são enviados, este codigo coloca dados um por um de cada vez nas tabelas,
        # logo se a luz for abaixo ele pode colocar alguns dos dados enviamos e outros não oque está mal, ele devia colocar os dados todos ou nenhuns

    
    def update_user(self, username, password):
        self.username = username
        self.password = password

    
    def delete_user(self):
        bd.session.delete(self)  # Delete próprio do python
        bd.session.commit()
