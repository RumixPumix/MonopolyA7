import React from 'react';

const PlayerBox = ({ player }) => {
    const playerStyle = {
        backgroundColor: player.color,
        width: '30px',
        height: '30px',
        borderRadius: '5px',
        margin: '2px',
    };

    return <div className="player" style={playerStyle}></div>;
};

export default PlayerBox;
