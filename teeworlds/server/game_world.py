from pygame import sprite

from block import Platform, PLATFORM_WIDTH, PLATFORM_HEIGHT

class Game_world():
    def __init__(self):
        self.all_entities = sprite.Group()
        self.platforms = []

    def add_entity(self, entity):
        self.all_entities.add(entity)

    def remove_entity(self, entity):
        self.all_entities.remove(entity)

    def uploading_map(self, map):
        x = 0
        y = 0
        for row in map:
            for col in row:
                if col != " ":
                    platform = Platform(x, y)
                    self.all_entities.add(platform)
                    self.platforms.append(platform)
                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0