// src/components/UserSetup.js
import React from 'react';
import '../styles/UserSetup.css';

const UserSetup = ({ username, setUsername, color, setColor, joinGame, isGameStarted }) => {
  return (
    <div id="user-setup">
      {!isGameStarted ? (
        <>
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
            value={color}
            onChange={(e) => setColor(e.target.value)}
          />
          <button onClick={joinGame}>Join Game</button>
        </>
      ) : (
        <button onClick={joinGame} disabled={isGameStarted}>Start Game</button>
      )}
    </div>
  );
};

export default UserSetup;
