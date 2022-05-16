import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import store from './store'
import { initializeApp } from "firebase/app"

const firebaseConfig = {
    apiKey: "AIzaSyD5w0CdtqdXQF5Fx0sk4FKKky6LeO4UumY",
    authDomain: "enduring-lane-329703.firebaseapp.com",
    databaseURL: "https://enduring-lane-329703-default-rtdb.firebaseio.com",
    projectId: "enduring-lane-329703",
    storageBucket: "enduring-lane-329703.appspot.com",
    messagingSenderId: "595707837853",
    appId: "1:595707837853:web:91b96c92710a98b3834374",
    measurementId: "G-573XM6LJ2H"
};
  
  // Initialize Firebase
let app = createApp(App)
  
initializeApp(firebaseConfig);
app.config.globalProperties.firebaseConfig = firebaseConfig; 
app.use(store).use(router).mount('#app')
