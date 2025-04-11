// src/components/GameBoard.js
import React from 'react';
import '../styles/GameBoard.css';

const GameBoard = ({ players, boardImage, positions, currentPlayer }) => {
  return (
    <div className="game-container">
      <div className="board-container">
        <img 
          src={boardImage} 
          alt="Monopoly Board" 
          className="board-image" 
        />
        
        {players.map((player, index) => {
          const isCurrent = player.username === currentPlayer;
          return (
            <div
              key={index}
              className={`player-token ${isCurrent ? 'active' : ''}`}
              style={{
                backgroundColor: player.color,
                top: positions[index]?.top || '50%',
                left: positions[index]?.left || '50%',
              }}
            >
              <span className="player-initial">
                {player.username.charAt(0).toUpperCase()}
              </span>
              {isCurrent && <div className="player-pulse"></div>}
            </div>
          );
        })}
      </div>
      
      <div className="player-panel">
        <h3>Players</h3>
        <div className="player-list">
          {players.map((player, index) => (
            <div 
              key={index} 
              className={`player-info ${player.username === currentPlayer ? 'current' : ''}`}
            >
              <div 
                className="player-color" 
                style={{ backgroundColor: player.color }}
              ></div>
              <span>{player.username}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default GameBoard;