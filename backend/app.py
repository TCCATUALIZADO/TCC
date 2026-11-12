from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
import bcrypt
import os

app = Flask(__name__)

# ========================================================
# 1. CONFIGURAÇÃO DE CONEXÃO COM O BANCO DE DADOS MYSQL
# ========================================================
# Pega o host das variáveis de ambiente (útil quando rodar no Docker)
# ou usa "localhost" por padrão (quando rodar no WampServer no Windows)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "trabalho")

def conectar():
    """Função básica para abrir conexão com o banco MySQL."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# ========================================================
# 2. CONFIGURAÇÃO DE CORS (Cross-Origin Resource Sharing)
# ========================================================
# Permite que o aplicativo móvel (React Native / Expo) consiga
# fazer requisições para a nossa API sem ser bloqueado pelo navegador/dispositivo
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


# ========================================================
# 3. ROTAS DAS PÁGINAS WEB (HTML/CSS/JS)
# ========================================================

@app.route("/")
def home():
    """Página de cadastro na interface Web."""
    return render_template("home.html")

@app.route("/index")
def index():
    """Página de login na interface Web."""
    return render_template("index.html")

@app.route("/menu")
def menu():
    """Menu principal do sistema."""
    return render_template("menu.html")

@app.route("/paginaconsulta")
def paginaconsulta():
    """Página web que exibe a tabela com todos os itens do estoque."""
    erro = None
    objetos = []
    try:
        banco = conectar()
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM objetos ORDER BY id DESC")
        objetos = cursor.fetchall()
        cursor.close()
        banco.close()
    except Exception as e:
        print("Erro ao conectar ou consultar:", e)
        erro = "Não foi possível conectar ao banco MySQL. Verifique se o MySQL ou Docker está iniciado."

    return render_template("paginaconsulta.html", objetos=objetos, erro=erro)

@app.route("/paginadeentrada")
def paginadeentrada():
    """Página web para registrar entrada de estoque."""
    return render_template("paginadeentrada.html")

@app.route("/paginadesaida")
def paginadesaida():
    """Página web para registrar saída de estoque."""
    return render_template("paginadesaida.html")

@app.route("/paginadonovoitem")
def paginadonovoitem():
    """Página web com formulário para cadastrar novo item."""
    return render_template("paginadonovoitem.html")

@app.route("/adicionaritem", methods=["POST"])
def adicionaritem():
    """Recebe os dados do formulário web e salva o novo item no banco."""
    nome = request.form["nome"]
    descricao = request.form["descricao"]
    qtd = request.form["qtd"]
    preco = request.form["preco"]

    banco = conectar()
    cursor = banco.cursor()

    # Insere o produto
    cursor.execute(
        "INSERT INTO objetos (nome, descricao, qtd, preco) VALUES (%s, %s, %s, %s)",
        (nome, descricao, qtd, preco)
    )

    # Registra no histórico que houve uma entrada
    cursor.execute(
        "INSERT INTO historico (nome, tipo, quantidade) VALUES (%s, %s, %s)",
        (nome, "Entrada", qtd)
    )

    banco.commit()
    cursor.close()
    banco.close()

    return redirect("/paginaconsulta")

@app.route("/excluir_todos")
def excluir_todos():
    """Exclui todos os itens do estoque pela interface web."""
    banco = conectar()
    cursor = banco.cursor()
    cursor.execute("DELETE FROM objetos")
    banco.commit()
    cursor.close()
    banco.close()
    return redirect("/paginaconsulta")

@app.route("/excluir/<id>")
def excluir(id):
    """Exclui um item específico pelo ID na interface web."""
    banco = conectar()
    cursor = banco.cursor()

    cursor.execute("SELECT nome, qtd FROM objetos WHERE id = %s", (id,))
    objeto = cursor.fetchone()

    if objeto:
        cursor.execute(
            "INSERT INTO historico (nome, tipo, quantidade) VALUES (%s, %s, %s)",
            (objeto[0], "Saída", objeto[1])
        )
        cursor.execute("DELETE FROM objetos WHERE id = %s", (id,))
        banco.commit()

    cursor.close()
    banco.close()

    return redirect("/paginaconsulta")

@app.route("/historico")
def historico():
    """Página web que exibe todas as movimentações feitas."""
    erro = None
    historico = []
    try:
        banco = conectar()
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM historico ORDER BY id DESC")
        historico = cursor.fetchall()
        cursor.close()
        banco.close()
    except Exception as e:
        print("Erro ao consultar historico:", e)
        erro = "Não foi possível conectar ao banco MySQL. Verifique se o MySQL ou Docker está iniciado."

    return render_template("historico.html", historico=historico, erro=erro)

@app.route("/apagarhistorico")
def apagarhistorico():
    """Limpa o histórico de movimentações."""
    try:
        banco = conectar()
        cursor = banco.cursor()
        cursor.execute("DELETE FROM historico")
        banco.commit()
        cursor.close()
        banco.close()
    except Exception as e:
        print("Erro ao apagar historico:", e)

    return redirect("/historico")


# ========================================================
# 4. ROTAS EXTERNAS DE API REST (Consumidas pelo App Mobile)
# ========================================================

# --- ROTA REST 1: Cadastro de Usuário com Bcrypt ---
@app.route("/api/cadastro", methods=["POST"])
def api_cadastro():
    """
    Recebe {usuario, senha} em JSON e salva no banco com a senha
    criptografada usando a biblioteca Bcrypt.
    """
    dados = request.get_json(silent=True) or request.form
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if not usuario or not senha:
        return jsonify({"sucesso": False, "mensagem": "Usuário e senha são obrigatórios!"}), 400

    try:
        # 1. Gera o salt e a senha criptografada (hash)
        senha_bytes = senha.encode("utf-8")
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, salt).decode("utf-8")

        banco = conectar()
        cursor = banco.cursor()

        # 2. Verifica se já existe um usuário com esse mesmo nome
        cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (usuario,))
        if cursor.fetchone():
            cursor.close()
            banco.close()
            return jsonify({"sucesso": False, "mensagem": "Este nome de usuário já existe!"}), 400

        # 3. Salva no banco de dados
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)", (usuario, senha_hash))
        banco.commit()
        cursor.close()
        banco.close()

        return jsonify({"sucesso": True, "mensagem": "Usuário cadastrado com sucesso!"}), 201

    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro interno: {str(e)}"}), 500


# --- ROTA REST 2: Login e Autenticação de Usuário com Bcrypt ---
@app.route("/api/login", methods=["POST"])
def api_login():
    """
    Recebe {usuario, senha} em JSON, busca o usuário no banco e
    usa o bcrypt.checkpw para verificar se a senha está correta.
    """
    dados = request.get_json(silent=True) or request.form
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if not usuario or not senha:
        return jsonify({"sucesso": False, "mensagem": "Informe usuário e senha!"}), 400

    try:
        banco = conectar()
        cursor = banco.cursor()
        cursor.execute("SELECT id, senha FROM usuarios WHERE usuario = %s", (usuario,))
        resultado = cursor.fetchone()
        cursor.close()
        banco.close()

        if not resultado:
            return jsonify({"sucesso": False, "mensagem": "Usuário não encontrado!"}), 401

        id_usuario, senha_hash_banco = resultado

        # Compara a senha digitada em texto com o hash criptografado salvo no banco
        senha_correta = bcrypt.checkpw(senha.encode("utf-8"), senha_hash_banco.encode("utf-8"))

        if senha_correta:
            return jsonify({
                "sucesso": True,
                "mensagem": "Login realizado com sucesso!",
                "usuario": usuario,
                "id": id_usuario
            }), 200
        else:
            return jsonify({"sucesso": False, "mensagem": "Senha incorreta!"}), 401

    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro interno: {str(e)}"}), 500


# --- ROTA REST 3: Listar Todos os Produtos (Consulta) ---
@app.route("/api/produtos", methods=["GET"])
def api_listar_produtos():
    """
    Retorna uma lista JSON de todos os produtos do estoque.
    """
    try:
        banco = conectar()
        cursor = banco.cursor()
        cursor.execute("SELECT id, nome, descricao, qtd, preco FROM objetos ORDER BY id DESC")
        linhas = cursor.fetchall()
        cursor.close()
        banco.close()

        produtos = []
        for linha in linhas:
            produtos.append({
                "id": linha[0],
                "nome": linha[1],
                "descricao": linha[2] or "",
                "qtd": int(linha[3]),
                "preco": float(linha[4]) if linha[4] is not None else 0.0
            })

        return jsonify({"sucesso": True, "produtos": produtos}), 200

    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro interno: {str(e)}"}), 500


# --- ROTA REST 4: Cadastrar Novo Produto ---
@app.route("/api/produtos", methods=["POST"])
def api_adicionar_produto():
    """
    Recebe {nome, descricao, qtd, preco} e cadastra um novo produto no estoque.
    """
    dados = request.get_json(silent=True) or request.form
    nome = dados.get("nome")
    descricao = dados.get("descricao", "")
    qtd = dados.get("qtd", 0)
    preco = dados.get("preco", 0.0)

    if not nome:
        return jsonify({"sucesso": False, "mensagem": "O campo 'nome' é obrigatório!"}), 400

    try:
        qtd = int(qtd)
        preco = float(preco)
    except:
        return jsonify({"sucesso": False, "mensagem": "Quantidade e Preço devem ser numéricos!"}), 400

    try:
        banco = conectar()
        cursor = banco.cursor()

        # Insere na tabela objetos
        cursor.execute(
            "INSERT INTO objetos (nome, descricao, qtd, preco) VALUES (%s, %s, %s, %s)",
            (nome, descricao, qtd, preco)
        )
        novo_id = cursor.lastrowid

        # Registra entrada inicial no historico
        cursor.execute(
            "INSERT INTO historico (nome, tipo, quantidade) VALUES (%s, %s, %s)",
            (nome, "Entrada", qtd)
        )

        banco.commit()
        cursor.close()
        banco.close()

        return jsonify({
            "sucesso": True,
            "mensagem": "Produto cadastrado com sucesso!",
            "id": novo_id
        }), 201

    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro interno: {str(e)}"}), 500


# --- ROTA REST 5: Editar Produto Existente ---
@app.route("/api/produtos/<int:id>", methods=["PUT", "POST"])
@app.route("/api/produtos/<int:id>/editar", methods=["POST"])
def api_editar_produto(id):
    """
    Atualiza as informações de um produto pelo seu ID.
    """
    dados = request.get_json(silent=True) or request.form
    nome = dados.get("nome")
    descricao = dados.get("descricao", "")
    qtd = dados.get("qtd")
    preco = dados.get("preco")

    if not nome:
        return jsonify({"sucesso": False, "mensagem": "Nome do produto é obrigatório!"}), 400

    try:
        qtd = int(qtd)
        preco = float(preco)
    except:
        return jsonify({"sucesso": False, "mensagem": "Quantidade e Preço inválidos!"}), 400

    try:
        banco = conectar()
        cursor = banco.cursor()

        cursor.execute(
            "UPDATE objetos SET nome = %s, descricao = %s, qtd = %s, preco = %s WHERE id = %s",
            (nome, descricao, qtd, preco, id)
        )
        banco.commit()
        cursor.close()
        banco.close()

        return jsonify({"sucesso": True, "mensagem": "Produto atualizado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro interno: {str(e)}"}), 500


# --- ROTA REST 6: Excluir Produto ---
@app.route("/api/produtos/<int:id>", methods=["DELETE", "POST"])
@app.route("/api/produtos/<int:id>/excluir", methods=["POST"])
def api_excluir_produto(id):
    """
    Remove um produto pelo ID e registra a saída de todo o estoque no histórico.
    """
    try:
        banco = conectar()
        cursor = banco.cursor()

        cursor.execute("SELECT nome, qtd FROM objetos WHERE id = %s", (id,))
        produto = cursor.fetchone()

        if not produto:
            cursor.close()
            banco.close()
            return jsonify({"sucesso": False, "mensagem": "Produto não encontrado!"}), 404

        nome, qtd = produto

        # Registra a saída no histórico
        cursor.execute(
            "INSERT INTO historico (nome, tipo, quantidade) VALUES (%s, %s, %s)",
            (nome, "Saída", qtd)
        )

        cursor.execute("DELETE FROM objetos WHERE id = %s", (id,))
        banco.commit()
        cursor.close()
        banco.close()

        return jsonify({"sucesso": True, "mensagem": f"Produto '{nome}' excluído com sucesso!"}), 200

    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro interno: {str(e)}"}), 500


# --- ROTA REST 7: Movimentações de Entrada e Saída de Itens ---
@app.route("/api/movimentacao", methods=["POST"])
def api_movimentacao():
    """
    Recebe {id, nome, tipo: 'Entrada'|'Saída', quantidade}
    Atualiza a quantidade do item no estoque e adiciona um registro no histórico.
    """
    dados = request.get_json(silent=True) or request.form
    prod_id = dados.get("id")
    nome = dados.get("nome")
    tipo = dados.get("tipo") # "Entrada" ou "Saída"
    quantidade = dados.get("quantidade")

    if not tipo or tipo not in ["Entrada", "Saída"]:
        return jsonify({"sucesso": False, "mensagem": "Tipo de movimentação deve ser 'Entrada' ou 'Saída'!"}), 400

    try:
        quantidade = int(quantidade)
        if quantidade <= 0:
            return jsonify({"sucesso": False, "mensagem": "Quantidade deve ser maior que zero!"}), 400
    except:
        return jsonify({"sucesso": False, "mensagem": "Quantidade numérica inválida!"}), 400

    try:
        banco = conectar()
        cursor = banco.cursor()

        # Localiza o produto por ID ou por Nome
        if prod_id:
            cursor.execute("SELECT id, nome, qtd FROM objetos WHERE id = %s", (prod_id,))
        elif nome:
            cursor.execute("SELECT id, nome, qtd FROM objetos WHERE LOWER(nome) = LOWER(%s)", (nome.strip(),))
        else:
            cursor.close()
            banco.close()
            return jsonify({"sucesso": False, "mensagem": "Informe o ID ou Nome do produto!"}), 400

        produto = cursor.fetchone()
        if not produto:
            cursor.close()
            banco.close()
            return jsonify({"sucesso": False, "mensagem": "Produto não encontrado no estoque!"}), 404

        p_id, p_nome, p_qtd = produto

        # Calcula a nova quantidade
        if tipo == "Entrada":
            nova_qtd = p_qtd + quantidade
        else: # Saída
            if p_qtd < quantidade:
                cursor.close()
                banco.close()
                return jsonify({
                    "sucesso": False,
                    "mensagem": f"Estoque insuficiente! Disponível: {p_qtd}, Solicitado: {quantidade}"
                }), 400
            nova_qtd = p_qtd - quantidade

        # Atualiza a tabela objetos
        cursor.execute("UPDATE objetos SET qtd = %s WHERE id = %s", (nova_qtd, p_id))

        # Grava no histórico
        cursor.execute(
            "INSERT INTO historico (nome, tipo, quantidade) VALUES (%s, %s, %s)",
            (p_nome, tipo, quantidade)
        )

        banco.commit()
        cursor.close()
        banco.close()

        return jsonify({
            "sucesso": True,
            "mensagem": f"{tipo} de {quantidade} unidade(s) registrada com sucesso para '{p_nome}'!",
            "nova_qtd": nova_qtd
        }), 200

    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro interno: {str(e)}"}), 500


# --- ROTA REST 8: Listar Histórico de Movimentações ---
@app.route("/api/historico", methods=["GET"])
def api_listar_historico():
    """
    Retorna uma lista JSON de todas as movimentações de estoque registradas.
    """
    try:
        banco = conectar()
        cursor = banco.cursor()
        cursor.execute("SELECT id, nome, tipo, quantidade, data FROM historico ORDER BY id DESC")
        linhas = cursor.fetchall()
        cursor.close()
        banco.close()

        historico_lista = []
        for linha in linhas:
            historico_lista.append({
                "id": linha[0],
                "nome": linha[1],
                "tipo": linha[2],
                "quantidade": linha[3],
                "data": str(linha[4]) if linha[4] else ""
            })

        return jsonify({"sucesso": True, "historico": historico_lista}), 200

    except Exception as e:
        return jsonify({"sucesso": False, "mensagem": f"Erro interno: {str(e)}"}), 500


# ========================================================
# 5. INICIALIZAÇÃO DO SERVIDOR FLASK
# ========================================================
if __name__ == "__main__":
    # host="0.0.0.0" permite que outros dispositivos (como seu celular via Expo Go)
    # ou outros computadores da mesma rede acessem o servidor Flask
    print("=" * 60)
    print(" Servidor Flask iniciado com sucesso!")
    print(" Acesse no navegador: http://localhost:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)
