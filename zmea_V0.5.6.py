import pygame
import random
import copy
import sys
import os
import json
import traceback
import datetime
import webbrowser
from pygame.locals import *

# --- Константи ---
SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"
LEVELS_FILE = "levels.json"
LEVEL_PROGRESS_FILE = "level_progress.json"
ERROR_LOG_FILE = "error_log.txt"
MOD_STATES_FILE = "mod_states.json" # --- НОВЕ: Файл для збереження стану модів ---

# Кольори інтерфейсу
BG_COLOR = (10, 10, 10)
BUTTON_COLOR = (50, 50, 50)
HOVER_COLOR = (100, 100, 100)
TEXT_COLOR = (0, 255, 0)      # Зелений текст
ERROR_TEXT_COLOR = (255, 0, 0)   # Червоний для помилок
WARN_TEXT_COLOR = (255, 165, 0) # Помаранчевий для попереджень
INFO_TEXT_COLOR = (200, 200, 200) # Сірий для інформації
UNLOCKED_LEVEL_COLOR = (0, 180, 0) # Зелений для доступних рівнів
LOCKED_LEVEL_COLOR = (100, 100, 100) # Сірий для заблокованих рівнів
PROGRESS_BAR_BG = (100, 100, 100)
PROGRESS_BAR_FG = (0, 200, 0)
PAUSE_OVERLAY_COLOR = (0, 0, 0, 150) # Напівпрозорий чорний

# Ігрові кольори та параметри
DEFAULT_SNAKE_COLOR = [0, 200, 0] # Типовий зелений (список, щоб бути JSON-сумісним)
FOOD_COLOR = (255, 0, 0)
SPECIAL_FOOD_COLOR = (0, 0, 255)
CELL_SIZE = 20
DEFAULT_GAME_FPS = 15 # Типова швидкість гри (можна налаштувати)

# Передвстановлені кольори для скінів змійки (RGB у вигляді списків)
PREDEFINED_SKINS = {
    "crimson_red": [220, 20, 60], "light_sky_blue": [135, 206, 250],
    "medium_blue": [0, 0, 205], "dark_violet": [148, 0, 211],
    "purple": [128, 0, 128], "lavender": [230, 230, 250],
    "white": [255, 255, 255], "gold_yellow": [255, 215, 0],
    "hot_pink": [255, 105, 180], "default_green": [0, 200, 0],
    "dark_orange": [255, 140, 0], "dark_turquoise": [0, 206, 209],
    "lawn_green": [124, 252, 0], "saddle_brown": [139, 69, 19],
    "dark_gray": [169, 169, 169], "medium_sea_green": [60, 179, 113]
}
# Доступні роздільні здатності
AVAILABLE_RESOLUTIONS = ["800x600", "1024x768", "1280x720", "1366x768", "1600x900", "1920x1080"]

# Типові налаштування
DEFAULT_SETTINGS = {
    "profile": {"nickname": "Гравець", "language": "uk"},
    "graphics": {"resolution": "1024x768", "fullscreen": False, "fps": 60},
    "audio": {"music_volume": 0.5, "sound_volume": 0.7, "sound_enabled": True},
    "controls": {"up": "K_UP", "down": "K_DOWN", "left": "K_LEFT", "right": "K_RIGHT", "pause": "K_ESCAPE"},
    "gameplay": {"default_speed": DEFAULT_GAME_FPS},
    "appearance": {"skin_color": DEFAULT_SNAKE_COLOR}
}

