<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { auth } from "../firebase/config";
import { onAuthStateChanged, signOut } from "firebase/auth";

import GameBoard from "../components/GameBoard.vue";
import ProgressTracker from "../components/ProgressTracker.vue";
import Leaderboard from "../components/Leaderboard.vue";

const user = ref(null);
const router = useRouter();

onMounted(() => {
  onAuthStateChanged(auth, (currentUser) => {
    if (currentUser) {
      user.value = currentUser;
    } else {
      router.push("/login"); // Redirect if not logged in
    }
  });
});

const logout = async () => {
  await signOut(auth);
  router.push("/login");
};
</script>

<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <h1>Welcome, {{ user?.email }}</h1>
      <button @click="logout">Logout</button>
    </header>

    <main class="dashboard-content">
      <section class="game-section">
        <GameBoard />
      </section>
      
      <section class="progress-section">
        <ProgressTracker />
      </section>

      <section class="leaderboard-section">
        <Leaderboard />
      </section>
    </main>
  </div>
</template>

<style scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: linear-gradient(to bottom right, #1a1a1a, #d3d3d3);
  padding: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.2);
  padding: 15px;
  border-radius: 10px;
  color: white;
}

button {
  background: red;
  color: white;
  border: none;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 5px;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-top: 20px;
}

.game-section {
  grid-column: span 2;
}
</style>
