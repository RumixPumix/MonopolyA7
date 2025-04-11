// src/components/GameBoard.js
import React from 'react';
import '../styles/GameBoard.css';

const GameBoard = ({ players, boardImage, positions }) => {
  return (
    <div id="game-board">
      <img src={boardImage} alt="Game Board" className="board-image" />
      <div id="players-container">
        {players.map((player, index) => {
          const playerPosition = positions[index] || { top: '0px', left: '0px' };
          return (
            <div
              key={index}
              className="player"
              style={{
                backgroundColor: player.color,
                position: 'absolute',
                top: playerPosition.top,
                left: playerPosition.left,
              }}
            >
              {player.username}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default GameBoard;
