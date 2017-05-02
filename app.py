from flask import Flask, render_template
from chatterbot import ChatBot

app = Flask(__name__)

english_bot = ChatBot(
	"English Bot",
  logic_adapters=[
      {
          'import_path': 'chatterbot.logic.BestMatch'
      },
      {
          'import_path': 'chatterbot.logic.LowConfidenceAdapter',
          'threshold': 0.65,
          'default_response': '我这东西可难做了，池翔云好厉害，可惜还是需要更多的时间培养，要耐心哦~'
      }
  ],
  trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

english_bot.train("chatterbot.corpus.english")
english_bot.train("chatterbot.corpus.chinese")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get/<string:query>")
def get_raw_response(query):
    return str(english_bot.get_response(query))


if __name__ == "__main__":
    app.run()
