<template>
    <div class="container login-container">
        <div class="row">
            <div class="col-md-6 login-form-1">
                <h3>Login</h3>
                <hr>
                <form>
                        <div class="form-group">
                            <input type="text" class="form-control" placeholder="Your Email *" v-model="email" />
                        </div>
                        <div class="form-group">
                            <input type="password" class="form-control" placeholder="Your Password *" v-model="password" />
                        </div>
                        <div class="form-group">
                            <input class="btn btn-primary btn-lg" @click="loginUser" type="button" value="Login" />
                        </div>
                        <div class="form-group">
                            <a href="#" class="ForgetPwd">Forget Password?</a>
                        </div>
                        <div class="form-group">
                            <p>Don't have an account? <a href="#" @click="goToRegister" class="ForgetPwd"> Register</a></p>
                        </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import {getAuth, onAuthStateChanged, signInWithEmailAndPassword} from 'firebase/auth';
export default {
    name: 'login',
    
    data(){
        return{
            email: '',
            password: '',
        };
    },

    beforeCreate(){
          onAuthStateChanged( getAuth(), (user) => {
            if (user) {    
                this.$router.push('/musicToday');
            }else{
                this.$router.push('/login');
            }
          });
    },

    methods:{
        goToRegister(){
            this.$router.push('/register');
        },
        async loginUser(){
            signInWithEmailAndPassword(getAuth(),this.email,this.password)
            .then(()=>{
                console.log("User logged in");
                this.$router.push('/musicToday');
            })
            .catch((error)=>{
                switch (error.code){ 
                    case 'auth/user-not-found':
                        alert("Incorrect Password or Email")
                        break                
                    case 'auth/invalid-email':
                        alert("Invalid email")
                        break               
                    case 'auth/wrong-password':
                        alert("Incorrect Password or Email")
                        break
                    default:
                        alert("Something went wrong: "+error.code )
                }
            });
        },
    },
}
</script>

<style scoped>
.login-container{
    margin: auto;
    width:auto;
}
.login-form-1{
    margin: auto;
    padding: 10%;
    width:auto;
}
.login-form-1 h3{
    text-align: center;
    color: #333;
}
.login-container form{
    padding: 10px;
    margin:auto;
    width: auto;
    
}
</style>

