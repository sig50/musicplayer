"""Audio playback logic built on pygame.mixer (no GUI dependencies)."""
import random

import pygame


class Player:
    def __init__(self):
        self.queue = []
        self.index = -1
        self.shuffle = False
        self.paused = False
        self.playing = False
        self._initialized = False

    def _init(self):
        if not self._initialized:
            pygame.mixer.init()
            self._initialized = True

    @property
    def current(self):
        if 0 <= self.index < len(self.queue):
            return self.queue[self.index]
        return None

    def set_queue(self, tracks, start=0):
        self.queue = list(tracks)
        self.index = start

    def play(self, index=None):
        if self.paused and index is None:
            return self.resume()
        if index is not None:
            self.index = index
        track = self.current
        if track is None:
            return False
        self._init()
        try:
            pygame.mixer.music.load(track.path)
            pygame.mixer.music.play()
        except pygame.error:
            self.playing = False
            return False
        self.playing, self.paused = True, False
        return True

    def pause(self):
        if self.playing and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True

    def resume(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            return True
        return False

    def stop(self):
        if self._initialized:
            pygame.mixer.music.stop()
        self.playing = self.paused = False

    def next_index(self):
        if not self.queue:
            return None
        if self.shuffle:
            if len(self.queue) == 1:
                return 0
            return random.choice([i for i in range(len(self.queue)) if i != self.index])
        nxt = self.index + 1
        return nxt if nxt < len(self.queue) else None

    def next(self):
        idx = self.next_index()
        if idx is None:
            self.stop()
            return False
        return self.play(idx)

    def previous(self):
        if not self.queue:
            return False
        return self.play(max(self.index - 1, 0))

    def is_finished(self):
        """True when a started track has ended naturally (not paused/stopped)."""
        return (self.playing and not self.paused and self._initialized
                and not pygame.mixer.music.get_busy())

    def set_volume(self, value):
        self._init()
        pygame.mixer.music.set_volume(max(0.0, min(1.0, value)))
