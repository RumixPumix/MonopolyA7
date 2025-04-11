import React from 'react';

const Lobby = ({ players, startGame }) => {
  return (
    <div id="lobby-container">
      <h2>Lobby</h2>
      <h3>Players</h3>
      <ul id="players-list">
        {players.map((player, index) => (
          <li key={index} style={{ color: player.color }}>
            {player.username}
          </li>
        ))}
      </ul>
      <button onClick={startGame} id="start-game-btn">
        Start Game
      </button>
    </div>
  );
};

export default Lobby;
