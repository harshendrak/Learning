from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()

client = OpenAI()


def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"  
    response = requests.get(url)  
    if response.status_code == 200:
        return f"The weather in {city} is: {response.text}"
    return "Something went wrong"


def main():
    user_query = input("Ask a question about the weather: ")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_query}
        ]
    )
    print(response.choices[0].message.content)


