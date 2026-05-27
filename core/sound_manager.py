"""
Manages audio loading, playback, and event bindings for the game's sound effects.
"""
import os
import sys
import pygame

def resource_path(relative_path):
    """
    Get absolute path to resource.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SoundManager:
    """
    Central controller for loading, caching, and playing game sound effects (SFX).
    Ensures the game does not crash if a sound file is missing.
    """

    def __init__(self, event_bus):
        """
        Initializes the Pygame mixer, sets up the registry, and subscribes to the Event Bus.
        
        Args:
            event_bus (EventBus): The global event bus to hook sound effects into.
        """
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"[AUDIO WARN] Mixer initialization failed: {e}")

        self.sfx_volume = 1.0
        self.muted = False
        self._sfx_cache = {}

        self.sfx_dir = resource_path(os.path.join("assets", "audio", "sfx"))

        self.sound_registry = {
            "ui_click": "click.wav",
            "ui_hover": "hover.wav",
            "tower_build": "build.wav",
            "tower_upgrade": "upgrade.wav",
            "tower_sell": "sell.wav",
            "coilgun_fire": "coilgun.wav",
            "railgun_fire": "railgun.wav",
            "laser_beam": "laser.wav",
            "enemy_spawn": "spawn.wav",
            "enemy_hit": "hit.wav",
            "enemy_die": "die.wav",
            "enemy_escaped": "escaped.wav",
            "wave_start": "wave_start.wav",
            "victory": "victory.wav",
            "defeat": "defeat.wav"
        }

        self._preload_sounds()

        for action_key in self.sound_registry.keys():
            event_bus.subscribe(action_key, lambda key=action_key: self.play(key))

    def _preload_sounds(self):
        """
        Attempts to scan the registry and cache all existing audio assets.
        Fails silently for missing files to avoid crashing the game.
        """
        for action_key, filename in self.sound_registry.items():
            path = os.path.join(self.sfx_dir, filename)
            
            if os.path.exists(path):
                try:
                    sound_obj = pygame.mixer.Sound(path)
                    sound_obj.set_volume(self.sfx_volume)
                    self._sfx_cache[action_key] = sound_obj
                except pygame.error as e:
                    print(f"[AUDIO ERROR] Failed to load {filename} for action '{action_key}': {e}")
            else:
                print(f"[AUDIO INFO] Missing audio file for '{action_key}' (Expected: {filename})")

    def play(self, action_key):
        """
        Plays a sound effect registered to a specific game action.
        If the sound is not loaded or muted, it degrades gracefully without operation.
        
        Args:
            action_key (str): The logical identifier for the event (e.g., 'tower_build').
        """
        if self.muted or action_key not in self._sfx_cache:
            return

        self._sfx_cache[action_key].play()

    def set_volume(self, volume):
        """
        Updates the global SFX volume dynamic level.
        
        Args:
            volume (float): Value between 0.0 (silent) and 1.0 (max).
        """
        self.sfx_volume = max(0.0, min(volume, 1.0))
        
        for sound_obj in self._sfx_cache.values():
            sound_obj.set_volume(self.sfx_volume)

    def toggle_mute(self):
        """
        Toggles the master audio output state.
        """
        self.muted = not self.muted