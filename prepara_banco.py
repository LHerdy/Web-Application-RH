import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='admi', host='127.0.0.1', port=3306)

# Descomente se quiser desfazer o banco...
#conn.cursor().execute("DROP DATABASE `cadastro`;")
#conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `cadastro` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `cadastro`;
    CREATE TABLE `funcionario` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) COLLATE utf8_bin NOT NULL,
      `cargo` varchar(40) COLLATE utf8_bin NOT NULL,
      `setor` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `usuario` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `nome` varchar(20) COLLATE utf8_bin NOT NULL,
      `senha` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
'''cursor.executemany(
      'INSERT INTO cadastro.usuario (id, nome, senha) VALUES (%s, %s, %s)',
      [
          ('Leandro', 'Leandro H', 'oi')
      ])'''

cursor.execute('select * from cadastro.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo funcionarios
cursor.executemany(
      'INSERT INTO cadastro.funcionario (nome, cargo, setor) VALUES (%s, %s, %s)',
      [
          ('Leandro', 'Programador', 'Desenvolvimanto')
      ])

cursor.execute('select * from cadastro.funcionario')
print(' -------------  Funcionario:  -------------')
for funcionario in cursor.fetchall():
    print(funcionario[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()