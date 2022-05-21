<template>
  <div v-for="(url1) in url" :key="url1">
    <div class="embed-responsive embed-responsive-16by9">
    <iframe :src="url1.url2" class="embed-responsive-item" width="80%" height="80" frameBorder="0" allow="autoplay; encrypted-media;" loading="lazy"></iframe>
    </div>
    <!--<button v-if="!likeList.includes(url1.uri1)" class="btn btn-primary" @click="likes(url1.uri1)"><span>Like</span></button>
    <button v-if="likeList.includes(url1.uri1)" class="btn btn-primary" @click="unlikes(url1.uri1)"><span>un Like</span></button>-->
  </div>
  <br>
  <!--<button class="btn btn-primary" @click="ppp"><span>Push</span> </button>-->
  <!--<button class="btn btn-primary" @click="PPush"><span>Push</span> </button>-->
</template>

<script>
import {getAuth} from 'firebase/auth';
import axios from 'axios'
export default {
  data(){
    return{
      uri:[],
      url:[],
      push1:'',
      likeList:[],
      og:[],
    };
  },
  beforeMount(){
    axios.get('https://project1-b1937-default-rtdb.firebaseio.com/users/.json')
      .then((res) => {
        var a= Object.values(res)[0]
        this.uri = Object.values(a)[0]
        //console.log(this.uri)
        for (let x of this.uri) {
          var obj = {};
          obj['uri1'] = x;
          obj['url2'] = 'https://open.spotify.com/embed/track/'+x+'?utm_source=generator';
          this.url.push(obj);
        }


      })
      .catch(err => console.log(err))
    
    
  },
  methods:{
    likes(items){
      this.likeList.push(items);
      console.log(this.likeList);
    },
    unlikes(items){
      let index = this.likeList.indexOf(items)
      this.likeList.splice(index,1);
      //console.log(this.likeList)
    },
    ppp(){
      
      this.axios.get('https://project1-b1937-default-rtdb.firebaseio.com/users/items.json')
      .then((res) => {
      
      var c = Object.values(res)[0]
  
       for(var i = 0; i < c.length; i++) {
        var obj = c[i];
        this.og.push(obj)
        }
      })
      .catch(err => console.log(err))
      
      for(var i =0; i < this.likeList.length; i++){
        this.og.push(this.likeList[i])
      }
      console.log(this.og)
      this.axios.put('https://project1-b1937-default-rtdb.firebaseio.com/users/.json', {
          items:this.og
      });
      this.axios.put('https://project1-b1937-default-rtdb.firebaseio.com/users/items.json', {
          items:this.og
      });
    },
    PPush(){
      
      for (var x of this.uri) {
        this.push1= this.push1+'spotify%3Atrack%3A'+x+'%2C'
      }
      console.log(this.push1);
      var url1 = "https://api.spotify.com/v1/playlists/0flbmzeOuRrYt4uEWa9Pm3/tracks?uris="+this.push1;

        var xhr = new XMLHttpRequest();
        xhr.open("POST", url1);

        xhr.setRequestHeader("Accept", "application/json");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("Authorization", "BQALaQYvp3-NQCsmy0Pfu07b3fUrKgQ4OwsivaGybW50B9RKmYwxXskITka8z7h8vzqwM_6IGuDZr4RnanbNHzxJvUL-gADaj5-_lOZuuVXhMyqqqig-e_L4UGgesWUKxgNS6Ps30781lXDHXhKpzxNtPcWQrvM");
        xhr.setRequestHeader("Content-Length", "0");

        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4) {
              console.log(xhr.status);
              console.log(xhr.responseText);
          }};

        xhr.send();
      window.open("https://open.spotify.com/playlist/0flbmzeOuRrYt4uEWa9Pm3");
    },
  }

}
</script>

<style>

</style>