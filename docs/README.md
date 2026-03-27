# AI_Agent_Basic

Bot de Telegram con IA para el **Curso de Agentes de IA — IEEE CS PUCP**.

---

## Requisitos

- Python 3.10 o superior
- Token de Telegram (ya configurado en `.env.example`)
- API Key de un proveedor LLM (OpenAI, Groq, OpenRouter, etc.)

---

## Inicio rápido

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
```bash
# Copia el template
copy .env.example .env  # Windows
# o
cp .env.example .env    # Linux/Mac

# Edita .env y agrega tu LLM_API_KEY
```

### 3. (Opcional) Personalizar el bot
Edita `config/system_prompt.txt` para cambiar la personalidad. No necesitas tocar código.

### 4. Iniciar el bot
```bash
python main.py
```

Verás algo como:
```
2026-03-17 17:00:00 | INFO     | __main__ — Iniciando AI_Agent_Basic...
2026-03-17 17:00:01 | INFO     | __main__ — Bot listo. Esperando mensajes (Ctrl+C para detener)...
```

---

## Comandos del bot

| Comando | Descripción |
|---|---|
| `/start` | Mensaje de bienvenida |
| `/help` | Lista de comandos disponibles |
| `/reset` | Borra el historial de conversación |
| Cualquier texto | Respuesta del LLM con memoria conversacional |

---

## Cambiar el proveedor LLM

Solo edita tu `.env`:

```ini
# Groq (rápido y gratuito con límites generosos)
LLM_API_KEY=gsk_...
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.1-70b-versatile

# OpenAI
LLM_API_KEY=sk-...
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini

# OpenRouter (acceso a cientos de modelos)
LLM_API_KEY=sk-or-...
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

---

## Estructura del proyecto

```
AI_Agent_Basic/
├── config/
│   ├── system_prompt.txt   ← Edita aquí la personalidad del bot
│   └── settings.py         ← Carga todas las configuraciones
├── src/
│   ├── llm_client.py       ← Cliente LLM (OpenAI-compatible)
│   └── handlers.py         ← Lógica de los comandos de Telegram
├── docs/
│   ├── CLAUDE.md           ← Contexto para asistentes IA
│   └── README.md           ← Este archivo
├── main.py                 ← Punto de entrada
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Seguridad

- [x] El archivo `.env` está en `.gitignore` — nunca se sube al repositorio
- [x] El token de Telegram y keys nunca están en el código fuente
- [!] Nunca compartas tu `.env` ni tu token de Telegram

---

## Próximos pasos — Nivel Intermedio

Ver `../AI_Agent_Intermediate/` para una versión con:
- RAG (busca en documentos propios)
- Tool calling (funciones externas)
- Persistencia de memoria en base de datos
- Webhooks para producción

---

*IEEE Computer Society PUCP — Curso de Agentes de IA*
