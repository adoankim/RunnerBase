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
    Collider classes abstraction for actions and sprites
"""

from cocos import actions, sprite, collision_model as cm, euclid as eu
from runner.config import settings


class ColliderMoveTo(actions.MoveTo):
    """
        Class that wraps the Coco2d's MoveTo for cshape collidable param updating
    """
    def update(self, t):
        super(ColliderMoveTo, self).update(t)
        self.target.cshape.center = self.target.position


class ColliderJumpTo(actions.JumpTo):
    """
        Class that wraps the Coco2d's JumpTo for cshape collidable param updating
    """
    def update(self, t):
        super(ColliderJumpTo, self).update(t)
        self.target.cshape.center = self.target.position


class CollidableSprite(sprite.Sprite):
    """
        Coco2d's Sprite class extension.
        It manages the collision for the runner skeleton sprites
    """

    colman = cm.CollisionManagerGrid(xmin=0,
                                     xmax=settings.win_width,
                                     ymin=0,
                                     ymax=settings.win_height,
                                     cell_height=settings.cell_size,
                                     cell_width=settings.cell_size)

    def __init__(self, img):
        """
        Initializes the sprite with the given image and set up cshape and btype params.

        :Parameters:
            `img` : string
                Path to the image
        """
        super(CollidableSprite, self).__init__(img)
        self.btype = None
        self.cshape = None

    def set_collidable(self, type_name=None):
        """
        Enables the collision for the current sprite.
        It surrounds the sprite with a rectangle shape,
        so the collision is calculated based on rectangular overlapping

        # TODO : Allow the possibility of Circle surrounding for circular objects

        :Parameters:
            `type_name` : string
                type name to identify the sprite
                Defaults to None
        """
        self.btype = type_name
        self.cshape = cm.AARectShape(center=eu.Vector2(0, 0), half_width=self.image.width//2, half_height=self.image.height//2)
        CollidableSprite.colman.add(self)

    def on_collide(self, **kwargs):
        """
        Template method for collision responses

        :Parameters:
            `kwargs` : dict
                Dictionary that saves the information interchanged by collided items
        """
        pass

    def check_self_colliding(self):
        """
        Method that check if the sprite is colliding with other sprites,
        then performs on_collide method call for the sprite and the collision targets.
        """
        collisions = []
        for item in self.colman.iter_colliding(self):
            self.on_collide(target_type=item.btype)
            collisions.append(item)

        for item in collisions:
            item.on_collide(target_type=self.btype)