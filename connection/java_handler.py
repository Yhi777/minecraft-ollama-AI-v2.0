import os
import time
from javascript import require, On, Once, ASYNC, eval_js

# Load mineflayer and pathfinder
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder').pathfinder
Movements = require('mineflayer-pathfinder').Movements
goals = require('mineflayer-pathfinder').goals

class JavaBot:
    def __init__(self, host, port, username, version='1.21.1'):
        self.host = host
        self.port = port
        self.username = username
        self.version = version
        self.bot = None
        self.connected = False

    def connect(self):
        print(f"Connecting to {self.host}:{self.port} as {self.username} (v{self.version})...")
        self.bot = mineflayer.createBot({
            'host': self.host,
            'port': int(self.port),
            'username': self.username,
            'version': self.version,
            'hideErrors': False
        })

        # Load plugins
        self.bot.loadPlugin(pathfinder)

        @On(self.bot, 'spawn')
        def on_spawn(*args):
            print(f"Bot spawned at {self.bot.entity.position}")
            self.connected = True
            # Set up movements
            mc_data = require('minecraft-data')(self.bot.version)
            movements = Movements(self.bot, mc_data)
            self.bot.pathfinder.setMovements(movements)

        @On(self.bot, 'kicked')
        def on_kicked(reason, loggedIn, *args):
            print(f"Bot kicked: {reason}")
            self.connected = False

        @On(self.bot, 'error')
        def on_error(err, *args):
            print(f"Bot error: {err}")

    def disconnect(self):
        if self.bot:
            self.bot.quit()
            self.connected = False

    def get_position(self):
        if self.bot and self.bot.entity:
            pos = self.bot.entity.position
            return {'x': pos.x, 'y': pos.y, 'z': pos.z}
        return None

    def get_inventory(self):
        if not self.bot or not self.bot.inventory:
            return []
        items = self.bot.inventory.items()
        inventory_data = []
        for item in items:
            inventory_data.append({
                'name': item.name,
                'count': item.count,
                'slot': item.slot
            })
        return inventory_data

    def move_to(self, x, y, z):
        if not self.bot:
            return
        goal = goals.GoalNear(x, y, z, 1)
        self.bot.pathfinder.setGoal(goal)

    def chat(self, message):
        if self.bot:
            self.bot.chat(message)

    def look_at(self, x, y, z):
        if self.bot:
            self.bot.lookAt(eval_js(f"new (require('vec3'))({x}, {y}, {z})"))
