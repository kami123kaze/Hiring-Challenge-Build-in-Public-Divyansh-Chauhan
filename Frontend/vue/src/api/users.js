import { db } from "../firebase/config";
import { doc, getDoc, setDoc } from "firebase/firestore";

// Get user profile
export const getUserProfile = async (userId) => {
  try {
    const userRef = doc(db, "users", userId);
    const userSnap = await getDoc(userRef);

    if (userSnap.exists()) {
      return userSnap.data();
    } else {
      return null; // User not found
    }
  } catch (error) {
    console.error("Error fetching user profile:", error);
    throw error;
  }
};

// Create or update user profile
export const saveUserProfile = async (userId, userData) => {
  try {
    const userRef = doc(db, "users", userId);
    await setDoc(userRef, userData, { merge: true });
    return { success: true };
  } catch (error) {
    console.error("Error saving user profile:", error);
    throw error;
  }
};
