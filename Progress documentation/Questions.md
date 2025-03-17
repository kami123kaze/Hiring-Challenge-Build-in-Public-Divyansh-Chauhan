## What I Learned Along the Way
Getting everything to work together was the real challenge. Setting up Firebase Authentication and Firestore wasn’t too hard, but the tricky part was making sure the backend and frontend actually communicated properly. Firestore’s rules kept getting in the way, and debugging API calls was frustrating at times.

The gameboard itself took way longer than expected. Writing all the logic for how the scale tilts, how the weights behave, and making sure it all looked good took over 400 lines of CSS and JavaScript. It works, but I know the code could be cleaner.

Through all this, I’ve gotten much more comfortable with FastAPI, Vue.js, and Firestore. I’ve also learned that UI-related logic can be just as tricky as backend logic


## Design Decisions and Their Reasoning
Why balance Scale UI with CSS and JavaScript ?

I wanted full control over how the scale tilts, moves, and responds to weight changes. Using plain CSS and JavaScript instead of a library let me fine-tune the animations exactly how I wanted. Plus, it keeps the project lightweight.
Keeping the Backend Simple and Organized

FASTAPI structure 
Since I’m still learning FastAPI, I kept things as straightforward as possible. Instead of overcomplicating the API structure, I focused on making sure everything worked first—cleaning it up can come later.

Handling Firestore 

Firestore rules and structure gave me some trouble, so I kept things basic at first and refined them as I went along.(this lead to remkaing of rules almost 10+ times in debugging) I made sure users could only access their own data and that admin controls were set up properly.

About the elephant in the room (Gameboard.vue) will adress it in a diffrent file

I wanted the game to feel rewarding, so I added a streak system and difficulty-based points. This encourages players to challenge themselves while making progress feel more satisfying.similariy wanted a immersive landing page and tried to keep things user firendlt overall