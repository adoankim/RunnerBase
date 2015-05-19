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
    Runner sprite classes
"""

from pyglet import event
from pyglet.window import key
from cocos import director
from runner.collider import CollidableSprite, ColliderJumpTo


class Coin(CollidableSprite):
    """
    Class that represents a runner coin, making the character happy each time he grabs one!
    """

    COLLISION_NAME = 'coin'

    def __init__(self, position=(0, 0)):
        """
        Initializes the coin.

        :Parameters:
            `position` : tuple
                Represents the position of the Coin in the game world
                Defaults to (0, 0)
        """
        super(Coin, self).__init__('images/coin.png')
        self.anchor = 0.5, 0.5
        self.set_collidable(self.COLLISION_NAME)
        self.position = position
        self.cshape.center = position

    def on_collide(self, **kwargs):
        """
        When the player collides with the coin, it disappears from the world and the collision model!
        """

        if kwargs['target_type'] == Character.COLLISION_NAME:
            self.parent.remove(self)
            self.colman.remove_tricky(self)


class Character(CollidableSprite, event.EventDispatcher):
    """
    Class that represents the runner player! he must collect all the coins of the world!
    """
    COLLISION_NAME = 'player'

    def __init__(self):
        """
        Initializes the player with some base configuration.
        It setups the event handling system for the jump event.
        """
        super(Character, self).__init__('images/character.png')
        self.anchor = 0.5, 0.5
        self.key_handler = key.KeyStateHandler()
        director.director.window.push_handlers(self.key_handler)
        self.schedule(self.__update__)
        self.jump_timer = 0

        self.set_collidable(self.COLLISION_NAME)

    def on_collide(self, **kwargs):
        """
        When the player collides with a coin, he grabs it!
        """
        if kwargs['target_type'] == Coin.COLLISION_NAME:
            print("player grabs a coin")
            self.dispatch_event('on_grab_coin')

    def __update__(self, dt):
        """
        Handles the jump action of the player and performs the collision checking for each frame
        """
        if self.jump_timer <= 0 and self.key_handler[key.SPACE]:
            self.jump_timer = 1.2
            self.do(ColliderJumpTo(self.position, height=40, duration=1.2))

        self.jump_timer -= dt
        self.check_self_colliding()

# Announces that the player can fire on_grab_coin events
Character.register_event_type('on_grab_coin')