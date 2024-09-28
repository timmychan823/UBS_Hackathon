from flask import Flask
import json

app = Flask(__name__)

@app.route("/")
def helloworld():
    return 'Hello World'

@app.route("/wordle-game")
def wordle_game():
    value = {
        "language": language,
        "company": company,
        "Itemid": Itemid,
        "price": price
    }

    return json.dumps(value)

if __name__ == "__main__":
    app.run()

