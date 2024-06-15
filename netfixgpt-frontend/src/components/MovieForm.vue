<template>
  <div class="movie-form">
    <h1>Enter a description and get a list of movies!</h1>
    <input
      v-model="description"
      type="text"
      placeholder="Example: A comedy movie set in New York City"
    />
    <button @click="getRecommendations" :disabled="loading">Generate!</button>
    <div v-if="loading" class="loading">Loading...</div>
    <pre v-if="response">{{ response }}</pre>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      description: "",
      response: null,
      loading: false,
    };
  },
  methods: {
    async getRecommendations() {
      this.loading = true;
      this.response = null; // Clear previous response
      try {
        const res = await axios.post("http://localhost:8000/generate", {
          details: this.description,
        });
        this.response = res.data.answer;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes inputFocus {
  0% {
    box-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
  }
  50% {
    box-shadow: 0 0 20px rgba(255, 255, 255, 1);
  }
  100% {
    box-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
  }
}

.movie-form {
  background: linear-gradient(45deg, #ff8c00, #ff0080);
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  animation: fadeIn 2s ease-in-out;
}

.movie-form h1 {
  font-size: 24px;
  color: white;
  animation: fadeIn 2s ease-in-out;
}

.movie-form input {
  width: 80%;
  padding: 10px;
  margin: 10px 0;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  transition: all 0.3s ease;
}

.movie-form input:focus {
  animation: inputFocus 1s infinite;
}

.movie-form button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: black;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.movie-form button:disabled {
  background-color: grey;
  cursor: not-allowed;
}

.movie-form button:hover {
  background-color: darkgrey;
}

.loading {
  margin: 20px;
  font-size: 18px;
  color: white;
}

pre {
  background: #f4f4f4;
  padding: 10px;
  border-radius: 5px;
  text-align: left;
  animation: fadeIn 2s ease-in-out;
}
</style>
