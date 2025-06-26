CREATE TABLE IF NOT EXISTS microrregiao(
    co_microrregiao INTEGER PRIMARY KEY,
    no_microrregiao VARCHAR(100) NOT NULL,
    co_uf INTEGER NOT NULL,
    FOREIGN KEY (co_uf) REFERENCES uf(co_uf)
);
