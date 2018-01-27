# -*- coding: utf-8 -*-
"""

Script de teste para criar registros, recuperar e calcular a média

SQL de criação da tabela
CREATE TABLE `tb_customer_account` (
    `id_customer` INT NOT NULL ,
    `cpf_cnpj` VARCHAR(20) NOT NULL ,
    `nm_customer` VARCHAR(200) NOT NULL ,
    `is_active` BOOLEAN NOT NULL ,
    `vl_total` DECIMAL(60) NOT NULL ,
    PRIMARY KEY (`id_customer`),
    UNIQUE `unique_cpf_cnpj` (`cpf_cnpj`)
);

"""
from random import choice, randint, randrange

from mysql import connector


def gera_cpf():
    def calcula_digito(digs):
        s = 0
        qtd = len(digs)
        for i in xrange(qtd):
            s += n[i] * (1 + qtd - i)
        res = 11 - s % 11
        if res >= 10:
            return 0
        return res
    n = [randrange(10) for i in xrange(9)]
    n.append(calcula_digito(n))
    n.append(calcula_digito(n))
    return "%d%d%d.%d%d%d.%d%d%d-%d%d" % tuple(n)


DB_USER = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_DATABASE = 'camila_teste'
cnx = connector.connect(user=DB_USER, password=DB_PASSWORD,
                        host=DB_HOST, database=DB_DATABASE,)
cursor = cnx.cursor()


sql_add_customer = """ INSERT INTO tb_customer_account
    (id_customer, cpf_cnpj, nm_customer, is_active, vl_total) VALUE
    (%(id)s, %(cpf)s, %(nome)s, %(active)s, %(total)s);"""

# Criar os dados no Banco de Dados
for n in xrange(1, 3000):

    data = {
        'id': n,
        'cpf': gera_cpf(),
        'nome': 'Nome Cliente %s' % n,
        'active': choice(['1', '0']),
        'total': float(randint(10000, 100000)) / 100,
    }
    cursor.execute(sql_add_customer, data)

cnx.commit()
cursor.close()


# Recuperar e calcular a media

sql_list_customer = """ SELECT nm_customer, vl_total FROM tb_customer_account WHERE id_customer >= 1500 AND id_customer <= 2700; """
cursor = cnx.cursor()
cursor.execute(sql_list_customer)

total = 0.0
count = 0
list_customers = []
for nm_customer, vl_total in cursor:

    if vl_total > 560.0:
        total += float(vl_total)
        count += 1

        list_customers.append((nm_customer, total))

if count:
    print("Media Final: %s" % str(total / count))


list_customers = sorted(list_customers, key=lambda x: x[1])
for name in list_customers:
    print(name[0])

cursor.close()
cnx.close()
