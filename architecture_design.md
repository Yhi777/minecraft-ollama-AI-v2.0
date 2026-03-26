# Minecraft Autonomous AI Bot - Advanced Architecture Design (Upgrade v2.0)

## 1. Introduction

This document details the upgraded architectural design for an autonomous AI bot for Minecraft, targeting enhanced intelligence, more natural player movements, and improved self-learning capabilities. The bot will continue to operate in both Java Edition (1.21.1) and Bedrock Edition (offline multiplayer), featuring deeper integration with Ollama for advanced reasoning, a more sophisticated PyTorch learning model, refined real-time world and inventory scanning, precise building, and an enriched FreeSimpleGUI interface. The project maintains its automated setup via Conda and a `run.bat` script.

## 2. Core Components - Upgrades

Each module has been enhanced to contribute to a more "super smart" and "natural" AI experience.

### 2.1. Minecraft Connection Layer

(No significant changes to this layer, as its primary function is protocol abstraction.)

*   **Java Edition Handler**: Connects to Java servers (requiring IP and Port). Utilizes `mineflayer` for robust interaction.
*   **Bedrock Edition Handler**: Connects to local Bedrock worlds for offline multiplayer. This remains a placeholder for future direct implementation or integration with a Bedrock-specific client library.

### 2.2. Perception Module - Enhanced

Responsible for gathering and interpreting real-time information from the Minecraft world and the bot's inventory with greater depth.

*   **World Scanner**: Scans the surrounding environment, identifying blocks, entities, and terrain features. This module now not only provides raw positional data but also performs initial classification based on utility (e.g., `resource_wood`, `resource_stone`), threat level (`hostile_mob`, `neutral_mob`), and environmental context (`is_cave`, `is_water_body`, `is_open_field`). The AI still operates without visual input, relying solely on structured data from the game engine.
*   **Inventory Scanner**: Tracks the bot's inventory in real-time, including item types, quantities, durability, and now also assesses the **utility** of items relative to current goals (e.g., `has_pickaxe_for_stone`, `enough_wood_for_crafting`).

### 2.3. Action Module - Refined

Translates AI decisions into more natural and effective in-game actions.

*   **Movement Controller - Natural & Anti-Bot**: Handles advanced player movements (walking, running, jumping, swimming, flying, pathfinding). This module now incorporates:
    *   **Jitter**: Slight, random deviations in movement paths to mimic human imperfection.
    *   **Varied Speeds**: Dynamic adjustment of movement speed based on context (e.g., sprinting in open areas, slow walking in dangerous zones).
    *   **Anti-Bot Patterns**: Algorithms to avoid repetitive or predictable movement, including random pauses, detours, and changes in direction.
    *   **Advanced Pathfinding**: Utilizes more sophisticated algorithms that consider not just shortest distance but also terrain traversability, potential hazards (lava, cliffs), and resource locations.
*   **Interaction Handler**: Manages interactions with the world (breaking blocks, placing blocks, using items, attacking entities, opening chests, crafting).
*   **Building Sub-module**: Focuses on precise and accurate block placement for construction tasks, ensuring perfect builds. Enhanced with pattern recognition for common structures and error correction mechanisms.

### 2.4. AI/Decision-Making Module - Upgraded

The core intelligence of the bot, now with deeper reasoning and more robust decision-making capabilities.

*   **Ollama Integration - Enhanced Reasoning**: Interfaces with a local Ollama instance for advanced natural language understanding, strategic planning, and complex problem-solving. Prompts are now more elaborate, providing richer context about the game state, current goals, and available actions. Responses are strictly enforced to a **JSON schema** for reliable parsing and action execution.
*   **Contextual Memory**: Implements a mechanism to feed previous interactions, decisions, and outcomes back into Ollama as context, enabling more coherent and long-term planning.
*   **Goal Management**: Prioritizes and manages a dynamic list of tasks and objectives (e.g., gather resources, build a house, explore) with a more adaptive priority system.
*   **Problem Solving & Critical Thinking**: Enables the bot to adapt to unexpected situations, overcome obstacles, and make flexible decisions based on a deeper understanding of the environment and its goals.
*   **Self-Decision Making**: Allows the bot to act autonomously based on its current understanding and goals, with a higher degree of independence.

### 2.5. Learning Module - Advanced

Enables the bot to learn and improve over time with a more powerful PyTorch model and sophisticated training.

