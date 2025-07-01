import os
import subprocess
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

conversation = [
    {"role": "system", "content": "You are a helpful Termux assistant. Commands beginning with '!' should be executed in the shell."} 
]

while True:
    user_input = input("You: ").strip()

    if user_input.startswith("!"):
        command = user_input[1:]
        result = subprocess.getoutput(command)
        print(result)
        continue

    conversation.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.7,
    )
    message = response["choices"][0]["message"]["content"]
    conversation.append({"role": "assistant", "content": message})
    print(message)
