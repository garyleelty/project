<template>
<div v-if="progress<101">
  <h1>Loading {{progress}}%</h1>
    <section >
      <div class="box">
      <div class="mo" :style="{'--progress':-progress+100+'%'}"></div>
      <div class="line-box">
        <i></i>
        <i class="line-item"></i>
        <i class="line-item"></i>
        <i class="line-item"></i>
        <i></i>
      </div>
    </div>
    </section>
</div>
<div v-if="progress>100">
  <h1>Welcome to the music</h1>
  <button  class="btn btn-light" @click="pppp"> To Today Music </button>
</div>
</template>

<script>

  export default {
    data() {
      return {
        progress:0
      }
    },
    mounted(){
        if(this.progress <100){
                setInterval(() => {
            this.progress+=5
            }, 3000);
        }
    },
    methods:{
      pppp(){
        this.$router.push('/musicToday')
      }
    },
  }

</script>

<style scoped>

  .box {
    position: relative;
    width: 100%;
    height: 70px;
    overflow: hidden;
    background: linear-gradient(270deg, #FF4D4D 0%, #FADB6D 55.73%, #70FAC8 100%);
  }

  .mo {
    position: absolute;
    z-index: 1;
    right: 0;
    height: 100%;
    width: var(--progress, 0%);
    background-color: #ccc;
  }

  .line-box {
    position: absolute;
    z-index: 2;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: space-between;
  }

  .line-box .line-item {
    width: 2px;
    height: 100%;
    background-color: #fff;
  }

</style>