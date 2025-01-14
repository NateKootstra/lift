# MAIN.PY
# The runnable script that runs the web server.


from flask import Flask, render_template, send_from_directory, url_for, make_response, redirect, request
import os.path
import random

from datamanager import authenticate, addClient, addExercise, getClients, getExercises, getRepTypes, getUnits, getComplex, removeClient, removeExercise, setComplex

domain = 'http://127.0.0.1:5002'
app = Flask(__name__)


def get_clients():
    return getClients()
app.jinja_env.globals.update(get_clients=get_clients)

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
    except:
        return render_template('signin.html')

@app.route('/clients')
def clients():
    try:    
        if authenticate(request.cookies["name"], request.cookies["password"]):
            return render_template('clients.html')
        else:
            return render_template('signin.html')
    except:
        return render_template('signin.html')

@app.route('/exercises')
def exercises():
    try:    
        if authenticate(request.cookies["name"], request.cookies["password"]):
            return render_template('exercises.html')
        else:
            return render_template('signin.html')
    except:
        return render_template('signin.html')

@app.route('/settings')
def settings():
    try:    
        if authenticate(request.cookies["name"], request.cookies["password"]):
            return render_template('settings.html')
        else:
            return render_template('signin.html')
    except:
        return render_template('signin.html')

@app.route('/complex')
def complex():
    try:    
        if authenticate(request.cookies["name"], request.cookies["password"]):
            return render_template('complex.html')
        else:
            return render_template('signin.html')
    except:
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

@app.route('/addclient/<firstName>/<lastName>')
def add_client(firstName, lastName):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        addClient(firstName, lastName)
    return redirect(f'{domain}/clients')

@app.route('/addexercise/<name>/<reps>/<repType>/<tracking>')
def add_exercise(name, reps, repType, tracking):
    if authenticate(request.cookies["name"], request.cookies["password"]):
        addExercise(name, reps, repType, tracking)
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
    return redirect(f'{domain}/complex')
    

# Start the application.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)