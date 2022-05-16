import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import store from './store'
import { initializeApp } from "firebase/app"

const firebaseConfig = {
    apiKey: "AIzaSyC8Cbjf2Dosr3L-PKC0FoQHgKS67eVpatU",
    authDomain: "project1-b1937.firebaseapp.com",
    projectId: "project1-b1937",
    storageBucket: "project1-b1937.appspot.com",
    messagingSenderId: "844244535003",
    appId: "1:844244535003:web:3cf80c723183bcc03eaefe"
};
  
  // Initialize Firebase
let app = createApp(App)
  
initializeApp(firebaseConfig);
app.config.globalProperties.firebaseConfig = firebaseConfig; 
app.use(store).use(router).mount('#app')
