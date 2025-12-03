# Imagem base leve do Python
FROM python:3.12-slim

# Instala dependências do sistema necessárias para compilar pacotes Python e rodar uWSGI
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia lista de dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta do Flask/uWSGI
EXPOSE 5000

# Comando para iniciar a aplicação via uWSGI
CMD ["uwsgi", "--ini", "wsgi.ini"]
