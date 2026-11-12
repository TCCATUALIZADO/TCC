# ========================================================
# DOCKERFILE - CONSTRUÇÃO DA IMAGEM FLASK DO ESTOQUE
# ========================================================

# 1. Usa a imagem oficial do Python 3.11 versão slim (leve e estável)
FROM python:3.11-slim

# 2. Define a pasta de trabalho interna do container
WORKDIR /app

# 3. Copia o requirements.txt para o container
COPY requirements.txt .

# 4. Instala as dependências necessárias (Flask, mysql-connector, bcrypt)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todos os arquivos do projeto para o container
COPY . .

# 6. Informa que a aplicação escuta na porta 5000
EXPOSE 5000

# 7. Comando padrão executado quando o container é iniciado
CMD ["python", "app.py"]
