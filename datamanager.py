import json
from urllib.parse import unquote
import datetime

def getData():
    lists = open(f"data/lists.json")
    data = json.loads(lists.read())
    lists.close()
    return data

one_day = datetime.timedelta(days=1)
def getWeeks(date):
    """Return the full week (Sunday first) of the week containing the given date.

    'date' may be a datetime or date instance (the same type is returned).
    """
    day_idx = date.weekday() % 7  # turn sunday into 0, monday into 1, etc.
    monday = date - datetime.timedelta(days=day_idx)
    date = monday
    for n in range(7):
        yield date
        date += one_day
        
def getWeek():
    date = datetime.datetime.now().date()
    date_list = []
    sdate = datetime.date(date.year, 1, 1)
    edate = datetime.date(date.year, 12, 31)
    cdate = sdate
    while cdate <= edate:
        date_list.append(cdate)
        cdate += datetime.timedelta(days=1)
    weeks = []
    for i in range(53):
        if date in [d for d in getWeeks(date_list[i*7])]:
            return i

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
    data = json.loads(lists.read())
    data["clients"].append(name)
    data["clients"] = sorted(data["clients"])
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
    lists.close()
    return

def addExercise(name, unit):
    lists = open(f"data/lists.json", 'r')
    data = json.loads(lists.read())
    data["exercises"].append({"name" : name, "unit" : unit, "data" : {"reps": {"5": {}, "8": {}, "10": {}, "12": {}, "15": {}, "20": {}, "25": {}, "30": {}, "35": {}, "40": {}}}})
    data["exercises"] = sorted(data["exercises"], key=lambda x : x["name"])
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
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
    data = json.loads(lists.read())
    data["clients"].remove(client)
    for i,exercise in enumerate(data["exercises"]):
        for reps in exercise["data"]["reps"]:
            if client in exercise["data"]["reps"][reps].keys():
                data["exercises"][i]["data"]["reps"][reps].pop(client)
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
    lists.close()
    return

def removeExercise(exercise):
    lists = open(f"data/lists.json", 'r')
    data = json.loads(lists.read())
    for exercise2 in data["exercises"]:
        if exercise2["name"] == exercise:
            data["exercises"].remove(exercise2)
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
    lists.close()
    return

def setComplex(exerciseComplex):
    lists = open(f"data/lists.json", 'r')
    data = json.loads(lists.read())
    for i,exercise in enumerate(exerciseComplex):
        exerciseComplex[i] = unquote(exercise)
    print(exerciseComplex)
    data["complex"] = exerciseComplex
    for exercise in exerciseComplex:
        if not exercise == "None":
            for exercise2 in data["exercises"]:
                if exercise.split(" | ")[0] == exercise2["name"]:
                    try:
                        if not exercise.split(" | ")[1] in exercise2["data"]["reps"].keys():
                            exercise2["data"]["reps"][exercise.split(" | ")[1]] = {}
                    except:
                        pass
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
    lists.close()
    return

def addComplexExercise(index):
    lists = open(f"data/lists.json", 'r')
    data = json.loads(lists.read())
    data["complex"].insert(int(index), "None")
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
    lists.close()
    return

def removeComplexExercise(index):
    lists = open(f"data/lists.json", 'r')
    data = json.loads(lists.read())
    data["complex"].pop(int(index) - 1)
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
    lists.close()
    return

def updateValue(client, exercise, value):
    client = client.strip()
    lists = open(f"data/lists.json", 'r')
    data = json.loads(lists.read())
    exercise = exercise.split(" | ")
    print(exercise)
    for i,exercise2 in enumerate(data["exercises"]):
        if exercise2["name"] == exercise[0]:
            data["exercises"][i]["data"]["reps"][exercise[1]][client] = value
            if value == "NONE":
                data["exercises"][i]["data"]["reps"][exercise[1]][client] = ""
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
    lists.close()
    return

def updateValueSelect(client, exercise, value):
    lists = open(f"data/lists.json", 'r')
    data = json.loads(lists.read())
    exercise = exercise.split(" | ")
    for i,exercise2 in enumerate(data["exercises"]):
        if exercise2["name"] == exercise[0]:
            data["exercises"][i]["data"]["reps"][exercise[1]][client] = value
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
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
    
def removePreset(name):
    lists = open(f"data/lists.json", 'r')
    data = json.loads(lists.read())
    for i,preset in enumerate(data["presets"]):
        if preset["name"] == name:
            data["presets"].pop(i)
    lists.close()
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
    lists.close()
    
def renameExercise(old, new):
    lists = open(f"data/lists.json", 'r')
    data = json.loads(lists.read())
    for i,exercise in enumerate(data["exercises"]):
        if exercise["name"] == old:
            data["exercises"][i]["name"] = new
    data["exercises"] = sorted(data["exercises"], key=lambda x : x["name"])
    lists.close
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
    lists.close()
    
def renameClient(old, new):
    lists = open(f"data/lists.json", 'r')
    data = json.loads(lists.read())
    data["clients"].remove(old)
    data["clients"].append(new)
    data["clients"] = sorted(data["clients"])
    for i,exercise in enumerate(data["exercises"]):
        for reps in exercise["data"]["reps"]:
            if old in exercise["data"]["reps"][reps].keys():
                data["exercises"][i]["data"]["reps"][reps][new] = data["exercises"][i]["data"]["reps"][reps].pop(old)
    lists.close
    lists = open(f"data/lists.json", 'w')
    json.dump(data, lists)
    lists.close()