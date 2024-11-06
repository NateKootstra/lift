// Import Firebase libraries.
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.1/firebase-app.js";
import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/11.0.1/firebase-firestore.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/11.0.1/firebase-auth.js";


const firebaseConfig = {
    apiKey: "AIzaSyCcyjSl_1cD6LxYVpNwPoyEBUClEGBdzoI",
    authDomain: "liftmanagersite.firebaseapp.com",
    projectId: "liftmanagersite",
    storageBucket: "liftmanagersite.appspot.com",
    messagingSenderId: "154818722831",
    appId: "1:154818722831:web:ae740b9bc03a752269777a",
    measurementId: "G-9CREH93M3C"
};


// Initialize Firebase.
const app = initializeApp(firebaseConfig);
// Initialize Firestore.
const db = getFirestore(app);



email = "TODO"
password = "Add username and password input system."

const auth = getAuth();
signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
        const user = userCredential.user;
        alert("I think it worked?");
    })
    .catch((error) => {
        const errorCode = error.code;
        alert(errorCode);
    });




// Add an exercise to the database.
function addExercise(name, valuetype, value, weight, time, finalRepCount) {
    setDoc(doc(db, "exercises", name.toLowerCase() + "_" + value.toString()), {
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




// Export the functions.
export { addExercise };
