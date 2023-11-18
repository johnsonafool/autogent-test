import openai
from bs4 import BeautifulSoup
import requests

import json


def test_gpt_api_health():
    # client = OpenAI(
    #     api_key,
    # )

    chat_completion = openai.ChatCompletion.create(
        messages=[
            {
                "role": "user",
                "content": "who is the director of MIT Media Lab City Science Group, also provide your reference source and when]",
            }
        ],
        # model="gpt-4-0613",
        model="gpt-3.5-turbo-16k-0613",
    )

    print(chat_completion.choices[0].message.content)


# Define research function
def search_serper(query: str):
    url = "https://google.serper.dev/search"

    payload = json.dumps({"q": query})
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def scrape_browserless(url: str):
    """Scrape a website and summarize its content if it's too large."""
    print("Scraping website...")

    # Define the headers for the request
    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
    }

    # Build the POST URL
    post_url = f"https://chrome.browserless.io/content?token={BROWSERLESS_API_KEY}"

    # Send the POST request
    response = requests.post(post_url, headers=headers, json={"url": url})

    # Check the response status code
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        print("CONTENTTTTTT:", text)

        if len(text) > 8000:
            # output = summary(text)
            print('over 8000')
            output = text
            return output
        else:
            return text
    else:
        print(f"HTTP request failed with status code {response.status_code}")


if __name__ == "__main__":
    from dotenv import load_dotenv

    import os

    # Load environment variables
    load_dotenv()

    openai.api_key = os.getenv("OPENAI_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    BROWSERLESS_API_KEY = os.getenv("BROWSERLESS_API_KEY")

    #
    test_gpt_api_health()
    # print(search_serper("what is Say my name this quote from"))
    # scrape_browserless("https://react.dev/")
