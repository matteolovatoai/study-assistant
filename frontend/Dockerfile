# FASE 1: BUILD (Costruiamo l'app)
# Usiamo Alpine Linux perché è leggerissimo e perfetto per Docker
FROM node:24-alpine AS builder
WORKDIR /app

# Copiamo prima solo i file delle dipendenze (stesso trucco della cache usato nel backend!)
COPY package*.json ./
# Usiamo npm install invece di npm ci per evitare crash dovuti a differenze 
# tra l'architettura del tuo Mac (Node 24) e quella del Raspberry (Alpine/ARM64)
RUN npm install

# Copiamo tutto il codice sorgente
COPY . .

# Compiliamo il progetto Next.js in HTML/CSS/JS ottimizzati
RUN npm run build


# FASE 2: RUNNER (Ambiente di Produzione)
# Ripartiamo da un'immagine pulita, scartando tutto il ciarpame (cache, file non necessari) della fase di build
FROM node:24-alpine AS runner
WORKDIR /app

# Diciamo a Node.js che siamo in produzione (attiva ottimizzazioni interne)
ENV NODE_ENV=production

# Copiamo dalla FASE 1 solo ciò che ci serve per far girare l'app
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next

# Esponiamo la porta del frontend
EXPOSE 3000

# Comando di avvio standard per Next.js in produzione
CMD ["npm", "start"]
