import pygame
import random
import sys

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Константы
WIDTH, HEIGHT = 800, 600
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
VACUUM_SIZE = (100, 100)  # Размер пылесоса
TRASH_SIZE = (60, 60)     # Размер мусора

# Виды мусора
TRASH_TYPES = ["бумажка", "семечка", "волосы"]
trash_counts = {trash: 0 for trash in TRASH_TYPES}

# Функция для загрузки изображений и изменения их размера
def load_images():
    vacuum_image = pygame.image.load('vacuum.png').convert_alpha()
    vacuum_image = pygame.transform.scale(vacuum_image, VACUUM_SIZE)

    trash_images = {
        "бумажка": pygame.transform.scale(pygame.image.load('paper.png').convert_alpha(), TRASH_SIZE),
        "семечка": pygame.transform.scale(pygame.image.load('seeds.png').convert_alpha(), TRASH_SIZE),
        "волосы": pygame.transform.scale(pygame.image.load('hair.png').convert_alpha(), TRASH_SIZE)
    }
    return vacuum_image, trash_images

# Класс для мусора
class Trash:
    def __init__(self, x, y, trash_type, image):  # Исправлено на __init__
        self.x = x
        self.y = y
        self.trash_type = trash_type
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

# Функция для генерации мусора
def generate_trash(trash_images):
    trash_type = random.choice(TRASH_TYPES)
    x = random.randint(0, WIDTH - TRASH_SIZE[0])
    y = random.randint(0, HEIGHT - TRASH_SIZE[1])
    return Trash(x, y, trash_type, trash_images[trash_type])

# Устанавливаем размеры окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Меню")

# Шрифт для текста
font = pygame.font.Font(None, 40)

# Функция для отрисовки кнопок
def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Функция для главного меню
def main_menu():
    while True:
        screen.fill(WHITE)

        # Отрисовываем кнопки
        draw_button("Старт", 300, 200, 200, 100, (0, 255, 0))
        draw_button("Завершить", 300, 350, 200, 100, (255, 0, 0))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 300 <= mouse_x <= 500 and 200 <= mouse_y <= 300:  # Проверка нажатия на "Старт"
                    main()  # Переход к игровому циклу
                if 300 <= mouse_x <= 500 and 350 <= mouse_y <= 450:  # Проверка нажатия на "Завершить"
                    pygame.quit()
                    sys.exit()

        # Обновление экрана
        pygame.display.flip()

# Функция для отображения результата
def show_results(screen):
    font = pygame.font.Font(None, 36)
    y_offset = 50
    for trash_type, count in trash_counts.items():
        text = font.render(f"{trash_type}: {count}", True, BLACK)
        screen.blit(text, (10, y_offset))
        y_offset += 30

# Основная функция игры
def main():
    clock = pygame.time.Clock()

    vacuum_image, trash_images = load_images()
    trash_list = []

    for _ in range(10):  # Генерируем 10 объектов мусора
        trash_list.append(generate_trash(trash_images))

    vacuum_rect = vacuum_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and vacuum_rect.left > 0:
            vacuum_rect.x -= 5
        if keys[pygame.K_RIGHT] and vacuum_rect.right < WIDTH:
            vacuum_rect.x += 5
        if keys[pygame.K_UP] and vacuum_rect.top > 0:
            vacuum_rect.y -= 5
        if keys[pygame.K_DOWN] and vacuum_rect.bottom < HEIGHT:
            vacuum_rect.y += 5

        # Проверяем столкновение с мусором
        for trash in trash_list[:]:
            if vacuum_rect.colliderect(trash.rect):
                trash_counts[trash.trash_type] += 1  # Увеличиваем счётчик соответствующего мусора
                trash_list.remove(trash)  # Убираем мусор, который собрали

        # Обновление экрана
        screen.fill(GRAY)
        for trash in trash_list:
            trash.draw(screen)
        screen.blit(vacuum_image, vacuum_rect.topleft)

        # Если мусор собран, показываем результаты
        if not trash_list:
            show_results(screen)
            pygame.display.flip()
            pygame.time.wait(5000)  # Ждем 5 секунды, чтобы игрок увидел результаты
            trash_counts.clear()  # Сбрасываем подсчет
            main_menu()  # Возвращаемся в главное меню

        pygame.display.flip()
        clock.tick(FPS)

# Запуск главного меню
if __name__ == "__main__":
    main_menu()