<template>
    <div>
      <h1>Balance Scale Addition Game</h1>
      <p>Game content will go here.</p>
  
      <button @click="startGame">Start Game</button>
      <button @click="submitGame">Submit Progress</button>
  
      <div v-if="gameData">
        <h3>Game Data:</h3>
        <pre>{{ gameData }}</pre>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from "vue";
  import axios from "axios";
  
  export default {
    setup() {
      const gameData = ref(null);
  
      const startGame = async () => {
        try {
          const response = await axios.post("http://127.0.0.1:8000/game/start");
          gameData.value = response.data;
        } catch (error) {
          console.error("Error starting game:", error);
        }
      };
  
      const submitGame = async () => {
        try {
          const response = await axios.post("http://127.0.0.1:8000/game/submit", {
            session_id: gameData.value?.session_id,
            score: 10, // Example score
          });
          console.log("Game submitted:", response.data);
        } catch (error) {
          console.error("Error submitting game:", error);
        }
      };
  
      return { gameData, startGame, submitGame };
    },
  };
  </script>
  