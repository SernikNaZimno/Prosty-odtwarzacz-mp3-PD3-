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
        
        self.player = AudioPlayer()
        
        app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        songs_dir = os.path.join(app_dir, "songs")
        self.playlist = PlaylistManager(songs_dir)
        
        self.play_history = [] 
        
        self.shuffle_mode = False
        self.loop_single = False
        
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_player_display)
        self.update_timer.start(100)
        
        self.control_bar.btn_play.clicked.connect(self.on_play)
        self.control_bar.btn_pause.clicked.connect(self.on_pause)
        self.control_bar.btn_stop.clicked.connect(self.on_stop)
        self.control_bar.btn_next.clicked.connect(self.on_next)
        self.control_bar.btn_prev.clicked.connect(self.on_prev)
        self.control_bar.btn_shuffle.clicked.connect(self.on_shuffle_toggle)
        self.control_bar.btn_loop.clicked.connect(self.on_loop_toggle)
        
        self.display_board.volume_slider.valueChanged.connect(self.on_volume_changed)
        self.display_board.volume_slider.setValue(50)
        self.on_volume_changed(50)
        
        self.player.state_changed.connect(self.on_player_state_changed)
        self.player.error.connect(self.on_player_error)
        
        if self.playlist.get_songs_count() > 0:
            self.load_current_song()
        else:
            self.display_board.song_value.setText("00  -- NO SONGS --")
    
    def load_current_song(self):
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
        if self.playlist.get_current_song() is None: return
        if self.player.state == PlayerState.STOPPED:
            self.load_current_song()
        self.player.play()
    
    def on_pause(self):
        self.player.pause()
    
    def on_stop(self):
        self.player.stop()
        self.display_board.update_time(0, 0)
    
    def on_next(self):
        """Obsługa przycisku next - zapisuje historię w trybie shuffle"""
        if self.playlist.get_songs_count() == 0:
            return
            
        current_idx = self.playlist.get_current_index()
        self.play_history.append(current_idx)
        
        if len(self.play_history) > 100:
            self.play_history.pop(0)

        if self.shuffle_mode and self.playlist.get_songs_count() > 1:
            new_index = current_idx
            while new_index == current_idx:
                new_index = random.randint(0, self.playlist.get_songs_count() - 1)
            self.playlist.get_song_at(new_index)
        else:
            self.playlist.next_song()
        
        was_playing = self.player.state == PlayerState.PLAYING
        self.player.stop()
        self.load_current_song()
        if was_playing: self.player.play()
    
    def on_prev(self):
        """Obsługa przycisku prev - korzysta z historii w trybie shuffle"""
        if self.playlist.get_songs_count() == 0:
            return
            
        if self.shuffle_mode and self.play_history:
            prev_index = self.play_history.pop()
            self.playlist.get_song_at(prev_index)
        else:
            self.playlist.prev_song()
        
        was_playing = self.player.state == PlayerState.PLAYING
        self.player.stop()
        self.load_current_song()
        if was_playing: self.player.play()
    
    def on_shuffle_toggle(self):
        # Ręcznie odwracamy stan zmiennej logicznej
        self.shuffle_mode = not self.shuffle_mode
        
        if self.shuffle_mode:
            # Ustawiamy styl włączonego Shuffle
            self.control_bar.btn_shuffle.setStyleSheet("font-size: 9px; color: #00FF00; border: 1px solid #00FF00;")
            
            # Wzajemne wykluczanie - jeśli Loop jest włączony, wyłącz go
            if self.loop_single:
                self.loop_single = False
                self.control_bar.btn_loop.setStyleSheet("") # Resetujemy styl Loop
        else:
            # Czyszczenie historii i resetowanie stylu Shuffle
            self.play_history.clear()
            self.control_bar.btn_shuffle.setStyleSheet("font-size: 9px;")
    
    def on_loop_toggle(self):
        # Ręcznie odwracamy stan zmiennej logicznej
        self.loop_single = not self.loop_single
        
        if self.loop_single:
            # Ustawiamy styl włączonego Loop (R)
            self.control_bar.btn_loop.setStyleSheet("color: #00FF00; border: 1px solid #00FF00;")
            
            # Wzajemne wykluczanie - jeśli Shuffle jest włączone, wyłącz je
            if self.shuffle_mode:
                self.shuffle_mode = False
                self.play_history.clear()
                self.control_bar.btn_shuffle.setStyleSheet("font-size: 9px;") # Resetujemy styl Shuffle
        else:
            # Resetujemy styl Loop
            self.control_bar.btn_loop.setStyleSheet("")
    
    def on_volume_changed(self, value):
        self.player.set_volume(value / 100.0)
    
    def on_player_state_changed(self, state):
        pass
    
    def on_player_error(self, error_msg):
        print(f"Błąd odtwarzacza: {error_msg}")
    
    def update_player_display(self):
        if self.player.state == PlayerState.PLAYING:
            current_pos = self.player.get_position()
            song = self.playlist.get_current_song()
            if song:
                self.display_board.update_time(current_pos, song.duration * 1000)
            
            if self.player.is_music_finished():
                if self.loop_single:
                    self.player.stop()
                    self.load_current_song()
                    self.player.play()
                else:
                    self.on_next()
                    if self.player.state != PlayerState.PLAYING:
                        self.player.play()