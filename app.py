from flask import Flask
from flask import request
import json
import random

app = Flask(__name__)

@app.route("/")
def helloworld():
    return 'Hello World'

@app.route("/wordle-game", methods=["POST"])
def wordle_game():
    content = request.json
    characters = list("abcdefghijklmnopqrstuvwxyz")
    wrong_positions = []
    correct = [0,0,0,0,0]
    guess = {"guess": "oater"}        
    if len(content["guessHistory"])!=0:
        for i in range(len(content['guessHistory'])):
            for j in range(5):
                if content["evaluationHistory"][i][j] == "X":
                    wrong_positions.append(content["guessHistory"][i][j])
                elif content["evaluationHistory"][i][j] == "-":
                    try: 
                        characters.remove(content["guessHistory"][i][j])
                    except Exception as e:
                        continue
                elif content["evaluationHistory"][i][j] == "O":
                    correct[j]=content["guessHistory"][i][j]
        if len(content['guessHistory'])!=5:
            correct = random.choices(characters, k=5) 
        else:
            for j in range(5):
                if correct[j]==0:
                    if len(wrong_positions) == 0:
                        correct[j]="".join(random.choices(wrong_positions,k=1))
                    else:
                        correct[j]="".join(random.choices(characters,k=1))
        correct = "".join(correct)
        guess={"guess":correct}

                
                
    return json.dumps(guess)


@app.route('/efficient-hunter-kazuma', methods=['POST'])
def efficient_hunter_kazuma():
    data = request.get_json()
    data = f'{data}'
    print(f'{data}')
    data = data.replace("\'", "\"")
    print(data)
    data=json.loads(f'{data}')
    print(data)
    results = []
    for entry in data:
        print(entry)
        monsters = entry.get('monsters')
        efficiency = calculate_efficiency(monsters,0,0)
        results.append({"efficiency": efficiency})

    print(results)
    return json.dumps(results)


def calculate_efficiency(monsters, gold, stage):
    list=[]
    if stage == 0:
        # Prepare circle
        if len(monsters) == 0 or len(monsters) == 1:
            return gold
        else:
            #go stage 1
            temp=monsters.copy()
            temp.pop(0)

            nextstage1=calculate_efficiency(temp,gold - monsters[0],1)
            list.append(nextstage1)
            #stay stage 0
            temp=monsters.copy()
            temp.pop(0)
            staystage0=calculate_efficiency(temp,gold,0)
            list.append(staystage0)
    elif stage == 1:
        # Attack
        if len(monsters) == 1:
            return gold + monsters[0]
        elif len(monsters) == 0:
            return gold
        else:
            #now attack
            temp = monsters.copy()
            temp.pop(0)
            nowattack = calculate_efficiency(temp, gold + monsters[0], 2)
            list.append(nowattack)
            #later attack
            temp = monsters.copy()
            temp.pop(0)
            laterattack = calculate_efficiency(temp, gold, 1)
            list.append(laterattack)
    elif stage == 2:
        # Rest
        if (len(monsters) == 0) or (len(monsters) == 1):
            return gold
        else:
            temp = monsters.copy()
            temp.pop(0)
            return calculate_efficiency(temp,gold,0)
    else:
        # Add handling for other stages
        pass

    max_gold = max(list)

    return max_gold

if __name__ == "__main__":
    app.run(debug=True)

