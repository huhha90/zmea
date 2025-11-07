# -*- coding: utf-8 -*-
import pygame
import sys
import webbrowser
import os # Потрібно для resource_path, хоча тут він не використовується для ресурсів

# --- Константи ---
# Розміри вікна
WIDTH = 800
HEIGHT = 600

# Кольори
BG_COLOR = (30, 0, 0) # Темно-червоний фон
ERROR_TEXT_COLOR = (255, 0, 0)
INFO_TEXT_COLOR = (200, 200, 200)
LINK_COLOR = (100, 100, 255) # Колір для посилання

# Тексти (замість get_text)
ERROR_TITLE = "ПОМИЛКА"
ERROR_RESTART = "Будь ласка, перезапустіть."
ERROR_SUPPORT = "Якщо помилка повторюється — зверніться в підтримку."
ERROR_SITE = "Сайт:"
SUPPORT_SITE_URL = "afercorporftaon.onepage.me" # URL без https://

# --- Функція для відображення екрану помилки ---
def show_error_screen(screen, font, clock, error_message="Сталася невідома помилка"):
    """
    Відображає екран помилки і чекає на закриття вікна або клік по посиланню.
    """
    link_rect = None # Прямокутник для кліку по посиланню
    waiting = True

    while waiting:
        screen.fill(BG_COLOR)

        # Формуємо рядки для виводу
        error_texts = [
            ERROR_TITLE,
            str(error_message), # Виводимо передане повідомлення
            "", # Порожній рядок для відступу
            ERROR_RESTART,
            ERROR_SUPPORT,
            f"{ERROR_SITE} {SUPPORT_SITE_URL}"
        ]

        # Розраховуємо початкову позицію Y для центрування тексту
        total_text_height = len(error_texts) * 45 # Приблизна висота рядка
        start_y = HEIGHT // 2 - total_text_height // 2

        # Малюємо текст і визначаємо клікабельну область посилання
        for i, line in enumerate(error_texts):
            color = ERROR_TEXT_COLOR if i == 0 else INFO_TEXT_COLOR
            # Обробка довгих рядків (простий варіант без переносу слів)
            max_width = WIDTH * 0.9
            rendered_line = line
            line_surface = font.render(rendered_line, True, color)
            # Якщо текст занадто довгий, обрізаємо його
            while line_surface.get_width() > max_width and len(rendered_line) > 3:
                 rendered_line = rendered_line[:-4] + "..." # Обрізаємо з трьома крапками
                 line_surface = font.render(rendered_line, True, color)

            rect = line_surface.get_rect(center=(WIDTH // 2, start_y + i * 45))
            screen.blit(line_surface, rect)

            # Якщо це рядок з посиланням, зберігаємо його прямокутник
            if ERROR_SITE in line:
                link_rect = rect
                # Підкреслюємо посилання
                pygame.draw.line(screen, LINK_COLOR, rect.bottomleft, rect.bottomright, 1)

        pygame.display.flip()

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False # Виходимо з циклу очікування
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Вихід по Esc
                    waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Ліва кнопка миші
                    # Перевіряємо клік по посиланню
                    if link_rect and link_rect.collidepoint(event.pos):
                        try:
                            print(f"Спроба відкрити: https://{SUPPORT_SITE_URL}")
                            webbrowser.open(f"https://{SUPPORT_SITE_URL}")
                        except Exception as wb_err:
                            print(f"Не вдалося відкрити посилання: {wb_err}")

        clock.tick(15) # Обмежуємо частоту кадрів

# --- Головна частина скрипта ---
def main():
    # Ініціалізація Pygame
    pygame.init()
    pygame.font.init()

    # Створення вікна
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Екран Помилки - Тест")
    except pygame.error as e:
        print(f"Не вдалося створити вікно Pygame: {e}")
        sys.exit(1)

    # Завантаження шрифту
    try:
        font = pygame.font.Font(None, 40) # Використовуємо типовий шрифт
    except Exception as e:
        print(f"Не вдалося завантажити шрифт: {e}")
        try:
             font = pygame.font.Font(pygame.font.get_default_font(), 36) # Спробувати інший типовий
        except:
             print("Критична помилка: Немає доступних шрифтів.")
             pygame.quit()
             sys.exit(1)


    clock = pygame.time.Clock()

    # Приклад повідомлення про помилку
    sample_error = "Не вдалося завантажити файл 'assets/music/menu_music.mp3'"

    # Показ екрану помилки
    show_error_screen(screen, font, clock, sample_error)

    # Завершення роботи
    pygame.quit()
    sys.exit(0)

if __name__ == '__main__':
    main()
