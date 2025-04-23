-- Cria o banco de dados se ele ainda não existir (deve ser feito fora de uma transação no PostgreSQL)
-- CREATE DATABASE clean_database;

-- Cria a tabela 'users' se ela ainda não existir
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email_address VARCHAR(255) NOT NULL
);


CREATE TABLE FlowTable (
    token VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);


CREATE TABLE DetailTable (
    id BIGSERIAL PRIMARY KEY,
    token VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    column_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (token) REFERENCES flowtable(token)
);

CREATE TABLE Workspace(
    id_workspace BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
)

CREATE TABLE WorkspaceTablesUser(
    id BIGSERIAL PRIMARY KEY,
    token_table VARCHAR(255) NOT NULL,
    workspace_id BIGINT NOT NULL,
    FOREIGN KEY (token_table) REFERENCES flowtable(token),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id)
)
