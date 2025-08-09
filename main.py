# MAIN.PY
# The runnable script that runs the web server.


from flask import Flask, render_template, send_from_directory, url_for, make_response, redirect, request
import werkzeug
import os.path
import random
import urllib

from datamanager import authenticate, addClient, addExercise, getClients, getExercises, getRepTypes, getUnits, getComplex, getRepAmounts, getSuggestion, removeClient, removeExercise, setComplex, addComplexExercise, removeComplexExercise, updateValue, updateValueSelect, getRawData, getPresets, loadPreset, savePreset, removePreset, getWeek, renameExercise, renameClient

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

def get_week():
    return getWeek()
app.jinja_env.globals.update(get_week=get_week)


def auth():
    try:
        if authenticate(request.cookies["name"], request.cookies["password"]):
            return True
        else:
            return False
    except:
        return False
    
def domain():
    return urllib.parse.urlparse(request.base_url).hostname


@app.route('/status')
def status():
    return "OK"

# Public pages:

@app.route('/')
def menu(): 
    if auth():
        return render_template('menu.html')
    else:
        return render_template('signin.html')

@app.route('/clients')
def clients():
    if auth():
        return render_template('clients.html')
    else:
        return render_template('signin.html')

@app.route('/exercises')
def exercises():
    if auth():
        return render_template('exercises.html')
    else:
        return render_template('signin.html')

@app.route('/settings')
def settings():
    if auth():
        return render_template('settings.html')
    else:
        return render_template('signin.html')

@app.route('/complex')
def complex():
    if auth():
        return render_template('complex.html')
    else:
        return render_template('signin.html')

@app.route('/session')
def session():
    if auth():
        return render_template('session.html')
    else:
        return render_template('signin.html')



# Internally facing:
    
@app.route('/signin/<name>/<password>')
def signin_user(name, password):
    if authenticate(name, password):
        response = make_response(redirect(f'http://{domain()}'))
        response.set_cookie('name', name, max_age=31536000)
        response.set_cookie('password', password, max_age=31536000)
        return response
    else:
        return redirect(f'http://{domain()}/')

@app.route('/signout')
def signout_user():
    response = make_response(redirect(f'http://{domain()}'))
    response.delete_cookie('name')
    response.delete_cookie('password')
    response.delete_cookie('clients')
    return response

@app.route('/addclient/<name>')
def add_client(name):
    if auth():
        addClient(name)
        return redirect(f'http://{domain()}/clients')
    else:
        return render_template('signin.html')

@app.route('/addsessionclient/<name>')
def add_session_client(name):
    if auth():
        response = make_response(redirect(f'http://{domain()}/session'))
        try:
            if not "|" + name + "|" in request.cookies["clients"]:
                response.set_cookie('clients', request.cookies["clients"] + name + "|", max_age=31536000)
        except:
            response.set_cookie('clients', "|" + name + "|", max_age=31536000)
        return response
    else:
        return render_template('signin.html')

@app.route('/removesessionclient/<name>')
def remove_session_client(name):
    if auth():
        response = make_response(redirect(f'http://{domain()}/session'))
        response.set_cookie('clients', request.cookies["clients"].replace("|" + name + "|", "|"), max_age=31536000)
        while "||" in request.cookies["clients"]:
            request.cookies["clients"].replace("||", "|")
        print("." + request.cookies["clients"] + ".")
        if "|" + name + "|" == request.cookies["clients"]:
            response.delete_cookie("clients")
        return response
    else:
        return render_template('signin.html')

@app.route('/addexercise/<name>/<unit>')
def add_exercise(name, unit):
    if auth():
        addExercise(name, unit)
        return redirect(f'http://{domain()}/exercises')
    else:
        return render_template('signin.html')

@app.route('/removeclient/<client>')
def remove_client(client):
    if auth():
        response = make_response(redirect(f'http://{domain()}/clients'))
        removeClient(client)
        response.set_cookie('clients', '')
        return response
    else:
        return render_template('signin.html')

@app.route('/removeexercise/<exercise>')
def remove_exercise(exercise):
    if auth():
        removeExercise(exercise)
        return redirect(f'http://{domain()}/exercises')
    else:
        return render_template('signin.html')

@app.route('/setcomplex/<exerciseComplex>')
def set_complex(exerciseComplex):
    if auth():
        setComplex(exerciseComplex.split(","))
        return redirect(f'http://{domain()}/complex')
    else:
        return render_template('signin.html')

@app.route('/addcomplexexercise/<index>')
def add_complex_exercise(index):
    if auth():
        addComplexExercise(index)
        return redirect(f'http://{domain()}/complex')
    else:
        return render_template('signin.html')

@app.route('/removecomplexexercise/<index>')
def remove_complex_exercise(index):
    if auth():
        removeComplexExercise(index)
        return redirect(f'http://{domain()}/complex')
    else:
        return render_template('signin.html')

@app.route('/update/<client>/<exercise>/<value>')
def update(client, exercise, value):
    if auth():
        updateValue(client, exercise, value)
        return redirect(f'http://{domain()}/session')
    else:
        return render_template('signin.html')

@app.route('/updateselect/<client>/<exercise>/<value>')
def update_select(client, exercise, value):
    if auth():
        updateValueSelect(client, exercise, value)
        return redirect(f'http://{domain()}/session')
    else:
        return render_template('signin.html')

@app.route('/getrawdata')
def get_raw_data():
    if auth():
        return getRawData()
    else:
        return render_template('signin.html')

@app.route('/loadpreset/<name>')
def load_preset(name):
    if auth():
        loadPreset(name)
        return redirect(f'http://{domain()}/complex')
    else:
        return render_template('signin.html')

@app.route('/savepreset/<name>')
def save_preset(name):
    if auth():
        savePreset(name)
        return redirect(f'http://{domain()}/complex')
    else:
        return render_template('signin.html')

@app.route('/removepreset/<name>')
def remove_preset(name):
    if auth():
        removePreset(name)
        return redirect(f'http://{domain()}/complex')
    else:
        return render_template('signin.html')
    
@app.route('/renameexercise/<old>/<new>')
def rename_exercise(old, new):
    if auth():
        renameExercise(old, new)
        return redirect(f'http://{domain()}/exercises')
    else:
        return render_template('signin.html')
    
@app.route('/renameclient/<old>/<new>')
def rename_client(old, new):
    if auth():
        response = make_response(redirect(f'http://{domain()}/clients'))
        renameClient(old, new)
        response.delete_cookie('clients')
        return response
    else:
        return render_template('signin.html')
    
# Remote deploy version.
@app.route('/ver')
def version():
    return "v2 (August 8th, 2025)"


# Start the application.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)