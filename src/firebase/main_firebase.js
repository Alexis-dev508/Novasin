
  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.5/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.6.5/firebase-analytics.js";
  import { getFirestore, collection, addDoc, getDocs, onSnapshot} from "https://www.gstatic.com/firebasejs/9.6.5/firebase-firestore.js"; //Importamos los modulos necesarios de firestore
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyCcx2uUp-jrfc9IP8sN5IeKQU2O9Hm4tS4",
    authDomain: "novasin-96e4e.firebaseapp.com",
    projectId: "novasin-96e4e",
    storageBucket: "novasin-96e4e.appspot.com",
    messagingSenderId: "892249963931",
    appId: "1:892249963931:web:c282a3ff6340e51051353e",
    measurementId: "G-B3DZFPVD8P"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);

  const db = getFirestore();

  export const addNewProduct = (nombre, descripcion) =>{
      console.log('Entre al add')
    addDoc(collection(db, 'productos'), {nombre_prod: nombre, desc_prod: descripcion});
  };