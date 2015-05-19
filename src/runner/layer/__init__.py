from cocos import director, scene, layer, text, actions

from runner.config import settings
from runner.sprite import Character
from runner.spawner import CoinSpawner


class PointsLayer(layer.Layer):
    """
    Layer class that handles the grab_coin_action triggered by the player
   """

    def __init__(self):
        """
            Initializes de points layer.
            It creates a label that holds the text points value shown on the screen.
            Also creates the scale animation fired each time the on_grab_coin is triggered.
        """
        super(PointsLayer, self).__init__()
        self.points_label = text.Label(text="0", font_size=30)
        self.add(self.points_label)
        self.points_label.position = settings.win_width-75, settings.win_height-60
        self.points = 0
        self.point_action = actions.ScaleTo(1.5, 0.5) + actions.ScaleTo(1, 0.5)

    def on_grab_coin(self):
        self.points += 1
        self.points_label.do(action=self.point_action)
        self.points_label.element.text = "%d" % self.points


class EntitiesLayer(layer.ColorLayer):
    """
    Layer class that manages the game entities building and show them on the scene
   """
    def __init__(self):
        """
        Creates the layer and its entities.

        Responsibilities:
            Build and configure the character sprite and coin spawner, then put them into the scene
        """
        super(EntitiesLayer, self).__init__(150, 200, 255, 255)
        self.character = Character()
        self.character.position = 40, 130
        self.character.cshape.center = self.character.position
        self.coin_spawner = CoinSpawner(0.4, 130, 270)
        self.add(self.coin_spawner, name="coin_spawner")
        self.add(self.character, name="character")

    def set_player_events_listener(self, listener):
        self.character.push_handlers(listener)