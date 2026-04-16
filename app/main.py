import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import RetroPlayerWindow

GLOBAL_STYLES = """
        QWidget {
            background-color: #222222;
            color: #909090;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10px;
            font-weight: bold;
        }

        /* Wypukły przycisk retro */
        QPushButton {
            background-color: #bdbdbd;
            border-top: 2px solid #ffffff;
            border-left: 2px solid #ffffff;
            border-right: 2px solid #555555;
            border-bottom: 2px solid #555555;
            color: black;
            border-radius: 0px; /* Zabijamy nowoczesne zaokrąglenia */
        }

        QPushButton:pressed {
            border-top: 2px solid #333333;
            border-left: 2px solid #333333;
            border-bottom: 2px solid #b5b5b5;
            border-right: 2px solid #b5b5b5;
            background-color: #6a6a6a;
        }

        /* Duży wyświetlacz LCD i małe panele (wklęsłe) */
        .LCDScreen {
            background-color: #000000;
            color: #00ff00;
            font-family: 'Courier New', monospace; /* Zmień na swój pixel font */
            border: 1px solid #111111;
            border-top: 1px solid #0a0a0a;
            border-left: 1px solid #0a0a0a;
        }

        /* Czarne tło dla małych zielonych napisów (np. 128, 44) */
        .GreenBox {
            background-color: #000000;
            color: #00ff00;
            border: 1px solid #444444;
            padding: 1px 4px;
            font-family: 'Courier New', monospace;
        }

        /* Etykiety statyczne (SONG, BITRATE, itd.) */
        QLabel {
            background: transparent;
            color: #909090;
        }

        QLabel#ActiveStereo {
            color: #00ff00;
        }
    """

def main():
    app = QApplication(sys.argv)
    
    app.setStyleSheet(GLOBAL_STYLES)
    # OPCJONALNIE: Tutaj dodasz ładowanie czcionki QFontDatabase
    # font_path = os.path.join("assets", "fonts", "pixel_panel", "fonts", "ttf", "TwojaCzcionka.ttf")
    # QFontDatabase.addApplicationFont(font_path)
    
    window = RetroPlayerWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()