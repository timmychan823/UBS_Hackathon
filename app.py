from flask import Flask, jsonify
from flask import request
import json
import random
from functools import cache
import pandas as pd 

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
    # if len(content["guessHistory"])!=0:
    #     for i in range(len(content['guessHistory'])):
    #         for j in range(5):
    #             if content["evaluationHistory"][i][j] == "X":
    #                 wrong_positions.append(content["guessHistory"][i][j])
    #             elif content["evaluationHistory"][i][j] == "-":
    #                 try: 
    #                     characters.remove(content["guessHistory"][i][j])
    #                 except Exception as e:
    #                     continue
    #             elif content["evaluationHistory"][i][j] == "O":
    #                 correct[j]=content["guessHistory"][i][j]
    #     if len(content['guessHistory'])!=5:
    #         correct = random.choices(characters, k=5) 
    #     else:
    #         for j in range(5):
    #             if correct[j]==0:
    #                 if len(wrong_positions) == 0:
    #                     correct[j]="".join(random.choices(wrong_positions,k=1))
    #                 else:
    #                     correct[j]="".join(random.choices(characters,k=1))
        
    #     correct = "".join(correct)
    #     guess={"guess":correct}
    #     print(content)
    #     print(guess)
    #     print(characters)
    #     print(wrong_positions)
    guess = {"guess":"choir"}
    print(content)

                
                
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


@app.route('/dodge', methods =['POST'])
def dodge():
    print(request)
    data = request.json
    result = {"instructions": None}
    print(data)
    return jsonify(result)
    

@app.route('/bugfixer/p1', methods=['POST'])
def bugfixer():
    data = request.json
    result = []
    for x in data:
        print(x.get("time"))
        time_dict = dict()
        preq_dict = dict()
        for i in range(len(x.get("time"))):
            time_dict[i+1] =  x.get("time")[i]
            preq_dict[i+1] = []
        for y in x.get("prerequisites"):
            preq_dict[y[1]].append(y[0])
        result.append(min_days_to_finish_project(time_dict,preq_dict))
    return jsonify(result)

@app.route('/mailtime', methods=['POST'])
def mailitme():
    data = request.json
    result = {}
    userTimeZoneMapping = {}
    emailHashMap = {}
    userTimeSpent={}
    for x in data.get("users"):
        userTimeZoneMapping[x["name"]] = x["officeHours"]["timeZone"]
    emails = data.get("emails")
    for x in emails:
        x["timeSent"] = pd.Timestamp(x["timeSent"], tz=userTimeZoneMapping[x["sender"]])
        x["subject"]  = x["subject"].split("RE: ")[-1]
        if x["subject"] not in emailHashMap:
            emailHashMap[x["subject"]]=[x]
        else:
            emailHashMap[x["subject"]].append(x)
    for email in emailHashMap:
        emailHashMap[email].sort(key = lambda y: y["timeSent"])
        for i in range(len(emailHashMap[email])-1):
            temp=pd.Timedelta(emailHashMap[email][i+1]['timeSent']-emailHashMap[email][i]['timeSent'])
            if emailHashMap[email][i+1]['sender'] not in userTimeSpent:
                userTimeSpent[emailHashMap[email][i+1]['sender']] = [temp.days*60*60*24+temp.seconds]
            else:
                userTimeSpent[emailHashMap[email][i+1]['sender']].append(temp.days*60*60*24+temp.seconds)
    for user in userTimeSpent:
        userTimeSpent[user] = round(sum(userTimeSpent[user])/len(userTimeSpent[user]))

    return jsonify({"response":userTimeSpent})
        
        
    
@app.route('/coolcodehack', methods=['POST'])
def coolcodehack():
    print(request)
    result =  {
        "username": "timmychan823",
        "password": "Hkma#00001"
    }       
    return jsonify(result)

@app.route('/ub5-flags', methods=[])
def ub5_flags():
    data = result
    print(data)
    result = {"sanityScroll": {
        "flag": "UB5{FLAG_CONTENT_HERE}"
        }
    }
    return json(result)
    

@app.route('/bugfixer/p2', methods=['GET']) 
def bugfixer2():
    data = result.json
    result = []
    for x in data:
        intervals=x.get("bugseq")
        intervals.sort(key = lambda y: y[0])
        prevInterval =  intervals[0]
        minOverlaps = 0
        for i in range(1, len(intervals)):
            currInterval = intervals[i]
            if currInterval[0] <prevInterval[1]:
                minOverlaps+=1
                prevInterval = prevInterval if prevInterval[1] < currInterval[1] else currInterval
            else:
                prevInterval = currInterval
        result.append(minOverlaps)
    return jsonify(result)



def min_days_to_finish_project(cost, prerequisite):
    @cache
    def min_days_to_finish_task(t):
        return cost[t] + max((min_days_to_finish_task(p) for p in prerequisite[t]),default=0)

    return max(min_days_to_finish_task(t) for t in cost)

@app.route("/klotski", methods=["POST"])
def klotski():
    data = request.json
    result = []
    for game in data:
        blocks = {}
        final_board=[0 for i in range(20)]
        count = 0
        for cell in game.get("board"):
            if cell not in blocks: 
                if cell !="@":
                    blocks[cell] = [count//4, count%4,count//4, count%4]
            else:
                if count//4 > blocks[cell][2]:
                    blocks[cell][2] = count//4
                if count%4 > blocks[cell][3]:
                    blocks[cell][3] = count%4
            count+=1
        for i in range(0,len(game.get("moves")),2):
            move = game.get("moves")[i+1]
            if move == "E":
                blocks[game.get("moves")[i]][1]+=1
                blocks[game.get("moves")[i]][3]+=1
            if move == "W":
                blocks[game.get("moves")[i]][1]-=1
                blocks[game.get("moves")[i]][3]-=1
            if move == "S":
                blocks[game.get("moves")[i]][0]+=1
                blocks[game.get("moves")[i]][2]+=1
            if move == "N":
                blocks[game.get("moves")[i]][0]-=1
                blocks[game.get("moves")[i]][2]-=1
        for block in blocks:
            for i in range(blocks[block][0],blocks[block][2]+1):
                for j in range(blocks[block][1],blocks[block][3]+1):
                    final_board[i*4+j] = block
        for i in range(len(final_board)):
            if final_board[i]==0:
                final_board[i]="@"
        result.append("".join(final_board))
    return jsonify(result)
        







# Example
# c = {1: 5, 2: 8, 3: 13}  # tasks are [1, 2, 3]
# pre = {1: [], 2: [], 3: [1, 2]}
# print(min_days_to_finish_project(c, pre))  # 21

if __name__ == "__main__":
    app.run(debug=True)

