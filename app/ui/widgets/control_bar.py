from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel

class ControlBar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self.btn_prev = QPushButton("|<")
        self.btn_play = QPushButton(">")
        self.btn_pause = QPushButton("||")
        self.btn_stop = QPushButton("[]")
        self.btn_next = QPushButton(">|")

        for btn in [self.btn_prev, self.btn_play, self.btn_pause, self.btn_stop, self.btn_next]:
            btn.setFixedSize(30, 25)
            layout.addWidget(btn)

        layout.addSpacing(15)

        self.btn_shuffle = QPushButton("SHUFFLE")
        self.btn_shuffle.setFixedSize(60, 20)
        self.btn_shuffle.setCheckable(True)
        self.btn_shuffle.setStyleSheet("font-size: 9px;")
        
        self.btn_loop = QPushButton("R")
        self.btn_loop.setFixedSize(30, 20)
        self.btn_loop.setCheckable(True)

        layout.addWidget(self.btn_shuffle)
        layout.addWidget(self.btn_loop)

        layout.addStretch()

        lightning = QLabel("⚡")
        lightning.setStyleSheet("color: orange; font-size: 16px;")
        layout.addWidget(lightning)