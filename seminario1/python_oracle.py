import oracledb

# Configura la conexión a la base de datos Oracle
# Aquí se utiliza un DSN con conexión directa
dsn = "oracle0.ugr.es:1521/practbd"
usuario = "x8267949"
password = "x8267949"

# Conexión a la base de datos
conn = oracledb.connect(user=usuario, password=password, dsn=dsn)
conn.autocommit = False  # Desactivar autocommit para manejo manual de transacciones

# Solicitar información al usuario
id_origen = input('Ingrese el identificador de la cuenta de la que desea sacar dinero: ')
id_destino = input('Ingrese el identificador de la cuenta a la que desea ingresar dinero: ')
cantidad = float(input('Ingrese la cantidad de dinero que desea transferir: '))

# Crear un cursor
cur = conn.cursor()

try:
    # Verificar la existencia de la cuenta de origen
    cur.execute("SELECT idcuenta FROM cuenta WHERE idcuenta = :id FOR UPDATE", {'id': id_origen})
    if cur.fetchone() is None:
        raise Exception("La cuenta de origen no existe")

    # Verificar la existencia de la cuenta de destino
    cur.execute("SELECT idcuenta FROM cuenta WHERE idcuenta = :id FOR UPDATE", {'id': id_destino})
    if cur.fetchone() is None:
        raise Exception("La cuenta de destino no existe")

    # Verificar que la cuenta de origen tenga saldo suficiente
    cur.execute("SELECT saldo FROM cuenta WHERE idcuenta = :id FOR UPDATE", {'id': id_origen})
    saldo_origen = cur.fetchone()[0]
    if saldo_origen < cantidad:
        raise Exception("Saldo insuficiente en la cuenta de origen")

    # Obtener un nuevo identificador para la transacción
    cur.execute("SELECT NVL(MAX(idmov), 0) + 1 FROM movimiento")
    new_idmov = cur.fetchone()[0]

    # Confirmar antes de proceder con la transferencia
    print("Dinero retirado de la cuenta origen")
    resp = input(f"¿Seguro que quiere ingresar el dinero en la cuenta {id_destino}? (s/n): ")
    if resp.lower() != 's':
        raise Exception("Operación cancelada por el usuario")

    # Realizar la transferencia de saldo
    cur.execute("UPDATE cuenta SET saldo = saldo - :cantidad WHERE idcuenta = :id", {'cantidad': cantidad, 'id': id_origen})
    cur.execute("UPDATE cuenta SET saldo = saldo + :cantidad WHERE idcuenta = :id", {'cantidad': cantidad, 'id': id_destino})

    # Registrar la transferencia en la tabla de movimientos
    cur.execute("INSERT INTO movimiento (idmov, idcuenta, cantidad) VALUES (:idmov, :idcuenta, :cantidad)", {'idmov': new_idmov, 'idcuenta': id_origen, 'cantidad': -cantidad})
    cur.execute("INSERT INTO movimiento (idmov, idcuenta, cantidad) VALUES (:idmov, :idcuenta, :cantidad)", {'idmov': new_idmov + 1, 'idcuenta': id_destino, 'cantidad': cantidad})

    # Confirmar la transacción
    conn.commit()
    print("Dinero ingresado en la cuenta destino y transacción registrada exitosamente")

except Exception as e:
    # Revertir la transacción en caso de error
    conn.rollback()
    print(f"Error: {e}")

finally:
    # Cerrar cursor y conexión
    cur.close()
    conn.close()