# Словник для мов
LANGUAGES = {
    "en": {
    "language": "English", "play": "Play", "settings": "Settings", "exit": "Exit", "back": "Back",
    "loading": "Loading...", "optimizing": "Optimizing game", "pause_title": "Pause",
    "continue": "Continue", "menu": "Menu", "levels": "Levels", "train": "Training",
    "leaderboard": "Leaderboard", "change_nickname": "Change Nickname",
    "settings_audio": "Audio Settings", "settings_graphics": "Graphics Settings",
    "settings_skins": "Skin Settings", "settings_language": "Language",
    "volume_music": "Music Volume", "volume_sound": "Sound Volume", "sound_on": "Sound: On",
    "sound_off": "Sound: Off", "resolution": "Resolution", "fullscreen_on": "Fullscreen: On",
    "fullscreen_off": "Fullscreen: Off", "apply": "Apply", "skin_select": "Select Skin",
    "level_select": "Select Level", "level": "Level", "training_suffix": "(Training)",
    "score": "Score", "to_next_level": "To next level", "points_abbr": "pts.",
    "next_level_unlocked": "Next level unlocked!", "next_level_button": "Next Level",
    "game_over": "Game Over", "retry": "Retry", "error_title": "Error",
    "error_restart": "Please restart the game.",
    "error_support": "If the problem persists, contact support:", "error_site": "Site:",
    "game_title": "SNAKE",
    "skin_crimson_red": "Red", "skin_light_sky_blue": "Light Blue", "skin_medium_blue": "Blue",
    "skin_dark_violet": "Violet", "skin_purple": "Purple", "skin_lavender": "Lavender",
    "skin_white": "White", "skin_gold_yellow": "Yellow", "skin_hot_pink": "Pink",
    "skin_default_green": "Green", "skin_dark_orange": "Orange", "skin_dark_turquoise": "Turquoise",
    "skin_lawn_green": "Lime", "skin_saddle_brown": "Brown", "skin_dark_gray": "Gray",
    "skin_medium_sea_green": "Mint", "mods": "Mods", "active_mods": "Active Mods",
    "no_mods": "No mods found"
    },
    "uk": {
    "language": "Українська", "play": "Грати", "settings": "Налаштування", "exit": "Вихід", "back": "Назад",
    "loading": "Завантаження...", "optimizing": "Оптимізація гри", "pause_title": "Пауза",
    "continue": "Продовжити", "menu": "Меню", "levels": "Рівні", "train": "Тренування",
    "leaderboard": "Таблиця лідерів", "change_nickname": "Змінити нік",
    "settings_audio": "Налаштування Аудіо", "settings_graphics": "Налаштування Графіки",
    "settings_skins": "Налаштування Скінів", "settings_language": "Мова",
    "volume_music": "Гучність Музики", "volume_sound": "Гучність Звуків", "sound_on": "Звук: Увімк.",
    "sound_off": "Звук: Вимк.", "resolution": "Роздільна здатність", "fullscreen_on": "Повноекранний: Увімк.",
    "fullscreen_off": "Повноекранний: Вимк.", "apply": "Застосувати", "skin_select": "Вибір Скіна",
    "level_select": "Вибір Рівня", "level": "Рівень", "training_suffix": "(Тренування)",
    "score": "Рахунок", "to_next_level": "До рівня", "points_abbr": "оч.",
    "next_level_unlocked": "Наступний рівень відкрито!", "next_level_button": "Наступний Рівень",
    "game_over": "Гру Завершено", "retry": "Спробувати ще", "error_title": "Помилка",
    "error_restart": "Будь ласка, перезапустіть гру.",
    "error_support": "Якщо проблема не зникне, зверніться до підтримки:", "error_site": "Сайт:",
    "game_title": "ЗМІЙКА",
    "skin_crimson_red": "Червоний", "skin_light_sky_blue": "Голубий", "skin_medium_blue": "Синій",
    "skin_dark_violet": "Фіолетовий", "skin_purple": "Пурпурний", "skin_lavender": "Лавандовий",
    "skin_white": "Білий", "skin_gold_yellow": "Жовтий", "skin_hot_pink": "Рожевий",
    "skin_default_green": "Зелений", "skin_dark_orange": "Помаранчевий", "skin_dark_turquoise": "Бірюзовий",
    "skin_lawn_green": "Салатовий", "skin_saddle_brown": "Коричневий", "skin_dark_gray": "Сірий",
    "skin_medium_sea_green": "М'ятний", "mods": "Моди", "active_mods": "Активні моди",
    "no_mods": "Моди не знайдено"
    },
    "ru": {
    "language": "Русский", "play": "Играть", "settings": "Настройки", "exit": "Выход", "back": "Назад",
    "loading": "Загрузка...", "optimizing": "Оптимизация игры", "pause_title": "Пауза",
    "continue": "Продолжить", "menu": "Меню", "levels": "Уровни", "train": "Тренировка",
    "leaderboard": "Таблица лидеров", "change_nickname": "Сменить ник",
    "settings_audio": "Настройки Аудио", "settings_graphics": "Настройки Графики",
    "settings_skins": "Настройки Скинов", "settings_language": "Язык",
    "volume_music": "Громкость Музыки", "volume_sound": "Громкость Звуков", "sound_on": "Звук: Вкл.",
    "sound_off": "Звук: Выкл.", "resolution": "Разрешение", "fullscreen_on": "Полноэкранный: Вкл.",
    "fullscreen_off": "Полноэкранный: Выкл.", "apply": "Применить", "skin_select": "Выбор Скина",
    "level_select": "Выбор Уровня", "level": "Уровень", "training_suffix": "(Тренировка)",
    "score": "Счет", "to_next_level": "До уровня", "points_abbr": "очк.",
    "next_level_unlocked": "Следующий уровень открыт!", "next_level_button": "Следующий Уровень",
    "game_over": "Игра Окончена", "retry": "Попробовать снова", "error_title": "Ошибка",
    "error_restart": "Пожалуйста, перезапустите игру.",
    "error_support": "Если проблема не исчезнет, свяжитесь с поддержкой:", "error_site": "Сайт:",
    "game_title": "ЗМЕЙКА",
    "skin_crimson_red": "Красный", "skin_light_sky_blue": "Голубой", "skin_medium_blue": "Синий",
    "skin_dark_violet": "Фиолетовый", "skin_purple": "Пурпурный", "skin_lavender": "Лавандовый",
    "skin_white": "Белый", "skin_gold_yellow": "Желтый", "skin_hot_pink": "Розовый",
    "skin_default_green": "Зеленый", "skin_dark_orange": "Оранжевый", "skin_dark_turquoise": "Бирюзовый",
    "skin_lawn_green": "Салатовый", "skin_saddle_brown": "Коричневый", "skin_dark_gray": "Серый",
    "skin_medium_sea_green": "Мятный", "mods": "Моды", "active_mods": "Активные моды",
    "no_mods": "Моды не найдены"
    },
    "be": {
    "language": "Беларуская", "play": "Гуляць", "settings": "Налады", "exit": "Выхад", "back": "Назад",
    "loading": "Загрузка...", "optimizing": "Аптымізацыя гульні", "pause_title": "Паўза",
    "continue": "Працягнуць", "menu": "Меню", "levels": "Узроўні", "train": "Трэніроўка",
    "leaderboard": "Табліца лідэраў", "change_nickname": "Змяніць нік",
    "settings_audio": "Налады Аўдыё", "settings_graphics": "Налады Графікі",
    "settings_skins": "Налады Скінаў", "settings_language": "Мова",
    "volume_music": "Гучнасць Музыкі", "volume_sound": "Гучнасць Гукаў", "sound_on": "Гук: Укл.",
    "sound_off": "Гук: Выкл.", "resolution": "Раздзяленне", "fullscreen_on": "Поўнаэкранны: Укл.",
    "fullscreen_off": "Поўнаэкранны: Выкл.", "apply": "Ужыць", "skin_select": "Выбар Скіна",
    "level_select": "Выбар Узроўню", "level": "Узровень", "training_suffix": "(Трэніроўка)",
    "score": "Лік", "to_next_level": "Да ўзроўню", "points_abbr": "ачк.",
    "next_level_unlocked": "Наступны ўзровень адчынены!", "next_level_button": "Наступны Узровень",
    "game_over": "Гульня Скончана", "retry": "Паспрабаваць зноў", "error_title": "Памылка",
    "error_restart": "Калі ласка, перазапусціце гульню.",
    "error_support": "Калі праблема не знікне, звярніцеся ў падтрымку:", "error_site": "Сайт:",
    "game_title": "ЗМЕЙКА",
    "skin_crimson_red": "Чырвоны", "skin_light_sky_blue": "Блакітны", "skin_medium_blue": "Сіні",
    "skin_dark_violet": "Фіялетавы", "skin_purple": "Пурпурны", "skin_lavender": "Лавандавы",
    "skin_white": "Белы", "skin_gold_yellow": "Жоўты", "skin_hot_pink": "Ружовы",
    "skin_default_green": "Зялёны", "skin_dark_orange": "Аранжавы", "skin_dark_turquoise": "Бірузовы",
    "skin_lawn_green": "Салатавы", "skin_saddle_brown": "Карычневы", "skin_dark_gray": "Шэры",
    "skin_medium_sea_green": "Мятны", "mods": "Моды", "active_mods": "Актыўныя моды",
    "no_mods": "Моды не знойдзены"
    },
    "tr": {
    "language": "Türkçe", "play": "Oyna", "settings": "Ayarlar", "exit": "Çıkış", "back": "Geri",
    "loading": "Yükleniyor...", "optimizing": "Oyun optimize ediliyor", "pause_title": "Duraklatıldı",
    "continue": "Devam Et", "menu": "Menü", "levels": "Seviyeler", "train": "Antrenman",
    "leaderboard": "Lider Tablosu", "change_nickname": "Takma Adı Değiştir",
    "settings_audio": "Ses Ayarları", "settings_graphics": "Grafik Ayarları",
    "settings_skins": "Görünüm Ayarları", "settings_language": "Dil",
    "volume_music": "Müzik Sesi", "volume_sound": "Ses Efekti Sesi", "sound_on": "Ses: Açık",
    "sound_off": "Ses: Kapalı", "resolution": "Çözünürlük", "fullscreen_on": "Tam Ekran: Açık",
    "fullscreen_off": "Tam Ekran: Kapalı", "apply": "Uygula", "skin_select": "Görünüm Seç",
    "level_select": "Seviye Seç", "level": "Seviye", "training_suffix": "(Antrenman)",
    "score": "Skor", "to_next_level": "Sonraki seviyeye", "points_abbr": "p.",
    "next_level_unlocked": "Sonraki seviye açıldı!", "next_level_button": "Sonraki Seviye",
    "game_over": "Oyun Bitti", "retry": "Tekrar Dene", "error_title": "Hata",
    "error_restart": "Lütfen oyunu yeniden başlatın.",
    "error_support": "Sorun devam ederse, destek ile iletişime geçin:", "error_site": "Site:",
    "game_title": "YILAN",
    "skin_crimson_red": "Kırmızı", "skin_light_sky_blue": "Açık Mavi", "skin_medium_blue": "Mavi",
    "skin_dark_violet": "Menekşe", "skin_purple": "Mor", "skin_lavender": "Lavanta",
    "skin_white": "Beyaz", "skin_gold_yellow": "Sarı", "skin_hot_pink": "Pembe",
    "skin_default_green": "Yeşil", "skin_dark_orange": "Turuncu", "skin_dark_turquoise": "Turkuaz",
    "skin_lawn_green": "Çimen Yeşili", "skin_saddle_brown": "Kahverengi", "skin_dark_gray": "Gri",
    "skin_medium_sea_green": "Nane", "mods": "Modlar", "active_mods": "Aktif Modlar",
    "no_mods": "Mod bulunamadı"
    },
    "pl": {
    "language": "Polski", "play": "Graj", "settings": "Ustawienia", "exit": "Wyjście", "back": "Wróć",
    "loading": "Ładowanie...", "optimizing": "Optymalizacja gry", "pause_title": "Pauza",
    "continue": "Kontynuuj", "menu": "Menu", "levels": "Poziomy", "train": "Trening",
    "leaderboard": "Tablica wyników", "change_nickname": "Zmień pseudonim",
    "settings_audio": "Ustawienia Dźwięku", "settings_graphics": "Ustawienia Grafiki",
    "settings_skins": "Ustawienia Skórek", "settings_language": "Język",
    "volume_music": "Głośność Muzyki", "volume_sound": "Głośność Dźwięków", "sound_on": "Dźwięk: Wł.",
    "sound_off": "Dźwięk: Wył.", "resolution": "Rozdzielczość", "fullscreen_on": "Pełny ekran: Wł.",
    "fullscreen_off": "Pełny ekran: Wył.", "apply": "Zastosuj", "skin_select": "Wybierz Skórkę",
    "level_select": "Wybierz Poziom", "level": "Poziom", "training_suffix": "(Trening)",
    "score": "Wynik", "to_next_level": "Do poziomu", "points_abbr": "pkt.",
    "next_level_unlocked": "Następny poziom odblokowany!", "next_level_button": "Następny Poziom",
    "game_over": "Koniec Gry", "retry": "Spróbuj ponownie", "error_title": "Błąd",
    "error_restart": "Proszę ponownie uruchomić grę.",
    "error_support": "Jeśli problem będzie się powtarzał, skontaktuj się z pomocą techniczną:", "error_site": "Strona:",
    "game_title": "WĄŻ",
    "skin_crimson_red": "Czerwony", "skin_light_sky_blue": "Błękitny", "skin_medium_blue": "Niebieski",
    "skin_dark_violet": "Fioletowy", "skin_purple": "Purpurowy", "skin_lavender": "Lawendowy",
    "skin_white": "Biały", "skin_gold_yellow": "Żółty", "skin_hot_pink": "Różowy",
    "skin_default_green": "Zielony", "skin_dark_orange": "Pomarańczowy", "skin_dark_turquoise": "Turkusowy",
    "skin_lawn_green": "Limonkowy", "skin_saddle_brown": "Brązowy", "skin_dark_gray": "Szary",
    "skin_medium_sea_green": "Miętowy", "mods": "Mody", "active_mods": "Aktywne mody",
    "no_mods": "Nie znaleziono modów"
    },
    "de": {
    "language": "Deutsch", "play": "Spielen", "settings": "Einstellungen", "exit": "Beenden", "back": "Zurück",
    "loading": "Wird geladen...", "optimizing": "Spiel wird optimiert", "pause_title": "Pause",
    "continue": "Fortsetzen", "menu": "Menü", "levels": "Level", "train": "Training",
    "leaderboard": "Bestenliste", "change_nickname": "Spitznamen ändern",
    "settings_audio": "Audioeinstellungen", "settings_graphics": "Grafikeinstellungen",
    "settings_skins": "Skin-Einstellungen", "settings_language": "Sprache",
    "volume_music": "Musiklautstärke", "volume_sound": "Soundlautstärke", "sound_on": "Ton: Ein",
    "sound_off": "Ton: Aus", "resolution": "Auflösung", "fullscreen_on": "Vollbild: Ein",
    "fullscreen_off": "Vollbild: Aus", "apply": "Anwenden", "skin_select": "Skin auswählen",
    "level_select": "Level auswählen", "level": "Level", "training_suffix": "(Training)",
    "score": "Punkte", "to_next_level": "Bis Level", "points_abbr": "Pkt.",
    "next_level_unlocked": "Nächstes Level freigeschaltet!", "next_level_button": "Nächstes Level",
    "game_over": "Spiel vorbei", "retry": "Erneut versuchen", "error_title": "Fehler",
    "error_restart": "Bitte starten Sie das Spiel neu.",
    "error_support": "Wenn das Problem weiterhin besteht, wenden Sie sich an den Support:", "error_site": "Webseite:",
    "game_title": "SNAKE",
    "skin_crimson_red": "Rot", "skin_light_sky_blue": "Hellblau", "skin_medium_blue": "Blau",
    "skin_dark_violet": "Violett", "skin_purple": "Lila", "skin_lavender": "Lavendel",
    "skin_white": "Weiß", "skin_gold_yellow": "Gelb", "skin_hot_pink": "Pink",
    "skin_default_green": "Grün", "skin_dark_orange": "Orange", "skin_dark_turquoise": "Türkis",
    "skin_lawn_green": "Limette", "skin_saddle_brown": "Braun", "skin_dark_gray": "Grau",
    "skin_medium_sea_green": "Minze", "mods": "Mods", "active_mods": "Aktive Mods",
    "no_mods": "Keine Mods gefunden"
    }
}

