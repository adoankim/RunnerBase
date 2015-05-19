from cocos import director, scene, layer

from runner.config import settings
from runner.sprite import Character
from runner.spawner import CoinSpawner


class PointsLayer(layer.Layer):
    """
    Layer class that handles the grab_coin_action triggered by the player
   """

    def __init__(self):
        super(PointsLayer, self).__init__()

    def on_grab_coin(self):
        print("grab_coin!")


class EntitiesLayer(layer.Layer):
    """
    Layer class that manages the game entities building and show them on the scene
   """
    def __init__(self):
        """
        Creates the layer and its entities.

        Responsibilities:
            Build and configure the character sprite and coin spawner, then put them into the scene
        """
        super(EntitiesLayer, self).__init__()
        self.character = Character()
        self.character.position = 10, 40
        self.character.cshape.center = self.character.position
        self.coin_spawner = CoinSpawner(0.2, 40, 90)

        self.add(self.coin_spawner, name="coin_spawner")
        self.add(self.character, name="character")

    def set_player_events_listener(self, listener):
        self.character.push_handlers(listener)