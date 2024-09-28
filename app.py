from flask import Flask, jsonify
from flask import request
import json
import random
from functools import cache

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
        print(content)
        print(guess)
        print(characters)
        print(wrong_positions)
    

                
                
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
    return jsonify(results, status=200, mimetype='application/json')

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


@app.route('/bugfixer/p1', methods=['POST'])
def bugfixer():
    data = request.json
    result = []
    for x in data:
        time_dict = dict()
        preq_dict = dict()
        for i in range(len(x.get("time"))):
            time_dict[i+1] =  x.get("time")[i]
            preq_dict[i+1] = []
        for y in x.get("prerequisites"):
            preq_dict[y[1]].append(y[0])
        result.append(min_days_to_finish_project(time_dict,preq_dict))
    return jsonify(result, status=200, mimetype='application/json')

        




def min_days_to_finish_project(cost, prerequisite):
    @cache
    def min_days_to_finish_task(t):
        return cost[t] + max((min_days_to_finish_task(p) for p in prerequisite[t]),default=0)

    return max(min_days_to_finish_task(t) for t in cost)

# Example
c = {1: 5, 2: 8, 3: 13}  # tasks are [1, 2, 3]
pre = {1: [], 2: [], 3: [1, 2]}
print(min_days_to_finish_project(c, pre))  # 21

if __name__ == "__main__":
    app.run(debug=True)

