// ─────────────────────────────────────────────────────────
//  src/firebase/config.js
//  Replace ALL values below with your Firebase project keys
//  Firebase Console → Project Settings → Your Apps → SDK setup
// ─────────────────────────────────────────────────────────

import { initializeApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider } from 'firebase/auth'

const firebaseConfig = {
  apiKey: "AIzaSyDSMUQbClIVN83aOZ6_vESrX-XsW_U96C8",
  authDomain: "training-776a1.firebaseapp.com",
  projectId: "training-776a1",
  storageBucket: "training-776a1.firebasestorage.app",
  messagingSenderId: "417609025045",
  appId: "1:417609025045:web:b858172398455e32f7b01c",
  measurementId: "G-9T8V0TCD7L"
};

const app  = initializeApp(firebaseConfig)
export const auth     = getAuth(app)
export const provider = new GoogleAuthProvider()
export default app
