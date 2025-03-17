
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore, collection, doc, setDoc, getDocs, query, orderBy, limit } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyCDnUmr4iD-iOcb9DyrcKzwgRIJu1pLI14",
  authDomain: "balance-game-18585.firebaseapp.com",
  projectId: "balance-game-18585",
  storageBucket: "balance-game-18585.firebasestorage.app",
  messagingSenderId: "472731595042",
  appId: "1:472731595042:web:72020c152bdd0df1e0357b",
  measurementId: "G-YYGG2ED1B5"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Analytics (Optional, only if needed)
const analytics = getAnalytics(app);

// Get Firebase Auth instance
const auth = getAuth(app);
//get db
const db = getFirestore(app);

export { app, auth, analytics, db, collection, doc, setDoc, getDocs, query, orderBy, limit };