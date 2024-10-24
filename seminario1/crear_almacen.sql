drop table if exists stock CASCADE;
drop table if exists pedido CASCADE;
drop table if exists detalle_pedido CASCADE;

CREATE TABLE IF NOT EXISTS stock(
    Cproducto INTEGER PRIMARY KEY,
    Cantidad INTEGER
);

CREATE TABLE IF NOT EXISTS pedido(
    Cpedido INTEGER PRIMARY KEY,
    Ccliente INTEGER,
    Fecha_pedido DATE
);

CREATE TABLE IF NOT EXISTS detalle_pedido(
    Cpedido REFERENCES pedido(Cpedido),
    Cproducto REFERENCES stock(Cproducto),
    Cantidad INTEGER,
    PRIMARY KEY(Cpedido,Cproducto)
);
