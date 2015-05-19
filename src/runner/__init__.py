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
 It exposes the game running point
"""

import os
import platform
# Windows "pyglet Context sharing" problem workaround
if platform.system() == "Windows":
    os.environ["PYGLET_SHADOW_WINDOW"] = "0"

import pyglet
from cocos import director, scene
from runner.config import settings
from runner.layer import PointsLayer, EntitiesLayer


def init_game():
    """
    Public function that initialize the entry point of the game

    Responsibilities:
        director initialization based on config settings, scene and layers building
    """

    # adding assets path to the pyglet ressource manager
    assets_abspath = unicode(os.path.join(os.path.dirname(__file__), '..', '..', 'assets'))
    pyglet.resource.path.append(assets_abspath)
    pyglet.resource.reindex()

    director.director.init(width=settings.win_width, height=settings.win_height)
    main_scene = scene.Scene()

    points_layer = PointsLayer()
    entities_layer = EntitiesLayer()
    entities_layer.set_player_events_listener(points_layer)

    main_scene.add(entities_layer, z=0)
    main_scene.add(points_layer, z=1, name='points_layer')

    director.director.run(main_scene)
