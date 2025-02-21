# ChatBot de Telegram con OpenAI

Este es un chatbot de Telegram que utiliza la API de OpenAI para generar respuestas inteligentes a los mensajes de los usuarios. Está desarrollado en Python usando FastAPI.
EL API KEY ES UN EJEMPLO, YA NO FUNCIONA
## Características

- Responde preguntas utilizando la inteligencia artificial de OpenAI.
- Integración con la API de Telegram para recibir y enviar mensajes.

## Tecnologías utilizadas

- **Python**
- **Telegram Bot API**
- **OpenAI API**

## Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python 3.8 o superior
- Un bot de Telegram creado en [BotFather](https://t.me/BotFather)
- Una clave de API de OpenAI obtenida desde [OpenAI](https://platform.openai.com/)

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/OscarJunior007/chatbot-telegram.git
   cd chatbot-telegram
   ```
2. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración

Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables:

```env
TELEGRAM_BOT_TOKEN=tu_token_de_telegram
OPENAI_API_KEY=tu_clave_de_openai
```

## Uso

En Telegram, busca tu bot y comienza a interactuar con él.

## Estructura del proyecto
```
chatbot-telegram/
│── main.py
│── requirements.txt
│── .env (archivo de configuración)
│── README.md
└── venv/ (entorno virtual)
```



