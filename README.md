# Minecraft Autonomous AI Bot - Advanced Edition

## 1. Project Overview

This project is a sophisticated, autonomous AI player for Minecraft (Java Edition 1.21.1 and Bedrock Edition offline multiplayer). It integrates cutting-edge AI technologies to provide a "super smart" experience with natural movements, self-learning capabilities, and real-time environmental awareness.

### Key Components:
- **Ollama AI Integration**: Uses local Large Language Models for high-level reasoning, strategy, and problem-solving.
- **PyTorch Self-Learning**: A deep reinforcement learning brain that improves its efficiency in gathering resources, building, and surviving over time.
- **Natural Movement Engine**: Implements human-like movement patterns, avoiding the robotic look of traditional bots.
- **Real-time World Perception**: Scans the surrounding blocks and entities using positional data to build a 3D understanding of the environment.
- **Building Sub-module**: Allows the AI to construct complex structures with high accuracy and speed.
- **FreeSimpleGUI Dashboard**: A comprehensive user interface for monitoring and controlling every aspect of the AI.

## 2. Installation and Setup

The project is designed for easy setup using Conda and a dedicated batch script.

### Prerequisites:
1. **Conda**: Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/).
2. **Node.js**: Required for the `mineflayer` bridge that connects to Minecraft Java Edition.
3. **Ollama**: Install [Ollama](https://ollama.ai/) and download a model (e.g., `llama2` or `mistral`).

### Quick Start:
1. Extract the project ZIP file.
2. Double-click `run.bat`. This will:
   - Create a Conda environment named `minecraft_ai_bot`.
   - Install all necessary Python packages (PyTorch, Pandas, FreeSimpleGUI, etc.).
   - Install Node.js dependencies (`mineflayer`, `mineflayer-pathfinder`).
   - Launch the application GUI.

## 3. Usage Instructions

### Connecting to a Server:
- **Java Edition**: Enter the server IP and port in the GUI and click **Connect**. The bot will join as a regular player.
- **Bedrock Edition**: The bot is designed to join local multiplayer worlds. Ensure your Bedrock world is open to LAN.

### Autonomous Mode:
- Set a high-level goal (e.g., "Build a stone tower" or "Gather 64 iron ore").
- Click **Start Autonomous Mode**. The AI will begin processing the environment and executing actions to achieve the goal.

### Monitoring Performance:
- The **Real-time Status** panel shows the bot's position, health, inventory, and current action.
- The **AI Log** displays the reasoning process from the Ollama model.
- Click **Generate Analytics Spreadsheet** to export a detailed CSV/Excel report of the bot's activities and learning progress.

## 4. Technical Architecture

### Perception Module
The bot uses a "non-visual" perception system. It queries the Minecraft server for block data within a specific radius and maintains an internal map. This allows it to "see" through walls and optimize its pathfinding.

### Learning Pipeline
The PyTorch model (`models/advanced_brain_v1.pth`) uses a custom neural network to map environmental states to optimal actions. Every action taken is rewarded or penalized, and the model is updated in real-time.

### Ollama Integration
When the bot encounters a complex problem (e.g., "How do I cross this lava lake?"), it sends a prompt to Ollama. The response is parsed into a sequence of low-level actions that the bot then executes.

## 5. Troubleshooting

- **Connection Failed**: Ensure the Minecraft server version matches (1.21.1) and that no firewall is blocking the connection.
- **Ollama Not Responding**: Verify that the Ollama service is running and that the endpoint URL in the GUI is correct.
- **Slow Performance**: The PyTorch training and Ollama inference can be resource-intensive. Ensure your machine has sufficient RAM and CPU/GPU power.

---
Developed by ME, for AI advanced Minecraft automation.
