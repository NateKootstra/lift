function signIn(name, password) {
    window.location.href = `/signin/${name}/${password}`;
}

function signOut() {
    window.location.href = `/signout`;
}


function addClient(firstName, lastName) {
    window.location.href = `/addclient/${firstName}/${lastName}`;
}

function addExercise(name, reps, repType, tracking) {
    window.location.href = `/addexercise/${name}/${reps}/${repType}/${tracking}`;
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