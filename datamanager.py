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
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def addExercise(name, unit):
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    newLists["exercises"].append({"name" : name, "unit" : unit, "data" : {}})
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

def getComplex():
    lists = open(f"data/lists.json", 'r')
    exerciseComplex = json.loads(lists.read())["complex"]
    lists.close()
    return exerciseComplex

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
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def addComplexExercise():
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    newLists["complex"].append("None")
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def removeComplexExercise():
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    newLists["complex"].pop(-1)
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def updateValue(client, exercise, value):
    allowedChars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    if exercise.endswith(" reps)"):
        exercise = exercise.split(" reps)")[0].split(" (")
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
    if exercise.endswith(" reps)"):
        exercise = exercise.split(" reps)")[0].split(" (")
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