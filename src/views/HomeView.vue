<template>
    <div>
    <ul class="no-bullets">
        <span>Choose what Genre you like</span>
        <li v-for="(product, index) in items" :key="index" >
            <button @click="add(product,index)" >
            <!--<input  :value="product" name="product" type="checkbox" v-model="checkedGenre" />
            <label :for="product.lang"><span>{{product}}</span></label>-->
            <span>{{product}}</span>
            </button>
        </li>
    </ul>
    <span>You have Choose</span>
    <ul class="no-bullets one-line">
        
        <li v-for="(product, index) in checkedGenre" :key="index" >
            <button @click="remove(product,index)" >
            <!--<input  :value="product" name="product" type="checkbox" v-model="checkedGenre" />
            <label :for="product.lang"><span>{{product}}</span></label>-->
            <span>{{product}}</span>
            </button>
        </li>
    </ul>

    <button @click="submit">
        <span>Next page</span>
    </button>
    
  </div>
</template>

<script>
import axios from 'axios';
import {getAuth} from 'firebase/auth';
export default {
    data(){
        return {
            items:[
                "hippop",
                "Lo-fi",
                "Punk",
                "Chinese",
                "Jazz Blues"
            ],
            checkedGenre:[],
        }
    },
    methods:{
        add(product,index){
            this.checkedGenre.push(product);
            this.items.splice(index,1);
        },
        remove(product,index){
            this.checkedGenre.splice(index,1);
            this.items.push(product);
        },
        submit(){
            const user = getAuth().currentUser;
            axios.post('https://project1-b1937-default-rtdb.firebaseio.com/users/'+user+'.json', {
                items : this.items

            });
        }
    }
}

</script>

<style>

</style>