<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { auth, db } from "../firebase/config";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { doc, setDoc } from "firebase/firestore";

const email = ref("");
const password = ref("");
const role = ref("student");
const errorMessage = ref("");
const router = useRouter();

const signup = async () => {
  errorMessage.value = "";

  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email.value, password.value);
    const user = userCredential.user;

    // Ensure role is correctly assigned
    const assignedRole = role.value === "educator" ? "teacher" : "student";

    await setDoc(doc(db, "users", user.uid), {
      email: user.email,
      role: assignedRole, // Use "teacher" instead of "educator"
    });

    router.push(assignedRole === "teacher" ? "/educator-dashboard" : "/student-dashboard");
  } catch (error) {
    if (error.code === "auth/email-already-in-use") {
      errorMessage.value = "Email is already registered.";
    } else if (error.code === "auth/weak-password") {
      errorMessage.value = "Password must be at least 6 characters.";
    } else {
      errorMessage.value = "Signup failed. Try again.";
    }
  }
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-gray-300">
    <div class="glass-container p-8 max-w-md w-full">
      <h2 class="text-3xl font-bold text-center text-white mb-6">Create Account</h2>

      <form @submit.prevent="signup">
        <div class="mb-4">
          <label class="block text-white text-lg mb-1">Email</label>
          <input 
            v-model="email" 
            type="email" 
            class="input-field" 
            required 
            autocomplete="off" 
            placeholder="Enter your email"
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
            placeholder="Create a password"
          />
        </div>

        <div class="mb-4">
          <label class="block text-white text-lg mb-1">Role</label>
          <select v-model="role" class="input-field">
            <option value="student">Student</option>
            <option value="educator">Educator</option>
          </select>
        </div>

        <p v-if="errorMessage" class="text-red-400 text-center mb-4">{{ errorMessage }}</p>

        <button type="submit" class="btn-glass">Sign Up</button>
      </form>

      <p class="text-white text-center mt-4">
        Already have an account? <router-link to="/login" class="text-blue-300 hover:underline">Log in</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Background with dark-to-light gradient */
.bg-gradient-to-br {
  background: linear-gradient(to bottom right, #1a1a1a, #d3d3d3);
}

/* Glassmorphism container */
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
  background: rgba(255, 255, 255, 0.2); /* Improved contrast */
  border: 1px solid rgba(255, 255, 255, 0.3); /* Better visibility */
  outline: none;
  border-radius: 8px;
  transition: background 0.3s ease-in-out, border 0.3s ease-in-out;
}

.input-field:focus {
  background: rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

/* Glassmorphic button */
.btn-glass {
  width: 100%;
  padding: 12px;
  font-size: 18px;
  font-weight: bold;
  color: white;
  background: rgba(255, 255, 255, 0.3); /* Increased opacity */
  border: 1px solid rgba(255, 255, 255, 0.4); /* Added subtle border */
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease-in-out, border 0.3s ease-in-out;
}

.btn-glass:hover {
  background: rgba(255, 255, 255, 0.4); /* Slightly brighter on hover */
  border: 1px solid rgba(255, 255, 255, 0.6);
}

/* Role dropdown text color fix */
.input-field option {
  color: black;
}
</style>
