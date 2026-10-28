import ollama
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

MODELO = "d1-omni:latest"
UMBRAL = 0.05
PARTES = ["condicion", "sujeto", "verbo", "accion", "objeto", "criterio"]

PREGUNTAS = {
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


def evaluar(requerimiento):
    response = ollama.systemone(
        model=MODELO,
        state=requerimiento,
        questions=PREGUNTAS
    )

    resultados = []
    cumple_todo = True

    for numero, parte in enumerate(PARTES, start=1):
        valor = response.answers[parte].noul
        cumple = valor >= UMBRAL
        if not cumple:
            cumple_todo = False
        resultados.append({
            "numero": numero,
            "parte": parte,
            "valor": valor,
            "cumple": cumple
        })

    return {"resultados": resultados, "cumple_todo": cumple_todo}


@app.route("/")
def inicio():
    return send_file("index.html")


@app.route("/evaluar", methods=["POST"])
def ruta_evaluar():
    datos = request.get_json(silent=True) or {}
    requerimiento = datos.get("requerimiento", "").strip()

    if not requerimiento:
        return jsonify({"error": "Escribe un requerimiento."}), 400

    try:
        return jsonify(evaluar(requerimiento))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)