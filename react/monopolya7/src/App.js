import React, { useState, useEffect } from 'react';
import './styles.css';
import { io } from 'socket.io-client';

// Initialize the SocketIO client
const socket = io('http://127.0.0.1:5000');

const App = () => {
  const [isJoined, setIsJoined] = useState(false);
  const [players, setPlayers] = useState([]);
  const [username, setUsername] = useState('');
  const [color, setColor] = useState('');

  useEffect(() => {
    // Listen for updates to the players list
    socket.on('update_players', (data) => {
      setPlayers(data.players);
    });

    // Clean up the socket connection when the component is unmounted
    return () => {
      socket.off('update_players');
    };
  }, []);

  const joinGame = async () => {
    console.log('Username:', username);  // Ensure the username is being logged
    console.log('Color:', color);        // Ensure the color is being logged
    
    const response = await fetch('http://127.0.0.1:5000/join', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, color })  // Ensure color is being sent in the request
    });
    
    const data = await response.json();
    
    if (data.success) {
      setPlayers(data.players);
      setIsJoined(true);
    } else {
      alert('Failed to join the game');
    }
  };

  return (
    <div id="game-container">
      {!isJoined ? (
        <div id="user-setup">
          <input 
            type="text" 
            id="username" 
            placeholder="Enter username" 
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input 
            type="color" 
            id="color-picker" 
            value={color} // This binds the input to the state
            onChange={(e) => setColor(e.target.value)} // Ensure color is updated correctly
          />
          <button onClick={joinGame}>Join Game</button>
        </div>
      ) : (
        <div id="game-board">
          <div id="players-container">
            {players.map((player) => (
              <div key={player.username} className="player" style={{ backgroundColor: player.color }}>
                {player.username}
              </div>
            ))}
          </div>
          <button id="roll-dice">Roll Dice</button>
        </div>
      )}
    </div>
  );
};

export default App;
