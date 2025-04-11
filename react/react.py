import React, { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";

const BOARD_SIZE = 1500;
const PLAYER_COLORS = ["red", "blue", "green", "purple"];
const TOTAL_FIELDS = 40;

// Pretpostavljene koordinate polja u krugu (samo primjeri za sada)
const generateBoardPositions = () => {
  const positions = [];
  const padding = 80;
  const edge = BOARD_SIZE - padding;

  // Donja linija (10 polja)
  for (let i = 0; i < 10; i++) {
    positions.push({ x: edge - i * (edge / 10), y: edge });
  }
  // Lijeva strana
  for (let i = 1; i < 10; i++) {
    positions.push({ x: padding, y: edge - i * (edge / 10) });
  }
  // Gornja linija
  for (let i = 0; i < 10; i++) {
    positions.push({ x: padding + i * (edge / 10), y: padding });
  }
  // Desna strana
  for (let i = 1; i < 10; i++) {
    positions.push({ x: edge, y: padding + i * (edge / 10) });
  }

  return positions;
};

const boardPositions = generateBoardPositions();

export default function Ace7Monopol() {
  const [players, setPlayers] = useState([0, 0, 0, 0]); // pozicije igrača

  const rollDice = () => {
    setPlayers((prev) =>
      prev.map((pos) => (pos + Math.ceil(Math.random() * 6)) % TOTAL_FIELDS)
    );
  };

  return (
    <div
      className="relative"
      style={{ width: BOARD_SIZE, height: BOARD_SIZE, backgroundImage: "url('/monopoly-board.png')", backgroundSize: "cover" }}
    >
      {players.map((pos, i) => {
        const coords = boardPositions[pos];
        return (
          <motion.div
            key={i}
            className="absolute rounded-full w-8 h-8 border-2 border-white"
            style={{ backgroundColor: PLAYER_COLORS[i], left: coords.x, top: coords.y }}
            animate={{ left: coords.x, top: coords.y }}
            transition={{ duration: 0.5 }}
          />
        );
      })}

      <Button
        className="absolute bottom-10 left-1/2 -translate-x-1/2 px-6 py-3 text-lg"
        onClick={rollDice}
      >
        Baci kocku
      </Button>
    </div>
  );
}
