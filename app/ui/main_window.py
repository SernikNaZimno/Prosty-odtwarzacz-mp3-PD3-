from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer
from ui.widgets.display_board import DisplayBoard
from ui.widgets.control_bar import ControlBar
from core.audio_player import AudioPlayer, PlayerState
from core.metadata_parser import PlaylistManager
import os
import random

class RetroPlayerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Winamp Retro Clone")
        self.setFixedSize(360, 115)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.display_board = DisplayBoard()
        self.control_bar = ControlBar()

        self.main_layout.addWidget(self.display_board)
        self.main_layout.addWidget(self.control_bar)
        
        # Inicjalizacja odtwarzacza
        self.player = AudioPlayer()
        
        # Inicjalizacja playlisty - szukaj piosenek w folderze projektu
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.playlist = PlaylistManager(app_dir)
        
        # Tryby odtwarzania
        self.shuffle_mode = False
        self.loop_mode = False
        self.loop_single = False  # True = loop jednej piosenki, False = loop playlisty
        
        # Timer do aktualizacji UI
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_player_display)
        self.update_timer.start(100)  # Aktualizuj co 100ms
        
        # Połączenia sygnałów
        self.control_bar.btn_play.clicked.connect(self.on_play)
        self.control_bar.btn_pause.clicked.connect(self.on_pause)
        self.control_bar.btn_stop.clicked.connect(self.on_stop)
        self.control_bar.btn_next.clicked.connect(self.on_next)
        self.control_bar.btn_prev.clicked.connect(self.on_prev)
        self.control_bar.btn_shuffle.clicked.connect(self.on_shuffle_toggle)
        self.control_bar.btn_loop.clicked.connect(self.on_loop_toggle)
        
        # Volume slider
        self.display_board.volume_slider.valueChanged.connect(self.on_volume_changed)
        self.display_board.volume_slider.setValue(50)
        self.on_volume_changed(50)
        
        # Połączenie sygnałów z odtwarzacza
        self.player.state_changed.connect(self.on_player_state_changed)
        self.player.error.connect(self.on_player_error)
        
        # Wczytaj pierwszą piosenkę
        if self.playlist.get_songs_count() > 0:
            self.load_current_song()
        else:
            self.display_board.song_value.setText("00  -- NO SONGS --")
    
    def load_current_song(self):
        """Wczytaj bieżącą piosenkę"""
        song = self.playlist.get_current_song()
        if song:
            self.player.load(song.file_path)
            self.display_board.update_song_info(
                self.playlist.get_current_index() + 1,
                song.get_display_title(26)
            )
            self.display_board.update_bitrate(song.bitrate)
            self.display_board.update_sample_rate(song.sample_rate)
            self.display_board.update_time(0, song.duration * 1000)
    
    def on_play(self):
        """Obsługa przycisku play"""
        if self.playlist.get_current_song() is None:
            return
        
        if self.player.state == PlayerState.STOPPED:
            self.load_current_song()
        
        self.player.play()
    
    def on_pause(self):
        """Obsługa przycisku pause"""
        self.player.pause()
    
    def on_stop(self):
        """Obsługa przycisku stop"""
        self.player.stop()
        self.display_board.update_time(0, 0)
    
    def on_next(self):
        """Obsługa przycisku next"""
        if self.playlist.get_songs_count() == 0:
            return
            
        if self.shuffle_mode:
            # Losowa następna piosenka
            new_index = random.randint(0, self.playlist.get_songs_count() - 1)
            self.playlist.get_song_at(new_index)
        else:
            self.playlist.next_song()
        
        was_playing = self.player.state == PlayerState.PLAYING
        self.player.stop()
        self.load_current_song()
        
        if was_playing:
            self.player.play()
    
    def on_prev(self):
        """Obsługa przycisku previous"""
        if self.playlist.get_songs_count() == 0:
            return
            
        self.playlist.prev_song()
        
        was_playing = self.player.state == PlayerState.PLAYING
        self.player.stop()
        self.load_current_song()
        
        if was_playing:
            self.player.play()
    
    def on_shuffle_toggle(self):
        """Obsługa toggle shuffle"""
        self.shuffle_mode = self.control_bar.btn_shuffle.isChecked()
    
    def on_loop_toggle(self):
        """Obsługa toggle loop"""
        if not self.control_bar.btn_loop.isChecked():
            self.loop_mode = False
            self.loop_single = False
        else:
            self.loop_mode = True
            self.loop_single = True
    
    def on_volume_changed(self, value):
        """Obsługa zmiany głośności"""
        volume = value / 100.0
        self.player.set_volume(volume)
    
    def on_player_state_changed(self, state):
        """Obsługa zmiany stanu odtwarzacza"""
        pass
    
    def on_player_error(self, error_msg):
        """Obsługa błędu z odtwarzacza"""
        print(f"Błąd odtwarzacza: {error_msg}")
    
    def update_player_display(self):
        """Aktualizuj wyświetlanie czasu i sprawdzaj koniec piosenki"""
        if self.player.state == PlayerState.PLAYING:
            current_pos = self.player.get_position()
            song = self.playlist.get_current_song()
            if song:
                self.display_board.update_time(current_pos, song.duration * 1000)
            
            # Sprawdzaj czy piosenka się skończyła
            if self.player.is_music_finished():
                if self.loop_single:
                    # Loop jednej piosenki
                    self.player.stop()
                    self.player.play()
                else:
                    # Przejdź do następnej
                    self.on_next()