# Chitti Chatbot

A browser-based AI chatbot built with Python, Streamlit, and Google's Gemini API. It is configured for deployment on Render.

## Features

- Chat-style web interface
- Gemini-powered responses
- Multi-turn conversation context during the active Streamlit session
- Clear conversation control
- API key read from a server-side environment variable

## Deploy on Render

This repository is configured to run as a Python web service.

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT`
- **Runtime:** Python
- **Recommended region:** Singapore (close to India)

After the service is created, open its Render dashboard → **Environment** and add:

```text
GEMINI_API_KEY = your_private_Gemini_API_key
```

Optionally add `GEMINI_MODEL` if you want to select another model available to your Google AI Studio project. The default is `gemini-2.5-flash`.

Never commit an actual API key to this repository. Create or manage a key at https://aistudio.google.com/apikey.

## Run locally (optional)

```bash
pip install -r requirements.txt
```

Set `GEMINI_API_KEY` in your environment, then run:

```bash
streamlit run app.py
```

## Notes

- The conversation is kept in Streamlit session state and is not a permanent chat history.
- Gemini API access, available models, quotas, and pricing depend on your Google account and project.
