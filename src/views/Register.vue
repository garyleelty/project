<template>
    <div class="container login-container">
        <div class="row">
            <div class="col-md-6 login-form-1">
                <h3>Register</h3>
                <hr>
                <form>
                        <div class="form-group">
                            <input type="text" class="form-control" placeholder="Your Email *" v-model="email" />
                        </div>
                        <div class="form-group">
                            <input type="password" class="form-control" placeholder="Your Password *" v-model="password" />
                        </div>
                        <div class="form-group">
                            <input class="btn btn-primary btn-lg" @click="registerUser" type="button" value="Login" />
                        </div>
                        <div class="form-group">
                            <a href="#" class="ForgetPwd">Forget Password?</a>
                        </div>
                        <div class="form-group">
                            <p>Have an account? <a href="#" @click="goToLogin" class="ForgetPwd"> Login</a></p>
                        </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import {getAuth, onAuthStateChanged, createUserWithEmailAndPassword} from 'firebase/auth';
export default {
    name:'register',
    data(){
        return{
            email: '',
            password:'',
        };
    },
    beforeCreate(){
        onAuthStateChanged( getAuth(), (user) => {
        if (user) {    
            this.$router.push('/wait');
        }else{
            this.$router.push('/register');
        }
        });
    },
    methods:{
        goToLogin(){
            this.$router.push('/login');
        },
        async registerUser(){
            if(this.email == "" || this.password == "" ){
                alert('No email or password')
            }
            createUserWithEmailAndPassword(getAuth(),this.email,this.password)
            .then(()=>{
                alert("Successfully Registered");
                this.$router.push('/')
            })
            .catch((error)=>{
                switch (error.code){
                   case 'auth/email-already-in-use':
                        alert("Email already in use")
                        this.$router.push('/login')
                        break
                    case 'auth/invalid-email':
                        alert("Invalid email")
                        break
                    case 'auth/operation-not-allowed':
                        alert("Operation not allowed")
                        break
                    case 'auth/weak-password':
                        alert("Password should be 6 characters up")
                        break
                    default:
                        alert("Something went wrong" + error.message)
                }
            });
        },
    },

}
</script>

<style>
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