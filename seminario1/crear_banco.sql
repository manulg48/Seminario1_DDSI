drop table if exists cuenta CASCADE;
drop table if exists movimiento CASCADE;

CREATE TABLE IF NOT EXISTS cuenta(
    idcuenta INTEGER PRIMARY KEY,
    saldo FLOAT
);

CREATE TABLE IF NOT EXISTS movimiento(
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