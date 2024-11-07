drop table if exists stock CASCADE;
drop table if exists pedido CASCADE;
drop table if exists detalle_pedido CASCADE;

CREATE TABLE  stock(
    Cproducto INTEGER PRIMARY KEY,
    Cantidad INTEGER
);

CREATE TABLE  pedido(
    Cpedido INTEGER PRIMARY KEY,
    Ccliente INTEGER,
    Fecha_pedido DATE
);

CREATE TABLE  detalle_pedido(
    Cpedido REFERENCES pedido(Cpedido),
    Cproducto REFERENCES stock(Cproducto),
    Cantidad INTEGER,
    PRIMARY KEY(Cpedido,Cproducto)
);

drop table if exists cuenta CASCADE;
drop table if exists movimiento CASCADE;

CREATE TABLE  cuenta(
    idcuenta INTEGER PRIMARY KEY,
    saldo FLOAT
);

CREATE TABLE movimiento(
    idmov INTEGER PRIMARY KEY,
    idcuenta INTEGER,
    cantidad FLOAT,
    FOREIGN KEY(idcuenta) REFERENCES cuenta(idcuenta)
);

INSERT INTO cuenta VALUES (1, 1000);
INSERT INTO cuenta VALUES (2, 2000);
INSERT INTO cuenta VALUES (3, 3000);
INSERT INTO cuenta VALUES (4, 4000);

INSERT INTO movimiento VALUES (1, 1, 100);
INSERT INTO movimiento VALUES (2, 3, -400);




SELECT version FROM dual;




SELECT * FROM pedido;

INSERT INTO pedido VALUES (1, 1, '10/10/2020');
INSERT INTO pedido VALUES (2, 2, '10/10/2020');
INSERT INTO pedido VALUES (3, 3, '10/10/2020');
DELETE FROM pedido WHERE Cpedido=5; 
INSERT INTO pedido (Cpedido, Ccliente, fecha_pedido) VALUES (5, 2, '07/11/2024' );
commit;
