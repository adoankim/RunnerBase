# The MIT License (MIT)

# Copyright (c) 2015 Adoankim

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
    Running point of the runner skeleton game
"""

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


def init_game():
    """
    Public function that initialize the entry point of the game

    Responsibilities:
        director initialization based on config settings, scene and layers building
    """
    director.director.init(width=settings.win_width, height=settings.win_height)
    main_scene = scene.Scene()

    points_layer = PointsLayer()
    entities_layer = EntitiesLayer()
    entities_layer.set_player_events_listener(points_layer)

    main_scene.add(entities_layer, z=0)
    main_scene.add(points_layer, z=1, name='points_layer')

    director.director.run(main_scene)

if __name__ == '__main__':
    init_game()
