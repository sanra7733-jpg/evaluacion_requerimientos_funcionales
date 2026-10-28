from ollama import chat

response = chat(
    model='llama3.2',
    messages=[
        {
            'role': 'user', 
            'content': 'HOLA!, Soy tu asistente personal. En que puedo ayudarte.'
            }
    ],
    stream=True,

)
print(response.message.content)