async function evaluacion() {
    const salida = document.getElementById("resultado");
    const requerimiento = document.getElementById("requerimiento").value.trim();

    if (!requerimiento) {
        salida.textContent = "Escribe un requerimiento.";
        return;
    }

    salida.textContent = "Evaluando...";

    try {
        const response = await fetch("/evaluar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ requerimiento: requerimiento })
        });

        const datos = await response.json();

        if (!response.ok) {
            salida.textContent = "Error: " + datos.error;
            return;
        }

        console.log("Conexión exitosa: ", datos);

        let html = "<ul>";
        datos.resultados.forEach(r => {
            const texto = r.cumple ? "Cumple con" : "NO cumple con";
            html += `<li>${r.numero}. ${texto} ${r.parte}: ${r.valor}</li>`;
        });
        html += "</ul>";
        html += datos.cumple_todo
            ? "<p><b>El requerimiento cumple con la fórmula.</b></p>"
            : "<p><b>El requerimiento NO cumple con la fórmula.</b></p>";

        salida.innerHTML = html;

    } catch (error) {
        salida.textContent = "Ups algo falló: " + error.message;
        console.log("Ups algo falló ", error.message);
    }
}