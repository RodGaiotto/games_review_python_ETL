#Developed by Rodrigo Gaiotto - 2025, based on Venilton Falvo's code and proposal from DIO

#importing required libs...
import pandas as pd
import json
import csv
import openai

#declaring the OpenAI ChatCompletion API key
#You can generate your key from your OpenAI account from the OpenAI website.
openai_api_key = '*key-here!!*'

#EXTRACTING
#Normalizing CSV data into JSON

df = pd.read_csv('games.csv')
#collection_ids = df['ID'].tolist()
games_collection = df[['ID','Name']]

#Printing for tests purposes
#print(games_collection)
#print(json.dumps(games_collection, indent=2))

#Converting from CSV to JSON
with open('games.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    data = list(csv.DictReader(csvfile))

with open('games.json', mode='w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, indent=4)

#Printing to validate
print(json.dumps(data, indent=4))


#TRANSFORMING using OpenAI ChatCompletion API
#The idea is getting a review from the ChatGTP for each game
#from the list

#Declaring OpenAI variable
openai.api_key = openai_api_key

#Coding the function that will consume from the API
def generate_ai_game_review(game):
  completion = openai.ChatCompletion.create(
    model="gpt-4.1",
    messages=[
      {
          "role": "system",
          "content": "You are specialist in games reviews"
      },
      {
          "role": "user",
          "content": f"Share a brief review about the game {game['Name']} including its release date (max 100 characters)"
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')


for game in data:
  review = generate_ai_game_review(game)
  print(review)
  game['review'].append({
      "description": review
  })
