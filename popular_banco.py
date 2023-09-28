import pandas as pd
import mysql.connector as mysql

df = pd.read_csv('campeonato-brasileiro-revised.csv')

connection = mysql.connect(
   host='localhost',
   user='root',
   password='123456',
   database='db_brasileirao'
)

cursor = connection.cursor()

# NoRepeat Items Function
def norepeat(value):
    value = list(set(value))
    value.sort()
    return value

# Junta Duas Colunas
def twocolumns(list1, list2):
    list1_list2 = []

    for index, one in enumerate(list1):
        tupla1_2 = (f"{one}", f"{list2[index]}",)
        list1_list2.append(tupla1_2)
    
    list1_list2 = list(set(list1_list2))
    list1_list2.sort()
    return list1_list2

#Estados
estados = df['mandante_Estado'].tolist()
estados_nr = norepeat(estados)

for estado in estados_nr:
    query = f'INSERT INTO tb_estado (sg_estado) VALUES ("{estado}")'
    cursor.execute(query)
    connection.commit()

#Times
times = df['mandante'].tolist()
times_estados = twocolumns(times, estados)

for time_estado in times_estados:
    query = f'INSERT INTO tb_time (nm_time, sg_estado) VALUES ("{time_estado[0]}", "{time_estado[1]}")'
    cursor.execute(query)
    connection.commit()

# Arenas
arenas = df['arena'].tolist()
arenas_aux = arenas.copy()
for index, value in enumerate(arenas_aux):
    value = ' '.join(value.split())
    arenas_aux[index] = value

arenas_estados = twocolumns(arenas_aux, estados)

arenas_remove = [
('Arena Barueri', 'BA'),
('Arena Barueri', 'SC'), 
('Arena Joinville', 'PR'),
('Arena Pantanal', 'GO'),
('Arena Pantanal', 'MG'),
('Arena Pantanal', 'PE'),
('Arena Pantanal', 'RJ'),
('Arena Pantanal', 'SP'),
('Arena de Pernambuco', 'RJ'),
('Batistão', 'RJ'),
('Boca do Jacaré', 'GO'),
('Castelão (CE)', 'SP'),
('Pacaembu', 'RJ'),
('Mané Garrincha', 'SP'),
('Mané Garrincha', 'AL'),
('Mané Garrincha', 'MG'),
('Mané Garrincha', 'PR'),
('Mané Garrincha', 'RJ'),
('Mané Garrincha', 'SC'),
('Estádio do Café', 'MG'),
('Estádio do Café', 'SC'),
('Mário Helênio', 'GO'),
('Mário Helênio', 'RJ'),
('Mangueirão', 'GO'),
('Parque do Sabiá', 'PR'),
('Parque do Sabiá', 'RJ'),
('Pedro Pedrossian', 'RJ'),
('Pedro Pedrossian', 'SP'),
('Morumbi', 'MG'),
('Morumbi', 'RJ'),
('Neo Química Arena', 'RJ'),
('Orlando Scarpelli', 'PR'),
('Orlando Scarpelli', 'RJ'),
('Ressacada', 'RJ'),
('Santa Cruz', 'SC'),
('Serra Dourada', 'PR'),
]

for arena in arenas_remove:
    arenas_estados.remove(arena)

for arena_estado in arenas_estados:
    query = f'INSERT INTO tb_arena (nm_arena, sg_estado) VALUES ("{arena_estado[0]}", "{arena_estado[1]}")'
    cursor.execute(query)
    connection.commit()

# Tecnicos
tecnico_mandante = df['tecnico_mandante'].tolist()
tecnico_visitante = df['tecnico_visitante'].tolist()
tecnicos_aux = tecnico_mandante.copy()
tecnicos_aux.extend(tecnico_visitante)

for index, value in enumerate(tecnicos_aux):
    tecnicos_aux[index] = str(value)

tecnicos_nr = norepeat(tecnicos_aux)

for tecnico in tecnicos_nr:
    query = f'INSERT INTO tb_tecnico (nm_tecnico) VALUES ("{tecnico}")'
    cursor.execute(query)
    connection.commit()

rodada = df['rodada'].tolist()
datas = df['data'].tolist()
horas = df['hora'].tolist()
visitantes = df['visitante'].tolist()
formacao_mandante = df['formacao_mandante'].tolist()
formacao_visitante = df['formacao_visitante'].tolist()
placar_mandante = df['mandante_Placar'].tolist()
placar_visitante = df['visitante_Placar'].tolist()

