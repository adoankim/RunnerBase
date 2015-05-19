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
    Object spawning classes
"""
import random as rnd
from cocos import cocosnode, actions
from runner.config import settings
from runner.collider import ColliderMoveTo
from runner.sprite import Coin


class CoinSpawner(cocosnode.CocosNode):
    """
    Spawner class for coin generation (it feeds the player!)
    """
    def __init__(self, gen_rate, ymin, ymax):
        """
        Initializes the spawner and launch scheduled calling methods for coin spawning and screen off coins removal
        :param rate: float
            Generation rate for coin spawning.
            It must be between 0 and 1.

        :param ymin: float
            Minimal y position for generated coins

        :param ymax: float
            Maximal y position for generated coins
        """
        super(CoinSpawner, self).__init__()
        self.ymax, self.ymin = ymax, ymin
        self.x_start = settings.win_width - 45
        self.gen_rate = gen_rate
        self.__spawn_coins(0)
        self.schedule_interval(self.__spawn_coins, 1)
        self.schedule_interval(self.__remove_offscreen_coins, 1)

    def __spawn_coins(self, _):
        """
            It creates a coin in the most rightest position of the screen with random y position between ymin and ymax.
            Then it triggers the movement of the coin to the leftest side of the screen
            and apply some "bumping" effect to it.
        """
        if rnd.uniform(0, 1) < self.gen_rate:
            return

        pos = self.x_start, rnd.uniform(self.ymin, self.ymax)
        coin = Coin(pos)
        coin.set_collidable('coin')

        coin.do(ColliderMoveTo((-10, pos[1]), duration=2))
        wrapper = cocosnode.CocosNode()
        wrapper.add(coin, name="coin")
        jumping = actions.MoveBy((0, 10), duration=0.1)
        wrapper.do(actions.Repeat(jumping + actions.Reverse(jumping)))
        self.add(wrapper)

    def __remove_offscreen_coins(self, _):
        """
        If some coin goes off of the screen, it must be deleted in order to save the resources!
        """
        for _, obj in self.children:
            coin = obj.get("coin")
            if coin.position[0] < 0 or coin.position[0] >= settings.win_width:
                print("removed")
                self.remove(obj)