<script setup>
import { ref, onMounted } from "vue";
import { db } from "../firebase/config";
import { collection, query, orderBy, limit, getDocs } from "firebase/firestore";

const leaderboard = ref([]);
const loading = ref(true);
const errorMessage = ref("");

// Fetch leaderboard from Firestore
const fetchLeaderboard = async () => {
  const leaderboardRef = collection(db, "leaderboard");
  const leaderboardQuery = query(leaderboardRef, orderBy("score", "desc"), limit(10));
  try {
    const querySnapshot = await getDocs(leaderboardQuery);
    leaderboard.value = querySnapshot.docs.map((doc, index) => ({
      rank: index + 1,  // Ranking based on position in the query
      username: doc.data().userId, 
      score: doc.data().score,
    }));
  } catch (error) {
    errorMessage.value = "Error fetching leaderboard: " + error.message;
  } finally {
    loading.value = false;
  }
};

// Fetch leaderboard when component is mounted
onMounted(fetchLeaderboard);
</script>

<template>
  <div class="leaderboard">
    <h2 class="title">Leaderboard</h2>

    <!-- Loading text -->
    <p v-if="loading" class="loading-text">Loading leaderboard...</p>

    <!-- Error text -->
    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

    <!-- Leaderboard table -->
    <table v-if="leaderboard.length">
      <thead>
        <tr>
          <th>Rank</th>
          <th>Username</th>
          <th>Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="player in leaderboard" :key="player.rank">
          <td>{{ player.rank }}</td>
          <td>{{ player.username }}</td>
          <td>{{ player.score }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.leaderboard {
  background: rgba(0, 80, 100, 0.8); /* Dark teal with slight transparency */
  padding: 16px;
  border-radius: 8px;
  color: white;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.title {
  font-size: 22px;
  font-weight: bold;
  color: #ff9800; /* Orange accent */
  margin-bottom: 10px;
}

.loading-text,
.error-text {
  font-size: 18px;
  margin: 10px 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

th {
  font-weight: bold;
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

td {
  background: rgba(255, 255, 255, 0.15);
}

tr:hover {
  background: rgba(255, 255, 255, 0.25); /* Subtle hover effect */
  transition: background 0.3s;
}
</style>
