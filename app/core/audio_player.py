from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, QObject, pyqtSignal

class PlayerState:
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2

class AudioPlayer(QObject):
    state_changed = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.state = PlayerState.STOPPED
        
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.audio_output.setVolume(0.5)

    def load(self, file_path):
        """Ładuje plik używając lokalnej ścieżki QUrl"""
        self.player.setSource(QUrl.fromLocalFile(file_path))
        self.state = PlayerState.STOPPED

    def play(self):
        self.player.play()
        self.state = PlayerState.PLAYING
        self.state_changed.emit(self.state)

    def pause(self):
        self.player.pause()
        self.state = PlayerState.PAUSED
        self.state_changed.emit(self.state)

    def stop(self):
        self.player.stop()
        self.state = PlayerState.STOPPED
        self.state_changed.emit(self.state)

    def set_volume(self, volume):
        """Volume w PyQt6 to wartość od 0.0 do 1.0"""
        self.audio_output.setVolume(volume)

    def get_position(self):
        """Zwraca pozycję w milisekundach"""
        return self.player.position()

    def is_music_finished(self):
        """Sprawdza, czy muzyka dotarła do końca"""
        return self.player.mediaStatus() == QMediaPlayer.MediaStatus.EndOfMedia