for i, data in enumerate(datas):
    query = f'INSERT INTO tb_jogo (cd_rodada, dt_jogo, time_mandante, time_visitante, formacao_mandante, formacao_visitante, tecnico_mandante, tecnico_visitante, nm_arena, placar_mandante, placar_visitante) VALUES ({rodada[i]}, STR_TO_DATE("{data} {horas[i]}:00","%d/%m/%Y %H:%i:%s"), "{times[i]}", "{visitantes[i]}", "{formacao_mandante[i]}", "{formacao_visitante[i]}", "{tecnico_mandante[i] or ""}", "{tecnico_visitante[i] or ""}", "{arenas[i]}", {placar_mandante[i]}, {placar_visitante[i]})'
    cursor.execute(query)
    connection.commit()

# Tabela de pontos    
query = f'SELECT IF(dt_jogo BETWEEN "2021-01-01 00:00:00" AND "2021-02-26 00:00:00", 2020, YEAR(dt_jogo)), time_mandante, placar_mandante, time_visitante, placar_visitante FROM tb_jogo;'
cursor.execute(query)
result = cursor.fetchall()

for jogo in result:
    ano = jogo[0]
    mandante = jogo[1]
    placar_mandante = jogo[2]
    visitante = jogo[3]
    placar_visitante = jogo[4]
    result = 0

    if (placar_mandante > placar_visitante):
        query = f'SELECT qt_pontos FROM tb_pontos WHERE cd_ano = {ano} AND nm_time = "{mandante}";'
        cursor.execute(query)
        result = cursor.fetchall()
        if (len(result) == 0):
            query = f'INSERT INTO tb_pontos (cd_ano, nm_time, qt_pontos) VALUES ({ano}, "{mandante}", 3)'
            cursor.execute(query)
            connection.commit()
        else:
            ponto = result[0][0] + 3
            query = f'UPDATE tb_pontos SET qt_pontos={ponto} WHERE cd_ano = {ano} AND nm_time = "{mandante}"'
            cursor.execute(query)
            connection.commit()

    elif (placar_visitante > placar_mandante):
        query = f'SELECT qt_pontos FROM tb_pontos WHERE cd_ano = {ano} AND nm_time = "{visitante}";'
        cursor.execute(query)
        result = cursor.fetchall()
        if (len(result) == 0):
            query = f'INSERT INTO tb_pontos (cd_ano, nm_time, qt_pontos) VALUES ({ano}, "{visitante}", 3)'
            cursor.execute(query)
            connection.commit()
        else:
            ponto = result[0][0] + 3
            query = f'UPDATE tb_pontos SET qt_pontos={ponto} WHERE cd_ano = {ano} AND nm_time = "{visitante}"'
            cursor.execute(query)
            connection.commit()
    else:
        query = f'SELECT qt_pontos FROM tb_pontos WHERE cd_ano = {ano} AND nm_time = "{visitante}";'
        cursor.execute(query)
        result = cursor.fetchall()
        if (len(result) == 0):
            query = f'INSERT INTO tb_pontos (cd_ano, nm_time, qt_pontos) VALUES ({ano}, "{visitante}", 1)'
            cursor.execute(query)
            connection.commit()
        else:
            ponto = result[0][0] + 1
            query = f'UPDATE tb_pontos SET qt_pontos={ponto} WHERE cd_ano = {ano} AND nm_time = "{visitante}"'
            cursor.execute(query)
            connection.commit()
        query = f'SELECT qt_pontos FROM tb_pontos WHERE cd_ano = {ano} AND nm_time = "{mandante}";'
        cursor.execute(query)
        result = cursor.fetchall()
        if (len(result) == 0):
            query = f'INSERT INTO tb_pontos (cd_ano, nm_time, qt_pontos) VALUES ({ano}, "{mandante}", 1)'
            cursor.execute(query)
            connection.commit()
        else:
            ponto = result[0][0] + 1
            query = f'UPDATE tb_pontos SET qt_pontos={ponto} WHERE cd_ano = {ano} AND nm_time = "{mandante}"'
            cursor.execute(query)
            connection.commit()

cursor.close()
connection.close()
