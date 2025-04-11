// src/api/api.js
export const joinGameApi = async (username, color, sid) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/join', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, color, sid})
      });
      return await response.json(); // returns { success: true, players: [] }
    } catch (error) {
      console.error("Error joining game", error);
    }
  };
  
  export const startGameApi = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/start-game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      return await response.json(); // returns { success: true, positions: [] }
    } catch (error) {
      console.error("Error starting the game", error);
    }
  };
  