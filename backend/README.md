# 📦 PROJETO FINAL — SISTEMA DE GESTÃO DE ESTOQUE (ALMOXARIFADO)

Projeto desenvolvido com **Flask (Python)**, **MySQL**, **Bcrypt**, **Docker Compose** e **Aplicativo Móvel em React Native (Expo Go)**.

---

## 🎯 1. O que este projeto tem?

1. **Backend Flask (Python)** com rotas para as páginas Web e rotas de **API REST** em JSON.
2. **Segurança com Bcrypt**: senhas dos usuários criptografadas com hash seguro (nunca em texto puro).
3. **Banco de Dados MySQL**: tabelas de `usuarios`, `objetos` (estoque) e `historico` (entradas e saídas).
4. **Containerização completa com Docker Compose**: sobe o banco MySQL e o servidor Flask em containers com apenas um comando.
5. **Aplicativo Mobile (React Native + Expo Go)**: consome as rotas REST para login, cadastro, consulta de itens, adição de novo produto, movimentações de entrada/saída e histórico.
6. **Interface Web (HTML, CSS e JavaScript)** estilizada e conectada ao banco de dados.

---

## 🚀 2. Como Rodar o Projeto

Você tem duas maneiras muito simples de rodar: **com Docker** (recomendado para a entrega) ou **localmente sem Docker** (com WampServer / XAMPP).

### Opção A: Rodando com Docker Compose (Requisito da Apresentação)

1. Abra o **Docker Desktop** no seu computador e espere ele iniciar.
2. Abra o terminal na pasta do projeto (`d:\NovoRayanGay\Rayan-gay`).
3. Execute o comando:
   ```bash
   docker compose up --build
   ```
4. Pronto! O Docker vai:
   - Baixar a imagem do MySQL e criar o banco com o script `banco.sql`.
   - Construir a imagem da sua aplicação Flask e iniciá-la na porta `5000`.
5. Acesse no navegador:
   - Web: `http://localhost:5000`

---

### Opção B: Rodando Localmente sem Docker (com WampServer / XAMPP)

1. Abra o **WampServer** ou **XAMPP** (inicie o serviço do MySQL).
2. Se for a primeira vez, execute o script para criar o banco e as tabelas:
   ```bash
   python criar_banco.py
   ```
3. Inicie o servidor Flask:
   ```bash
   python app.py
   ```
4. Acesse no navegador:
   - Web: `http://localhost:5000`

---

## 📱 3. Como Rodar o Aplicativo Mobile (Expo Go)

1. Abra o terminal e entre na pasta do aplicativo mobile:
   ```bash
   cd mobile
   ```
2. Instale as dependências (apenas na primeira vez):
   ```bash
   npm install
   ```
3. Inicie o Expo:
   ```bash
   npx expo start
   ```
4. Vai aparecer um **QR Code** no terminal ou no navegador.
5. No seu celular Android ou iOS:
   - Instale o app **Expo Go** pela Google Play Store ou App Store.
   - Abra o Expo Go e escaneie o QR Code que apareceu na tela do computador.
6. **Importante para conectar com o PC**:
   - O celular e o computador devem estar conectados na **mesma rede Wi-Fi**.
   - Na tela de login do app no celular, você pode tocar no botão **"⚙ Configurar IP do PC"** e conferir o IP da sua máquina (ex: `http://10.154.20.95:5000` ou `http://192.168.0.x:5000`).

---

## 🔑 4. Usuários Padrão para Teste

Ao iniciar o banco, dois usuários já vêm cadastrados com senha criptografada em **Bcrypt**:

| Usuário | Senha | Função |
|---|---|---|
| `admin` | `1234` | Administrador |
| `user` | `1234` | Usuário padrão |

*(Você também pode cadastrar novos usuários pela tela de cadastro da Web ou pelo próprio App Mobile!)*

---

## 📡 5. Tabela de Rotas da API REST (Documentação)

Todas as rotas aceitam e respondem dados em formato **JSON**:

| Método | Rota | O que faz? |
|---|---|---|
| `POST` | `/api/cadastro` | Cadastra novo usuário com senha criptografada via Bcrypt |
| `POST` | `/api/login` | Valida o usuário e a senha comparando o hash Bcrypt |
| `GET` | `/api/produtos` | Retorna a lista de todos os produtos do estoque |
| `POST` | `/api/produtos` | Cadastra um novo produto no estoque |
| `PUT` | `/api/produtos/<id>` | Atualiza as informações de um produto existente |
| `DELETE` | `/api/produtos/<id>` | Exclui um produto do estoque e grava a saída no histórico |
| `POST` | `/api/movimentacao` | Dá entrada ou saída de quantidade de um produto específico |
| `GET` | `/api/historico` | Retorna o histórico de todas as movimentações feitas |

---

## 📂 6. Estrutura dos Arquivos do Projeto

```text
Rayan-gay/
├── app.py                 # Servidor Flask com as rotas Web e rotas da API REST
├── banco.sql              # Script SQL com a criação de tabelas e dados iniciais
├── conexao.py             # Script de teste de conexão com o MySQL
├── criar_banco.py         # Script Python auxiliar para criar o banco de dados
├── Dockerfile             # Receita para construir a imagem da aplicação Flask
├── docker-compose.yml     # Orquestrador dos containers (Flask + MySQL)
├── requirements.txt       # Lista de dependências Python (Flask, bcrypt, mysql-connector)
├── static/                # Arquivos de estilo (CSS), imagens e scripts (JS)
├── templates/             # Páginas HTML (login, cadastro, menu, estoque, histórico)
└── mobile/                # Pasta do Aplicativo Mobile
    ├── App.js             # Código completo do app React Native para o Expo Go
    ├── package.json       # Dependências do Expo / React Native
    └── app.json           # Configurações do app no Expo
```
