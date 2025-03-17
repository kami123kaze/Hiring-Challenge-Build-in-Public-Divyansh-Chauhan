import { db } from "../firebase/config";
import { doc, getDoc, setDoc, updateDoc } from "firebase/firestore";

// Fetch existing game session for a student
export const getGameSession = async (userId) => {
  try {
    const sessionRef = doc(db, "game_sessions", userId);
    const sessionSnap = await getDoc(sessionRef);

    if (sessionSnap.exists()) {
      return sessionSnap.data();
    } else {
      return null; // No session found
    }
  } catch (error) {
    console.error("Error fetching game session:", error);
    throw error;
  }
};

// Create a new game session
export const createGameSession = async (userId, initialData) => {
  try {
    const sessionRef = doc(db, "game_sessions", userId);
    await setDoc(sessionRef, initialData);
    return { success: true };
  } catch (error) {
    console.error("Error creating game session:", error);
    throw error;
  }
};

// Update an ongoing game session
export const updateGameSession = async (userId, newData) => {
  try {
    const sessionRef = doc(db, "game_sessions", userId);
    await updateDoc(sessionRef, newData);
    return { success: true };
  } catch (error) {
    console.error("Error updating game session:", error);
    throw error;
  }
};
