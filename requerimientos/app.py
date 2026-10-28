import ollama

requerimiento = input("Requerimiento Funcional: ")

response = ollama.systemone(
    model="d1-omni:600m",
    state=requerimiento,
    questions={
        "condicion": {
            "type": "noul",
            "instructions": "¿Incluye una situación que detona el evento?",
            "criteria": {
                "true": "Especifica claramente el evento o situación detonante",
                "false": "No menciona qué situación dispara la acción"
            }
        },
        "sujeto": {
            "type": "noul",
            "instructions": "¿Incluye el sujeto o módulo que realiza la acción?",
            "criteria": {
                "true": "Especifica claramente quién realiza la acción",
                "false": "No menciona quién realiza la acción"
            }
        },
        "verbo": {
            "type": "noul",
            "instructions": "¿Incluye el verbo normativo «debe»?",
            "criteria": {
                "true": "Incluye el verbo «debe»",
                "false": "No incluye el verbo «debe»"
            }
        },
        "accion": {
            "type": "noul",
            "instructions": "¿Incluye una sola acción técnica?",
            "criteria": {
                "true": "Especifica una acción técnica clara, por ejemplo validar, registrar o mostrar",
                "false": "No menciona la acción, o mezcla más de una acción en el mismo requerimiento"
            }
        },
        "objeto": {
            "type": "noul",
            "instructions": "¿Incluye el objeto o entidad sobre el que se realiza la acción?",
            "criteria": {
                "true": "Especifica claramente el objeto o entidad, por ejemplo una tabla, una dependencia o un elemento de la pantalla",
                "false": "No menciona sobre qué objeto o entidad se realiza la acción"
            }
        },
        "criterio": {
            "type": "noul",
            "instructions": "¿Incluye un criterio verificable o una restricción?",
            "criteria": {
                "true": "Indica cómo se comprueba que la acción se cumplió, con un resultado medible o una restricción",
                "false": "No indica cómo comprobarlo, o usa palabras ambiguas como rápido o eficiente"
            }
        }
    }
)

UMBRAL = 0.05
partes = ["condicion", "sujeto", "verbo", "accion", "objeto", "criterio"]
cumple_todo = True

for numero, parte in enumerate(partes, start=1):
    valor = response.answers[parte].noul
    if valor >= UMBRAL:
        print(f"{numero}. Cumple con {parte}: {valor}")
    else:
        print(f"{numero}. NO cumple con {parte}: {valor}")
        cumple_todo = False

if cumple_todo:
    print("El requerimiento cumple con la fórmula.")
else:
    print("El requerimiento NO cumple con la fórmula.")