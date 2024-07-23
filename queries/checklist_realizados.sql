SELECT 
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