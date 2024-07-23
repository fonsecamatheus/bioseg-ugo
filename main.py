import mysql.connector
from mysql.connector import Error
import pandas as pd
from config import DATABASE

def connect_and_query():
    try:
        con = mysql.connector.connect(**DATABASE)
        print('Conectando ao banco de dados')
        if con.is_connected():
            cursor = con.cursor()
            
            query = ''' SELECT 
                            t1.id_realizado AS ID, 
                            t1.data_criacao AS DATA, 
                            t2.nome AS CHECKLIST, 
                            t3.nome AS TÉCNICO, 
                            t4.nome AS UNIDADE, 
                            (SELECT resposta 
                            FROM respostas_checklists 
                            WHERE id_realizado = t1.id_realizado 
                            AND id_indicador = 3101) AS 'REALIZADO'
                        FROM 
                            realizados t1
                        LEFT JOIN 
                            checklists t2 
                            ON t1.id_checklist = t2.id_checklist
                        LEFT JOIN 
                            usuarios t3 
                            ON t1.id_usuario = t3.id_usuario 
                        LEFT JOIN 
                            unidades t4 
                            ON t1.id_unidade = t4.id_unidade
                        WHERE 
                            t1.id_realizado IN (
                                SELECT id_realizado
                                FROM respostas_checklists
                                WHERE indicador = 'Haverá possibilidade de desenvolver a tarefa?'); 
            '''
            
            cursor.execute(query)
            results = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(results, columns=column_names)
 
            if 'DATA' in df.columns:
                df['DATA'] = df['DATA'].dt.strftime('%d/%m/%Y')
                df['MÊS'] = df['DATA'].apply(lambda x: pd.to_datetime(x, format='%d/%m/%Y').month)
                df['ANO'] = df['DATA'].apply(lambda x: pd.to_datetime(x, format='%d/%m/%Y').year)
            
            df.to_excel('H:\CONSULTORIAS\#OPERACIONAL\CONSULTAS UGO\CHECKLISTS REALIZADOS.xlsx', index=False)
                
    except Error as e:
        print(f'Erro ao conectar ao banco de dados: {e}' )
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
            print('Conexão com o banco de dados encerrada')


if __name__ == '__main__':
    connect_and_query()     