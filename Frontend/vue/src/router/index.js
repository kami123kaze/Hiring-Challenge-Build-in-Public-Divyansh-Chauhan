import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/Login.vue";
import Game from "../components/Game.vue";
import StudentDashboard from "../views/StudentDashboard.vue";
import Landing from "../components/Landing.vue"
import SignUp from "../components/SignUp.vue";
import TeacherDashboard from "../components/TeacherDashboard.vue";

const routes = [
  { path: "/", component: Landing },
  { path: "/login", component: Login},
  { path: "/game", component: Game },
  { path: "/student-dashboard", component: StudentDashboard },
  {path: "/signup", component: SignUp},
  {path:"/educator-dashboard", component: TeacherDashboard}
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
