<template>
  <div id="app">
    <myChat/>
    <!-- <myTest/> -->
  </div>
</template>

<script>
import myChat from './components/myChat.vue'
import myTest from './components/myTest.vue'
export default {
  name: 'App',
  components: {
    myChat,
    myTest
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
