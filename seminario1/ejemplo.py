import pyodbc

# Conectarse a la base de datos Oracle
conn = pyodbc.connect(
    'DRIVER={Oracle in OraClient11g_home1};'
    'DBQ=nombre_del_servicio;'
    'UID=usuario;'
    'PWD=password;'
)
conn.autocommit = False

id_origen = input('Ingrese el identificador de la cuenta de la que desea sacar dinero: ')
id_destino = input('Ingrese el identificador de la cuenta a la que desea ingresar dinero: ')
cantidad = input('Ingrese la cantidad de dinero que desea sacar: ')
cantidad = float(cantidad)

# Crear un cursor
cur = conn.cursor()

cur.execute("BEGIN;")

# Comprobar que las cuentas existen
try:
    cur.execute(f"SELECT idcuenta FROM cuenta WHERE idcuenta = ? FOR UPDATE;", (id_origen,))
    data = cur.fetchall()
    if len(data) == 0:
        raise Exception("La cuenta de origen no existe")
    
    cur.execute(f"SELECT idcuenta FROM cuenta WHERE idcuenta = ? FOR UPDATE;", (id_destino,))
    data = cur.fetchall()
    if len(data) == 0:
        raise Exception("La cuenta de destino no existe")
except Exception as e:
    conn.rollback()
    raise e

# Comprobar que hay suficiente saldo
try:
    cur.execute(f"SELECT saldo FROM cuenta WHERE idcuenta = ? FOR UPDATE;", (id_origen,))
    saldo = cur.fetchone()[0]
    if saldo < cantidad:
        raise Exception("No hay suficiente saldo")
except Exception as e:
    conn.rollback()
    raise e

# Obtener el identificador de la nueva transacción
cur.execute("SELECT MAX(idmov) FROM movimiento;")
last_idmove = cur.fetchone()[0]
if last_idmove is None:
    last_idmove = 0
else:
    last_idmove = int(last_idmove)
new_idmov = last_idmove + 1

# Comenzar la transferencia

# Primer paso: retirar el dinero de la cuenta origen
try:
    cur.execute(f"UPDATE cuenta SET saldo = saldo - ? WHERE idcuenta = ?;", (cantidad, id_origen))
except Exception as e:
    conn.rollback()
    raise e

# Segundo paso: ingresar el dinero en la cuenta destino
print("Dinero retirado de la cuenta origen")
resp = input(f"¿Seguro que quiere ingresar el dinero en la cuenta {id_destino}? (s/n): ")
if resp != 's':
    conn.rollback()
    raise Exception("Operación cancelada por el usuario")
else:
    try:
        cur.execute(f"UPDATE cuenta SET saldo = saldo + ? WHERE idcuenta = ?;", (cantidad, id_destino))
        cur.execute(f"INSERT INTO movimiento (idmov, idcuenta, cantidad) VALUES (?, ?, ?);", (new_idmov, id_origen, -cantidad))
        cur.execute(f"INSERT INTO movimiento (idmov, idcuenta, cantidad) VALUES (?, ?, ?);", (new_idmov + 1, id_destino, cantidad))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    print("Dinero ingresado en la cuenta destino")

cur.close()
conn.close()

