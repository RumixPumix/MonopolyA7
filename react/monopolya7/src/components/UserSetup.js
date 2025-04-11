// src/components/UserSetup.js
import React from 'react';
import '../styles/UserSetup.css';

const UserSetup = ({ username, setUsername, color, setColor, joinGame }) => {
  return (
    <div className="setup-container">
      <div className="setup-card">
        <h2>Join Monopoly Game</h2>
        <div className="input-group">
          <label htmlFor="username">Player Name</label>
          <input
            type="text"
            id="username"
            placeholder="Enter your name"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="input-group">
          <label htmlFor="color-picker">Choose Color</label>
          <div className="color-picker-container">
            <input
              type="color"
              id="color-picker"
              value={color}
              onChange={(e) => setColor(e.target.value)}
            />
            <span className="color-value">{color || '#000000'}</span>
          </div>
        </div>
        <button 
          onClick={joinGame} 
          className="join-btn"
          disabled={!username || !color}
        >
          Join Game
        </button>
      </div>
    </div>
  );
};

export default UserSetup;