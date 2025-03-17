<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { auth, db } from "../firebase/config";
import { signInWithEmailAndPassword } from "firebase/auth";
import { doc, getDoc } from "firebase/firestore";

const email = ref("");
const password = ref("");
const errorMessage = ref("");
const router = useRouter();

const login = async () => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email.value, password.value);
    const user = userCredential.user;
    console.log("✅ Authenticated User:", user); // Debugging

    // Get Firebase Token
    const token = await user.getIdToken();
    localStorage.setItem("token", token); // Store token for API calls

    // Fetch user role from Firestore
    const userDoc = await getDoc(doc(db, "users", user.uid));

    if (userDoc.exists()) {
      const role = userDoc.data().role; // "student" or "teacher"

      // Redirect based on role
      if (role === "student") {
        router.push("/student-dashboard");
      } else if (role === "teacher") {
        router.push("/educator-dashboard");
      } else {
        errorMessage.value = "Invalid role assigned!";
      }
    } else {
      errorMessage.value = "User data not found!";
    }
  } catch (error) {
    errorMessage.value = "Login failed. Please check your credentials.";
    console.error("Login error:", error.message);
  }
};

</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-gray-300">
    <div class="glass-container p-8 max-w-md w-full">
      <h2 class="text-3xl font-bold text-center text-white mb-6">Login</h2>

      <form @submit.prevent="login">
        <div class="mb-4">
          <label class="block text-white text-lg mb-1">Email</label>
          <input 
            v-model="email" 
            type="email" 
            class="input-field" 
            required 
            autocomplete="off" 
            inputmode="email"
          />
        </div>

        <div class="mb-4">
          <label class="block text-white text-lg mb-1">Password</label>
          <input 
            v-model="password" 
            type="password" 
            class="input-field" 
            required 
            autocomplete="new-password"
          />
        </div>

        <p v-if="errorMessage" class="text-red-400 text-center mb-4">{{ errorMessage }}</p>

        <button type="submit" class="btn-glass">Login</button>
      </form>

      <p class="text-white text-center mt-4">
        Don't have an account? 
        <router-link to="/signup" class="link-dark">Sign Up</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Background gradient */
.bg-gradient-to-br {
  background: linear-gradient(to bottom right, #1a1a1a, #d3d3d3);
}

/* Glass effect container */
.glass-container {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Input fields */
.input-field {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  color: white;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  transition: background 0.3s, border 0.3s;
}

.input-field:focus {
  background: rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

/* Button styles */
.btn-glass {
  width: 100%;
  padding: 12px;
  font-size: 18px;
  font-weight: bold;
  color: white;
  background: rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s, border 0.3s;
}

/* Darker hover effect */
.btn-glass:hover {
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.7);
}

/* Darker text for better visibility */
.text-light {
  color: rgba(255, 255, 255, 0.8);
}

/* Make "Sign Up" link pop more */
.link-dark {
  color: rgb(173, 216, 230);
}

.link-dark:hover {
  color: rgb(135, 206, 250);
}
</style>
