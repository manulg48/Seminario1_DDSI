import os
import oracledb
import time

# Configura la conexión a la base de datos Oracle
# Aquí se utiliza un DSN con conexión directa
dsn = "oracle0.ugr.es:1521/practbd"
usuario = "x8267949"
password = "x8267949"

# Conexión a la base de datos
conn = oracledb.connect(user=usuario, password=password, dsn=dsn)
conn.autocommit = False  # Desactivar autocommit para manejo manual de transacciones
cursor = conn.cursor()
    
def opcion1():
    #Borrado

    borrar = ["stock","pedido","detalle_pedido"]
    for tabla in borrar:
        try:
            cursor.execute(f"DROP TABLE {tabla}")
            print(f"La tabla {tabla} ha sido eliminida de la base de datos.")
        except oracledb.DatabaseError as err:
            error = err.args
            if error.code == 942:
                print(f"{tabla} no existe")
            else:
                print(f"Error al eliminar la tabla {tabla}: {error.message}")


    #Creacion

    # Crear la tabla stock
    cursor.execute("""
        CREATE TABLE stock (
            Cproducto INTEGER PRIMARY KEY,
            Cantidad INTEGER
        )
    """)
    print("Tabla 'stock' creada.")

    # Crear la tabla pedido
    cursor.execute("""
        CREATE TABLE pedido (
            Cpedido INTEGER PRIMARY KEY,
            Ccliente INTEGER,
            Fecha_pedido DATE
        )
    """)
    print("Tabla 'pedido' creada.")

    # Crear la tabla detalle_pedido
    cursor.execute("""
        CREATE TABLE detalle_pedido (
            Cpedido INTEGER,
            Cproducto INTEGER,
            Cantidad INTEGER,
            PRIMARY KEY (Cpedido, Cproducto),
            FOREIGN KEY (Cpedido) REFERENCES pedido(Cpedido),
            FOREIGN KEY (Cproducto) REFERENCES stock(Cproducto)
        )
    """)
    print("Tabla 'detalle_pedido' creada.")

    #Insercion

    # Tuplas predefinidas a insertar
    tuplas_stock = [
        (101, 50),
        (102, 120),
        (103, 80),
        (104, 200),
        (105, 150),
        (106, 60),
        (107, 30),
        (108, 90),
        (109, 40),
        (110, 300)
    ]

    for cproducto, cantidad in tuplas_stock:
        cursor.execute(
            "INSERT INTO Stock (Cproducto, Cantidad) VALUES (:1, :2)",
            (cproducto, cantidad)
        )
        print(f"Insertado producto {cproducto} con cantidad {cantidad}")

    # Confirmar los cambios
    conn.commit()
    print("Las 10 tuplas han sido insertadas exitosamente en la tabla 'Stock'.")


def opcion2():
    os.system('clear')
    print ( '\nBuenas Fran!! :)' )
    print( 'Elija qué opción quiere hacer del menú 1-4' )
    print( '\t1. Añadir detalle de producto' )
    print( '\t2. Eliminar todos los detalles de producto' )
    print( '\t3. Cancelar pedido' )
    print( '\t4. Finalizar pedido' )

    opcion = int(input(' Ingrese la opción: '))
    
    match opcion:
        case 1:
            articulo = int(input( 'Ingrese articulo: ' ))
            cantidad = float(input(' Ingrese cantidad: '))
            #Ingresar en la tabla Detalle-Pedido
            
            
            op = str(input('¿Quiere ingresar mas articulos? S/N\n'))
            if( op.lower() == 's' ): 
                menu()
            else:
                print('\tMuchas gracias maquina ;)' )
        case 2:
            #Hacer rollback
            print('')
        case 3:
            #Volver al menu principal
            menu()
        case 4:
            #Hacer commit
            menu()
        case _:
            print(' Ups, te has equivocado de numero, vuelve a intentarlo...')
            menu()


def opcion4():
    print( 'Conexión cerrada, Bye...' )
    time.sleep(100)
    cursor.close()
    conn.close()
    

def menu():
    os.system('clear')
    print ( '\nBuenas Fran!! :)' )
    print( 'Elija qué opción quiere hacer del menú 1-4' )
    print( '\t1. Borrado, creación e inserción de 10 tuplas en la tabla Stock' )
    print( '\t2. Dar de alta nuevo pedido' )
    print( '\t3. Mostrar contenido de la BD' )
    print( '\t4. Salir programa y cerrar conexión ' )
    
    
    opcion = input(' Ingrese la opción: ')
    
    match opcion:
        case 1: 
            opcion1()
        case 2:
            opcion2()
        case 3: 
            opcion3()
        case 4: 
            opcion4()
            
    
menu()
