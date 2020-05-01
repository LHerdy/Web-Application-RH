class Funcionario:
    def __init__(self, nome, cargo, setor, id=None):
        self.id = id
        self.nome = nome
        self.cargo = cargo
        self.setor = setor

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha