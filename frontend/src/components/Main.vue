<template>
  <div class='main'>
    <Header />
    <Segmenter />
    <Footer />
  </div>
</template>

<script>
import Footer from '@/components/Footer.vue';
import Header from '@/components/Header.vue';
import Segmenter from '@/components/Segmenter.vue';

export default {
  name: 'Main',
  components: {
    Header,
    Footer,
    Segmenter,
  }
}
</script>

<style lang='scss' scoped>
.main {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
</style>
