async function evaluacion() {
    try {
        const uri = "http://127.0.0.1:11434/v1/systemone";
        const requerimiento = "El usuario ingresa su email y contraseña y el sistema autentica los datos.";
        
        const data = {
            model: "d1-omni:600m",
            state: requerimiento,
            questions: {
                "condicion": {
                    "type": "noul",
                    "instructions": "¿Incluye una situación que detona el evento?",
                    "criteria": {
                        "true": "Especifica claramente el evento o situación detonante",
                        "false": "No menciona qué situación dispara la acción"
                    }
                }
            }
        };

        const response = await fetch(
            uri,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        );

        const resultado = await response.json();
        console.log("Conexión con la API exitosa: ", resultado);
        console.log("Criterio: ", resultado.answers.criterio.noul);

    } catch (error) {
        console.log("Ups algo fallo ", error.message);
    }
}