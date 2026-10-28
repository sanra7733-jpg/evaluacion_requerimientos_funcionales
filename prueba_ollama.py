import requests

respuesta = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2:1b",
        "prompt": "Explica en dos frases qué es un requerimiento funcional.",
        "stream": False,
    },
)
print(respuesta.json()["response"])