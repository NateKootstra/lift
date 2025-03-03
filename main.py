# MAIN.PY
# The runnable script that runs the web server.


from flask import Flask, render_template, send_from_directory, url_for, make_response, redirect, request
import werkzeug
import os.path
import random

from datamanager import authenticate, addClient, addExercise, getClients, getExercises, getRepTypes, getUnits, getComplex, removeClient, removeExercise, setComplex, addComplexExercise, removeComplexExercise, updateValue, updateValueSelect

domain = 'http://127.0.0.1:5002'
app = Flask(__name__)


def get_clients():
    return getClients()
app.jinja_env.globals.update(get_clients=get_clients)

def get_session_clients():
    try:
        return request.cookies["clients"].split(" | ")
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

@app.route('/session2')
def session2():
    return render_template('session2.html')
    


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
            if not name + " |" in request.cookies["clients"] and not "| " + name in request.cookies["clients"]:
                response.set_cookie('clients', request.cookies["clients"] + " | " + name)
        except:
            response.set_cookie('clients', name)
    return response

@app.route('/addexercise/<name>/<unit>')
def add_exercise(name, unit):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        addExercise(name, unit)
    return redirect(f'{domain}/exercises')

@app.route('/removeclient/<client>')
def remove_client(client):
    removeClient(client)
    return redirect(f'{domain}/clients')

@app.route('/removeexercise/<exercise>')
def remove_exercise(exercise):
    removeExercise(exercise)
    return redirect(f'{domain}/exercises')

@app.route('/setcomplex/<exerciseComplex>')
def set_complex(exerciseComplex):
    setComplex(exerciseComplex.split(","))
    return redirect(f'{domain}/settings')

@app.route('/addcomplexexercise')
def add_complex_exercise():
    addComplexExercise()
    return redirect(f'{domain}/complex')

@app.route('/removecomplexexercise')
def remove_complex_exercise():
    removeComplexExercise()
    return redirect(f'{domain}/complex')

@app.route('/update/<client>/<exercise>/<value>')
def update(client, exercise, value):
    updateValue(client, exercise, value)
    return redirect(f'{domain}/session')

@app.route('/updateselect/<client>/<exercise>/<value>')
def update_select(client, exercise, value):
    updateValueSelect(client, exercise, value)
    return redirect(f'{domain}/session')
    

# Start the application.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)