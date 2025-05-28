<script setup>
import Home from './components/Home.vue';

</script>

<template>
  <header>
  </header>

  <main>
    <Home />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}


@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }
}
</style>
