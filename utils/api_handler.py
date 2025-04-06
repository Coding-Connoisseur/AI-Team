from openai import OpenAI

def load_api_key():
    with open("/home/obsidian/Github/AI-Team/openai.key") as f:
        return f.read().strip()

client = OpenAI(api_key=load_api_key())

async def chatgpt_call(messages, model="gpt-4"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
    )
    return response.choices[0].message.content
