import os
import oracledb
import datetime
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

    
def opcion2():

    os.system('clear')
    print ( '\nHas seleccionado la opción 2 "Dar de alta nuevo pedido" ' )
    
    
    cursor.execute("SAVEPOINT PrincipioOpcion2")
    
    #Capturar datos básicos del pedido
    Ccliente = int(input(' Ingrese su numero de cliente: ' ))
    fecha_actual = datetime.date.today().strftime("%d/%m/%Y")
    
    #Coger el valor siguiente de Cpedido
    cursor.execute("SELECT MAX(Cpedido) FROM pedido")
    last_Cpedido =   cursor.fetchone()[0]
    new_Cpedido = last_Cpedido + 1 
    
    try:
        cursor.execute ( f"INSERT INTO pedido VALUES ({new_Cpedido}, {Ccliente}, TO_DATE('{fecha_actual}', 'DD/MM/YYYY') )" )
    except Exception as e:
        cursor.execute("ROLLBACK TO PrincipioOpcion2")
        raise e
            
    print( 'Elija qué opción quiere hacer del menú 1-4' )
    print( '\t1. Añadir detalle de producto' )
    print( '\t2. Eliminar todos los detalles de producto' )
    print( '\t3. Cancelar pedido' )
    print( '\t4. Finalizar pedido' )

    opcion = int(input(' Ingrese la opción: '))
    
    cursor.execute("SAVEPOINT Antes")


    match opcion:
        case 1:
            
            cursor.execute("SAVEPOINT AntesDeIngresarPedido")

            #Capturar datos de articulo / cantidad
            Cproducto = int(input( 'Ingrese producto: ' ))
            cantidad = int(input(' Ingrese cantidad: '))
            #Ingresar en la tabla Detalle-Pedido
            try:
                
                cursor.execute(f"SELECT cantidad FROM stock WHERE Cproducto = {Cproducto}")
                stock = cursor.fetchone()
                
                if ( stock[0] is not None and stock[0] >= cantidad ):  # Si hay stock
                    cursor.execute(f"INSERT INTO detalle_pedido VALUES ({new_Cpedido}, {Cproducto}, {cantidad})" )
                    cursor.execute(f"UPDATE stock SET cantidad = cantidad + {-cantidad} WHERE Cproducto = {Cproducto}")
                    cursor.execute(f"UPDATE detalle_pedido SET cantidad = cantidad + {-cantidad} WHERE Cproducto = {Cproducto}")
                else:              #Si no hay stock
                    print( 'No hay stock de este producto, presione Enter para continuar' ) 
                    input()

            except Exception as e:
                cursor.execute("ROLLBACK TO AntesDeIngresarPedido")
                raise e
           

            opcion2()
                
        
           
        case 2:
            #Hacer rollback
            cursor.execute( "ROLLBACK TO Antes")
            opcion2()
            
        case 3:
            #Volver al menu principal
            cursor.execute( "ROLLBACK TO PrincipioOpcion2" )
            menu()
        case 4:
            #Hacer commit
            conn.commit()
            menu()
        case _:
            print(' Ups, te has equivocado de numero, vuelve a intentarlo...')
            opcion2()



def opcion1():
        
    #Borrado
    try:
        cursor.execute(f"DROP TABLE detalle_pedido")
        cursor.execute(f"DROP TABLE stock")
        cursor.execute(f"DROP TABLE pedido")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar las tablas")
        raise e


    #Creacion

    # Crear la tabla stock
    cursor.execute("CREATE TABLE stock (Cproducto INTEGER PRIMARY KEY,Cantidad INTEGER)")
    print("Tabla 'stock' creada.")

    # Crear la tabla pedido
    cursor.execute("CREATE TABLE pedido (Cpedido INTEGER PRIMARY KEY,Ccliente INTEGER,Fecha_pedido DATE)")
    print("Tabla 'pedido' creada.")

    # Crear la tabla detalle_pedido
    cursor.execute("CREATE TABLE detalle_pedido ( Cpedido INTEGER, Cproducto INTEGER,Cantidad INTEGER,PRIMARY KEY (Cpedido, Cproducto),FOREIGN KEY (Cpedido) REFERENCES pedido(Cpedido),FOREIGN KEY (Cproducto) REFERENCES stock(Cproducto))")
    print("Tabla 'detalle_pedido' creada.")

    #Insercion

    # Tuplas predefinidas a insertar
    tuplas_stock = {
        1:50,
        2:120,
        3:80,
        4:200,
        5:150,
        6:60,
        7:30,
        8:90,
        9:40,
        10:300
    }

    for cproducto, cantidad in tuplas_stock.items():
        cursor.execute( f"INSERT INTO stock VALUES ({cproducto}, {cantidad})")
        print(f"Insertado producto {cproducto} con cantidad {cantidad}")

    # Confirmar los cambios
    conn.commit()
    print("Las 10 tuplas han sido insertadas exitosamente en la tabla 'Stock'.")




def opcion3():
    queries = {"Pedido":"SELECT * FROM pedido","Stock":"SELECT * FROM stock","Detalle_Pedido":"SELECT * FROM detalle_pedido"}
    for title, query in queries.items():
        print(f"\n--- Resultados de {title} ---")
        cursor.execute(query)

        column_names = [col[0] for col in cursor.description]
        print(" | ".join(column_names))
        for row in cursor:
                print(" | ".join(map(str, row)))

def opcion4():
    print( 'Conexión cerrada, Bye...' )
    time.sleep(2)
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
    
    
    opcion = int(input(' Ingrese la opción: '))
    
    match opcion:
        case 1: 
            opcion1()
        case 2:
            opcion2()
        case 3: 
            opcion3()
        case 4: 
            opcion4()
        case _:
            print(' Ups, te has equivocado de numero, vuelve a intentarlo...')
            menu()
            
    
menu()
