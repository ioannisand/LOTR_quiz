import requests
from dotenv import load_dotenv
import os
import json
import random

load_dotenv()

number_of_questions = 10

# Setting api headers and url
URL = "https://the-one-api.dev/v2/quote"
api_key = "Bearer " + os.getenv("apikey")
headers = {
    "Authorization": api_key
}

# making request
response = requests.get(URL, headers=headers)
data = json.loads(response.text)

#class that takes  a random quote from the total quotes and stores the dialog and character name
class RandomQuote():
    def __init__(self):
        self.quote = random.choice(data["docs"])
        self.quote_text = self.quote["dialog"]
        self.character_id = self.quote["character"]
        self.character_name = self.get_character_name()

    def get_character_name(self):
        character_response = requests.get(url=f"https://the-one-api.dev/v2/character/{self.character_id}", headers=headers)
        char_data = json.loads(character_response.text)
        return char_data['docs'][0]["name"]



def generate_quotedict():
    quotes = {}
    for i in range(number_of_questions):
        new_quote = RandomQuote()
        quotes[new_quote.quote_text] = new_quote.character_name
    return quotes


characters_response = requests.get("https://the-one-api.dev/v2/character", headers=headers)
chars_data = json.loads(characters_response.text)["docs"]
characters_list = [character["name"] for character in chars_data]

