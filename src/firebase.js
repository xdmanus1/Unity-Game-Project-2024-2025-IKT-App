import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

const firebaseConfig = {
    apiKey: "AIzaSyBKzP_Gzj9vKl0SeNGvwqyPNTjyJFP1cNg",

    authDomain: "blissful-acumen-403110.firebaseapp.com",

    databaseURL: "https://blissful-acumen-403110-default-rtdb.europe-west1.firebasedatabase.app",

    projectId: "blissful-acumen-403110",

    storageBucket: "blissful-acumen-403110.appspot.com",

    messagingSenderId: "906620326246",

    appId: "1:906620326246:web:ae4df89c2b39b2230578a7"

};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const storage = getStorage(app);

export { db, storage };