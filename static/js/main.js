function signIn(name, password) {
    window.location.href = `/signin/${name}/${password}`;
}

function signOut() {
    window.location.href = `/signout`;
}


function addClient(name) {
    window.location.href = `/addclient/${name}`;
}

function addExercise(name, unit) {
    window.location.href = `/addexercise/${name}/${unit}`;
}


function removeClient(client) {
    window.location.href = `/removeclient/${client}`;
}

function removeExercise(exercise) {
    window.location.href = `/removeexercise/${exercise}`;
}


function setComplex(complex) {
    window.location.href = `/setcomplex/${complex}`
}

function addComplexExercise() {
    window.location.href = `/addcomplexexercise`
}

function removeComplexExercise() {
    window.location.href = `/removecomplexexercise`
}


function addSessionClient(name) {
    if (!(name == "none"))
        window.location.href = `/addsessionclient/${name}`
}

function updateInfo(client, exercise, value) {
    if (!(value == ""))
        window.location.href = `/update/${client}/${exercise}/${value}`
}


function updateInfoSelect(client, exercise, value) {
    window.location.href = `/updateselect/${client}/${exercise}/${value}`
}