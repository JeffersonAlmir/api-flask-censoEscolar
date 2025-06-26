CREATE TABLE IF NOT EXISTS mesorregiao(
    co_mesorregiao INTEGER PRIMARY KEY,
    no_mesorregiao VARCHAR(100) NOT NULL,
    co_uf INTEGER NOT NULL,
    FOREIGN KEY (co_uf) REFERENCES uf(co_uf)
);