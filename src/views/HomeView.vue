<template>
    <div>
    <p>{{counter}}/10</p>
    <ul class="no-bullets">
        <span>Choose what Genre you like</span>
        <li v-for="(product , index) in items" :key="index" >
            <button @click="add(product,index)" >
            <!--<input  :value="product" name="product" type="checkbox" v-model="checked" />
            <label :for="product.lang"><span>{{product}}</span></label>-->
            <span>{{'Track name:'+product.track + ' Artist name:' + product.artist}}</span>
            </button>
        </li>
    </ul>
    <span>You have Choose</span>
    <ul class="no-bullets one-line">
        <li v-for="(product, index) in checked" :key="index" >
            <button @click="remove(product,index)" >
            <!--<input  :value="product" name="product" type="checkbox" v-model="checked" />
            <label :for="product.lang"><span>{{product}}</span></label>-->
            <span>{{'Track name:'+product.track + ' Artist name:' + product.artist}}</span>
            </button>
        </li>
    </ul>
    <button @click="nextPage">
        <span>nextPage</span>
    </button>
    <button @click="submit">
        <span>Submit</span>
    </button>
    
  </div>
</template>

<script>
import axios from 'axios';
import {getAuth} from 'firebase/auth';

import * as d3 from "d3";

export default {
    data(){
        return {
            items:[],
            checked:[],
            counter:0,
        }
    },
    mounted() {
        d3.csv("data.csv").then((data) => {
            for (let i = 0; i < 20; i++) {
                var rand = Math.floor(Math.random()*67500)
                var track = data[rand]['track_name'];
                var artist = data[rand]['artist_name'];
                var url = data[rand]['track_uri'];
                var obj = {};
                obj['track'] = track
                obj['artist'] = artist
                obj['uri'] = url
                this.items.push(obj);
            }
            });
    },
    methods:{
        randomList(){
            d3.csv("data.csv").then((data) => {
            for (let i = 0; i < 20; i++) {
                var rand = Math.floor(Math.random()*67500)
                var track = data[rand]['track_name'];
                var artist = data[rand]['artist_name'];
                var url = data[rand]['track_uri'];
                var obj = {};
                obj['track'] = track
                obj['artist'] = artist
                obj['uri'] = url
                this.items.push(obj);
            }
            });
        },
        add(product,index){
            if(this.counter < 10){
                this.checked.push(product);
                this.items.splice(index,1);
                this.counter++;
            }else{
                alert('Good');
            }
        },
        remove(product,index){
            this.checked.splice(index,1);
            this.items.push(product);
            this.counter--;
        },
        submit(){
            if(this.counter < 10){
                alert('Please pick 10 songs')
            }else{
                const user = getAuth().currentUser;
                let returnUri = [];
                const myArray = this.checked.valueOf()
                console.log(this.checked)
                for (let x of myArray) {
                    returnUri.push(x.uri);
                }
                console.log(returnUri);
                axios.put('https://project1-b1937-default-rtdb.firebaseio.com/users/.json', {
                    user: user.uid,
                    email: user.email,
                    items : returnUri
                });
                
                
                this.$router.push('/musicToday');
            }         
        },
        nextPage(){
            this.items=[];
            this.randomList();
        },
    }
}

</script>

<style>

</style>