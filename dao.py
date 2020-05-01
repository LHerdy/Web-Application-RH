from models import Funcionario, Usuario

SQL_DELETA_FUNCIONARIO = 'delete from funcionario where id = %s'
SQL_FUNCIONARIO_POR_ID = 'SELECT id, nome, cargo, setor from funcionario where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_FUNCIONARIO = 'UPDATE funcionario SET nome=%s, cargo=%s, setor=%s where id = %s'
SQL_BUSCA_FUNCIONARIOS = 'SELECT id, nome, cargo, setor from funcionario'
SQL_CRIA_FUNCIONARIO = 'INSERT into funcionario (nome, cargo, setor) values (%s, %s, %s)'


class FuncionarioDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, funcionario):
        cursor = self.__db.connection.cursor()

        if (funcionario.id):
            cursor.execute(SQL_ATUALIZA_FUNCIONARIO, (funcionario.nome, funcionario.cargo, funcionario.setor, funcionario.id))
        else:
            cursor.execute(SQL_CRIA_FUNCIONARIO, (funcionario.nome, funcionario.cargo, funcionario.setor))
            funcionario.id = cursor.lastrowid
        self.__db.connection.commit()
        return funcionario

    def listar(self):
       cursor = self.__db.connection.cursor()
       cursor.execute(SQL_BUSCA_FUNCIONARIOS)
       funcionarios = traduz_funcionarios(cursor.fetchone())
       return funcionarios

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_FUNCIONARIO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Funcionario(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_FUNCIONARIO, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_funcionarios(funcionarios):
    def cria_funcionario_com_tupla(tupla):
        return Funcionario(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_funcionario_com_tupla, funcionarios))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])
