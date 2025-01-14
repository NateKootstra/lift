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

def addClient(firstName, lastName):
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    newLists["clients"].append(firstName + "_" + lastName)
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(newLists, lists)
    lists.close()
    return

def addExercise(name, reps, repType, tracking):
    lists = open(f"data/lists.json", 'r')
    newLists = json.loads(lists.read())
    newLists["exercises"].append(name + "_" + reps + "_" + repType + "_" + tracking)
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
    newLists["exercises"].remove(exercise)
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