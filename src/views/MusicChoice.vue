<template>
  <div v-for="(url1) in url">
    <iframe :src="url1" width="50%" height="80" frameBorder="0" allow="autoplay; encrypted-media;"></iframe>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data(){
    return{
      uri:[],
      url:[],
    };
  },
  beforeMount(){
    axios.get('https://project1-b1937-default-rtdb.firebaseio.com/users/.json')
      .then((res) => {
        var a= Object.values(res)[0]
        this.uri = Object.values(a)[0]
        console.log(this.uri)
        for (let x of this. uri) {
          this.url.push('https://open.spotify.com/embed/track/'+x+'?utm_source=generator');
        }


      })
      .catch(err => console.log(err))
    
    
  },
  methods:{
    get(){
      axios.get('https://project1-b1937-default-rtdb.firebaseio.com/users/.json')
      .then((res) => {
        console.log(res)
      })
      .catch(err => console.log(err))
    },
  }
}
</script>

<style>

</style>