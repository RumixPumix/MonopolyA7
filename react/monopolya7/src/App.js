import React, { useState, useEffect } from 'react';
import './styles.css';
import { joinGameApi, startGameApi } from './api/api';
import UserSetup from './components/UserSetup';
import GameBoard from './components/GameBoard';
import Lobby from './components/Lobby';
import io from 'socket.io-client';

const socket = io('http://127.0.0.1:5000', {
  withCredentials: true,
  reconnection: true,
  reconnectionAttempts: Infinity,
  reconnectionDelay: 1000,
  transports: ['websocket', 'polling'],
  autoConnect: true,
  extraHeaders: {
    "Access-Control-Allow-Origin": "http://localhost:3000"
  }
});

const App = () => {
  const [isJoined, setIsJoined] = useState(false);
  const [players, setPlayers] = useState([]);
  const [username, setUsername] = useState('');
  const [color, setColor] = useState('');
  const [isGameStarted, setIsGameStarted] = useState(false);
  const [boardImage, setBoardImage] = useState('monopoly-board.png');
  const [positions, setPositions] = useState([]);
  const [gameState, setGameState] = useState({
    currentPlayer: '',
    players: [],
    currentProperty: null,
    currentAction: 'none',
    currentOwner: '',
    rentAmount: 0,
    diceRolled: false,
    canEndTurn: false,
    logs: []
  });

  // Game action handlers
  const handleRollDice = () => socket.emit('roll_dice');
  const handleBuyProperty = () => socket.emit('buy_property');
  const handlePayRent = () => socket.emit('pay_rent');
  const handleEndTurn = () => socket.emit('end_turn');
  const handleInitiateTrade = (player) => socket.emit('initiate_trade', { target: player.username });

  useEffect(() => {
    const reconnectGame = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/reconnect', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        const data = await response.json();
        
        if (data.success) {
          if (data.username) {
            setUsername(data.username);
            setColor(data.color);
            setIsJoined(true);
            setPlayers(data.players || []);
            setIsGameStarted(data.game_started || false);
            
            if (data.game_started) {
              socket.emit('request_game_state');
            }
          }
        }
      } catch (error) {
        console.error('Reconnection error:', error);
      }
    };

    if (!username) {
      reconnectGame();
    }

    socket.on('connect', () => {
      console.log('Connected to server with socket ID:', socket.id);
      if (username) {
        socket.emit('update_sid', { username, sid: socket.id });
      }
    });

    socket.on('update_players', (data) => {
      setPlayers(data.players);
    });

    socket.on('start_game', (data) => {
      setIsGameStarted(true);
      if (data.positions) {
        setPositions(data.positions);
      }
    });

    socket.on('game_state', (data) => {
      setGameState(prev => ({
        ...prev,
        ...data,
        players: data.players || prev.players,
        logs: data.logs || prev.logs
      }));
      if (data.players) setPlayers(data.players);
      if (data.positions) setPositions(data.positions);
      setIsGameStarted(true);
    });

    return () => {
      socket.off('connect');
      socket.off('update_players');
      socket.off('start_game');
      socket.off('game_state');
    };
  }, [username]);

  const joinGame = async () => {
    const response = await joinGameApi(username, color, socket.id);
    if (response.success) {
      setIsJoined(true);
      setPlayers(response.players || []);
    } else {
      alert(response.error || 'Failed to join the game');
    }
  };

  const startGame = async () => {
    const response = await startGameApi();
    if (response.success) {
      setPositions(response.positions);
      setIsGameStarted(true);
    } else {
      alert(response.error || 'Failed to start the game');
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
        />
      ) : isGameStarted ? (
        <GameBoard 
          players={players} 
          boardImage={boardImage} 
          positions={positions} 
          currentPlayer={username}
          gameState={gameState}
          onRollDice={handleRollDice}
          onBuyProperty={handleBuyProperty}
          onPayRent={handlePayRent}
          onEndTurn={handleEndTurn}
          onTrade={handleInitiateTrade}
        />
      ) : (
        <Lobby 
          players={players} 
          startGame={startGame} 
          currentPlayer={username}
        />
      )}
    </div>
  );
};

export default App;