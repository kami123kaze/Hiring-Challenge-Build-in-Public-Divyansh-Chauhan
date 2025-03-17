<template>
  <div class="flex min-h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-blue-600 text-white p-5">
      <h2 class="text-xl font-semibold">Teacher Dashboard</h2>
      <nav class="mt-5">
        <button @click="logout" class="mt-5 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded w-full">
          Logout
        </button>
      </nav>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 p-10">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">Custom Games</h1>

      <div class="bg-white shadow-md rounded-lg p-5">
        <h2 class="text-2xl font-semibold mb-4">Existing Custom Games</h2>
        <div v-if="customGames.length">
          <ul>
            <li v-for="game in customGames" :key="game.id" class="p-3 border-b">
              <h3 class="text-lg font-medium">{{ game.target_number }} - Weights: {{ game.weights.join(', ') }}</h3>
            </li>
          </ul>
        </div>
        <div v-else>
          <p class="text-gray-600">No custom games available.</p>
        </div>
      </div>

      <div class="mt-8 bg-white shadow-md rounded-lg p-5">
        <h2 class="text-2xl font-semibold mb-4">Add New Custom Game</h2>
        <form @submit.prevent="addCustomGame" class="space-y-4">
          <div>
            <label class="block font-medium">Target Number</label>
            <input v-model="newGame.target_number" type="number" required class="w-full p-2 border rounded" />
          </div>
          <div>
            <label class="block font-medium">Available Weights (comma-separated)</label>
            <input v-model="newGame.weights" type="text" required class="w-full p-2 border rounded" />
          </div>
          <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
            Add Game
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { db, auth } from "../firebase/config";
import { collection, getDocs, addDoc } from "firebase/firestore";
import { signOut } from "firebase/auth";
import { useRouter } from "vue-router";

export default {
  data() {
    return {
      customGames: [],
      newGame: {
        target_number: null,
        weights: "",
      },
    };
  },
  methods: {
    async fetchCustomGames() {
      try {
        const querySnapshot = await getDocs(collection(db, "custom_games"));
        this.customGames = querySnapshot.docs.map((doc) => {
          const data = doc.data();
          return {
            id: doc.id,
            target_number: data.target_number || 0,
            weights: Array.isArray(data.weights) ? data.weights : [],
          };
        });
      } catch (error) {
        console.error("Error fetching custom games:", error);
      }
    },
    async addCustomGame() {
      const { target_number, weights } = this.newGame;
      const weightsArray = weights.split(",").map((weight) => weight.trim());
      try {
        await addDoc(collection(db, "custom_games"), {
          target_number: Number(target_number),
          weights: weightsArray,
        });
        this.newGame.target_number = null;
        this.newGame.weights = "";
        this.fetchCustomGames();
      } catch (error) {
        console.error("Error adding custom game:", error);
      }
    },
    async logout() {
      try {
        await signOut(auth);
        this.$router.push("/login");
      } catch (error) {
        console.error("Error logging out:", error);
      }
    },
  },
  created() {
    this.fetchCustomGames();
  },
};
</script>