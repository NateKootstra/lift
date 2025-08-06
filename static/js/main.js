function signIn(name, password) {
    window.location.href = encodeURI(`/signin/${String(name).replace("/", "%2F")}/${String(password).replace("/", "%2F")}`)
}

function signOut() {
    window.location.href = encodeURI(`/signout`)
}


function addClient(name) {
    window.location.href = encodeURI(`/addclient/${String(name).replace("/", "%2F")}`)
}

function addExercise(name, unit) {
    name = name.replace("/", "|")
    window.location.href = encodeURI(`/addexercise/${String(name).replace("/", "%2F")}/${String(unit).replace("/", "%2F")}`)
}


function removeClient(client) {
    window.location.href = encodeURI(`/removeclient/${String(client).replace("/", "%2F")}`)
}

function removeExercise(exercise) {
    window.location.href = encodeURI(`/removeexercise/${String(exercise).replace("/", "%2F")}`)
}


function setComplex(complex) {
    window.location.href = `/setcomplex/${String(complex).replace("/", "%2F")}`
}

function addComplexExercise(index) {
    window.location.href = encodeURI(`/addcomplexexercise/${String(index).replace("/", "%2F")}`)
}

function removeComplexExercise(index) {
    window.location.href = encodeURI(`/removecomplexexercise/${String(index).replace("/", "%2F")} `)
}


function addSessionClient(name) {
    if (!(name == "none"))
        window.location.href = encodeURI(`/addsessionclient/${String(name).replace("/", "%2F")}`)
}

function removeSessionClient(name) {
    if (!(name == "none"))
        window.location.href = encodeURI(`/removesessionclient/${String(name).replace("/", "%2F")}`)
}

function updateInfo(client, exercise, value) {
    if (!(value == ""))
        window.location.href = encodeURI(`/update/${String(client).replace("/", "%2F")} /${String(exercise).replace("/", "%2F")}/${String(value).replace(" ", "%2F")}`)
}


function updateInfoSelect(client, exercise, value) {
    window.location.href = encodeURI(`/updateselect/${String(client).replace("/", "%2F")}/${String(exercise).replace("/", "%2F")}/${String(value).replace("/", "%2F")}`)
}


function saveComplex(name) {
    window.location.href = encodeURI(`/savepreset/${String(name).replace("/", "%2F")}`)
}

function loadComplex(name) {
    window.location.href = encodeURI(`/loadpreset/${String(name).replace("/", "%2F")}`)
}

function removeComplex(name) {
    window.location.href = encodeURI(`/removepreset/${String(name).replace("/", "%2F")}`)
}

function renameExercise(old, name) {
    window.location.href = encodeURI(`/renameexercise/${String(old).replace("/", "%2F")}/${String(name).replace("/", "%2F")}`)
}

function renameClient(old, name) {
    window.location.href = encodeURI(`/renameclient/${String(old).replace("/", "%2F")}/${String(name).replace("/", "%2F")}`)
}