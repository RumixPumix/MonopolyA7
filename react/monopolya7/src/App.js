import React, { useState, useEffect } from 'react';
import './styles.css';
import { joinGameApi, startGameApi } from './api/api';
import UserSetup from './components/UserSetup';
import GameBoard from './components/GameBoard';
import Lobby from './components/Lobby'; // Importing the Lobby component
import io from 'socket.io-client';

const socket = io('http://127.0.0.1:5000'); // Connect to Flask backend via Socket.IO

const App = () => {
  const [isJoined, setIsJoined] = useState(false);
  const [players, setPlayers] = useState([]);
  const [username, setUsername] = useState('');
  const [color, setColor] = useState('');
  const [isGameStarted, setIsGameStarted] = useState(false);
  const [boardImage, setBoardImage] = useState('monopoly-board.png');
  const [positions, setPositions] = useState([]);

  useEffect(() => {

    const reconnectGame = async () => {
      const response = await fetch('http://127.0.0.1:5000/reconnect', {
        method: 'POST',
        credentials: 'include'  // <-- THIS is required
      });
      const data = await response.json();
    
      if (data.success) {
        if (data.game_started) {
          setUsername(data.username);
          setColor(data.color);
          setIsJoined(true);  // Allow them to join the game directly
        }
      } else {
        alert('Failed to reconnect');
      }
    };

    reconnectGame();

    // Listen for player updates via Socket.IO
    socket.on('update_players', (data) => {
      setPlayers(data.players);
    });
  
    socket.on('start_game', (data) => {
      console.log(data.message); // Log the message or update your state to reflect that the game has started
      setIsGameStarted(true); // Update state to start the game
    });
  
    return () => {
      socket.off('update_players'); // Clean up when the component is unmounted
      socket.off('game_started');
    };
  }, []);

  const joinGame = async () => {
    const response = await joinGameApi(username, color, socket.id);
    if (response.success) {
      setIsJoined(true);
    } else {
      alert('Failed to join the game');
    }
  };

  const startGame = async () => {
    const response = await startGameApi();
    if (response.success) {
      setPositions(response.positions);
      setIsGameStarted(true);
    } else {
      alert('Failed to start the game');
    }
  };

  return (
    <div id="game-container">
      {!isJoined ? (
        <UserSetup 
          username={username}
          setUsername={setUsername}
          color={color}
          setColor={setColor}
          joinGame={joinGame}
          startGame={startGame}
          isGameStarted={isGameStarted}
        />
      ) : isGameStarted ? (
        <GameBoard players={players} boardImage={boardImage} positions={positions} />
      ) : (
        <Lobby players={players} startGame={startGame} />
      )}
    </div>
  );
};

export default App;