*   **PyTorch Model - Deeper Architecture**: The `MinecraftBrain` now features a significantly deeper neural network architecture with more layers and neurons, allowing for more complex pattern recognition and nuanced decision-making. This enables the bot to learn optimal strategies for a wider range of Minecraft tasks.
*   **Improved Training Loop**: Incorporates more sophisticated reinforcement learning techniques (e.g., Proximal Policy Optimization (PPO) or Advantage Actor-Critic (A2C)) for more stable and efficient learning. The reward function is enhanced to consider long-term goals, survival metrics, and resource efficiency.
*   **Enhanced State Representation**: The `get_state_vector` function now includes more nuanced environmental data, such as relative positions of important blocks/entities, recent changes in the environment, and a more comprehensive inventory utility assessment.
*   **Data Collection & Preprocessing**: Gathers rich in-game data (observations, actions, rewards) to train the PyTorch model, with improved filtering and normalization.
*   **Model Training & Updates**: Manages the training process for the PyTorch model, including periodic updates, fine-tuning, and potentially transfer learning from pre-existing Minecraft datasets.

### 2.6. Data Logging & Analytics Module

Records and analyzes the bot's performance and learning progress with enhanced metrics.

*   **Spreadsheet Data Generation**: Automatically creates and updates spreadsheet data based on collected in-game metrics, learning progress, and decision-making patterns. Now includes more detailed metrics on movement efficiency, building accuracy, and resource management.
*   **Performance Monitoring**: Tracks key performance indicators (KPIs) such as resource gathering rates, building efficiency, survival time, and learning curve progression.
*   **Pth Model Development Tracking**: Logs the evolution and performance of the PyTorch model over time, including training loss, reward curves, and model versioning.

### 2.7. User Interface (FreeSimpleGUI) - Enriched

A graphical user interface for monitoring and controlling the bot with more advanced features.

*   **Real-time Status Display**: Shows current bot activities, inventory, health, coordinates, active goals, and now also displays key learning metrics (e.g., current reward, loss).
*   **Ollama Interaction Log**: A dedicated section to display the prompts sent to Ollama and its raw responses, aiding in debugging and understanding AI decisions.
*   **Control Panel - Advanced**: Provides more granular controls for starting/stopping the bot, setting specific sub-goals, adjusting learning rates, and toggling AI modules (e.g., enable/disable natural movement jitter).
*   **Data Visualization**: Displays interactive charts or graphs based on the spreadsheet data for performance analysis and learning progress visualization.

## 3. Project Structure

(The directory structure remains largely the same, but files within modules will be updated to reflect the new functionalities.)

```
minecraft_ai_bot/
├── run.bat
├── environment.yml  # Conda environment definition
├── main.py          # Main application entry point
├── config.py        # Configuration settings
├── gui/             # FreeSimpleGUI interface files
│   └── main_gui.py
├── connection/      # Minecraft connection handlers
│   ├── java_handler.py
│   └── bedrock_handler.py
├── perception/      # World and inventory scanning
│   ├── world_scanner.py
│   └── inventory_scanner.py
├── action/          # Movement, interaction, and building
│   ├── movement_controller.py
│   ├── interaction_handler.py
│   └── building_submodule.py
├── ai/              # Ollama integration and decision-making
│   ├── ollama_interface.py
│   └── decision_maker.py
├── learning/        # PyTorch model and training
│   ├── pytorch_model.py
│   └── data_collector.py
├── data_analytics/  # Data logging and spreadsheet generation
│   ├── data_logger.py
│   └── spreadsheet_generator.py
├── utils/           # Utility functions
└── models/          # Trained PyTorch models, Ollama custom models
```

## 4. Technologies Used

*   **Python**: Primary programming language.
*   **Ollama**: For local LLM inference and advanced AI reasoning.
*   **PyTorch**: For the self-learning capabilities (reinforcement learning).
*   **FreeSimpleGUI**: For the user interface.
*   **Conda**: For environment management and dependency resolution.
*   **Minecraft Client Libraries**: `mineflayer` (Node.js) for Java Edition interaction.

## 5. Development Plan - Upgraded

1.  **Phase 1: Analyze current AI and design upgrades (Current)**
2.  **Phase 2: Upgrade PyTorch model**: Implement deeper architecture, improved training loop, and enhanced state representation.
3.  **Phase 3: Enhance Ollama integration**: Implement more detailed reasoning prompts, JSON schema enforcement, and contextual memory.
4.  **Phase 4: Implement advanced natural movement engine**: Incorporate jitter, varied speeds, anti-bot patterns, and advanced pathfinding.
5.  **Phase 5: Refine perception system**: Improve block/entity classification and environmental context inference.
6.  **Phase 6: Update FreeSimpleGUI**: Add advanced controls, real-time learning metrics, and Ollama interaction log.
7.  **Phase 7: Re-assemble, test, and zip the upgraded project**: Integrate all enhanced modules, perform thorough testing, and package the project (ensuring 4MB+ size).
8.  **Phase 8: Deliver upgraded project to user**.

This upgraded architecture provides a significantly more intelligent, adaptable, and natural-acting Minecraft AI bot, pushing the boundaries of autonomous gameplay. The modular design facilitates targeted enhancements and continuous improvement.
