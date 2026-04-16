import pygame
from enum import Enum
from PyQt6.QtCore import QObject, pyqtSignal
import os

class PlayerState(Enum):
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2

class AudioPlayer(QObject):
    state_changed = pyqtSignal(PlayerState)
    time_changed = pyqtSignal(int)  # Emituje bieżący czas w ms
    song_finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.current_file = None
        self.state = PlayerState.STOPPED
        self.duration = 0
        self.is_playing = False
        
    def load(self, file_path: str) -> bool:
        """Wczytaj plik MP3"""
        try:
            if not os.path.exists(file_path):
                self.error.emit(f"Plik nie znaleziony: {file_path}")
                return False
                
            pygame.mixer.music.load(file_path)
            self.current_file = file_path
            self.state = PlayerState.STOPPED
            self.state_changed.emit(self.state)
            return True
        except Exception as e:
            self.error.emit(f"Błąd wczytywania pliku: {str(e)}")
            return False
    
    def play(self) -> bool:
        """Odtwarzaj aktualny plik"""
        try:
            if self.state == PlayerState.PAUSED:
                pygame.mixer.music.unpause()
            elif self.state == PlayerState.STOPPED:
                if self.current_file:
                    pygame.mixer.music.play()
                else:
                    return False
            
            self.state = PlayerState.PLAYING
            self.is_playing = True
            self.state_changed.emit(self.state)
            return True
        except Exception as e:
            self.error.emit(f"Błąd odtwarzania: {str(e)}")
            return False
    
    def pause(self) -> bool:
        """Pauza"""
        try:
            if self.state == PlayerState.PLAYING:
                pygame.mixer.music.pause()
                self.state = PlayerState.PAUSED
                self.is_playing = False
                self.state_changed.emit(self.state)
                return True
            return False
        except Exception as e:
            self.error.emit(f"Błąd pauzy: {str(e)}")
            return False
    
    def stop(self) -> bool:
        """Zatrzymaj odtwarzanie"""
        try:
            pygame.mixer.music.stop()
            self.state = PlayerState.STOPPED
            self.is_playing = False
            self.state_changed.emit(self.state)
            return True
        except Exception as e:
            self.error.emit(f"Błąd zatrzymywania: {str(e)}")
            return False
    
    def set_position(self, milliseconds: int) -> bool:
        """Ustaw pozycję odtwarzania"""
        try:
            if self.state != PlayerState.STOPPED:
                pygame.mixer.music.set_pos(milliseconds / 1000.0)
                return True
            return False
        except Exception as e:
            self.error.emit(f"Błąd ustawiania pozycji: {str(e)}")
            return False
    
    def set_volume(self, volume: float) -> bool:
        """Ustaw głośność (0.0 - 1.0)"""
        try:
            volume = max(0.0, min(1.0, volume))
            pygame.mixer.music.set_volume(volume)
            return True
        except Exception as e:
            self.error.emit(f"Błąd ustawiania głośności: {str(e)}")
            return False
    
    def get_position(self) -> int:
        """Pobierz bieżącą pozycję w ms"""
        try:
            if self.is_playing:
                pos = pygame.mixer.music.get_pos()
                return max(0, pos)  # Upewnij się, że wartość nie jest ujemna
            return 0
        except:
            return 0
    
    def is_music_finished(self) -> bool:
        """Sprawdzić czy muzyka się skończyła"""
        return not pygame.mixer.music.get_busy() and self.state == PlayerState.PLAYING
