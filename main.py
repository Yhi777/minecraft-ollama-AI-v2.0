import sys
import os
import time
import threading
import datetime
import random
import json
from connection.java_handler import JavaBot
from perception.world_scanner import WorldScanner
from action.movement_controller import NaturalMovementController
from ai.ollama_interface import OllamaAI
from learning.pytorch_model import LearningModule
from data_analytics.data_logger import DataLogger
from gui.main_gui import BotGUI

class UpgradedMinecraftAIBot:
    def __init__(self):
        self.bot_wrapper = None
        self.scanner = None
        self.movement = None
        self.ai = OllamaAI()
        self.learning = LearningModule()
        self.logger = DataLogger()
        self.gui = BotGUI()
        self.current_goal = "Explore, gather resources, and build a safe base"
        self.running = False
        self.autonomous_mode = False
        self.last_game_state = {}

    def start_bot(self, config):
        host = config.get('-IP-', 'localhost')
        port = config.get('-PORT-', '25565')
        username = config.get('-USERNAME-', 'SuperSmartBot')
        
        # Initialize Java connection
        self.bot_wrapper = JavaBot(host, port, username)
        self.bot_wrapper.connect()
        
        # Wait for connection to be established
        print("Waiting for bot to connect...")
        while not self.bot_wrapper.connected:
            time.sleep(1)
        
        # Initialize upgraded components
        self.scanner = WorldScanner(self.bot_wrapper.bot)
        self.movement = NaturalMovementController(self.bot_wrapper.bot)
        self.running = True
        
        # Start the main loop in a separate thread
        threading.Thread(target=self.main_loop, daemon=True).start()

    def main_loop(self):
        print("Upgraded AI main loop started.")
        while self.running:
            if not self.bot_wrapper or not self.bot_wrapper.connected:
                time.sleep(1)
                continue

            try:
                # 1. Perception: Advanced world and inventory scanning
                game_state = self.scanner.scan_surroundings(radius=8)
                inventory = self.scanner.get_inventory_summary()
                game_state['inventory'] = inventory
                self.last_game_state = game_state
                
                # 2. Decision Making (Autonomous Mode)
                action_data = {"action": "wait", "reason": "idle"}
                if self.autonomous_mode:
                    # Use Ollama for high-level reasoning with enhanced prompts
                    decision = self.ai.get_decision(game_state, self.current_goal)
                    action_data = decision
                    
                    # Use PyTorch for low-level skill optimization and learning
                    state_vector = self.get_advanced_state_vector(game_state)
                    ai_action_idx = self.learning.get_action(state_vector)
                    
                    # Execute action using the natural movement engine
                    self.execute_action(decision)
                    
                    # 3. Learning: Advanced training step
                    reward = self.calculate_sophisticated_reward(game_state, decision)
                    next_state_vector = self.get_advanced_state_vector(game_state)
                    loss = self.learning.train_step(state_vector, ai_action_idx, reward, next_state_vector, False)
                    
                    # 4. Data Logging
                    self.logger.log_activity(
                        datetime.datetime.now().isoformat(),
                        game_state['player_pos'],
                        decision.get('action', 'unknown'),
                        self.current_goal,
                        len(inventory),
                        game_state.get('health', 20)
                    )

                # 5. Natural Idle Behaviors (Anti-Bot)
                if not self.autonomous_mode or action_data.get('action') == 'wait':
                    self.movement.anti_bot_idle()

                # 6. Update GUI (This would ideally be via thread-safe events)
                # status_data = {
                #     'status': 'Online',
                #     'pos': game_state['player_pos'],
                #     'health': game_state.get('health', 20),
                #     'inv_count': len(inventory),
                #     'action': action_data.get('action', 'Idle'),
                #     'ai_log': action_data.get('thought', 'Thinking...')
                # }
                # self.gui.update_status(status_data)

            except Exception as e:
                print(f"Error in main loop: {e}")
            
            time.sleep(1)

    def execute_action(self, decision):
        action = decision.get('action')
        target_pos = decision.get('target_pos')
        
        if action == 'move' and target_pos:
            self.movement.move_to(target_pos['x'], target_pos['y'], target_pos['z'])
        elif action == 'chat':
            self.bot_wrapper.chat(decision.get('message', "I am exploring."))
        elif action == 'attack' and target_pos:
            self.movement.look_at(target_pos['x'], target_pos['y'], target_pos['z'])
            # Add attack logic here via bot_wrapper
        elif action == 'mine' and target_pos:
            self.movement.move_to(target_pos['x'], target_pos['y'], target_pos['z'], range_val=2)
            # Add mining logic here
        elif action == 'wait':
            self.movement.stop_moving()

    def get_advanced_state_vector(self, game_state):
        """Convert game state to a detailed 128-element vector for the upgraded PyTorch brain."""
        pos = game_state['player_pos']
        vector = [0.0] * 128
        
        # Position and basic stats
        vector[0] = pos['x'] / 1000.0
        vector[1] = pos['y'] / 256.0
        vector[2] = pos['z'] / 1000.0
        vector[3] = game_state.get('health', 20) / 20.0
        vector[4] = game_state.get('food', 20) / 20.0
        
        # Nearby block counts by classification
        blocks = game_state.get('blocks', [])
        vector[5] = len([b for b in blocks if b['type'] == 'resource_wood']) / 50.0
        vector[6] = len([b for b in blocks if b['type'] == 'resource_stone']) / 50.0
        vector[7] = len([b for b in blocks if 'hazard' in b['type']]) / 10.0
        
        # Nearby entity counts
        entities = game_state.get('entities', [])
        vector[8] = len([e for e in entities if e['classification'] == 'hostile']) / 5.0
        vector[9] = len([e for e in entities if e['classification'] == 'passive']) / 5.0
        
        # Inventory status
        inv = game_state.get('inventory', [])
        vector[10] = len(inv) / 36.0
        vector[11] = 1.0 if any(i['utility'] == 'tool' for i in inv) else 0.0
        
        # Rest is padding or can be used for more features
        return vector

    def calculate_sophisticated_reward(self, game_state, decision):
        """A more complex reward function considering survival and goal progress."""
        reward = 0.0
        action = decision.get('action')
        
        # Survival reward
        if game_state.get('health', 20) > self.last_game_state.get('health', 20):
            reward += 1.0  # Healed
        elif game_state.get('health', 20) < self.last_game_state.get('health', 20):
            reward -= 2.0  # Took damage
            
        # Goal-based rewards
        if action == 'mine' and len(game_state.get('inventory', [])) > len(self.last_game_state.get('inventory', [])):
            reward += 0.5  # Successfully gathered resource
            
        if action == 'move':
            reward += 0.01  # Small reward for exploring
            
        return reward

    def run(self):
        # The GUI run method is blocking and handles events
        self.gui.run(self.start_bot)

if __name__ == "__main__":
    app = UpgradedMinecraftAIBot()
    app.run()
