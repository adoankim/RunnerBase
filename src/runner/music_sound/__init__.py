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
    Utils for music and sound effects management
"""

import pyglet

from runner.config import settings

pyglet.options['audio'] = ('openal', 'silent')


class BackgroundMusicManager:
    def __init__(self, song_path):
        music = pyglet.media.load(settings.get_assets(song_path))
        self.player = pyglet.media.Player()
        self.player.queue(music)
        self.player.volume = 0.2

    def start(self):
        self.player.play()


class SFXManager:
    """
        It manages Sound fx of the game
    """
    def __init__(self):
        self.sounds = {
            'jump': self.__load_static_sound(settings.sounds['jump']),
            'coin': self.__load_static_sound(settings.sounds['coin'])
        }

    @staticmethod
    def __load_static_sound(path):
        sound_media = pyglet.media.load(settings.get_assets(path))
        return pyglet.media.StaticSource(sound_media)

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play().volume = settings.default_sound_volume


class SoundListener:
    """
        Class handler that plays the sound registered for the given events
    """
    sfx_manager = SFXManager()

    def on_grab_coin(self):
        self.sfx_manager.play('coin')

    def on_jump(self):
        self.sfx_manager.play('jump')


