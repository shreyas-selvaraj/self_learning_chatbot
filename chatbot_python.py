import wolframalpha
import wikipedia
from googlesearch import search
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging 
import asyncio
import requests
import json

logger = logging.getLogger() 
logger.setLevel(logging.CRITICAL)



client = wolframalpha.Client("6WE9ET-7KQRKPRAQH")

bot = ChatBot(
    'Shrey bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
    ],
    database_uri='sqlite:///database.sqlite3'
)

trainer = ListTrainer(bot)
trainer_corpus = ChatterBotCorpusTrainer(bot)

# trainer_corpus.train(
#     "chatterbot.corpus.english.greetings",
#     "chatterbot.corpus.english.conversations"
# )

# trainer.train([
#     "Hi there!",
#     "Hello",
# ])

# trainer.train([
#     "Greetings!",
#     "Hello",
# ])

# trainer.train([
#     "Hey",
#     "Hello",
# ])

# trainer.train([
#     "Hi, can I help you?",
#     "Sure, I'd like to book a flight to Iceland.",
#     "Your flight has been booked."
# ])

# trainer.train([
#     "How are you?",
#     "I am good.",
#     "That is good to hear.",
#     "Thank you",
#     "You are welcome.",
# ])

async def train_model(argument, my_str):
    trainer.train([
            f"{argument}",
            f"{my_str}", 
        ])
    return 1

async def parse_input():
    print(">> ", end = '')
    inp = input().split(":")
    bot_type = inp[0]
    argument = inp[1]
    if(bot_type == "bot"):
        bot_input = bot.get_response(argument)
        print(bot_input)

    if(bot_type == "wiki"):
        try:
            page = wikipedia.page(argument)
            print(page.title)
            print(page.url)
            print(page.content)
        except Exception as e:
            print(e)
            pass
            
    if(bot_type == "wolfram"):
        try:
            res = client.query(argument)
            answer = next(res.results).text 
            my_str = answer
            print(answer)
            wait = train_model(argument, my_str)
            await (wait)
        except Exception as e:
                print("Exception Thrown", end = '')
                print(e)
                pass

    if(bot_type == "google"):
        search_result_list = list(search(argument, num=10, stop=10, pause=1))
        for item in search_result_list:
            print(item)

    if(bot_type == "medical"):
        try:
            temp_argument = argument
            argument = argument.split(" ")[len(argument.split(' ')) - 1]
            r = requests.get(url = f"https://www.dictionaryapi.com/api/v3/references/medical/json/{argument}?key=c8cec991-9081-4077-b973-752fe75707fb") 
            data = json.loads(r.text)
            data = data[0]['shortdef']
            print(data[0])
            wait = train_model(temp_argument, data[0])
            await (wait)

        except Exception as e:
                print("Exception Thrown", end = '')
                print(e)
                pass

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(parse_input())
        except:
            print("Async failed")

