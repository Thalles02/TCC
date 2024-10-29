-- Cria o banco de dados se ele ainda não existir (deve ser feito fora de uma transação no PostgreSQL)
-- CREATE DATABASE clean_database;

-- Cria a tabela 'users' se ela ainda não existir
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email_adress VARCHAR(255) NOT NULL
);
