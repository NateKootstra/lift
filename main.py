# MAIN.PY
# The runnable script that runs the web server.


from flask import Flask, render_template, send_from_directory, url_for, make_response, redirect, request
import werkzeug
import os.path
import random

from datamanager import authenticate, addClient, addExercise, getClients, getExercises, getRepTypes, getUnits, getComplex, getRepAmounts, getSuggestion, removeClient, removeExercise, setComplex, addComplexExercise, removeComplexExercise, updateValue, updateValueSelect, getRawData, getPresets, loadPreset, savePreset

domain = 'http://localhost'
app = Flask(__name__)


def get_clients():
    return getClients()
app.jinja_env.globals.update(get_clients=get_clients)

def get_session_clients():
    try:
        clients = request.cookies["clients"].split("|")
        while "" in clients:
            clients.remove("")
        return clients
    except:
        return []
app.jinja_env.globals.update(get_session_clients=get_session_clients)

def get_exercises():
    return getExercises()
app.jinja_env.globals.update(get_exercises=get_exercises)

def get_rep_types():
    return getRepTypes()
app.jinja_env.globals.update(get_rep_types=get_rep_types)

def get_units():
    return getUnits()
app.jinja_env.globals.update(get_units=get_units)

def get_complex():
    return getComplex()
app.jinja_env.globals.update(get_complex=get_complex)

def get_rep_amounts():
    return getRepAmounts()
app.jinja_env.globals.update(get_rep_amounts=get_rep_amounts)

def get_suggestion(exercise, reps, client):
    return getSuggestion(exercise, reps, client)
app.jinja_env.globals.update(get_suggestion=get_suggestion)

def get_presets():
    return getPresets()
app.jinja_env.globals.update(get_presets=get_presets)

# Public pages:

@app.route('/')
def menu():
    try:    
        if authenticate(request.cookies["name"], request.cookies["password"]):
            return render_template('menu.html')
        else:
            return render_template('signin.html')
    except werkzeug.exceptions.BadRequestKeyError:
        return render_template('signin.html')

@app.route('/clients')
def clients():
    try:    
        if authenticate(request.cookies["name"], request.cookies["password"]):
            return render_template('clients.html')
        else:
            return render_template('signin.html')
    except werkzeug.exceptions.BadRequestKeyError:
        return render_template('signin.html')

@app.route('/exercises')
def exercises():
    try:    
        if authenticate(request.cookies["name"], request.cookies["password"]):
            return render_template('exercises.html')
        else:
            return render_template('signin.html')
    except werkzeug.exceptions.BadRequestKeyError:
        return render_template('signin.html')

@app.route('/settings')
def settings():
    try:    
        if authenticate(request.cookies["name"], request.cookies["password"]):
            return render_template('settings.html')
        else:
            return render_template('signin.html')
    except werkzeug.exceptions.BadRequestKeyError:
        return render_template('signin.html')

@app.route('/complex')
def complex():
    try:    
        if authenticate(request.cookies["name"], request.cookies["password"]):
            return render_template('complex.html')
        else:
            return render_template('signin.html')
    except werkzeug.exceptions.BadRequestKeyError:
        return render_template('signin.html')
    
@app.route('/session')
def session():
    try:    
        if authenticate(request.cookies["name"], request.cookies["password"]):
            return render_template('session.html')
        else:
            return render_template('signin.html')
    except werkzeug.exceptions.BadRequestKeyError:
        return render_template('signin.html')
    


# Internally facing:
    
@app.route('/signin/<name>/<password>')
def signin_user(name, password):
    if authenticate(name, password):
        response = make_response(redirect(f'{domain}'))
        response.set_cookie('name', name)
        response.set_cookie('password', password)
        return response
    else:
        return redirect(f'{domain}/')
    
@app.route('/signout')
def signout_user():
    response = make_response(redirect(f'{domain}'))
    response.delete_cookie('name')
    response.delete_cookie('password')
    return response

@app.route('/addclient/<name>')
def add_client(name):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        addClient(name)
    return redirect(f'{domain}/clients')

@app.route('/addsessionclient/<name>')
def add_session_client(name):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        response = make_response(redirect(f'{domain}/session'))
        try:
            if not "|" + name + "|" in request.cookies["clients"]:
                response.set_cookie('clients', request.cookies["clients"] + name + "|")
        except:
            response.set_cookie('clients', "|" + name + "|")
    return response

@app.route('/removesessionclient/<name>')
def remove_session_client(name):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        response = make_response(redirect(f'{domain}/session'))
        response.set_cookie('clients', request.cookies["clients"].replace("|" + name + "|", "|"))
        while "||" in request.cookies["clients"]:
            request.cookies["clients"].replace("||", "|")
        if "|" + name + "|" == request.cookies["clients"]:
            response.delete_cookie("clients")
    return response

@app.route('/addexercise/<name>/<unit>')
def add_exercise(name, unit):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        addExercise(name, unit)
    return redirect(f'{domain}/exercises')

@app.route('/removeclient/<client>')
def remove_client(client):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        removeClient(client)
    return redirect(f'{domain}/clients')

@app.route('/removeexercise/<exercise>')
def remove_exercise(exercise):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        removeExercise(exercise)
    return redirect(f'{domain}/exercises')

@app.route('/setcomplex/<exerciseComplex>')
def set_complex(exerciseComplex):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        setComplex(exerciseComplex.split(","))
    return redirect(f'{domain}/settings')

@app.route('/addcomplexexercise/<index>')
def add_complex_exercise(index):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        addComplexExercise(index)
    return redirect(f'{domain}/complex')

@app.route('/removecomplexexercise/<index>')
def remove_complex_exercise(index):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        removeComplexExercise(index)
    return redirect(f'{domain}/complex')

@app.route('/update/<client>/<exercise>/<value>')
def update(client, exercise, value):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        updateValue(client, exercise, value)
    return redirect(f'{domain}/session')

@app.route('/updateselect/<client>/<exercise>/<value>')
def update_select(client, exercise, value):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        updateValueSelect(client, exercise, value)
    return redirect(f'{domain}/session')

@app.route('/getrawdata')
def get_raw_data():
    if authenticate(request.cookies["name"], request.cookies["password"]):
        return getRawData()
    
@app.route('/loadpreset/<name>')
def load_preset(name):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        loadPreset(name)
    return redirect(f'{domain}/complex')

@app.route('/savepreset/<name>')
def save_preset(name):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        savePreset(name)
    return redirect(f'{domain}/complex')
    

# Start the application.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)