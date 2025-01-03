// Import Firebase libraries.
import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.0.1/firebase-app.js';
import { getFirestore, doc, setDoc, getDoc, getDocs, collection } from 'https://www.gstatic.com/firebasejs/11.0.1/firebase-firestore.js';
import { getAuth, signInWithEmailAndPassword, signOut, onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/11.0.1/firebase-auth.js';


// Set configuration.
const firebaseConfig = {
    apiKey: 'AIzaSyCcyjSl_1cD6LxYVpNwPoyEBUClEGBdzoI',
    authDomain: 'liftmanagersite.firebaseapp.com',
    projectId: 'liftmanagersite',
    storageBucket: 'liftmanagersite.appspot.com',
    messagingSenderId: '154818722831',
    appId: '1:154818722831:web:ae740b9bc03a752269777a',
    measurementId: 'G-9CREH93M3C'
};

// Initialize Firebase.
const app = initializeApp(firebaseConfig);
// Initialize Firestore.
const db = getFirestore(app);
// Get Auth.
const auth = getAuth();


// Redirect user to sign in page if the user hasn't signed in.
onAuthStateChanged(auth, (user) => {
    if (user == null) {
        if (!window.location.href.endsWith('signin/'))
            window.location.href = '/signin/';
    }
    else {
        if (window.location.href.endsWith('signin/'))
            window.location.href = '/';
    }
});


// Sign in.
function signIn(email, password) {
    signInWithEmailAndPassword(auth, email, password)
        .then(() => {
            window.location.href = '/';
        })
        .catch(() => {
            alert('Incorrect email/password.');
        });
}

// Sign out.
function signOutUser() {
    const auth = getAuth();
    signOut(auth).then(() => {
        window.location.href = '/signin';
    }).catch(() => {
        alert("Couldn't sign you out.")
    });
}


// Add a client to the database.
async function addClient(firstName, lastName) {
    let clients = await getClients();
    clients.push(firstName + "_" + lastName);
    setDoc(doc(db, 'clients', 'list'), {
        clients: clients
    });
    console.log(clients);
    await new Promise(resolve => setTimeout(resolve, 2000));
    location.reload();
}

// Add an exercise to the database.
function addExercise(name, valuetype, value, weight, time, finalRepCount) {
    setDoc(doc(db, 'exercises', name.toLowerCase() + '_' + value.toString()), {
        name: name,
        value: value,
        valueType: valuetype,
        fields: {
            weight: weight,
            time: time,
            finalRepCount: finalRepCount
        }
    });
}


// Get clients from the database.
async function getClients() {
    const clients = await getDoc(doc(db, 'clients', 'list'));
    return clients.data()['clients'];
}

// Get exercises from the database.
async function getExercises() {
    const clients = await getDoc(doc(db, 'exercises', 'list'));
    return clients.data()['exercises'];
}

// Display clients.
async function showClients() {
    let clients = await getClients();
    let template = document.getElementsByTagName('template')[0];
    for (let i = 0; i < clients.length; i++) {
        let id = clients[i];
        let name = id.replace('_', ' ');

        let clone = template.content.cloneNode(true);
        clone.childNodes[1].childNodes[0].textContent = name;
        clone.childNodes[1].childNodes[0].href = `/clients/view?id=${id}`;
        document.body.appendChild(clone);
    }
}

// Display exercises.
async function showExercises() {
    let exercises = await getExercises()
    let template = document.getElementsByTagName('template')[0];
    for (let i = 0; i < exercises.length; i++) {
        let id = exercises[i];
        let name = id.replace('_', ' ');

        let clone = template.content.cloneNode(true);
        clone.childNodes[0].textContent = name
        console.log(clone.childNodes[0].href)
        clone.childNodes[0].href = `/exercises/view?id=${id}`
        document.body.appendChild(clone);
    }
}


// Export the functions.
export { signIn, signOutUser, addClient, addExercise, showClients, showExercises };

// Make them global.
window.signIn = signIn;
window.signOut = signOutUser;
window.addClient = addClient;
window.showClients = showClients;
window.showExercises = showExercises;
