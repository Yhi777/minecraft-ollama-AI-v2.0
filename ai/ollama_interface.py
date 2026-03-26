import requests
import json
import time

class OllamaAI:
    def __init__(self, endpoint="http://localhost:11434", model="llama2"):
        self.endpoint = f"{endpoint}/api/generate"
        self.model = model
        self.history = []
        self.max_history = 10

    def set_model(self, model_name):
        self.model = model_name

    def set_endpoint(self, endpoint):
        self.endpoint = f"{endpoint}/api/generate"

    def ask(self, prompt, context=None):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_ctx": 4096
            }
        }
        if context:
            payload["context"] = context

        try:
            response = requests.post(self.endpoint, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result.get("response", ""), result.get("context", [])
            else:
                return f"Error: {response.status_code} - {response.text}", []
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}", []

    def get_decision(self, game_state, current_goal):
        # Enhanced prompt for "super smart" behavior
        prompt = f"""
        System: You are an autonomous Minecraft AI player with critical thinking and problem-solving skills.
        Current Goal: {current_goal}
        
        Perception Data:
        - Position: {game_state.get('player_pos')}
        - Health: {game_state.get('health', 20)}/20
        - Inventory: {game_state.get('inventory', [])}
        - Nearby Blocks: {game_state.get('blocks', [])[:10]}
        - Nearby Entities: {game_state.get('entities', [])[:5]}
        
        Strategic Reasoning:
        1. Analyze current situation and resource availability.
        2. Identify immediate threats or obstacles.
        3. Determine the most efficient sequence of actions to reach the goal.
        
        Response Format (Strict JSON):
        {{
            "thought": "Your reasoning process...",
            "action": "move|mine|place|attack|craft|chat|wait",
            "reason": "Why this action?",
            "target_pos": {{"x": 0.0, "y": 0.0, "z": 0.0}},
            "target_item": "item_name",
            "message": "Chat message if action is chat"
        }}
        """
        
        response_text, context = self.ask(prompt)
        
        # Add to history for contextual memory
        self.history.append({"prompt": prompt, "response": response_text})
        if len(self.history) > self.max_history:
            self.history.pop(0)
            
        try:
            # Clean response text and parse JSON
            json_str = response_text.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()
            
            decision = json.loads(json_str)
            return decision
        except Exception as e:
            print(f"Failed to parse Ollama response: {e}")
            return {
                "thought": "Failed to parse AI response, defaulting to wait.",
                "action": "wait",
                "reason": "parse_error",
                "target_pos": None
            }
