import os
import mysql.connector

# Pega as credenciais de variáveis de ambiente (útil para Docker) ou usa localhost (WampServer)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

def criar_banco():
    print(f"Conectando ao MySQL em {DB_HOST}...")
    try:
        # Conecta no MySQL
        conexao = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conexao.cursor()

        # 1. Cria o banco de dados 'trabalho' se não existir
        cursor.execute("CREATE DATABASE IF NOT EXISTS trabalho")
        cursor.execute("USE trabalho")
        print("[OK] Banco de dados 'trabalho' pronto!")

        # 2. Cria a tabela de usuários (autenticação com Bcrypt)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario VARCHAR(100) NOT NULL UNIQUE,
                senha VARCHAR(255) NOT NULL
            )
        """)
        print("[OK] Tabela 'usuarios' pronta!")

        # 3. Cria a tabela de objetos (itens do almoxarifado)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS objetos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                descricao VARCHAR(255),
                qtd INT NOT NULL DEFAULT 0,
                preco DECIMAL(10, 2) NOT NULL DEFAULT 0.00
            )
        """)
        print("[OK] Tabela 'objetos' pronta!")

        # 4. Cria a tabela de historico de movimentações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                tipo VARCHAR(50) NOT NULL,
                quantidade INT NOT NULL,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("[OK] Tabela 'historico' pronta!")

        # 5. Adiciona usuários padrão se ainda não existirem (senha 1234 criptografada com Bcrypt)
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        if total_usuarios == 0:
            senha_padrao_hash = "$2b$12$FTcIscYIdVTA8TcsBxWkQONOAxn8xsk1i0xwcW9BpqvsII/QcmQJW"
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)", ("admin", senha_padrao_hash))
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)", ("user", senha_padrao_hash))
            conexao.commit()
            print("[OK] Usuários padrão 'admin' e 'user' criados (senha: 1234)!")

        # 6. Verifica se já existem itens cadastrados
        cursor.execute("SELECT COUNT(*) FROM objetos")
        total_objetos = cursor.fetchone()[0]

        if total_objetos == 0:
            itens_iniciais = [
                ('Papel Sulfite A4', 'Pacote com 500 folhas brancas', 50, 28.90),
                ('Caneta Esferográfica Azul', 'Caixa com 50 unidades', 30, 45.00),
                ('Grampeador Médio', 'Grampeador metálico de mesa', 8, 22.50),
                ('Fita Adesiva Transparente', 'Rolo de 45mm x 50m', 25, 7.80),
                ('Bloco de Notas Post-it', 'Bloco com 100 folhas amarelas', 40, 6.50),
                ('Tesoura Multiuso', 'Tesoura de aço inox 21cm', 12, 14.90),
                ('Mouse Óptico USB', 'Mouse padrão para escritório', 15, 25.00),
                ('Teclado USB ABNT2', 'Teclado padrão para escritório', 10, 39.90)
            ]

            for nome, desc, qtd, preco in itens_iniciais:
                cursor.execute(
                    "INSERT INTO objetos (nome, descricao, qtd, preco) VALUES (%s, %s, %s, %s)",
                    (nome, desc, qtd, preco)
                )
                cursor.execute(
                    "INSERT INTO historico (nome, tipo, quantidade) VALUES (%s, %s, %s)",
                    (nome, "Entrada", qtd)
                )

            conexao.commit()
            print("[OK] 8 itens básicos de estoque foram adicionados!")
        else:
            print(f"[INFO] A tabela já possui {total_objetos} itens cadastrados.")

        cursor.close()
        conexao.close()
        print("\n[SUCESSO] Tudo pronto! Banco de dados configurado com sucesso.")

    except mysql.connector.Error as err:
        print("\n[ERRO] Erro ao conectar ao MySQL:")
        print(err)
        print("\n[DICA] Verifique se o WampServer/MySQL está iniciado.")

if __name__ == "__main__":
    criar_banco()
