<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const activeSide = ref(null);

const goToLogin = () => {
  router.push(`/login`);
};

// Reset hover when mouse leaves
const resetHover = () => {
  activeSide.value = null;
};
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-800 p-6">
    <!-- Wrapper with dark gray margins -->
    <div 
      class="relative w-full max-w-5xl h-[80vh] flex rounded-xl overflow-hidden shadow-lg border border-gray-700 bg-gray-900"
      style="background-image: url('/public/3907915.jpg'); background-size: cover; background-position: center;"
      @mouseleave="resetHover"
    >
      <!-- Student Side -->
      <div
        class="w-1/2 flex items-center justify-center cursor-pointer transition-all duration-300 relative p-4"
        :class="{ 'brightness-100': activeSide === 'student', 'brightness-50': activeSide !== 'student' }"
        @mouseover="activeSide = 'student'"
        @click="goToLogin"
      >
        <div class="absolute inset-0 transition-opacity duration-300 bg-black"
          :class="{ 'opacity-50': activeSide !== 'student', 'opacity-0': activeSide === 'student' }">
        </div>
        <h2 class="text-2xl font-bold text-white relative z-10 bg-blue-600 px-6 py-2 rounded-lg shadow-md">
          Student
        </h2>
      </div>

      <!-- Wavy Divider -->
      <div class="absolute left-1/2 top-0 w-[5px] h-full bg-transparent">
        <svg
          class="absolute inset-0 w-full h-full"
          viewBox="0 0 10 100"
          preserveAspectRatio="none"
        >
          <path
            d="M5,0 C8,30 2,60 5,100"
            stroke="rgb(156, 163, 175)"
            stroke-width="2"
            fill="transparent"
          />
        </svg>
      </div>

      <!-- Educator Side -->
      <div
        class="w-1/2 flex items-center justify-center cursor-pointer transition-all duration-300 relative p-4"
        :class="{ 'brightness-100': activeSide === 'educator', 'brightness-50': activeSide !== 'educator' }"
        @mouseover="activeSide = 'educator'"
        @click="goToLogin"
      >
        <div class="absolute inset-0 transition-opacity duration-300 bg-black"
          :class="{ 'opacity-50': activeSide !== 'educator', 'opacity-0': activeSide === 'educator' }">
        </div>
        <h2 class="text-2xl font-bold text-white relative z-10 bg-blue-600 px-6 py-2 rounded-lg shadow-md">
          Educator
        </h2>
      </div>
    </div>
  </div>
</template>
