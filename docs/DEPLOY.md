# Deploy Rápido - Heroku

## Pré-requisitos
- Conta no Heroku
- Heroku CLI instalado

## Passos

### 1. Login no Heroku
```bash
heroku login
```

### 2. Criar App
```bash
heroku create calculadora-trabalhista
```

### 3. Configurar Variáveis de Ambiente
```bash
heroku config:set CLIENT_ID=seu_client_id
heroku config:set CLIENT_SECRET=seu_client_secret
heroku config:set TENANT_ID=seu_tenant_id
heroku config:set WORKBOOK_ID=seu_workbook_id
heroku config:set DRIVE_ID=seu_drive_id
```

### 4. Deploy
```bash
git push heroku main
```

### 5. Abrir App
```bash
heroku open
```

## Procfile
Criar arquivo `Procfile` na raiz:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## runtime.txt
Criar arquivo `runtime.txt` na raiz:
```
python-3.11.0
```

## Logs
```bash
heroku logs --tail
```

## Escalar
```bash
heroku ps:scale web=1
```

---

# Deploy Alternativo - Vercel

## Não recomendado para este projeto
Vercel é otimizado para frontend. Para backend Python com FastAPI, prefira:
- **Render.com**
- **Railway.app**
- **Fly.io**
- **AWS EC2**
- **Azure App Service**

---

# Deploy Recomendado - Render.com

## Passos

### 1. Criar conta em render.com

### 2. New Web Service

### 3. Conectar repositório GitHub

### 4. Configurações:
- **Name:** calculadora-trabalhista
- **Environment:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 5. Environment Variables:
Adicionar todas as variáveis do .env

### 6. Deploy!

URL será algo como: `https://calculadora-trabalhista.onrender.com`
