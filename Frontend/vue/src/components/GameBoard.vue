<script setup>
import { ref, watch, onBeforeUnmount, onMounted  } from "vue";
import { doc, getDoc } from "firebase/firestore";
import { db } from "../firebase/config";  
import { collection, getDocs, query, orderBy, limit, setDoc } from "firebase/firestore";


const difficulty = ref("easy");
const targetNumber = ref(10);
const placedWeights = ref([]);
const availableWeights = ref([]);
const balanceTilt = ref(0);
const score = ref(0);
const streak = ref(0);
const highScore = ref(0);
const showPopup = ref(false);
const popupMessage = ref("");
const popupColor = ref("");
const leaderboard = ref([]);  // To store the leaderboard data

import { getAuth } from "firebase/auth";  // Import Firebase Authentication

// Firebase function to save high score
const saveHighScore = async (score) => {
  const auth = getAuth();
  const user = auth.currentUser;

  if (!user) {
    console.error("User not authenticated");
    return;
  }

  const userId = user.uid;  // Get the current user's UID
  const userDoc = doc(db, "leaderboards", userId);

  // Save or update the user's score
  await setDoc(userDoc, { score }, { merge: true });
};
const fetchCustomGameData = async () => {
  const gameRef = doc(db, "custom_games", difficulty.value);
  const gameSnapshot = await getDoc(gameRef);
  
  if (gameSnapshot.exists()) {
    const gameData = gameSnapshot.data();
    targetNumber.value = gameData.targetNumber;
    availableWeights.value = gameData.availableWeights;
  } else {
    console.log("Custom game data not found for this difficulty.");
    // You can add a fallback here in case custom data is missing
  }
};

// Call fetchCustomGameData on difficulty change or component mount
watch(difficulty, async () => {
  await fetchCustomGameData();
  startNewGame();  // Reset the game when difficulty changes
});

onMounted(async () => {
  await fetchCustomGameData(); // Fetch custom data on initial load
  startNewGame();
});

// Firebase function to fetch leaderboard data
const fetchLeaderboard = async () => {
  const leaderboardRef = collection(db, "leaderboards");
  const q = query(leaderboardRef, orderBy("score", "desc"), limit(10));  // Get top 10 players
  const querySnapshot = await getDocs(q);
  leaderboard.value = querySnapshot.docs.map((doc) => doc.data());
};

// Generate a random target number based on difficulty
const generateTarget = () => {
  const ranges = {
    easy: [1, 20],
    normal: [50, 999],
    hard: [1000, 99999],
    extreme: [1, 9999999],
  };
  const [min, max] = ranges[difficulty.value];
  targetNumber.value = Math.floor(Math.random() * (max - min + 1)) + min;
};

// Ensure at least one solution exists
const ensureSolvableWeights = () => {
  const ranges = {
    easy: [1, 20],
    normal: [50, 999],
    hard: [1000, 99999],
    extreme: [1, 9999999],
  };
  const [min, max] = ranges[difficulty.value];

  let weights = Array.from({ length: 4 }, () => Math.floor(Math.random() * (max - min + 1)) + min);
  const possibleValues = [...weights];
  let remaining = targetNumber.value;
  let guaranteedSubset = [];

  for (let i = 0; i < possibleValues.length; i++) {
    if (remaining - possibleValues[i] >= 0) {
      guaranteedSubset.push(possibleValues[i]);
      remaining -= possibleValues[i];
    }
    if (remaining === 0) break;
  }

  if (remaining !== 0) {
    guaranteedSubset.push(remaining);
  }

  availableWeights.value = [...weights, ...guaranteedSubset].sort(() => Math.random() - 0.5);
};

const addWeight = (weight) => {
  placedWeights.value.push(weight);
  updateTilt();
};

const resetWeights = () => {
  placedWeights.value = [];
  updateTilt();
};

// Adjust balance tilt
const updateTilt = () => {
  const placedSum = placedWeights.value.reduce((sum, w) => sum + w, 0);
  balanceTilt.value = Math.min(Math.max((placedSum - targetNumber.value) * 1.5, -15), 15);
};

// Show feedback popup
const showFeedback = (message, color) => {
  popupMessage.value = message;
  popupColor.value = color;
  showPopup.value = true;
  setTimeout(() => (showPopup.value = false), 2000);
};

// Handle answer submission
const submitAnswer = () => {
  const placedSum = placedWeights.value.reduce((sum, w) => sum + w, 0);
  if (placedSum === targetNumber.value) {
    streak.value++;
    const points = { easy: 1, normal: 5, hard: 10, extreme: 100 };
    score.value += points[difficulty.value];

    if (streak.value >= 10) score.value += 15;
    else if (streak.value >= 8) score.value += 10;
    else if (streak.value >= 5) score.value += 5;
    else if (streak.value >= 3) score.value += 1;

    showFeedback("Correct!", "green");
    startNewGame();
  } else {
    updateHighScore();
    score.value = 0;
    streak.value = 0;
    showFeedback("Incorrect!", "red");
  }
};

