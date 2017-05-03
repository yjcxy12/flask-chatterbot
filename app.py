from flask import Flask, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json
from pprint import pprint

with open('corpus.json') as data_file:    
   data = json.load(data_file)

app = Flask(__name__)

zhuzhu_bot = ChatBot(
  "Zhuzhu Bot",
  storage_adapter={
      'import_path': 'chatterbot.storage.MongoDatabaseAdapter',
      'database_name': 'chatterbot-database',
      'database_uri': 'mongodb://178.62.126.50'
  },
  logic_adapters=[
      {
          'import_path': 'chatterbot.logic.BestMatch'
      },
      {
          'import_path': 'chatterbot.logic.LowConfidenceAdapter',
          'threshold': 0.35,
          'default_response': '我这东西可难做了，池翔云好厉害，可惜还是需要更多的时间培养，要耐心哦~'
      }
  ],
  trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

zhuzhu_bot.train("chatterbot.corpus.english")
zhuzhu_bot.train("chatterbot.corpus.chinese")

zhuzhu_bot.set_trainer(ListTrainer)
zhuzhu_bot.train(data)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get/<string:query>")
def get_raw_response(query):
    return str(zhuzhu_bot.get_response(query))


if __name__ == "__main__":
    app.run()
