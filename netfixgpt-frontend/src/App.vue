<template>
  <div id="app">
    <header class="top-bar">NETFIXGPT</header>
    <MovieForm />
  </div>
</template>

<script>
import MovieForm from "./components/MovieForm.vue";

export default {
  name: "App",
  components: {
    MovieForm,
  },
};
</script>

<style>
@keyframes gradientBackground {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

#app {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(45deg, #ff8c00, #ff0080);
  background-size: 200% 200%;
  animation: gradientBackground 10s ease infinite;
}

.top-bar {
  width: 100%;
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  text-align: center;
  font-size: 24px;
  font-family: "Arial", sans-serif;
  position: absolute;
  top: 0;
}
</style>
