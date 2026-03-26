from javascript import require

class WorldScanner:
    def __init__(self, bot):
        self.bot = bot
        self.mc_data = require('minecraft-data')(bot.version)

    def classify_block(self, block_name):
        """Classify blocks based on their utility for 'super smart' AI reasoning."""
        classification = 'other'
        if 'wood' in block_name or 'log' in block_name or 'planks' in block_name:
            classification = 'resource_wood'
        elif 'stone' in block_name or 'cobblestone' in block_name or 'ore' in block_name:
            classification = 'resource_stone'
        elif 'water' in block_name:
            classification = 'environmental_hazard_water'
        elif 'lava' in block_name:
            classification = 'environmental_hazard_lava'
        elif 'chest' in block_name:
            classification = 'container'
        elif 'crafting_table' in block_name:
            classification = 'utility_crafting'
        elif 'furnace' in block_name:
            classification = 'utility_smelting'
        return classification

    def classify_entity(self, entity_name, entity_type):
        """Classify entities based on their threat level or utility."""
        classification = 'neutral'
        if entity_type == 'mob':
            hostile_mobs = ['zombie', 'skeleton', 'creeper', 'spider', 'enderman', 'witch', 'slime', 'drowned', 'husk']
            if any(mob in entity_name.lower() for mob in hostile_mobs):
                classification = 'hostile'
            else:
                classification = 'passive'
        elif entity_type == 'player':
            classification = 'player'
        elif entity_type == 'object':
            classification = 'item_drop'
        return classification

    def scan_surroundings(self, radius=8):
        """Perform a detailed 3D scan of the environment with classification."""
        if not self.bot or not self.bot.entity:
            return {}

        pos = self.bot.entity.position
        blocks = []
        # Optimization: scan every 2 blocks or use a more efficient method if available
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    block_pos = pos.offset(dx, dy, dz)
                    block = self.bot.blockAt(block_pos)
                    if block and block.name != 'air':
                        blocks.append({
                            'name': block.name,
                            'type': self.classify_block(block.name),
                            'x': block_pos.x,
                            'y': block_pos.y,
                            'z': block_pos.z,
                            'hardness': block.hardness,
                            'diggable': block.diggable
                        })
        
        entities = []
        for entity_id in self.bot.entities:
            entity = self.bot.entities[entity_id]
            if entity.id != self.bot.entity.id:
                entity_pos = entity.position
                entities.append({
                    'name': entity.name,
                    'type': entity.type,
                    'classification': self.classify_entity(entity.name, entity.type),
                    'x': entity_pos.x,
                    'y': entity_pos.y,
                    'z': entity_pos.z,
                    'health': entity.health if hasattr(entity, 'health') else None,
                    'distance': pos.distanceTo(entity_pos)
                })

        # Sort entities by distance for better AI prioritization
        entities.sort(key=lambda x: x['distance'])

        return {
            'blocks': blocks,
            'entities': entities,
            'player_pos': {'x': pos.x, 'y': pos.y, 'z': pos.z},
            'biome': self.bot.biome if hasattr(self.bot, 'biome') else None,
            'health': self.bot.health if hasattr(self.bot, 'health') else 20,
            'food': self.bot.food if hasattr(self.bot, 'food') else 20
        }

    def get_inventory_summary(self):
        """Get a detailed inventory summary including item utility assessment."""
        if not self.bot or not self.bot.inventory:
            return []
        
        items = self.bot.inventory.items()
        summary = []
        for item in items:
            utility = 'material'
            if 'pickaxe' in item.name or 'axe' in item.name or 'shovel' in item.name or 'sword' in item.name:
                utility = 'tool'
            elif 'food' in item.name or 'steak' in item.name or 'apple' in item.name:
                utility = 'food'
            elif 'torch' in item.name:
                utility = 'utility_light'
            
            summary.append({
                'name': item.name,
                'count': item.count,
                'utility': utility,
                'metadata': item.metadata,
                'slot': item.slot
            })
        return summary
