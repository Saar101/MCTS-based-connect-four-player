# 🧠 MCTS-Based Connect Four Player

> A competitive Connect Four AI implemented using **Monte Carlo Tree Search (MCTS)**  
> Designed for academic use and presented in a clean, professional GitHub format.

---

## 📌 Overview

This repository contains an implementation of a **Connect Four** playing agent based purely on  
**Monte Carlo Tree Search (MCTS)**.

The project was developed as part of an academic assignment with strict constraints:
- ✅ **MCTS only** (no Minimax, Alpha-Beta, or Neural Networks)
- ✅ **No modification** to the provided game logic
- ✅ Correct handling of terminal states, wins, losses, and draws
- ✅ Strong play as **both first (RED)** and **second (YELLOW)** player

---

## 🎯 Key Features

- ♟️ Full **Monte Carlo Tree Search** implementation (UCT-based)
- 🔁 Single shared game state using `make / unmake`
- 🧮 Correct backpropagation from the AI’s perspective
- 🚨 Immediate win detection and threat blocking
- 🎯 Deterministic optimal opening (center column)
- 🧪 Automated tests for correctness and stability
- 🧑 Human vs AI terminal gameplay

---

## 🧠 Monte Carlo Tree Search (MCTS)

The agent follows the standard four-stage MCTS pipeline:

### 1️⃣ Selection  
Traverses the tree using **UCT** to balance exploration and exploitation.

### 2️⃣ Expansion  
Expands one unexplored legal move.

### 3️⃣ Simulation (Rollout)  
Plays until a terminal state using random moves enhanced with light heuristics.

### 4️⃣ Backpropagation  
Propagates the result upward, updating visit counts and value estimates.

### 📐 UCT Formula
```
UCT = (value / visits) + c * sqrt(ln(parent_visits) / visits)
```

---

## ⚙️ Design Decisions

### 🔹 Single Shared Game State
- Nodes do **not** store game copies
- State traversal uses `make()` and `unmake()`
- Guarantees memory efficiency and correctness

### 🔹 Result Convention
- `+1` → RED wins  
- `-1` → YELLOW wins  
- `0` → Draw  

If the AI plays as **YELLOW**, results are flipped internally so the agent always maximizes its own outcome.

---

## 🚀 Heuristics (Assignment-Compliant)

The following heuristics significantly improve play quality while remaining within assignment rules:

- 🏆 **Immediate Win** – If a winning move exists, take it
- 🛑 **Immediate Block** – Block opponent’s one-move win
- 🎯 **Optimal Opening** – If AI starts as RED, always opens with column **3**

---

## 📁 Project Structure

```
.
├── connect_four_class.py   # Provided game logic (unchanged)
├── MCTSNode.py             # Tree node (statistics only)
├── MCTSPlayer.py           # MCTS implementation
├── play.py                 # Human vs AI gameplay
└── test_mcts.py            # Automated tests
```

---

## ▶️ Running the Project

### ▶️ Play Against the AI
```bash
py play.py
```

Choose whether you want to play as **RED** or **YELLOW**.

---

### 🧪 Run Automated Tests
```bash
py test_mcts.py
```

Tests validate:
- Game state restoration
- Terminal state handling
- Immediate win detection
- Valid move selection

---

## 🧪 Learning Behavior

- The agent **does not learn across games**
- Each move runs a fresh MCTS search
- No state or statistics are persisted

This behavior aligns with classical MCTS as taught in academic settings.

---

## 📚 Academic Context

This project was developed as part of a course on:
- Adversarial search
- Monte Carlo Tree Search
- Game AI design
- Correct state-space exploration

All implementation choices strictly follow assignment requirements.

---

## ✅ Summary

✔ Pure MCTS solution  
✔ Efficient state management  
✔ Strong play as first and second player  
✔ Deterministic and explainable behavior  
✔ Professional GitHub-ready structure  

---

## 👤 Author

**Saar Niran**  
Software Engineering B.Sc.  
Monte Carlo Tree Search – Connect Four
