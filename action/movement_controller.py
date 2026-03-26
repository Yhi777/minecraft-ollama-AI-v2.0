import random
import time
import math
from javascript import require, eval_js

class NaturalMovementController:
    def __init__(self, bot):
        self.bot = bot
        self.pathfinder = bot.pathfinder
        self.goals = require('mineflayer-pathfinder').goals
        self.is_moving = False
        self.last_move_time = time.time()
        self.jitter_range = 0.1  # Random movement deviation
        self.movement_mode = 'natural'  # 'natural', 'stealth', 'sprint'

    def move_to(self, x, y, z, range_val=1):
        """Move to a position with natural human-like behavior."""
        if not self.bot:
            return

        # Add natural jitter to the target position to avoid exact coordinates
        target_x = x + random.uniform(-self.jitter_range, self.jitter_range)
        target_z = z + random.uniform(-self.jitter_range, self.jitter_range)
        
        # Select movement mode based on distance and environment
        current_pos = self.bot.entity.position
        dist = math.sqrt((x - current_pos.x)**2 + (z - current_pos.z)**2)
        
        if dist > 10:
            self.bot.setControlState('sprint', True)
        else:
            self.bot.setControlState('sprint', False)

        # Natural movement patterns (anti-bot)
        # 1. Random look-around while moving
        if random.random() < 0.05:
            self.bot.lookAt(eval_js(f"new (require('vec3'))({x + random.randint(-5, 5)}, {y + random.randint(-2, 2)}, {z + random.randint(-5, 5)})"))

        # 2. Occasional jump (natural parkour)
        if random.random() < 0.02 and dist > 2:
            self.bot.setControlState('jump', True)
            time.sleep(0.1)
            self.bot.setControlState('jump', False)

        # 3. Use pathfinder for navigation
        goal = self.goals.GoalNear(target_x, y, target_z, range_val)
        self.pathfinder.setGoal(goal)
        self.is_moving = True
        self.last_move_time = time.time()

    def stop_moving(self):
        self.pathfinder.setGoal(None)
        self.bot.clearControlStates()
        self.is_moving = False

    def look_at(self, x, y, z):
        """Look at a position with natural speed and smoothing."""
        # mineflayer's lookAt is relatively smooth, but we can add small offsets
        target_vec = eval_js(f"new (require('vec3'))({x + random.uniform(-0.1, 0.1)}, {y + random.uniform(-0.1, 0.1)}, {z + random.uniform(-0.1, 0.1)})")
        self.bot.lookAt(target_vec)

    def anti_bot_idle(self):
        """Perform natural idle behaviors when not moving."""
        if self.is_moving:
            return

        now = time.time()
        if now - self.last_move_time > 5:
            # Randomly look around
            if random.random() < 0.1:
                self.bot.lookAt(eval_js(f"new (require('vec3'))({self.bot.entity.position.x + random.randint(-10, 10)}, {self.bot.entity.position.y + random.randint(-5, 5)}, {self.bot.entity.position.z + random.randint(-10, 10)})"))
            
            # Occasional slight shift
            if random.random() < 0.05:
                dx = random.uniform(-0.5, 0.5)
                dz = random.uniform(-0.5, 0.5)
                self.move_to(self.bot.entity.position.x + dx, self.bot.entity.position.y, self.bot.entity.position.z + dz)
            
            self.last_move_time = now
