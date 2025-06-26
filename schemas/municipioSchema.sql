CREATE TABLE IF NOT EXISTS municipio(
    co_municipio INTEGER PRIMARY KEY,
    no_municipio VARCHAR(150) NOT NULL,
    co_uf INTEGER NOT NULL,
    FOREIGN KEY (co_uf) REFERENCES uf(co_uf)
);
