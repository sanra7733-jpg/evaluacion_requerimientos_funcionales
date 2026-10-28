import ollama 
requerimiento = "El usuario ingresa a su email, y el sistema autentica los datos"

response = ollama.systemone(
    model='d1-omni:600m',
    state = requerimiento,
    questions = {
        "condicion":{
            "type":"noul",
            "instructions":'¿Incluye una situación que detone el evento?',
            "criteria": {
                "true": "Especifica claramente el evento o situación detonante",
                "false": "No menciona qué situaión dispara la acción"
            }
        }
    }

)
condicion = response.answers['condicion'].noul

if condicion >=0.05:
    print(f"1.Cumple con la condición : {condicion}")
else:
    print(f"1.NO Cumple con la condición: {condicion}")