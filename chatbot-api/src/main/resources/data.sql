-- Inserir dados iniciais apenas se as tabelas estiverem vazias

-- Cidades disponíveis para reservas
INSERT INTO
    opcoes_cidades (nome)
SELECT 'Rio de Janeiro'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_cidades
        WHERE
            nome = 'Rio de Janeiro'
    );

INSERT INTO
    opcoes_cidades (nome)
SELECT 'São Paulo'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_cidades
        WHERE
            nome = 'São Paulo'
    );

INSERT INTO
    opcoes_cidades (nome)
SELECT 'Brasília'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_cidades
        WHERE
            nome = 'Brasília'
    );

INSERT INTO
    opcoes_cidades (nome)
SELECT 'Recife'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_cidades
        WHERE
            nome = 'Recife'
    );

INSERT INTO
    opcoes_cidades (nome)
SELECT 'Salvador'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_cidades
        WHERE
            nome = 'Salvador'
    );

-- Hotéis disponíveis por cidade
INSERT INTO
    opcoes_hoteis (cidade, nome)
SELECT 'Rio de Janeiro', 'Copacabana Palace'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_hoteis
        WHERE
            cidade = 'Rio de Janeiro'
            AND nome = 'Copacabana Palace'
    );

INSERT INTO
    opcoes_hoteis (cidade, nome)
SELECT 'Rio de Janeiro', 'Windsor Oceanico'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_hoteis
        WHERE
            cidade = 'Rio de Janeiro'
            AND nome = 'Windsor Oceanico'
    );

INSERT INTO
    opcoes_hoteis (cidade, nome)
SELECT 'São Paulo', 'Renaissance Hotel'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_hoteis
        WHERE
            cidade = 'São Paulo'
            AND nome = 'Renaissance Hotel'
    );

INSERT INTO
    opcoes_hoteis (cidade, nome)
SELECT 'São Paulo', 'Tivoli Mofarrej'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_hoteis
        WHERE
            cidade = 'São Paulo'
            AND nome = 'Tivoli Mofarrej'
    );

INSERT INTO
    opcoes_hoteis (cidade, nome)
SELECT 'Brasília', 'Royal Tulip'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_hoteis
        WHERE
            cidade = 'Brasília'
            AND nome = 'Royal Tulip'
    );

INSERT INTO
    opcoes_hoteis (cidade, nome)
SELECT 'Brasília', 'Melia Brasil 21'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_hoteis
        WHERE
            cidade = 'Brasília'
            AND nome = 'Melia Brasil 21'
    );

INSERT INTO
    opcoes_hoteis (cidade, nome)
SELECT 'Recife', 'Mar Hotel'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_hoteis
        WHERE
            cidade = 'Recife'
            AND nome = 'Mar Hotel'
    );

INSERT INTO
    opcoes_hoteis (cidade, nome)
SELECT 'Recife', 'Sheraton Reserva'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_hoteis
        WHERE
            cidade = 'Recife'
            AND nome = 'Sheraton Reserva'
    );

INSERT INTO
    opcoes_hoteis (cidade, nome)
SELECT 'Salvador', 'Wish Hotel da Bahia'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_hoteis
        WHERE
            cidade = 'Salvador'
            AND nome = 'Wish Hotel da Bahia'
    );

INSERT INTO
    opcoes_hoteis (cidade, nome)
SELECT 'Salvador', 'Gran Hotel Stella Maris'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_hoteis
        WHERE
            cidade = 'Salvador'
            AND nome = 'Gran Hotel Stella Maris'
    );

-- Voos disponíveis
INSERT INTO
    opcoes_voos (
        codigo,
        origem,
        destino,
        horarios
    )
SELECT 'VLRJS', 'Rio de Janeiro', 'São Paulo', '["07:00", "12:00", "15:30", "19:45"]'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_voos
        WHERE
            codigo = 'VLRJS'
    );

INSERT INTO
    opcoes_voos (
        codigo,
        origem,
        destino,
        horarios
    )
SELECT 'VLRJB', 'Rio de Janeiro', 'Brasília', '["08:15", "13:20", "18:00"]'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_voos
        WHERE
            codigo = 'VLRJB'
    );

INSERT INTO
    opcoes_voos (
        codigo,
        origem,
        destino,
        horarios
    )
SELECT 'VLSPR', 'São Paulo', 'Rio de Janeiro', '["06:30", "11:45", "17:15", "21:00"]'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_voos
        WHERE
            codigo = 'VLSPR'
    );

INSERT INTO
    opcoes_voos (
        codigo,
        origem,
        destino,
        horarios
    )
SELECT 'VLSPB', 'São Paulo', 'Brasília', '["07:20", "11:00", "16:40", "20:15"]'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_voos
        WHERE
            codigo = 'VLSPB'
    );

INSERT INTO
    opcoes_voos (
        codigo,
        origem,
        destino,
        horarios
    )
SELECT 'VLBRE', 'Brasília', 'Recife', '["08:00", "14:30", "19:00"]'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_voos
        WHERE
            codigo = 'VLBRE'
    );

INSERT INTO
    opcoes_voos (
        codigo,
        origem,
        destino,
        horarios
    )
SELECT 'VLREC', 'Recife', 'Salvador', '["09:15", "15:40", "18:30"]'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM opcoes_voos
        WHERE
            codigo = 'VLREC'
    );