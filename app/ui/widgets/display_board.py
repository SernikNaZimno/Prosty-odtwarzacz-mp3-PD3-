from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from ui.widgets.volume_slider import VolumeSlider

class DisplayBoard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.time_display = QLabel("> 00:00")
        self.time_display.setProperty("class", "LCDScreen")
        self.time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_display.setFixedSize(130, 45)
        self.time_display.setStyleSheet("font-size: 24px; letter-spacing: 2px;") 

        layout.addWidget(self.time_display)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(4)

        song_row = QHBoxLayout()
        song_label = QLabel("SONG")
        self.song_value = QLabel("01  --  --")
        self.song_value.setProperty("class", "LCDScreen")
        self.song_value.setFixedSize(160, 16)
        song_row.addWidget(song_label)
        song_row.addWidget(self.song_value)
        
        tech_row = QHBoxLayout()
        tech_row.addWidget(QLabel("BITRATE"))
        
        self.bitrate_val = QLabel("128")
        self.bitrate_val.setProperty("class", "GreenBox")
        tech_row.addWidget(self.bitrate_val)
        tech_row.addWidget(QLabel("kbps"))
        
        tech_row.addSpacing(10)
        tech_row.addWidget(QLabel("MIXRATE"))
        
        self.mixrate_val = QLabel("44")
        self.mixrate_val.setProperty("class", "GreenBox")
        tech_row.addWidget(self.mixrate_val)
        tech_row.addWidget(QLabel("kHz"))

        vol_row = QHBoxLayout()
        vol_row.addWidget(QLabel("VOLUME"))
        self.volume_slider = VolumeSlider()
        vol_row.addWidget(self.volume_slider)
        vol_row.addStretch()
        vol_row.addWidget(QLabel("mono"))
        
        self.stereo_label = QLabel("stereo")
        self.stereo_label.setObjectName("ActiveStereo")
        vol_row.addWidget(self.stereo_label)

        right_layout.addLayout(song_row)
        right_layout.addLayout(tech_row)
        right_layout.addLayout(vol_row)

        layout.addWidget(right_panel)
    
    def update_time(self, current_ms: int, duration_ms: int):
        """Aktualizuj wyświetlany czas"""
        if duration_ms == 0:
            time_str = "> 00:00"
        else:
            current_sec = current_ms // 1000
            duration_sec = duration_ms // 1000
            
            current_min = current_sec // 60
            current_s = current_sec % 60
            
            time_str = f"> {current_min:02d}:{current_s:02d}"
        self.time_display.setText(time_str)
    
    def update_song_info(self, song_index: int, song_title: str):
        """Aktualizuj informacje o piosence"""
        display_text = f"{song_index:02d}  {song_title}"
        if len(display_text) > 32:
            display_text = display_text[:29] + "..."
        self.song_value.setText(display_text)
    
    def update_bitrate(self, bitrate: int):
        """Aktualizuj bitrate"""
        self.bitrate_val.setText(str(bitrate))
    
    def update_sample_rate(self, sample_rate: int):
        """Aktualizuj mixrate (sample rate)"""
        khz = sample_rate // 1000
        self.mixrate_val.setText(str(khz))