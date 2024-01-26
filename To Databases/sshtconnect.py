# bibliotecas necessárias

from sshtunnel import SSHTunnelForwarder as id_ssh
import pymysql
import pandas as pd
import credentials as c # credenciais de acesso do servidor ssh e banco de dados
########## condicional de banco ##########

ssh_tunnel_ = True # Caso o banco a ser acessado tenha ssh tunnel deixe a variável True caso não coloque False

if ssh_tunnel_ == True:
	######## criando o tunel ssh ####################

	server = id_ssh(
		(,), # tupla contendo o host e a porta (nesta ordem) do servidor SSH
		ssh_username="", # Nome do usuário do servidor SSH
		ssh_password="", # A senha do servidor SSH
		remote_bind_address=('', )) # Tupla contendo host e porta do servidor (nesta ordem) MYSQL na máquina remota

	server.start() # inicia o tunel ssh e estabelece conexão com a máquina remota

	# Conectando ao banco de dados MYSQL
	conn = pymysql.connect(
		host='', # O nome de host do servidor MySQL. Este deve ser definido como 'localhost' pois estamos nos conectando através do túnel SSH.
		user='', # Usuário do DB
		passwd='', # Senha do DB
		port=server.local_bind_port,  #O nome de host do servidor MySQL. Este deve ser definido como 'localhost' pois estamos nos conectando através do túnel SSH.
		db='' # Nome do DB a ser conectado
		)
		

	consulta_sql = pd.read_sql_query(''' SELECT * FROM register r ''', conn) # Esta linha executa uma consulta SQL no banco de dados MySQL e armazena os resultados em um DataFrame do Pandas. A consulta SQL real está atualmente vazia e precisa ser preenchida.

	server.stop() #Esta linha para o túnel SSH, fechando a conexão com a máquina remota.


	############ Exemplo de campos preenchidos #####################

	from sshtunnel import SSHTunnelForwarder as id_ssh
	import pymysql
	import pandas as pd

	server = id_ssh(
		(192.168.1.1, 22), 
		ssh_username="user", 
		ssh_password="password", 
		remote_bind_address=("localhost", 3306))
	server.start()

	conn = pymysql.connect(
		host="localhost", 
		user="user", 
		passwd="password", 
		port=server.local_bind_port, 
		db="database")

	consulta_sql = pd.read_sql_query("SELECT * FROM registers r", conn)

	server.stop()
else:
	connection = pymysql.connect(
		host="",
		port="",
		user="",
		password="",
		database="")
		
	consulta_sql = pd.read_sql_query('''SELECT * FROM registers r''',connection)
	connection.close()