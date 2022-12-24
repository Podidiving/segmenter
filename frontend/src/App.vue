<template>
  <div id="app">
    <Main/>
  </div>
</template>

<script>
import Main from './components/Main.vue'

export default {
  name: 'App',
  components: {
    Main
  }
}
</script>

<style lang='scss'>
#app {
    display: flex;
    height: 100%;
    width: 100%;
    padding: 10px;
    box-sizing: border-box;
    background-color: $BGCOLOR;
}
</style>
