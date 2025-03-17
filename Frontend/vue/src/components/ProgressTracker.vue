<script setup>
import { ref, onMounted } from "vue";
import { auth, db } from "../firebase/config";
import { collection, getDocs, query, where } from "firebase/firestore";

const progress = ref([]);
const loading = ref(true);
const errorMessage = ref("");

onMounted(async () => {
  const user = auth.currentUser;
  if (!user) {
    errorMessage.value = "Please log in to track progress.";
    loading.value = false;
    return;
  }

  try {
    const q = query(collection(db, "game_sessions"), where("userId", "==", user.uid));
    const querySnapshot = await getDocs(q);

    progress.value = querySnapshot.docs.map((doc) => ({
      id: doc.id,
      targetNumber: doc.data().targetNumber,
      leftSide: doc.data().leftSide,
      rightSide: doc.data().rightSide,
      balanced: doc.data().balanced,
      timestamp: new Date(doc.data().timestamp.seconds * 1000).toLocaleString(),
    }));

    loading.value = false;
  } catch (error) {
    errorMessage.value = "Error loading progress.";
    console.error("Firestore error:", error);
    loading.value = false;
  }
});
</script>

<template>
  <div class="progress-container">
    <h2 class="progress-title">Game Progress</h2>

    <p v-if="loading" class="loading-text">Loading progress...</p>
    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

    <ul v-if="progress.length">
      <li v-for="session in progress" :key="session.id" class="progress-item">
        <p><strong>Target:</strong> {{ session.targetNumber }}</p>
        <p><strong>Left Side:</strong> {{ session.leftSide.join(" + ") || "Empty" }}</p>
        <p><strong>Right Side:</strong> {{ session.rightSide.join(" + ") || "Empty" }}</p>
        <p><strong>Status:</strong> {{ session.balanced ? "✅ Balanced" : "❌ Not Balanced" }}</p>
        <p class="timestamp">{{ session.timestamp }}</p>
      </li>
    </ul>

    <p v-else-if="!loading" class="no-progress">No progress recorded yet.</p>
  </div>
</template>

<style scoped>
.progress-container {
  background: rgba(255, 255, 255, 0.2);
  padding: 20px;
  border-radius: 10px;
  color: white;
  text-align: center;
}

.progress-title {
  font-size: 24px;
  margin-bottom: 10px;
}

.loading-text, .error-text, .no-progress {
  font-size: 18px;
  margin: 10px 0;
}

.progress-item {
  background: rgba(255, 255, 255, 0.3);
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 8px;
  text-align: left;
}

.timestamp {
  font-size: 12px;
  color: lightgray;
}
</style>
