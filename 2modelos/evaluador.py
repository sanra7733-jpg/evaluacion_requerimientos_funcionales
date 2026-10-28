import json
import sys

import ollama
import requests

# Modelo por defecto. También se puede elegir al ejecutar:
#   python evaluador.py d1-omni:latest
#   python evaluador.py llama3.2:1b
MODELO = sys.argv[1] if len(sys.argv) > 1 else "d1-omni:latest"
UMBRAL = 0.05

questions = {
    "condicion": {
        "type": "noul",
        "instructions": "¿Incluye una situación que detona el evento?",
        "criteria": {
            "true": "Especifica claramente el evento o situación detonante",
            "false": "No menciona qué situación dispara la acción",
        },
    },
    "sujeto": {
        "type": "noul",
        "instructions": "¿Incluye el sujeto o módulo que realiza la acción?",
        "criteria": {
            "true": "Especifica claramente quién realiza la acción",
            "false": "No menciona quién realiza la acción",
        },
    },
    "verbo": {
        "type": "noul",
        "instructions": "¿Incluye el verbo normativo «debe»?",
        "criteria": {
            "true": "Incluye el verbo «debe»",
            "false": "No incluye el verbo «debe»",
        },
    },
    "accion": {
        "type": "noul",
        "instructions": "¿Incluye una sola acción técnica?",
        "criteria": {
            "true": "Especifica una acción técnica clara, por ejemplo validar, registrar o mostrar",
            "false": "No menciona la acción, o mezcla más de una acción en el mismo requerimiento",
        },
    },
    "objeto": {
        "type": "noul",
        "instructions": "¿Incluye el objeto o entidad sobre el que se realiza la acción?",
        "criteria": {
            "true": "Especifica claramente el objeto o entidad, por ejemplo una tabla, una dependencia o un elemento de la pantalla",
            "false": "No menciona sobre qué objeto o entidad se realiza la acción",
        },
    },
    "criterio": {
        "type": "noul",
        "instructions": "¿Incluye un criterio verificable o una restricción?",
        "criteria": {
            "true": "Indica cómo se comprueba que la acción se cumplió, con un resultado medible o una restricción",
            "false": "No indica cómo comprobarlo, o usa palabras ambiguas como rápido o eficiente",
        },
    },
}


def evaluar_con_d1(requerimiento):
    """Modelo de decisión (d1): devuelve la probabilidad de 'true' por cada pregunta."""
    if hasattr(ollama, "systemone"):
        response = ollama.systemone(
            model=MODELO,
            state=requerimiento,
            questions=questions,
        )
        return {parte: response.answers[parte].noul for parte in questions}

    # Si la librería no tiene systemone, se llama directo al servidor de Ollama
    respuesta = requests.post(
        "http://localhost:11434/v1/systemone",
        json={"model": MODELO, "state": requerimiento, "questions": questions},
        timeout=120,
    )
    respuesta.raise_for_status()
    answers = respuesta.json()["answers"]
    return {parte: answers[parte]["noul"] for parte in questions}


def evaluar_con_llama(requerimiento):
    """Modelo de chat (llama): responde cumple sí/no; se convierte a 1.0 o 0.0."""
    esquema = {
        "type": "object",
        "properties": {
            "cumple": {"type": "boolean"},
            "motivo": {"type": "string"},
        },
        "required": ["cumple", "motivo"],
    }
    resultados = {}
    for parte, datos in questions.items():
        prompt = (
            f"Requerimiento: {requerimiento}\n\n"
            f"Pregunta: {datos['instructions']}\n"
            f"Responde cumple=true si: {datos['criteria']['true']}.\n"
            f"Responde cumple=false si: {datos['criteria']['false']}.\n"
            "Da el motivo en una frase corta."
        )
        respuesta = ollama.chat(
            model=MODELO,
            messages=[
                {"role": "system", "content": "Eres un revisor de requerimientos funcionales. Responde solo con JSON."},
                {"role": "user", "content": prompt},
            ],
            format=esquema,
        )
        resultado = json.loads(respuesta.message.content)
        resultados[parte] = 1.0 if resultado["cumple"] else 0.0
    return resultados


requerimiento = input("Requerimiento Funcional: ")
print(f"Modelo: {MODELO}")

if MODELO.startswith("d1"):
    valores = evaluar_con_d1(requerimiento)
else:
    valores = evaluar_con_llama(requerimiento)

cumple_todo = True
for numero, (parte, valor) in enumerate(valores.items(), start=1):
    if valor >= UMBRAL:
        print(f"{numero}. Cumple con {parte}: {valor}")
    else:
        print(f"{numero}. NO cumple con {parte}: {valor}")
        cumple_todo = False

if cumple_todo:
    print("El requerimiento cumple con la fórmula.")
else:
    print("El requerimiento NO cumple con la fórmula.")