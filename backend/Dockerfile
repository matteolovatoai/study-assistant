# Usiamo una base ufficiale leggera di Python 3.12
# "slim" è perfetto per risparmiare spazio sul Raspberry Pi
FROM python:3.12-slim

# Impostiamo la directory di lavoro dentro il container
WORKDIR /app

# Installiamo 'uv' tramite pip nativo per rispettare le nostre regole di velocità
RUN pip install --no-cache-dir uv

# Copiamo PRIMA solo il file delle dipendenze. 
# Questo è un trucco per sfruttare la cache di Docker: 
# se non cambiamo i requirements, Docker non reinstallerà tutto ogni volta!
COPY requirements.txt .

# Installiamo le dipendenze a livello di sistema nel container usando uv
RUN uv pip install --system -r requirements.txt

# Copiamo il resto del codice sorgente
COPY . .

# Esponiamo la porta usata da FastAPI
EXPOSE 8000

# Comando per avviare il server in produzione
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
