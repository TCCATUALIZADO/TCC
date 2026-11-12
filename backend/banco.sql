-- ========================================================
-- BANCO DE DADOS: SISTEMA DE GESTÃO DE ESTOQUE / ALMOXARIFADO
-- ========================================================

-- 1. Criação do Banco de Dados
CREATE DATABASE IF NOT EXISTS trabalho;
USE trabalho;

-- 2. Tabela de Usuários (para autenticação com Bcrypt)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

-- 3. Tabela de Estoque Atual (Itens / Objetos)
CREATE TABLE IF NOT EXISTS objetos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    qtd INT NOT NULL DEFAULT 0,
    preco DECIMAL(10, 2) NOT NULL DEFAULT 0.00
);

-- 4. Tabela de Histórico de Movimentações
CREATE TABLE IF NOT EXISTS historico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    quantidade INT NOT NULL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Inserção de Usuários Padrão (ambos com a senha '1234' criptografada em Bcrypt)
INSERT IGNORE INTO usuarios (usuario, senha) VALUES
('admin', '$2b$12$FTcIscYIdVTA8TcsBxWkQONOAxn8xsk1i0xwcW9BpqvsII/QcmQJW'),
('user', '$2b$12$FTcIscYIdVTA8TcsBxWkQONOAxn8xsk1i0xwcW9BpqvsII/QcmQJW');

-- 6. Inserção de Itens Básicos para o Almoxarifado (Exemplos)
INSERT INTO objetos (nome, descricao, qtd, preco) VALUES
('Papel Sulfite A4', 'Pacote com 500 folhas brancas', 50, 28.90),
('Caneta Esferográfica Azul', 'Caixa com 50 unidades', 30, 45.00),
('Grampeador Médio', 'Grampeador metálico de mesa', 8, 22.50),
('Fita Adesiva Transparente', 'Rolo de 45mm x 50m', 25, 7.80),
('Bloco de Notas Post-it', 'Bloco com 100 folhas amarelas', 40, 6.50),
('Tesoura Multiuso', 'Tesoura de aço inox 21cm', 12, 14.90),
('Mouse Óptico USB', 'Mouse padrão para escritório', 15, 25.00),
('Teclado USB ABNT2', 'Teclado padrão para escritório', 10, 39.90);

-- 7. Inserção de Histórico Inicial (Registros de Entrada)
INSERT INTO historico (nome, tipo, quantidade) VALUES
('Papel Sulfite A4', 'Entrada', 50),
('Caneta Esferográfica Azul', 'Entrada', 30),
('Grampeador Médio', 'Entrada', 8),
('Fita Adesiva Transparente', 'Entrada', 25),
('Bloco de Notas Post-it', 'Entrada', 40),
('Tesoura Multiuso', 'Entrada', 12),
('Mouse Óptico USB', 'Entrada', 15),
('Teclado USB ABNT2', 'Entrada', 10);
