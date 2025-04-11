// src/components/Lobby.js
import React from 'react';
import '../styles/Lobby.css';

const Lobby = ({ players, startGame, currentPlayer }) => {
  const canStartGame = players.length >= 2 && players[0].username === currentPlayer;

  return (
    <div className="lobby-container">
      <div className="lobby-card">
        <h2>Game Lobby</h2>
        <p>Waiting for players to join...</p>
        
        <div className="players-grid">
          {players.map((player, index) => (
            <div 
              key={index} 
              className="player-badge"
              style={{ borderColor: player.color }}
            >
              <div 
                className="badge-color" 
                style={{ backgroundColor: player.color }}
              ></div>
              <span>{player.username}</span>
            </div>
          ))}
        </div>

        {canStartGame && (
          <button 
            onClick={startGame} 
            className="start-button"
          >
            Start Game
          </button>
        )}
        
        {!canStartGame && players.length > 0 && players[0].username !== currentPlayer && (
          <p className="waiting-message">Waiting for host to start the game...</p>
        )}
      </div>
    </div>
  );
};

export default Lobby;