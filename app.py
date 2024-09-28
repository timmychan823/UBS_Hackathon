from flask import Flask
import json
import random

app = Flask(__name__)

@app.route("/")
def helloworld():
    return 'Hello World'

@app.route("/wordle-game", methods=["POST"])
def wordle_game():
    content = request.json()
    characters = list("abcdefghijklmnopqrstuvwxyz")
    wrong_positions = []
    correct = [0,0,0,0,0]
    guess = {"guess": "oater"}        
    if len(content[guessHistory])!=0:
        for i in range(len(content['guessHistory'])):
            for j in range(5):
                if content["evaluationHistory"][i][j] == "X":
                    wrong_positions.append(content["guessHistory"][i][j])
                else if content["evaluationHistory"][i][j] == "-":
                    characters.remove(content["guessHistory"][i][j])
                else if content["evaluationHistory"][i][j] == "O":
                    correct[j]=content["guessHistory"][i][j]
        if len(content['guessHistory'])!=5:
            correct = random.choices(characters, 5) 
        else:
            for j in range(5):
                if correct[j]==0:
                    if len(wrong_positions) == 0:
                        correct[j]="".join(random.choices(wrong_positions,1))
                    else:
                        correct[j]="".join(random.choices(characters,1))
        correct = "".join(correct)
        guess={"guess":correct}

                
                
    return json.dumps(guess)

if __name__ == "__main__":
    app.run()