# --- Допоміжні функції ---

def log_exception():
    """Записує детальну інформацію про виняток у лог-файл."""
    try:
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n=== [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ===\n")
            traceback.print_exc(file=f)
        print(f"Помилку записано у файл {ERROR_LOG_FILE}")
    except Exception as log_err:
        print(f"Критична помилка: Не вдалося записати лог помилок! {log_err}")

def resource_path(relative_path):
    """Отримує абсолютний шлях до ресурсу, працює для розробки та для PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_json_file(filepath, default_data):
    """Безпечно завантажує JSON-файл."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Попередження: Не вдалося завантажити {filepath}. Використовуються типові дані.")
        return json.loads(json.dumps(default_data)) # Глибоке копіювання
    except Exception as e:
        print(f"Помилка завантаження {filepath}: {e}")
        log_exception()
        return json.loads(json.dumps(default_data)) # Глибоке копіювання

def save_json_file(filepath, data):
    """Безпечно зберігає дані у JSON-файл."""
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Помилка збереження {filepath}: {e}")
        log_exception()
        return False

# --- Клас гри ---
class SnakeGame:
    def __init__(self):
        """Ініціалізація гри, Pygame, налаштувань, ресурсів."""
        try:
            self.settings = load_json_file(SETTINGS_FILE, DEFAULT_SETTINGS)
            self._ensure_settings_structure()

            pygame.init()
            pygame.mixer.init()

            self._apply_graphics_settings()

            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 28)
            self.clock = pygame.time.Clock()
            self.running = True
            self.game_running = False
            self.paused = False
            self.current_level = None
            self.training_mode = False
            self.next_level_available = False
            self.next_button_rect = None
            self.new_level_unlocked_message = ""
            self.new_level_timer = 0
            self.foods = []
            self.snake = []
            self._start_next_level_on_exit = False
            self.emoji_cache = {}

            # --- НОВА ЛОГІКА МОДІВ ---
            self.available_mods = []
            self.mod_states = {}
            self.custom_levels = []
            self.levels = []
            
            # На старті гри знаходимо моди, завантажуємо їх стан і застосовуємо активні
            self.discover_mods()
            self.load_mod_states()
            self.apply_mods()
            # --- КІНЕЦЬ НОВОЇ ЛОГІКИ ---
            
            self.loading_screen()

            self.sounds = self._load_sounds()
            try:
                self.apple_img = pygame.image.load(resource_path("assets/food/apple.png")).convert_alpha()
                scale = int(CELL_SIZE * 1.0)
                self.apple_img = pygame.transform.scale(self.apple_img, (scale, scale))
            except Exception as e:
                print(f"Помилка завантаження зображення яблука: {e}")
                self.apple_img = None # Встановлюємо None, щоб уникнути падіння при малюванні

            self.level_progress = load_json_file(LEVEL_PROGRESS_FILE, {"unlocked_levels": [0]})
            self.leaderboard = load_json_file(LEADERBOARD_FILE, [])
            
            self.play_music("menu")

        except Exception as e:
            print(f"Критична помилка під час ініціалізації гри: {e}")
            log_exception()
            self.show_critical_error_screen(str(e))
            self.running = False


    def spawn_food(self):
        """Створює їжу у випадковій вільній клітинці."""
        while True:
            x = random.randint(0, (self.width // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (self.height // CELL_SIZE) - 1) * CELL_SIZE
            if (x, y) not in self.snake and (x, y) not in self.obstacles:
                self.foods = [(x, y)]
                break


    def _apply_graphics_settings(self):
        """Застосовує графічні налаштування з файлу."""
        try:
            resolution = self.settings["graphics"].get("resolution", "1024x768")
            if resolution not in AVAILABLE_RESOLUTIONS:
                resolution = "1024x768"
                self.settings["graphics"]["resolution"] = resolution
            
            self.width, self.height = map(int, resolution.split("x"))
            
            flags = 0
            if self.settings["graphics"].get("fullscreen", False):
                flags = pygame.FULLSCREEN | pygame.SCALED

            self.screen = pygame.display.set_mode((self.width, self.height), flags)
            pygame.display.set_caption(self.get_text("game_title"))
        except Exception as e:
            print(f"Помилка застосування графічних налаштувань: {e}")
            log_exception()
            self.width, self.height = 800, 600
            self.screen = pygame.display.set_mode((self.width, self.height))

    def _ensure_settings_structure(self):
        """Переконується, що словник налаштувань має всі необхідні ключі."""
        changed = False
        temp_settings = copy.deepcopy(self.settings)
        for key, default_value in DEFAULT_SETTINGS.items():
            if key not in temp_settings:
                temp_settings[key] = json.loads(json.dumps(default_value))
                changed = True
            elif isinstance(default_value, dict):
                if not isinstance(temp_settings.get(key), dict):
                    temp_settings[key] = json.loads(json.dumps(default_value))
                    changed = True
                else:
                    for sub_key, sub_default_value in default_value.items():
                        if sub_key not in temp_settings[key]:
                            temp_settings[key][sub_key] = sub_default_value
                            changed = True
        if changed:
            self.settings = temp_settings
            print("Структуру налаштувань оновлено.")
            save_json_file(SETTINGS_FILE, self.settings)

    def _load_sounds(self):
        """Завантажує звукові ефекти."""
        sounds = {}
        sound_files = {
            "eat": "assets/music/eat.wav", 
            "collision": "assets/music/collision.wav", 
            "click": "assets/music/click.wav"
        }
        if self.settings["audio"]["sound_enabled"]:
            for name, path in sound_files.items():
                try:
                    sounds[name] = pygame.mixer.Sound(resource_path(path))
                except Exception as e:
                    print(f"Попередження: Не вдалося завантажити звук '{name}': {e}")
        return sounds

    def play_sound(self, name):
        """Відтворює звуковий ефект з поточною гучністю."""
        if self.settings["audio"]["sound_enabled"] and name in self.sounds:
            try:
                self.sounds[name].set_volume(self.settings["audio"]["sound_volume"])
                self.sounds[name].play()
            except Exception as e:
                print(f"Помилка відтворення звуку '{name}': {e}")

    def play_music(self, music_type, level_data=None):
        """Відтворює фонову музику залежно від контексту."""
        volume = self.settings["audio"]["music_volume"]
        pygame.mixer.music.set_volume(volume)
        if volume == 0:
            pygame.mixer.music.stop()
            return

        path = None
        music_map = {
            "menu": "assets/music/menu_music.mp3",
            "game": "assets/music/Snake_Rattle_Dendy.mp3",
            "training": "assets/music/training-mode.mp3",
            "game_over": "assets/music/gаme_over.mp3"
        }
        
        if music_type == "level" and level_data:
            level_music_file = level_data.get("music")
            if level_music_file:
                path = resource_path(f"assets/levels/{level_music_file}")
            else:
                path = resource_path(music_map["game"])
        elif music_type in music_map:
            path = resource_path(music_map[music_type])

        if path and os.path.exists(path):
            try:
                current_music = pygame.mixer.music.get_pos()
                if current_music != -1 and pygame.mixer.music.get_busy():
                     # Щоб уникнути перезапуску тієї ж мелодії
                    if hasattr(self, 'current_music_path') and self.current_music_path == path:
                        return
                
                pygame.mixer.music.stop()
                pygame.mixer.music.load(path)
                pygame.mixer.music.play(-1) # -1 для зациклювання
                self.current_music_path = path
            except Exception as e:
                print(f"Помилка відтворення музики {path}: {e}")
        elif path:
            print(f"Попередження: Файл музики не знайдено: {path}")

    def get_text(self, key):
        """Отримує перекладений текст за ключем."""
        lang_code = self.settings["profile"].get("language", "en")
        return LANGUAGES.get(lang_code, LANGUAGES["en"]).get(key, f"<{key}_missing>")

    def loading_screen(self):
        """Екран завантаження гри."""
        # Ця функція залишається без змін, оскільки вона вже функціональна.
        loading_active = True; percent = 0; start_time = pygame.time.get_ticks(); duration = 1500 # Швидше завантаження
        error = None; link_rect = None; support_site = "afercorporftaon.onepage.me"
        try: self._check_critical_files(); print("Перевірка крит. файлів успішна.")
        except Exception as e: error = str(e); log_exception()
        while loading_active:
            elapsed = pygame.time.get_ticks() - start_time; percent = min(100, int((elapsed / duration) * 100))
            self.screen.fill(BG_COLOR)
            if error:
                title = self.font.render(self.get_text("error_title"), True, ERROR_TEXT_COLOR); self.screen.blit(title, (self.width // 2 - title.get_width() // 2, self.height // 2 - 120))
                lines = [self.get_text("error_restart"), self.get_text("error_support"), f"{self.get_text('error_site')} {support_site}"]
                for i, line in enumerate(lines): text = self.font.render(line, True, INFO_TEXT_COLOR); text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 40 + i * 50)); self.screen.blit(text, text_rect);
                if self.get_text('error_site') in line: link_rect = text_rect; pygame.draw.line(self.screen, INFO_TEXT_COLOR, text_rect.bottomleft, text_rect.bottomright, 1)
            else:
                text = self.font.render(f"{self.get_text('loading')} {self.get_text('optimizing')}", True, TEXT_COLOR); self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 80))
                bar_width = self.width * 0.6; bar_height = 40; bar_x = self.width // 2 - bar_width // 2; bar_y = self.height // 2
                pygame.draw.rect(self.screen, PROGRESS_BAR_BG, (bar_x, bar_y, bar_width, bar_height), border_radius=10); current_width = bar_width * (percent / 100); pygame.draw.rect(self.screen, PROGRESS_BAR_FG, (bar_x, bar_y, current_width, bar_height), border_radius=10)
                percent_text = self.font.render(f"{percent}%", True, TEXT_COLOR); self.screen.blit(percent_text, (self.width // 2 - percent_text.get_width() // 2, bar_y + bar_height + 10))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.exit_game()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.exit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if error and link_rect and link_rect.collidepoint(event.pos):
                        try: webbrowser.open(f"https://{support_site}")
                        except Exception as wb_err: print(f"Не вдалося відкрити посилання: {wb_err}")
            if percent >= 100 and not error: loading_active = False
            self.clock.tick(self.settings["graphics"].get("fps", 60))

    def _check_critical_files(self):
        """Перевіряє наявність критично важливих файлів."""
        print("Перевірка крит. файлів...")
        required = ["assets/music/eat.wav", "assets/music/collision.wav", "assets/music/click.wav", 
                    "assets/music/menu_music.mp3", "assets/emoji/lock.png", "assets/emoji/skull.png", 
                    "assets/emoji/snake.png", "assets/emoji/trophy.png", "assets/food/apple.png"]
        missing = [p for p in required if not os.path.exists(resource_path(p))]
        if missing:
            print(f"ПОПЕРЕДЖЕННЯ: Відсутні файли: {', '.join(missing)}.")
        else:
            print("Крит. файли на місці.")

    def draw_emoji(self, name, x, y, size=64):
        """Малює емодзі з кешуванням для оптимізації."""
        cache_key = (name, size)
        if cache_key in self.emoji_cache:
            img = self.emoji_cache[cache_key]
        else:
            try:
                path = resource_path(f"assets/emoji/{name}.png")
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (size, size))
                self.emoji_cache[cache_key] = img
            except Exception as e:
                print(f"Попередження: Не вдалося завантажити емодзі '{name}': {e}")
                # Малюємо замінник, якщо зображення немає
                rect = pygame.Rect(x, y, size, size)
                pygame.draw.rect(self.screen, WARN_TEXT_COLOR, rect, 2)
                return
        self.screen.blit(img, (x, y))

    # --- Меню та UI ---
    def _create_button_rects(self, button_keys, start_y_offset=0, button_width=300, button_height=60, spacing=20):
        """Допоміжна функція для створення прямокутників кнопок."""
        rects = []
        total_height = len(button_keys) * button_height + (len(button_keys) - 1) * spacing
        start_y = (self.height - total_height) // 2 + start_y_offset
        for i, key in enumerate(button_keys):
            rect = pygame.Rect(self.width // 2 - button_width // 2, start_y + i * (button_height + spacing), button_width, button_height)
            rects.append((rect, key))
        return rects

    def _draw_buttons(self, button_rect_data, mouse_pos):
        """Малює кнопки зі списку (rect, text_key)."""
        for rect, text_key in button_rect_data:
            color = HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            label = self.font.render(self.get_text(text_key), True, TEXT_COLOR)
            self.screen.blit(label, label.get_rect(center=rect.center))

    def show_menu(self):
        """Показує головне меню гри."""
        menu_active = True
        self.play_music("menu")

        # Список дій для кнопок
        actions = {
            "play": lambda: self.run_game(start_level=None),
            "levels": self.level_select_menu,
            "train": lambda: self.run_game(training=True),
            "leaderboard": self.show_leaderboard,
            "mods": self.show_mods_menu,
            "settings": self.show_settings_menu,
            "change_nickname": self.change_nickname_menu,
            "exit": self.exit_game
        }
        
        # Створюємо прямокутники для основних кнопок
        main_button_keys = ["play", "levels", "train", "leaderboard", "mods", "settings", "exit"]
        button_rect_data = self._create_button_rects(main_button_keys, start_y_offset=40, button_width=350)

        # Створюємо кнопку для зміни ніку окремо
        nickname_text = self.settings["profile"].get("nickname", "Гравець")
        nickname_label = self.font.render(nickname_text, True, TEXT_COLOR)
        change_nick_button_text = self.get_text("change_nickname")
        change_nick_label = self.small_font.render(f"[{change_nick_button_text}]", True, HOVER_COLOR)
        
        # Позиція тексту нікнейму
        nickname_pos_x = self.width // 2 - (nickname_label.get_width() + change_nick_label.get_width() + 10) // 2
        nickname_pos_y = 70
        
        # Створюємо клікабельну область для кнопки зміни ніку
        change_nick_rect = change_nick_label.get_rect(
            topleft=(nickname_pos_x + nickname_label.get_width() + 10, nickname_pos_y + 5)
        )

        while menu_active:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(BG_COLOR)
            
            # Малюємо заголовок
            title_label = self.font.render(self.get_text("game_title"), True, TEXT_COLOR)
            self.screen.blit(title_label, (self.width // 2 - title_label.get_width() // 2, 20))

            # Малюємо нікнейм та кнопку зміни
            self.screen.blit(nickname_label, (nickname_pos_x, nickname_pos_y))
            self.screen.blit(change_nick_label, change_nick_rect.topleft)

            # Малюємо основні кнопки
            self._draw_buttons(button_rect_data, mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.exit_game()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.play_sound("click")
                    # Перевірка натискання на основні кнопки
                    for rect, key in button_rect_data:
                        if rect.collidepoint(mouse_pos):
                            actions[key]()
                            menu_active = False # Виходимо з меню після дії
                    
                    # Перевірка натискання на кнопку зміни ніку
                    if change_nick_rect.collidepoint(mouse_pos):
                        actions["change_nickname"]()
                        # Оскільки зміна ніку повертає нас в меню, не виходимо з циклу
                        # Але потрібно оновити відображення нікнейму після повернення
                        nickname_text = self.settings["profile"].get("nickname", "Гравець")
                        nickname_label = self.font.render(nickname_text, True, TEXT_COLOR)


            pygame.display.flip()
            self.clock.tick(self.settings["graphics"]["fps"])

    # --- MOD SYSTEM ---
    def discover_mods(self):
        """Знаходить усі доступні моди (рівні) у папці 'mods'."""
        self.available_mods = []
        mods_dir = "mods"
        if not os.path.isdir(mods_dir):
            os.makedirs(mods_dir)
            print(f"Створено папку '{mods_dir}'. Помістіть ваші моди сюди.")
            return

        # Розпаковуємо zip-архіви, якщо є
        for filename in os.listdir(mods_dir):
            if filename.endswith(".zip"):
                zip_path = os.path.join(mods_dir, filename)
                extract_path = os.path.join(mods_dir, filename[:-4])
                try:
                    import zipfile
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_path)
                    print(f"Розпаковано мод '{filename}' до '{extract_path}'")
                except Exception as e:
                    print(f"Не вдалося розпакувати мод '{filename}': {e}")
        
        # Шукаємо файли модів
        for root, _, files in os.walk(mods_dir):
            for file in files:
                if file.endswith(".json"):
                    mod_name = os.path.splitext(file)[0]
                    if mod_name not in self.available_mods:
                        self.available_mods.append(mod_name)
        print(f"Знайдено моди: {self.available_mods if self.available_mods else 'немає'}")

    def load_mod_states(self):
        """Завантажує стан (увімк/вимк) модів з файлу."""
        self.mod_states = load_json_file(MOD_STATES_FILE, {})
        # Переконуємось, що для всіх знайдених модів є запис у станах
        changed = False
        for mod_name in self.available_mods:
            if mod_name not in self.mod_states:
                self.mod_states[mod_name] = False # Нові моди типово вимкнені
                changed = True
        if changed:
            self.save_mod_states()
    
    def save_mod_states(self):
        """Зберігає поточний стан модів у файл."""
        save_json_file(MOD_STATES_FILE, self.mod_states)
        print("Стан модів збережено.")

    def apply_mods(self):
        """Застосовує увімкнені моди, додаючи їхні рівні до основного списку."""
        print("Застосування модів...")
        # Починаємо з базових рівнів
        self.levels = load_json_file(resource_path(LEVELS_FILE), [])
        self.custom_levels = []
        mods_dir = "mods"

        for mod_name in self.available_mods:
            if self.mod_states.get(mod_name, False): # Якщо мод увімкнено
                found_path = None
                for root, _, files in os.walk(mods_dir):
                    if f"{mod_name}.json" in files:
                        found_path = os.path.join(root, f"{mod_name}.json")
                        break
                
                if found_path:
                    try:
                        level_data = load_json_file(found_path, None)
                        if isinstance(level_data, dict) and "goal_score" in level_data:
                            level_data['name'] = level_data.get('name', mod_name)
                            level_data['mod_source'] = mod_name
                            self.custom_levels.append(level_data)
                            print(f"✅ Мод-рівень '{mod_name}' активовано.")
                        else:
                             print(f"⚠️ Файл моду '{mod_name}' має неправильний формат.")
                    except Exception as e:
                        print(f"❌ Не вдалося завантажити мод-рівень '{mod_name}': {e}")
        
        # Додаємо кастомні рівні до основного списку
        self.levels.extend(self.custom_levels)
        print(f"Застосовано модів. Загальна кількість рівнів: {len(self.levels)}")

    def show_mods_menu(self):
        """Меню для увімкнення/вимкнення модів."""
        self.play_sound("click")
        menu_active = True
        
        while menu_active:
            self.screen.fill(BG_COLOR)
            title = self.font.render(self.get_text("mods"), True, TEXT_COLOR)
            self.screen.blit(title, title.get_rect(center=(self.width // 2, 60)))
            mouse_pos = pygame.mouse.get_pos()
            
            y_offset = 120
            checkbox_size = 30
            checkbox_rects = []

            if not self.available_mods:
                no_mods_text = self.font.render(self.get_text("no_mods"), True, INFO_TEXT_COLOR)
                self.screen.blit(no_mods_text, no_mods_text.get_rect(center=(self.width // 2, self.height // 2)))
            else:
                for mod_name in self.available_mods:
                    checked = self.mod_states.get(mod_name, False)
                    rect = pygame.Rect(100, y_offset, checkbox_size, checkbox_size)
                    checkbox_rects.append((rect, mod_name))
                    
                    pygame.draw.rect(self.screen, TEXT_COLOR, rect, border_radius=4, width=2)
                    if checked:
                        pygame.draw.line(self.screen, TEXT_COLOR, (rect.left + 5, rect.centery), (rect.centerx, rect.bottom - 5), 3)
                        pygame.draw.line(self.screen, TEXT_COLOR, (rect.centerx, rect.bottom - 5), (rect.right - 5, rect.top + 5), 3)
                    
                    label = self.font.render(mod_name, True, TEXT_COLOR)
                    self.screen.blit(label, (rect.right + 20, rect.top))
                    y_offset += 50

            # Кнопки
            back_button = pygame.Rect(self.width // 2 - 100, self.height - 70, 200, 50)
            apply_button = pygame.Rect(self.width // 2 - 100, self.height - 140, 200, 50)

            # Малювання кнопок
            self._draw_buttons([(apply_button, "apply"), (back_button, "back")], mouse_pos)
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    menu_active = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(mouse_pos):
                        self.play_sound("click")
                        menu_active = False # Просто виходимо з меню
                    elif apply_button.collidepoint(mouse_pos):
                        self.play_sound("click")
                        self.apply_mods() # Застосовуємо зміни
                        self.save_mod_states() # Зберігаємо їх
                    else:
                        for rect, mod_name in checkbox_rects:
                            if rect.collidepoint(mouse_pos):
                                self.mod_states[mod_name] = not self.mod_states.get(mod_name, False)
                                self.play_sound("click")
                                break
        # Після виходу з меню повертаємось до головного меню
        self.show_menu()
        return

    def show_leaderboard(self):
        """Показує таблицю лідерів."""
        menu_active = True
        self.play_sound("click")
        self.leaderboard = load_json_file(LEADERBOARD_FILE, [])
        sorted_leaderboard = sorted(self.leaderboard, key=lambda x: x.get('score', 0), reverse=True)
        displayed_entries = sorted_leaderboard[:10]
        back_button_rect = pygame.Rect(self.width // 2 - 100, self.height - 80, 200, 50)
        
        while menu_active:
            self.screen.fill(BG_COLOR)
            title = self.font.render(self.get_text("leaderboard"), True, TEXT_COLOR)
            title_rect = title.get_rect(center=(self.width // 2, 60))
            self.screen.blit(title, title_rect)
            self.draw_emoji("trophy", title_rect.left - 70, title_rect.top - 10)
            
            entry_height = 40; start_y = 150; max_width = self.width - 40
            headers = ["#", self.get_text("nickname"), self.get_text("score"), self.get_text("level")]
            col_widths = [40, max_width // 2, max_width // 4, max_width // 4]
            header_y = start_y - 30
            current_x = 40
            for header, width in zip(headers, col_widths):
                header_text = self.small_font.render(header, True, TEXT_COLOR)
                self.screen.blit(header_text, (current_x, header_y))
                current_x += width

            for i, entry in enumerate(displayed_entries):
                y = start_y + i * entry_height
                rank = str(i + 1)
                nickname = entry.get('nickname', '???')
                score = str(entry.get('score', 0))
                level = str(entry.get('level', '-'))
                if len(nickname) > 20:
                    nickname = nickname[:18] + "..."
                
                columns = [rank, nickname, score, level]
                current_x = 40
                for text, width in zip(columns, col_widths):
                    text_surface = self.small_font.render(text, True, INFO_TEXT_COLOR)
                    self.screen.blit(text_surface, (current_x, y))
                    current_x += width

            mouse_pos = pygame.mouse.get_pos()
            self._draw_buttons([(back_button_rect, "back")], mouse_pos)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    menu_active = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button_rect.collidepoint(mouse_pos):
                        self.play_sound("click")
                        menu_active = False # Вихід з циклу, повернення до show_menu()
            
            self.clock.tick(self.settings["graphics"].get("fps", 60))
    
    def save_score_to_leaderboard(self, score, is_training=False, level_index=None):
        """Зберігає рахунок гравця до таблиці лідерів."""
        if is_training or score <= 0: # Не зберігаємо результати тренування або нульовий рахунок
            return
            
        try:
            leaderboard = load_json_file(LEADERBOARD_FILE, [])
            
            level_display = "-"
            if level_index is not None:
                # Намагаємось отримати назву рівня
                try:
                    level_display = self.levels[level_index].get('name', str(level_index + 1))
                except IndexError:
                    level_display = str(level_index + 1)
            
            new_entry = {
                'nickname': self.settings["profile"]["nickname"],
                'score': score,
                'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                'level': level_display
            }
            leaderboard.append(new_entry)
            save_json_file(LEADERBOARD_FILE, leaderboard)
        except Exception as e:
            print(f"Помилка збереження до таблиці лідерів: {e}")
            log_exception()
    
    def level_select_menu(self):
        """Меню вибору рівнів з гортанням та замками."""
        if not self.levels:
            # Показати повідомлення, що рівнів немає і повернутися
            print("Рівні не знайдено або не завантажено.")
            # Тут можна додати простий екран-повідомлення для гравця
            self.show_menu()
            return

        self.play_sound("click")
        menu_active = True
        levels_per_page = 20
        total_levels = len(self.levels) # --- ВИПРАВЛЕНО: Динамічна кількість рівнів ---
        current_page = 0
        total_pages = (total_levels + levels_per_page - 1) // levels_per_page

        level_width, level_height = 120, 60
        spacing_x, spacing_y = 20, 20
        cols, rows = 5, 4
        start_x = (self.width - (level_width * cols + spacing_x * (cols - 1))) // 2
        start_y = 150

        back_button_rect = pygame.Rect(self.width // 2 - 100, self.height - 70, 200, 50)
        left_arrow_rect = pygame.Rect(40, self.height // 2 - 25, 50, 50)
        right_arrow_rect = pygame.Rect(self.width - 90, self.height // 2 - 25, 50, 50)

        while menu_active:
            self.screen.fill(BG_COLOR)
            title = self.font.render(self.get_text("level_select"), True, TEXT_COLOR)
            self.screen.blit(title, title.get_rect(center=(self.width // 2, 60)))
            mouse_pos = pygame.mouse.get_pos()

            start_level_idx = current_page * levels_per_page
            end_level_idx = min(start_level_idx + levels_per_page, total_levels)
            
            level_rects = []

            for i, level_index in enumerate(range(start_level_idx, end_level_idx)):
                col, row = i % cols, i // cols
                x = start_x + col * (level_width + spacing_x)
                y = start_y + row * (level_height + spacing_y)
                rect = pygame.Rect(x, y, level_width, level_height)
                level_rects.append((rect, level_index))

                unlocked = level_index in self.level_progress.get("unlocked_levels", [0])
                pygame.draw.rect(self.screen, UNLOCKED_LEVEL_COLOR if unlocked else LOCKED_LEVEL_COLOR, rect, border_radius=8)

                if unlocked:
                    level_name = self.levels[level_index].get('name', str(level_index + 1))
                    if len(level_name) > 10: level_name = level_name[:9] + "…"
                    label = self.small_font.render(level_name, True, (255, 255, 255))
                    self.screen.blit(label, label.get_rect(center=rect.center))
                else:
                    self.draw_emoji("lock", rect.centerx - 16, rect.centery - 16, size=32)

            # Кнопки
            if current_page > 0:
                pygame.draw.rect(self.screen, BUTTON_COLOR if not left_arrow_rect.collidepoint(mouse_pos) else HOVER_COLOR, left_arrow_rect, border_radius=8)
                self.screen.blit(self.font.render("←", True, TEXT_COLOR), self.font.render("←", True, TEXT_COLOR).get_rect(center=left_arrow_rect.center))

            if current_page < total_pages - 1:
                pygame.draw.rect(self.screen, BUTTON_COLOR if not right_arrow_rect.collidepoint(mouse_pos) else HOVER_COLOR, right_arrow_rect, border_radius=8)
                self.screen.blit(self.font.render("→", True, TEXT_COLOR), self.font.render("→", True, TEXT_COLOR).get_rect(center=right_arrow_rect.center))
            
            self._draw_buttons([(back_button_rect, "back")], mouse_pos)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    menu_active = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button_rect.collidepoint(mouse_pos):
                        self.play_sound("click")
                        menu_active = False
                    elif current_page > 0 and left_arrow_rect.collidepoint(mouse_pos):
                        self.play_sound("click")
                        current_page -= 1
                    elif current_page < total_pages - 1 and right_arrow_rect.collidepoint(mouse_pos):
                        self.play_sound("click")
                        current_page += 1
                    else:
                        for rect, level_idx in level_rects:
                            unlocked = level_idx in self.level_progress.get("unlocked_levels", [0])
                            if unlocked and rect.collidepoint(mouse_pos):
                                self.play_sound("click")
                                self.run_game(start_level=level_idx)
                                return # Вихід з меню, бо гра почалась

            self.clock.tick(self.settings["graphics"].get("fps", 60))
        
        # Якщо вийшли з циклу (напр. через ESC), повертаємось в головне меню
        self.show_menu()
        return

    # --- Налаштування ---
    # Код для підменю налаштувань (аудіо, графіка, скіни, мова) залишається здебільшого без змін,
    # але їхній виклик і повернення тепер коректно обробляються головним меню.
    # Я залишу одну функцію як приклад. Решта працюватимуть аналогічно.
    def show_settings_menu(self):
        self.play_sound("click")
        menu_active = True
        
        button_keys = ["settings_audio", "settings_graphics", "settings_skins", "settings_language"]
        actions = {
            "settings_audio": self.show_audio_settings,
            "settings_graphics": self.show_graphics_settings,
            "settings_skins": self.show_skin_settings,
            "settings_language": self.show_language_settings
        }
        
        button_rect_data = self._create_button_rects(button_keys, start_y_offset=-20, button_height=50)
        back_button_rect = pygame.Rect(self.width // 2 - 100, self.height - 80, 200, 50)
        button_rect_data.append((back_button_rect, "back"))

        while menu_active:
            self.screen.fill(BG_COLOR)
            title = self.font.render(self.get_text("settings"), True, TEXT_COLOR)
            self.screen.blit(title, title.get_rect(center=(self.width // 2, 80)))
            
            mouse_pos = pygame.mouse.get_pos()
            self._draw_buttons(button_rect_data, mouse_pos)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    save_json_file(SETTINGS_FILE, self.settings)
                    menu_active = False # Вихід з циклу, повернення до show_menu()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, key in button_rect_data:
                        if rect.collidepoint(mouse_pos):
                            self.play_sound("click")
                            if key == "back":
                                save_json_file(SETTINGS_FILE, self.settings)
                                menu_active = False # Вихід з циклу
                            else:
                                actions[key]() # Викликаємо підменю
                                # Після повернення з підменю, цей цикл продовжиться
                            break
        
        self.show_menu()
        return

    def change_nickname_menu(self):
        """Меню для зміни нікнейму гравця."""
        # Ця функція в цілому працює, але ми виправимо повернення до меню
        input_active = True
        current_nickname = self.settings["profile"]["nickname"]
        max_nickname_length = 15
        input_box_rect = pygame.Rect(self.width // 2 - 150, self.height // 2 - 30, 300, 60)
        back_button_rect = pygame.Rect(self.width // 2 - 100, self.height - 100, 200, 50)

        while input_active:
            self.screen.fill(BG_COLOR)
            title = self.font.render(self.get_text("change_nickname"), True, TEXT_COLOR)
            self.screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 3)))
            
            pygame.draw.rect(self.screen, BUTTON_COLOR, input_box_rect, border_radius=10)
            nickname_surface = self.font.render(current_nickname, True, TEXT_COLOR)
            self.screen.blit(nickname_surface, nickname_surface.get_rect(midleft=(input_box_rect.left + 15, input_box_rect.centery)))

            mouse_pos = pygame.mouse.get_pos()
            self._draw_buttons([(back_button_rect, "back")], mouse_pos)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        input_active = False # Виходимо з циклу
                    elif event.key == pygame.K_RETURN:
                        if current_nickname.strip():
                            self.settings["profile"]["nickname"] = current_nickname.strip()
                            save_json_file(SETTINGS_FILE, self.settings)
                            input_active = False # Виходимо з циклу
                        else:
                            current_nickname = self.settings["profile"]["nickname"] # Скидаємо, якщо пустий
                    elif event.key == pygame.K_BACKSPACE:
                        current_nickname = current_nickname[:-1]
                    else:
                        if len(current_nickname) < max_nickname_length and (event.unicode.isalnum() or event.unicode in ' _-'):
                            current_nickname += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button_rect.collidepoint(event.pos):
                        self.play_sound("click")
                        input_active = False # Виходимо з циклу
        
        # Після виходу з циклу, керування повернеться до того меню, що викликало цю функцію.
        # Не потрібно викликати show_menu() тут.

    # Інші функції налаштувань (audio, graphics, skins, language) залишаються
    # здебільшого без змін, оскільки їхня внутрішня логіка коректна.
    # Головне - виправлена логіка виклику/повернення в/з них.
    def show_audio_settings(self):
        submenu_active = True

        # Кнопки
        back_button = pygame.Rect(self.width // 2 - 100, self.height - 80, 200, 50)

        while submenu_active:
            self.screen.fill(BG_COLOR)

            title = self.font.render(self.get_text("settings_audio"), True, TEXT_COLOR)
            self.screen.blit(title, title.get_rect(center=(self.width // 2, 80)))

            mouse_pos = pygame.mouse.get_pos()

            # --- Повзунок музики ---
            music_rect = pygame.Rect(200, 200, 300, 20)
            pygame.draw.rect(self.screen, PROGRESS_BAR_BG, music_rect)
            music_fill = int(self.settings["audio"]["music_volume"] * music_rect.width)
            pygame.draw.rect(self.screen, PROGRESS_BAR_FG, (music_rect.x, music_rect.y, music_fill, music_rect.height))
            self.screen.blit(self.small_font.render(self.get_text("volume_music"), True, TEXT_COLOR), (200, 170))

            # --- Повзунок звуків ---
            sound_rect = pygame.Rect(200, 300, 300, 20)
            pygame.draw.rect(self.screen, PROGRESS_BAR_BG, sound_rect)
            sound_fill = int(self.settings["audio"]["sound_volume"] * sound_rect.width)
            pygame.draw.rect(self.screen, PROGRESS_BAR_FG, (sound_rect.x, sound_rect.y, sound_fill, sound_rect.height))
            self.screen.blit(self.small_font.render(self.get_text("volume_sound"), True, TEXT_COLOR), (200, 270))

            # --- Перемикач звуку ---
            sound_status = self.get_text("sound_on") if self.settings["audio"]["sound_enabled"] else self.get_text("sound_off")
            status_rect = pygame.Rect(200, 370, 200, 40)
            pygame.draw.rect(self.screen, BUTTON_COLOR, status_rect, border_radius=8)
            self.screen.blit(self.small_font.render(sound_status, True, TEXT_COLOR), status_rect.move(10, 5))

            # Кнопка "Назад"
            self._draw_buttons([(back_button, "back")], mouse_pos)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.exit_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    submenu_active = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(mouse_pos):
                        save_json_file(SETTINGS_FILE, self.settings)
                        submenu_active = False
                    elif music_rect.collidepoint(mouse_pos):
                        rel_x = mouse_pos[0] - music_rect.x
                        self.settings["audio"]["music_volume"] = max(0, min(1, rel_x / music_rect.width))
                        pygame.mixer.music.set_volume(self.settings["audio"]["music_volume"])
                    elif sound_rect.collidepoint(mouse_pos):
                        rel_x = mouse_pos[0] - sound_rect.x
                        self.settings["audio"]["sound_volume"] = max(0, min(1, rel_x / sound_rect.width))
                    elif status_rect.collidepoint(mouse_pos):
                        self.settings["audio"]["sound_enabled"] = not self.settings["audio"]["sound_enabled"]



    def show_graphics_settings(self):
        submenu_active = True
        resolutions = AVAILABLE_RESOLUTIONS
        idx = resolutions.index(self.settings["graphics"]["resolution"])

        back_button = pygame.Rect(self.width // 2 - 100, self.height - 80, 200, 50)
        apply_button = pygame.Rect(self.width // 2 - 100, self.height - 150, 200, 50)

        while submenu_active:
            self.screen.fill(BG_COLOR)

            title = self.font.render(self.get_text("settings_graphics"), True, TEXT_COLOR)
            self.screen.blit(title, title.get_rect(center=(self.width // 2, 80)))

            mouse_pos = pygame.mouse.get_pos()

            # --- Список роздільних здатностей ---
            for i, res in enumerate(resolutions):
                rect = pygame.Rect(200, 180 + i * 40, 200, 35)
                color = HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
                pygame.draw.rect(self.screen, color, rect, border_radius=6)
                label = self.small_font.render(res, True, TEXT_COLOR)
                self.screen.blit(label, rect.move(10, 5))
                if rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                    idx = i

            # --- Fullscreen toggle ---
            fs_text = self.get_text("fullscreen_on") if self.settings["graphics"]["fullscreen"] else self.get_text("fullscreen_off")
            fs_rect = pygame.Rect(200, 400, 200, 40)
            pygame.draw.rect(self.screen, BUTTON_COLOR, fs_rect, border_radius=6)
            self.screen.blit(self.small_font.render(fs_text, True, TEXT_COLOR), fs_rect.move(10, 5))

            # Кнопки Apply / Back
            self._draw_buttons([(apply_button, "apply"), (back_button, "back")], mouse_pos)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.exit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(mouse_pos):
                        submenu_active = False
                    elif apply_button.collidepoint(mouse_pos):
                        self.settings["graphics"]["resolution"] = resolutions[idx]
                        self.settings["graphics"]["fullscreen"] = self.settings["graphics"]["fullscreen"]
                        save_json_file(SETTINGS_FILE, self.settings)
                        self._apply_graphics_settings()
                        submenu_active = False
                    elif fs_rect.collidepoint(mouse_pos):
                        self.settings["graphics"]["fullscreen"] = not self.settings["graphics"]["fullscreen"]


    def show_skin_settings(self):
        submenu_active = True
        back_button = pygame.Rect(self.width // 2 - 100, self.height - 80, 200, 50)

        skin_names = list(PREDEFINED_SKINS.keys())

        while submenu_active:
            self.screen.fill(BG_COLOR)

            title = self.font.render(self.get_text("settings_skins"), True, TEXT_COLOR)
            self.screen.blit(title, title.get_rect(center=(self.width // 2, 60)))

            mouse_pos = pygame.mouse.get_pos()

            rects = []
            start_x, start_y = 100, 150
            size = 50
            for i, name in enumerate(skin_names):
                x = start_x + (i % 6) * (size + 20)
                y = start_y + (i // 6) * (size + 20)
                rect = pygame.Rect(x, y, size, size)
                rects.append((rect, name))
                pygame.draw.rect(self.screen, PREDEFINED_SKINS[name], rect)
                if PREDEFINED_SKINS[name] == self.settings["appearance"]["skin_color"]:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 3)

            self._draw_buttons([(back_button, "back")], mouse_pos)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.exit_game()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(mouse_pos):
                        save_json_file(SETTINGS_FILE, self.settings)
                        submenu_active = False
                    for rect, name in rects:
                        if rect.collidepoint(mouse_pos):
                            self.settings["appearance"]["skin_color"] = PREDEFINED_SKINS[name]
                            save_json_file(SETTINGS_FILE, self.settings)


    
    def show_language_settings(self):
        submenu_active = True
        back_button = pygame.Rect(self.width // 2 - 100, self.height - 80, 200, 50)

        lang_codes = list(LANGUAGES.keys())

        while submenu_active:
            self.screen.fill(BG_COLOR)

            title = self.font.render(self.get_text("settings_language"), True, TEXT_COLOR)
            self.screen.blit(title, title.get_rect(center=(self.width // 2, 60)))

            mouse_pos = pygame.mouse.get_pos()
            rects = []
            start_y = 150
            for i, code in enumerate(lang_codes):
                rect = pygame.Rect(200, start_y + i * 50, 250, 40)
                rects.append((rect, code))
                color = HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
                pygame.draw.rect(self.screen, color, rect, border_radius=8)
                label = self.small_font.render(LANGUAGES[code]["language"], True, TEXT_COLOR)
                self.screen.blit(label, rect.move(10, 5))
                if code == self.settings["profile"]["language"]:
                    pygame.draw.rect(self.screen, (0, 255, 0), rect, 3)

            self._draw_buttons([(back_button, "back")], mouse_pos)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.exit_game()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(mouse_pos):
                        save_json_file(SETTINGS_FILE, self.settings)
                        submenu_active = False
                    for rect, code in rects:
                        if rect.collidepoint(mouse_pos):
                            self.settings["profile"]["language"] = code
                            save_json_file(SETTINGS_FILE, self.settings)


    # --- Основний ігровий процес ---
    # Ці функції залишаються переважно без змін, але тепер вони використовують
    # оновлений список self.levels, що включає моди.

    def pause_menu(self):
        """Меню паузи (ESC)."""
        self.paused = True
        menu_active = True

        continue_button = pygame.Rect(self.width // 2 - 100, self.height // 2 - 60, 200, 50)
        menu_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 10, 200, 50)

        while menu_active:
            self.screen.fill(BG_COLOR)

            title = self.font.render(self.get_text("pause_title"), True, TEXT_COLOR)
            self.screen.blit(title, title.get_rect(center=(self.width // 2, 150)))

            mouse_pos = pygame.mouse.get_pos()
            self._draw_buttons([(continue_button, "continue"), (menu_button, "menu")], mouse_pos)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.paused = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if continue_button.collidepoint(mouse_pos):
                        self.paused = False
                        return
                    elif menu_button.collidepoint(mouse_pos):
                        self.game_running = False
                        self.show_menu()
                        return

    def run_game(self, start_level=None, training=False):
        """Запускає гру з вибраного рівня або у тренувальному режимі."""
        self.game_running = True
        self.training_mode = training
        self.current_level = start_level if start_level is not None else 0

        # Ініціалізація
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = (CELL_SIZE, 0)
        self.foods = []
        self.spawn_food()   # 🍎 спавнимо їжу одразу
        self.score = 0
        self.paused = False

        # 🔧 перешкоди завжди список
        self.obstacles = []
        if not training and self.current_level is not None and self.current_level < len(self.levels):
            level_data = self.levels[self.current_level]
            if "obstacles" in level_data and isinstance(level_data["obstacles"], list):
                self.obstacles = level_data["obstacles"]

        # Музика
        if training:
            self.play_music("training")
        elif self.current_level is not None and self.current_level < len(self.levels):
            self.play_music("level", self.levels[self.current_level])
        else:
            self.play_music("game")

        # Основний цикл гри
        while self.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # 🔧 меню паузи
                        self.pause_menu()
                    elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        self.handle_direction(event.key)

            if not self.paused:
                self.update_snake()
                self.check_collisions()
                self.check_food()

            self.draw_game()
            self.clock.tick(self.settings["graphics"]["fps"])

    
    def start_snake(self):
        self.head_pos = pygame.math.Vector2(int(self.width / 2 // CELL_SIZE * CELL_SIZE), int(self.height / 2 // CELL_SIZE * CELL_SIZE))
        self.direction_vector = pygame.math.Vector2(CELL_SIZE, 0)
        self.next_direction = self.direction_vector.copy()
        self.snake = [self.head_pos - pygame.math.Vector2(i * CELL_SIZE, 0) for i in range(3)]
        self.score = 0
        self.foods = self._generate_multiple_foods(5)
        self.obstacles = []  # додано


    def start_snake_with_level(self, level_data):
        start_x = level_data.get("start_x_ratio", 0.5) * self.width
        start_y = level_data.get("start_y_ratio", 0.5) * self.height
        self.head_pos = pygame.math.Vector2(int(start_x // CELL_SIZE * CELL_SIZE), int(start_y // CELL_SIZE * CELL_SIZE))
        self.direction_vector = pygame.math.Vector2(CELL_SIZE, 0)
        self.next_direction = self.direction_vector.copy()
        self.snake = [self.head_pos - pygame.math.Vector2(i * CELL_SIZE, 0) for i in range(level_data.get("start_length", 3))]
        self.score = 0
        self.foods = self._generate_multiple_foods(level_data.get("food_count", 5), level_data.get("special_food_chance", 0.1))
        self.obstacles = level_data.get("obstacles", [])

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()

            # --- Пауза ---
            if self.paused:
                if event.type == pygame.KEYDOWN and event.key == getattr(pygame, self.settings["controls"]["pause"], K_ESCAPE):
                    self.toggle_pause()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.next_level_available and self.next_button_rect and self.next_button_rect.collidepoint(mouse_pos):
                        self.play_sound("click")
                        self.game_running = False
                        self._start_next_level_on_exit = True
            else:
                # --- Керування змійкою ---
                if event.type == pygame.KEYDOWN:
                    if event.key == getattr(pygame, self.settings["controls"]["up"], K_UP) and self.direction_vector.y == 0:
                        self.next_direction = pygame.math.Vector2(0, -CELL_SIZE)
                    elif event.key == getattr(pygame, self.settings["controls"]["down"], K_DOWN) and self.direction_vector.y == 0:
                        self.next_direction = pygame.math.Vector2(0, CELL_SIZE)
                    elif event.key == getattr(pygame, self.settings["controls"]["left"], K_LEFT) and self.direction_vector.x == 0:
                        self.next_direction = pygame.math.Vector2(-CELL_SIZE, 0)
                    elif event.key == getattr(pygame, self.settings["controls"]["right"], K_RIGHT) and self.direction_vector.x == 0:
                        self.next_direction = pygame.math.Vector2(CELL_SIZE, 0)
                    elif event.key == getattr(pygame, self.settings["controls"]["pause"], K_ESCAPE):
                        self.toggle_pause()

    
    def update_snake(self):
        # Рух голови
        self.direction_vector = self.next_direction
        self.head_pos = self.head_pos + self.direction_vector

        # Додаємо нову голову
        self.snake.insert(0, self.head_pos.copy())

        # Перевіряємо чи з’їв їжу
        ate_food = None
        for food in self.foods:
            if self.head_pos == pygame.math.Vector2(food["pos"]):
                ate_food = food
                break

        if ate_food:
            self.play_sound("eat")
            self.score += ate_food.get("points", 1)
            self.foods.remove(ate_food)
            self.foods.extend(self._generate_multiple_foods(1))  # додаємо нову їжу
        else:
            # Якщо їжу не з’їв — забираємо хвіст
            self.snake.pop()


    def check_collisions(self):
        # --- Зіткнення зі стінами ---
        if self.head_pos.x < 0 or self.head_pos.y < 0 or self.head_pos.x >= self.width or self.head_pos.y >= self.height:
            self.play_sound("collision")
            self.game_running = False
            return

        # --- Зіткнення з тілом ---
        if self.head_pos in self.snake[1:]:
            self.play_sound("collision")
            self.game_running = False
            return

        # --- Зіткнення з перешкодами (якщо є) ---
        if hasattr(self, "obstacles"):
            for obs in self.obstacles:
                rect = pygame.Rect(obs["x"], obs["y"], obs["w"], obs["h"])
                if rect.collidepoint(self.head_pos.x, self.head_pos.y):
                    self.play_sound("collision")
                    self.game_running = False
                    return

        
    def check_level_completion(self):
        if self.current_level is not None:
            try:
                level_data = self.levels[self.current_level]
                goal_score = level_data.get("goal_score", None)
                if goal_score and self.score >= goal_score:
                    # Відкриваємо наступний рівень
                    unlocked = self.level_progress.get("unlocked_levels", [0])
                    if self.current_level + 1 not in unlocked:
                        unlocked.append(self.current_level + 1)
                        self.level_progress["unlocked_levels"] = unlocked
                        save_json_file(LEVEL_PROGRESS_FILE, self.level_progress)
                        self.new_level_unlocked_message = self.get_text("next_level_unlocked")
                        self.next_level_available = True
            except Exception as e:
                print(f"Помилка у check_level_completion: {e}")


    def draw_game_state(self):
        self.screen.fill(BG_COLOR)

        # Малюємо їжу
        for food in self.foods:
            color = food.get("color", FOOD_COLOR)
            pos = food["pos"]
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, color, rect)

        # Малюємо перешкоди
        if hasattr(self, "obstacles"):
            for obs in self.obstacles:
                rect = pygame.Rect(obs["x"], obs["y"], obs["w"], obs["h"])
                pygame.draw.rect(self.screen, (150, 75, 0), rect)

        # Малюємо змійку
        for segment in self.snake:
            rect = pygame.Rect(segment.x, segment.y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, self.settings["appearance"]["skin_color"], rect)

        # Рахунок
        score_text = self.font.render(f"{self.get_text('score')}: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))

        # Якщо пауза → затемнення
        if self.paused:
            self.draw_pause_overlay()

        # Якщо відкрито новий рівень
        if self.new_level_unlocked_message:
            msg_surface = self.font.render(self.new_level_unlocked_message, True, UNLOCKED_LEVEL_COLOR)
            self.screen.blit(msg_surface, msg_surface.get_rect(center=(self.width // 2, self.height // 2 - 100)))

            # Кнопка "Next Level"
            self.next_button_rect = pygame.Rect(self.width // 2 - 100, self.height // 2, 200, 60)
            pygame.draw.rect(self.screen, BUTTON_COLOR, self.next_button_rect, border_radius=10)
            next_text = self.font.render(self.get_text("next_level_button"), True, TEXT_COLOR)
            self.screen.blit(next_text, next_text.get_rect(center=self.next_button_rect.center))

        pygame.display.flip()


    def _generate_single_food(self, special_chance=0.1):
        # ... (код генерації їжі залишається без змін)
        return pygame.math.Vector2(0,0), "normal", 1

    def _generate_multiple_foods(self, count, special_chance=0.1):
        # ... (код генерації їжі залишається без змін)
        return []

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def draw_pause_overlay(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(PAUSE_OVERLAY_COLOR)
        self.screen.blit(overlay, (0, 0))

        # Текст "Pause"
        pause_text = self.font.render(self.get_text("pause_title"), True, TEXT_COLOR)
        self.screen.blit(pause_text, pause_text.get_rect(center=(self.width // 2, self.height // 2 - 100)))

        # Кнопки
        buttons = [
            (pygame.Rect(self.width // 2 - 120, self.height // 2, 240, 60), "continue"),
            (pygame.Rect(self.width // 2 - 120, self.height // 2 + 80, 240, 60), "menu")
        ]
        mouse_pos = pygame.mouse.get_pos()
        self._draw_buttons(buttons, mouse_pos)


    def show_game_over_screen(self, final_score):
        self.play_music("game_over")
        menu_active = True

        retry_button = pygame.Rect(self.width // 2 - 120, self.height // 2, 240, 60)
        menu_button = pygame.Rect(self.width // 2 - 120, self.height // 2 + 80, 240, 60)

        while menu_active and self.running:
            self.screen.fill(BG_COLOR)

            # Текст "Game Over"
            over_text = self.font.render(self.get_text("game_over"), True, ERROR_TEXT_COLOR)
            self.screen.blit(over_text, over_text.get_rect(center=(self.width // 2, self.height // 2 - 120)))

            # Показати рахунок
            score_text = self.font.render(f"{self.get_text('score')}: {final_score}", True, TEXT_COLOR)
            self.screen.blit(score_text, score_text.get_rect(center=(self.width // 2, self.height // 2 - 60)))

            mouse_pos = pygame.mouse.get_pos()
            self._draw_buttons([(retry_button, "retry"), (menu_button, "menu")], mouse_pos)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    menu_active = False
                    self.show_menu()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry_button.collidepoint(mouse_pos):
                        self.play_sound("click")
                        menu_active = False
                        self.run_game(start_level=self.current_level, training=self.training_mode)
                    elif menu_button.collidepoint(mouse_pos):
                        self.play_sound("click")
                        menu_active = False
                        self.show_menu()

            self.clock.tick(self.settings["graphics"]["fps"])


    def show_critical_error_screen(self, error_message):
        menu_active = True
        while menu_active:
            self.screen.fill(BG_COLOR)

            title = self.font.render(self.get_text("error_title"), True, ERROR_TEXT_COLOR)
            self.screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 2 - 100)))

            msg = self.small_font.render(error_message, True, INFO_TEXT_COLOR)
            self.screen.blit(msg, msg.get_rect(center=(self.width // 2, self.height // 2 - 40)))

            support_text = self.small_font.render(self.get_text("error_support"), True, WARN_TEXT_COLOR)
            self.screen.blit(support_text, support_text.get_rect(center=(self.width // 2, self.height // 2 + 20)))

            site_text = self.small_font.render("afercorporftaon.onepage.me", True, INFO_TEXT_COLOR)
            self.screen.blit(site_text, site_text.get_rect(center=(self.width // 2, self.height // 2 + 60)))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.exit_game()
            self.clock.tick(15)


    def run(self):
        """Головний метод, що запускає гру."""
        if self.running:
            self.show_menu()
        print("Вихід з головного методу run().")

    def exit_game(self):
        """Коректно завершує роботу гри."""
        print("Завершення гри...")
        self.running = False
        self.game_running = False
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        game = SnakeGame()
        if game.running: # Якщо ініціалізація пройшла успішно
            game.run()
    except Exception as e:
        print("Сталася неперехоплена критична помилка.")
        log_exception() # Записуємо помилку в лог
        # Спробуйте показати екран помилки навіть тут, якщо можливо
        try:
            screen = pygame.display.set_mode((800, 600))
            font = pygame.font.Font(None, 36)
            screen.fill((10, 10, 10))
            error_text = font.render("Критична помилка. Див. error_log.txt", True, (255, 0, 0))
            screen.blit(error_text, (50, 50))
            pygame.display.flip()
            pygame.time.wait(5000) # Почекати 5 секунд
        except:
            pass # Якщо навіть pygame не працює, нічого не поробиш
        pygame.quit()
        sys.exit()
