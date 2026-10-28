import json
import ollama

MODELO = "llama3.2:1b"

questions = {
    "condicion": {
        "instructions": "¿Incluye una situación que detona el evento?",
        "true": "Especifica claramente el evento o situación detonante",
        "false": "No menciona qué situación dispara la acción",
    },
    "sujeto": {
        "instructions": "¿Incluye el sujeto o módulo que realiza la acción?",
        "true": "Especifica claramente quién realiza la acción",
        "false": "No menciona quién realiza la acción",
    },
    "verbo": {
        "instructions": "¿Incluye el verbo normativo «debe»?",
        "true": "Incluye el verbo «debe»",
        "false": "No incluye el verbo «debe»",
    },
    "accion": {
        "instructions": "¿Incluye una sola acción técnica?",
        "true": "Especifica una acción técnica clara, por ejemplo validar, registrar o mostrar",
        "false": "No menciona la acción, o mezcla más de una acción en el mismo requerimiento",
    },
    "objeto": {
        "instructions": "¿Incluye el objeto o entidad sobre el que se realiza la acción?",
        "true": "Especifica claramente el objeto o entidad, por ejemplo una tabla, una dependencia o un elemento de la pantalla",
        "false": "No menciona sobre qué objeto o entidad se realiza la acción",
    },
    "criterio": {
        "instructions": "¿Incluye un criterio verificable o una restricción?",
        "true": "Indica cómo se comprueba que la acción se cumplió, con un resultado medible o una restricción",
        "false": "No indica cómo comprobarlo, o usa palabras ambiguas como rápido o eficiente",
    },
}

esquema = {
    "type": "object",
    "properties": {
        "cumple": {"type": "boolean"},
        "motivo": {"type": "string"},
    },
    "required": ["cumple", "motivo"],
}

requerimiento = input("Requerimiento Funcional: ")
cumple_todo = True

for numero, (parte, datos) in enumerate(questions.items(), start=1):
    prompt = (
        f"Requerimiento: {requerimiento}\n\n"
        f"Pregunta: {datos['instructions']}\n"
        f"Responde cumple=true si: {datos['true']}.\n"
        f"Responde cumple=false si: {datos['false']}.\n"
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
    if resultado["cumple"]:
        print(f"{numero}. Cumple con {parte}: {resultado['motivo']}")
    else:
        print(f"{numero}. NO cumple con {parte}: {resultado['motivo']}")
        cumple_todo = False

print("El requerimiento cumple con la fórmula." if cumple_todo else "El requerimiento NO cumple con la fórmula.")