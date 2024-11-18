<script setup>
</script>

<template>
  <div id="app" style="backgroun-color:red">
    <div>
    <Chat />
    </div>
  </div>
</template>

<script>
import Chat from './components/chat.vue';

export default {
  components: {
    Chat,
  },
};
</script>

<style>
#app {
  display: flex;
  justify-content: center;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
