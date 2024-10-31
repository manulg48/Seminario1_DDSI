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
