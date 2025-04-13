import React, { useState } from 'react';
import '../styles/GameBoard.css';

const GameBoard = ({ 
  players = [], 
  boardImage = 'monopoly-board.png',
  positions = [], 
  currentPlayer = '',
  onRollDice = () => console.log('Roll dice'),
  onBuyProperty = () => console.log('Buy property'),
  onPayRent = () => console.log('Pay rent'),
  onEndTurn = () => console.log('End turn'),
  onTrade = () => console.log('Initiate trade'),
  gameState = {
    currentPlayer: '',
    players: [],
    currentProperty: null,
    currentAction: 'none',
    currentOwner: '',
    rentAmount: 0,
    diceRolled: false,
    canEndTurn: false,
    logs: []
  }
}) => {
  const [tradeModalOpen, setTradeModalOpen] = useState(false);
  const [selectedPlayer, setSelectedPlayer] = useState(null);

  // Current player actions
  const isCurrentTurn = gameState.currentPlayer === currentPlayer;
  const currentPosition = gameState.players.find(p => p.username === currentPlayer)?.position;

  return (
    <div className="game-container">
      {/* Main Game Board */}
      <div className="board-container">
        <img src={boardImage} alt="Monopoly Board" className="board-image" />
        
        {players.map((player, index) => (
          <PlayerToken 
            key={index}
            player={player}
            position={positions[index]}
            isCurrent={player.username === currentPlayer}
          />
        ))}
      </div>

      {/* Player Panel */}
      <div className="player-panel">
        <PlayerList 
          players={players} 
          currentPlayer={currentPlayer} 
          onTrade={setTradeModalOpen}
        />

        {/* Game Controls */}
        <div className="game-controls">
          {isCurrentTurn && (
            <>
              <button 
                onClick={onRollDice} 
                className="control-button roll-dice"
                disabled={gameState.diceRolled}
              >
                🎲 Roll Dice
              </button>
              
              {gameState.currentAction === 'can_buy' && (
                <PropertyPurchase 
                  property={gameState.currentProperty}
                  onBuy={onBuyProperty}
                  onDecline={onEndTurn}
                />
              )}

              {gameState.currentAction === 'pay_rent' && (
                <RentPayment 
                  property={gameState.currentProperty}
                  owner={gameState.currentOwner}
                  amount={gameState.rentAmount}
                  onPay={onPayRent}
                />
              )}

              <button 
                onClick={onEndTurn} 
                className="control-button end-turn"
                disabled={!gameState.canEndTurn}
              >
                ⏭️ End Turn
              </button>
            </>
          )}
        </div>

        {/* Game Log */}
        <div className="game-log">
          <h4>Game Log</h4>
          <div className="log-entries">
            {gameState.logs?.map((log, i) => (
              <div key={i} className="log-entry">{log}</div>
            ))}
          </div>
        </div>
      </div>

      {/* Trade Modal */}
      {tradeModalOpen && (
        <TradeModal
          players={players.filter(p => p.username !== currentPlayer)}
          onSelectPlayer={setSelectedPlayer}
          onClose={() => setTradeModalOpen(false)}
          onInitiateTrade={onTrade}
        />
      )}
    </div>
  );
};

// Sub-components
const PlayerToken = ({ player, position, isCurrent }) => (
  <div className={`player-token ${isCurrent ? 'active' : ''}`}
    style={{
      backgroundColor: player.color,
      top: position?.top || '50%',
      left: position?.left || '50%',
    }}>
    <span className="player-initial">{player.username.charAt(0).toUpperCase()}</span>
    {isCurrent && <div className="player-pulse"></div>}
  </div>
);

const PlayerList = ({ players, currentPlayer, onTrade }) => (
  <>
    <h3>Players</h3>
    <div className="player-list">
      {players.map((player, index) => (
        <div key={index} className={`player-info ${player.username === currentPlayer ? 'current' : ''}`}>
          <div className="player-color" style={{ backgroundColor: player.color }} />
          <span>{player.username}</span>
          <span className="player-cash">${player.money}</span>
          {player.username !== currentPlayer && (
            <button 
              onClick={() => onTrade(true)} 
              className="trade-button"
            >
              Trade
            </button>
          )}
        </div>
      ))}
    </div>
  </>
);

const PropertyPurchase = ({ property, onBuy, onDecline }) => (
  <div className="action-panel property-purchase">
    <h4>Property Available!</h4>
    <div className="property-info">
      <h5>{property.name}</h5>
      <p>Price: ${property.price}</p>
      <p>Rent: ${property.rent}</p>
      <p>Color Group: {property.color_group}</p>
    </div>
    <div className="action-buttons">
      <button onClick={onBuy} className="action-button buy">Buy Property</button>
      <button onClick={onDecline} className="action-button decline">Auction</button>
    </div>
  </div>
);

const RentPayment = ({ property, owner, amount, onPay }) => (
  <div className="action-panel rent-payment">
    <h4>Pay Rent!</h4>
    <div className="property-info">
      <h5>{property.name}</h5>
      <p>Owned by: {owner}</p>
      <p className="rent-amount">Amount Due: ${amount}</p>
    </div>
    <button onClick={onPay} className="action-button pay-rent">Pay ${amount}</button>
  </div>
);

const TradeModal = ({ players, onSelectPlayer, onClose, onInitiateTrade }) => (
  <div className="modal-overlay">
    <div className="trade-modal">
      <h3>Select Player to Trade With</h3>
      <div className="trade-players">
        {players.map(player => (
          <div key={player.username} className="trade-player-option">
            <button onClick={() => onSelectPlayer(player)}>
              {player.username} (${player.money})
            </button>
          </div>
        ))}
      </div>
      <div className="modal-actions">
        <button onClick={onClose} className="modal-button cancel">Cancel</button>
      </div>
    </div>
  </div>
);

export default GameBoard;