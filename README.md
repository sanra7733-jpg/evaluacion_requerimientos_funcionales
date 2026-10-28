# evaluacion_requerimientos_funcionales
Inferencias  a LLMs SDD, edge gallery + Ollama gemma 

# Evaluación de requerimientos funcionales

## Guía de instalación (Ollama + Python)

Esta guía deja listo el entorno para usar un modelo de lenguaje local con Ollama desde Python. Está pensada para **GitHub Codespaces** (Linux). Al final hay una nota para Windows.

## Requisitos

- Un Codespace de este repositorio, o una computadora con Linux o Windows.
- Python 3 y el entorno virtual `.venv` del proyecto.
- Unos 2 GB libres de disco para el modelo.

## Instalación paso a paso

### 1. Abrir una terminal

En Codespaces: menú **Terminal → Nueva terminal**.

### 2. Activar el entorno virtual

Debe aparecer `(.venv)` al inicio de la línea de la terminal. Si no aparece:

```bash
source .venv/bin/activate
```

### 3. Instalar las librerías de Python

```bash
pip install -r requirements.txt
pip install requests
```

### 4. Instalar Ollama (solo la primera vez)

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Si marca un error que menciona `zstd`:

```bash
sudo apt-get update && sudo apt-get install -y zstd
```

y vuelve a ejecutar el comando anterior.

### 5. Encender el servidor de Ollama

```bash
ollama serve > ollama.log 2>&1 &
```

Espera unos 5 segundos. Este paso se repite cada vez que el Codespace se apaga y se vuelve a abrir.

### 6. Descargar el modelo

```bash
ollama pull llama3.2:1b
```

Es un modelo pequeño (1.3 GB), elegido para que funcione en Codespaces, que no tiene tarjeta gráfica.

### 7. Comprobar que todo funciona

```bash
ollama --version
ollama list
python prueba_ollama.py
```

Si el script imprime una respuesta, la instalación quedó completa.

### 8. Evitar subir el registro de Ollama a GitHub

```bash
echo "ollama.log" >> .gitignore
```

## Script de arranque rápido

Crea un archivo `iniciar_ollama.sh` con este contenido:

```bash
#!/usr/bin/env bash
# Enciende Ollama en Codespaces y descarga el modelo si falta
if ! curl -s http://localhost:11434 > /dev/null; then
    echo "Encendiendo Ollama..."
    ollama serve > ollama.log 2>&1 &
    sleep 5
fi
ollama list | grep -q "llama3.2:1b" || ollama pull llama3.2:1b
echo "Listo: Ollama está corriendo."
```

Y ejecútalo cada vez que abras el Codespace:

```bash
bash iniciar_ollama.sh
```

## Archivo de prueba

`prueba_ollama.py` comprueba que Python se comunica con Ollama:

```python
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
```

Ejecútalo con `python prueba_ollama.py`.

## Errores comunes

- **`Connection refused`:** Ollama está apagado. Ejecuta `bash iniciar_ollama.sh`.
- **`ModuleNotFoundError: No module named 'requests'`:** ejecuta `pip install requests` con el entorno `(.venv)` activo.
- **`model 'llama3.2:1b' not found`:** ejecuta `ollama pull llama3.2:1b`.
- **`ollama: command not found`:** repite el paso 4.
- **`irm` o `iex` no se reconocen:** son comandos de PowerShell (Windows). En Codespaces se usa el comando `curl` del paso 4.

## Si se trabaja en Windows

Los pasos 4 y 5 cambian. En una terminal de **PowerShell**:

```powershell
irm https://ollama.com/install.ps1 | iex
```

Cierra PowerShell, abre uno nuevo y sigue con el paso 6.

## Nota sobre el modelo

`llama3.2:1b` es un modelo muy pequeño y puede dar respuestas incorrectas. Sus resultados deben revisarse siempre antes de darse por válidos.

```powershell
ollama run llama3.2
```

```powershell
ollama run d1-omni
```




##INSTALACION DE OLLAMA EN PYTHON ##
Ese error no es del modelo. Dice `No module named 'ollama'`, así que falta la **librería de Python** `ollama`. Son dos cosas distintas:

- **El modelo** (`llama3.2:1b`) ya lo descargaste con el programa Ollama y está en tu computadora.
- **La librería** `ollama` es el paquete que deja a Python hablar con ese programa, y se instala con `pip`.

## Paso a paso

**1. Instalar la librería.** En tu terminal, con `(.venv)` activo:
```bash
pip install ollama
```
Para comprobar que quedó instalada:
```bash
pip show ollama
```

**2. Revisar que el servidor de Ollama esté encendido:**
```bash
ollama list
```
Si marca un error de conexión, enciéndelo y espera 5 segundos:
```bash
ollama serve > ollama.log 2>&1 &
```

**3. Corregir el nombre del modelo.** En tu `app.py` pusiste `'llama3.2'`, pero el que tienes descargado es `llama3.2:1b`. Para Ollama son modelos distintos: `llama3.2` a secas es una versión más grande (unos 2 GB) que no has bajado. Cambia la línea 4:
```python
from ollama import chat

response = chat(
    model='llama3.2:1b',
    messages=[{'role': 'user', 'content': 'Hello!'}],
)
print(response.message.content)
```

**4. Ejecutarlo.** Guarda con Ctrl + S y corre:
```bash
python app.py
```
Como estás dentro de la carpeta `pruebas`, también puedes usar `python3 app.py`, que es lo que hiciste, pero con el entorno `(.venv)` activo ambos funcionan.

## Si prefieres usar `llama3.2` sin el `:1b`
Entonces descárgalo primero, aunque pesa más y en Codespaces puede ir lento:
```bash
ollama pull llama3.2
```
Para pruebas, el de `:1b` es suficiente.

## Para que tu equipo lo tenga también
Agrega la librería a `requirements.txt`, así quien instale el proyecto la recibe automáticamente. Desde la carpeta principal del repositorio:
```bash
echo "ollama" >> requirements.txt
```
Antes de hacerlo, abre el archivo y comprueba que no tenga ya una línea `ollama`.

## Si vuelve a fallar
- **`Connection refused` o `ConnectError`:** Ollama está apagado. Repite el paso 2.
- **`model 'llama3.2' not found`:** el nombre del modelo no coincide con `ollama list`. Repite el paso 3.
- **Sigue diciendo `No module named 'ollama'`:** pip instaló en otro Python. Usa `python -m pip install ollama` y ejecuta con `python app.py`.

Cuando te imprima la respuesta al «Hello!», ya tienes Python conectado con el modelo. ¿Qué dice el README modificado (aparece con una **M** en tu explorador)? Con eso veo qué sigue en tu parte.