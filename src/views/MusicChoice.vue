<template>
  <iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/6cfVDaIdvDtYH91RqC6Wox?utm_source=generator" width="50%" height="80" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
  <iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/0ml8EENbogTBv1oB7RJHY2?utm_source=generator" width="50%" height="80" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
</template>

<script>
import axios from 'axios'
export default {
  methods:{
    get(){
      axios.get('https://project1-b1937-default-rtdb.firebaseio.com/users/.json')
      .then((res) => console.log(res))
      .catch(err => console.log(err))
    }
  }
}
</script>

<style>

</style>