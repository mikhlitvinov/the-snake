"""Игра «Змейка»."""

from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Соответствие клавиш разрешённым направлениям:
KEY_DIRECTIONS = {
    (pg.K_UP, LEFT): UP,
    (pg.K_UP, RIGHT): UP,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT,
}

# Цвет фона — чёрный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Общий класс для игровых объектов."""

    def __init__(
        self,
        position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        body_color=None,
    ):
        """Задаёт начальное положение и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def _draw_cell(self, position=None, color=None):
        """Рисует одну клетку игрового объекта."""
        if position is None:
            position = self.position
        if color is None:
            color = self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Подготавливает отрисовку игрового объекта."""
        raise NotImplementedError(
            'Метод draw() должен быть реализован в дочернем классе.'
        )


class Apple(GameObject):
    """Описывает яблоко."""

    def __init__(self, occupied_positions=()):
        """Создаёт яблоко в свободной клетке поля."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Перемещает яблоко в случайную свободную клетку."""
        occupied_positions = set(occupied_positions)

        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if position not in occupied_positions:
                self.position = position
                return

    def draw(self):
        """Рисует яблоко на экране."""
        self._draw_cell()


class Snake(GameObject):
    """Описывает змейку."""

    def __init__(self):
        """Задаёт начальные параметры змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self, new_direction):
        """Меняет направление движения змейки."""
        self.direction = new_direction

    def move(self):
        """Перемещает змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_head = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)
        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length
            else None
        )

    def draw(self):
        """Рисует голову змейки и стирает прежний хвост."""
        if self.last:
            self._draw_cell(self.last, BOARD_BACKGROUND_COLOR)

        self._draw_cell(self.get_head_position())

    def get_head_position(self):
        """Возвращает положение головы змейки."""
        return self.positions[0]

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.length = 1
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
        )
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

        if event.type == pg.KEYDOWN:
            new_direction = KEY_DIRECTIONS.get(
                (event.key, game_object.direction),
                game_object.direction,
            )
            game_object.update_direction(new_direction)


def main():
    """Запускает игру."""
    pg.init()
    screen.fill(BOARD_BACKGROUND_COLOR)

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        head_position = snake.get_head_position()

        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if head_position in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
