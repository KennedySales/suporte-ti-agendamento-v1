
FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de requirements primeiro para aproveitar cache do Docker
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta (opcional, caso queira adicionar uma API futuramente)
EXPOSE 8000

# Comando para executar a aplicação
CMD ["python", "app.py"]
