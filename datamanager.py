import json

def authenticate(name = "", password = ""):
    lists = open(f"data/lists.json")
    accounts = json.loads(lists.read())["accounts"]
    correct = False
    for account in accounts:
        if account["name"] == name.lower() and account["password"] == password.lower():
            correct = True
    lists.close()
    return correct

def addClient(name):
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    newLists["clients"].append(name)
    newLists["clients"] = sorted(newLists["clients"])
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def addExercise(name, unit):
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    newLists["exercises"].append({"name" : name, "unit" : unit, "data" : {}})
    newLists["exercises"] = sorted(newLists["exercises"], key=lambda x : x["name"])
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def getClients():
    lists = open(f"data/lists.json", 'r')
    clients = json.loads(lists.read())["clients"]
    lists.close()
    return clients

def getExercises():
    lists = open(f"data/lists.json", 'r')
    exercises = json.loads(lists.read())["exercises"]
    lists.close()
    return exercises

def getRepTypes():
    lists = open(f"data/lists.json", 'r')
    repTypes = json.loads(lists.read())["repTypes"]
    lists.close()
    return repTypes

def getUnits():
    lists = open(f"data/lists.json", 'r')
    units = json.loads(lists.read())["units"]
    lists.close()
    return units

def getRepAmounts():
    lists = open(f"data/lists.json", 'r')
    units = json.loads(lists.read())["repamounts"]
    lists.close()
    return units

def getComplex():
    lists = open(f"data/lists.json", 'r')
    exerciseComplex = json.loads(lists.read())["complex"]
    lists.close()
    return exerciseComplex

def getSuggestion(exercise, reps, client):
    lists = open(f"data/lists.json", 'r')
    realExercise = None
    for tempExercise in json.loads(lists.read())["exercises"]:
        if exercise == tempExercise["name"]:
            realExercise = tempExercise
    lists.close()
    i = 0
    reps1 = int(reps)
    reps2 = int(reps)
    try:
        return realExercise["data"]["reps"][str(reps1)][client]
    except:
        pass
    while i < 100:
        reps1 += 1
        reps2 -= 1
        i += 1
        try:
            return str(realExercise["data"]["reps"][str(reps1)][client]) + f" ({reps1})"
        except:
            pass
        try:
            return str(realExercise["data"]["reps"][str(reps2)][client]) + f" ({reps2})"
        except:
            pass
    return ""

def removeClient(client):
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    newLists["clients"].remove(client)
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def removeExercise(exercise):
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    for exercise2 in newLists["exercises"]:
        if exercise2["name"] == exercise:
            newLists["exercises"].remove(exercise2)
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def setComplex(exerciseComplex):
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    newLists["complex"] = exerciseComplex
    for exercise in exerciseComplex:
        if not exercise == "None":
            for exercise2 in newLists["exercises"]:
                if exercise.split(" | ")[0] == exercise2["name"]:
                    print(exercise2)
                    if not exercise.split(" | ")[1] in exercise2["data"]["reps"].keys():
                        exercise2["data"]["reps"][exercise.split(" | ")[1]] = {}
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def addComplexExercise(index):
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    newLists["complex"].insert(int(index), "None")
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def removeComplexExercise(index):
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    newLists["complex"].pop(int(index) - 1)
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def updateValue(client, exercise, value):
    allowedChars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    exercise = exercise.split(" | ")
    for i,exercise2 in enumerate(newLists["exercises"]):
        if exercise2["name"] == exercise[0]:
            newLists["exercises"][i]["data"]["reps"][exercise[1]][client] = value
            if value == "NONE":
                newLists["exercises"][i]["data"]["reps"][exercise[1]][client] = ""
    lists.close()
    for character in value:
        if not character in allowedChars and not value == "NONE":
            return
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def updateValueSelect(client, exercise, value):
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    exercise = exercise.split(" | ")
    for i,exercise2 in enumerate(newLists["exercises"]):
        if exercise2["name"] == exercise[0]:
            newLists["exercises"][i]["data"]["reps"][exercise[1]][client] = value
            if value == "NONE":
                newLists["exercises"][i]["data"]["reps"][exercise[1]][client] = ""
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def getRawData():
    lists = open(f"data/lists.json", 'r')
    data = json.loads(lists.read())
    lists.close()
    return data

def getPresets():
    lists = open(f"data/lists.json", 'r')
    presets = json.loads(lists.read())["presets"]
    lists.close()
    return presets

def loadPreset(name):
    lists = open(f"data/lists.json", 'r')
    data = json.loads(lists.read())
    for preset in data["presets"]:
        if preset["name"] == name:
            data["complex"] = preset["exercises"]
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
    lists.close()

def savePreset(name):
    lists = open(f"data/lists.json", 'r')
    data = json.loads(lists.read())
    preset = {
        "name" : name,
        "exercises" : data["complex"]
    }
    data["presets"].append(preset)
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
    lists.close()