from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt

class VolumeSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Orientation.Horizontal)
        self.setRange(0, 100)
        self.setValue(50)
        self.setFixedSize(60, 15)
        self.setTickPosition(QSlider.TickPosition.NoTicks)
        
        self.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #111;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #003300, 
                                            stop:0.6 #006600, 
                                            stop:1 #880000);
                height: 10px;
            }
            QSlider::handle:horizontal {
                background: #7a7a7a;
                border-top: 1px solid #eee;
                border-left: 1px solid #eee;
                border-bottom: 1px solid #111;
                border-right: 1px solid #111;
                width: 8px;
                margin: -2px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #8a8a8a;
            }
            QSlider::handle:horizontal:pressed {
                background: #6a6a6a;
            }
        """)
    
    def mousePressEvent(self, event):
        """Obsługuj kliknięcie na suwaku"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Ustaw wartość na podstawie pozycji kliknięcia
            value = int((event.position().x() / self.width()) * (self.maximum() - self.minimum()) + self.minimum())
            self.setValue(max(self.minimum(), min(value, self.maximum())))
        super().mousePressEvent(event)