// Start a new round
const startNewGame = () => {
  placedWeights.value = [];
  generateTarget();
  ensureSolvableWeights();
  updateTilt();
};

// Save high score before game exit or difficulty change
const updateHighScore = async () => {
  if (score.value > highScore.value) {
    highScore.value = score.value;
    await saveHighScore(score.value);  // Save the new high score
  }
};

// Handle game exit or difficulty change
const handleGameExit = () => {
  updateHighScore();
};

// Handle game exit or difficulty change
watch(difficulty, () => {
  handleGameExit();
  score.value = 0;
  streak.value = 0;
  startNewGame();
});

// Save before the game is closed
onBeforeUnmount(() => {
  handleGameExit();
});

// Fetch leaderboard data on component mount
onMounted(async () => {
  await fetchLeaderboard();
});

startNewGame();
</script>


<template>
  <div class="game-container">
    <h2 class="title">Balance Scale Addition Game</h2>

    <div class="difficulty-selection">
      <label for="difficulty">Select Difficulty:</label>
      <select id="difficulty" v-model="difficulty">
        <option value="easy">Easy</option>
        <option value="normal">Normal</option>
        <option value="hard">Hard</option>
        <option value="extreme">Extreme</option>
      </select>
    </div>

    <div class="score-container">
      <p>Score: <strong>{{ score }}</strong></p>
      <p>Streak: <strong>{{ streak }}</strong></p>
      <p>High Score: <strong>{{ highScore }}</strong></p>
    </div>

    <div class="balance-scale">
      <div class="scale-bar" :style="{ transform: `rotate(${balanceTilt}deg)` }">
        <div class="scale-left">
          <span>{{ targetNumber }}</span>
        </div>
        <div class="pivot"></div>
        <div class="scale-right">
          <span>{{ placedWeights.reduce((sum, w) => sum + w, 0) || 0 }}</span>
        </div>
      </div>
    </div>

    <div class="weights-section">
      <h3 class="choose-weight">Choose a weight:</h3>
      <div class="weights-container">
        <button v-for="weight in availableWeights" :key="weight" @click="addWeight(weight)">
          {{ weight }}
        </button>
      </div>
    </div>

    <div class="controls">
      <button @click="resetWeights" class="reset-btn">Reset</button>
      <button @click="startNewGame" class="new-game-btn">New Game</button>
      <button @click="submitAnswer" class="submit-btn">Submit</button>
    </div>

    <!-- Popup for feedback -->
    <div v-if="showPopup" class="popup" :style="{ backgroundColor: popupColor }">
      {{ popupMessage }}
    </div>
  </div>
</template>

<style scoped>
/* Popup styling */
.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 15px 20px;
  color: white;
  font-size: 18px;
  font-weight: bold;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
  animation: fadeInOut 2s ease-in-out;
}

@keyframes fadeInOut {
  0%, 100% { opacity: 0; }
  20%, 80% { opacity: 1; }
}

/* Rest of your existing styles remain unchanged */
</style>


<style scoped>
.game-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(to bottom right, #1a1a1a, #d3d3d3);
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 600px;
  margin: auto;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: white;
  margin-bottom: 20px;
}

.difficulty-selection {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.difficulty-selection select {
  background: none;
  border: 1px solid white;
  color: white;
  padding: 5px 10px;
  font-size: 16px;
}

.difficulty-selection select option {
  background: #333;
  color: white;
}

.score-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 400px;
  color: white;
  margin-bottom: 15px;
}

.balance-scale {
  position: relative;
  width: 320px;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.scale-bar {
  width: 280px;
  height: 10px;
  background: brown;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.3s ease-in-out;
  position: relative;
}

.scale-left {
  width: 60px;
  height: 50px;
  background: green;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border-radius: 5px;
  color: white;
}

.scale-right {
  width: 60px;
  height: 50px;
  background: red;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border-radius: 5px;
  color: white;
}

.pivot {
  width: 15px;
  height: 40px;
  background: black;
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
}

.weights-section {
  text-align: center;
  margin-top: 30px;
}

.choose-weight {
  margin-bottom: 15px;
  font-size: 18px;
  color: white;
}

.weights-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.weights-container button {
  background: #4CAF50;
  color: white;
  font-size: 16px;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.3s;
  margin: 5px;
  border: 2px solid black;
}

.weights-container button:hover {
  background: #45a049;
  transform: scale(1.1);
}

.controls {
  margin-top: 20px;
  display: flex;
  gap: 20px;
}

.reset-btn,
.new-game-btn,
.submit-btn {
  padding: 10px 15px;
  border: none;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
}

.reset-btn { background: red; color: white; }
.new-game-btn { background: green; color: white; }
.submit-btn { background: blue; color: white; }
</style>
