import mysql.connector as mysql

connection = mysql.connect(
   host='localhost',
   user='root',
   password='123456',
   database='db_brasileirao'
)

cursor = connection.cursor()

ano = input("Digite o ano que deseja visualizar a tabela: ")

query = f'SELECT cd_ano, nm_time, qt_pontos FROM tb_pontos WHERE cd_ano = {ano} ORDER BY qt_pontos DESC'
cursor.execute(query)
result = cursor.fetchall()

for index, time in enumerate(result):
    print(f"{index+1} | {time[1]} | {time[2]}")

cursor.close()
connection.close()