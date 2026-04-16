import os
from mutagen.id3 import ID3
from mutagen.mp3 import MPEGInfo
from pathlib import Path

class SongMetadata:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.title = "Unknown"
        self.artist = "Unknown"
        self.duration = 0  # w sekundach
        self.bitrate = 0  # w kbps
        self.sample_rate = 0  # w Hz
        self.load_metadata()
    
    def load_metadata(self):
        """Wczytaj metadane z pliku MP3"""
        try:
            # Parsuj informacje audio
            audio = MPEGInfo(self.file_path)
            self.duration = int(audio.length)
            self.bitrate = audio.bitrate // 1000 if audio.bitrate else 128  # konwersja do kbps
            self.sample_rate = audio.sample_rate
            
            # Parsuj ID3 tags
            try:
                tags = ID3(self.file_path)
                if "TIT2" in tags:  # Title
                    self.title = str(tags["TIT2"])
                if "TPE1" in tags:  # Artist
                    self.artist = str(tags["TPE1"])
            except:
                # Jeśli brak tagów, użyj nazwy pliku
                filename = Path(self.file_path).stem
                self.title = filename
                
        except Exception as e:
            print(f"Błąd wczytywania metadanych z {self.file_path}: {str(e)}")
    
    def get_duration_string(self) -> str:
        """Zwróć czas w formacie MM:SS"""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_display_title(self, max_length: int = 32) -> str:
        """Zwróć tytuł piosenki gotowy do wyświetlenia"""
        title = f"{self.artist} - {self.title}" if self.artist != "Unknown" else self.title
        if len(title) > max_length:
            return title[:max_length-3] + "..."
        return title


class PlaylistManager:
    def __init__(self, music_folder: str = "."):
        self.music_folder = music_folder
        self.songs = []
        self.current_index = 0
        self.load_playlist()
    
    def load_playlist(self):
        """Wczytaj wszystkie pliki MP3 z folderu"""
        self.songs = []
        
        if not os.path.exists(self.music_folder):
            print(f"Folder nie istnieje: {self.music_folder}")
            return
        
        # Szukaj plików MP3
        for file in sorted(os.listdir(self.music_folder)):
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(self.music_folder, file)
                try:
                    metadata = SongMetadata(file_path)
                    self.songs.append(metadata)
                except Exception as e:
                    print(f"Błąd dodawania piosenki {file}: {str(e)}")
    
    def get_current_song(self) -> SongMetadata:
        """Pobierz bieżącą piosenkę"""
        if 0 <= self.current_index < len(self.songs):
            return self.songs[self.current_index]
        return None
    
    def next_song(self) -> SongMetadata:
        """Przejdź do następnej piosenki"""
        if len(self.songs) == 0:
            return None
        self.current_index = (self.current_index + 1) % len(self.songs)
        return self.get_current_song()
    
    def prev_song(self) -> SongMetadata:
        """Przejdź do poprzedniej piosenki"""
        if len(self.songs) == 0:
            return None
        self.current_index = (self.current_index - 1) % len(self.songs)
        return self.get_current_song()
    
    def get_song_at(self, index: int) -> SongMetadata:
        """Pobierz piosenkę o danym indeksie"""
        if 0 <= index < len(self.songs):
            self.current_index = index
            return self.songs[index]
        return None
    
    def get_current_index(self) -> int:
        """Pobierz indeks bieżącej piosenki"""
        return self.current_index
    
    def get_songs_count(self) -> int:
        """Pobierz liczbę piosenek"""
        return len(self.songs)
