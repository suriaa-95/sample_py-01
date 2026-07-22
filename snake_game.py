import sys
import random
import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# Colors (RGB)
COLOR_BG = (20, 20, 25)
COLOR_SNAKE_HEAD = (46, 204, 113)
COLOR_SNAKE_BODY = (39, 174, 96)
COLOR_FOOD = (231, 76, 60)
COLOR_TEXT = (236, 240, 241)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur_x, cur_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (cur_x + dir_x, cur_y + dir_y)

        # Self-collision check
        if new_head in self.positions[1:]:
            return False

        # Wall-collision check
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            return False

        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

        return True

    def draw(self, surface):
        for index, pos in enumerate(self.positions):
            rect = pygame.Rect(
                pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1
            )
            color = COLOR_SNAKE_HEAD if index == 0 else COLOR_SNAKE_BODY
            pygame.draw.rect(surface, color, rect)


class Food:
    def __init__(self):
        self.position = (0, 0)

    def randomize_position(self, snake_positions):
        while True:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            if pos not in snake_positions:
                self.position = pos
                break

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE - 1,
            GRID_SIZE - 1,
        )
        pygame.draw.rect(surface, COLOR_FOOD, rect)


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Helvetica", 24)

    snake = Snake()
    food = Food()
    food.randomize_position(snake.positions)

    score = 0
    game_over = False

    while True:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_SPACE:
                    snake.reset()
                    food.randomize_position(snake.positions)
                    score = 0
                    game_over = False
                elif not game_over:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

        # Logic Update
        if not game_over:
            if not snake.update():
                game_over = True
            else:
                # Eating Food
                if snake.get_head_position() == food.position:
                    snake.grow = True
                    score += 10
                    food.randomize_position(snake.positions)

        # Drawing
        screen.fill(COLOR_BG)
        snake.draw(screen)
        food.draw(screen)

        # UI Rendering
        score_surface = font.render(f"Score: {score}", True, COLOR_TEXT)
        screen.blit(score_surface, (10, 10))

        if game_over:
            over_surface = font.render(
                "Game Over! Press SPACE to Restart", True, COLOR_TEXT
            )
            rect = over_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            screen.blit(over_surface, rect)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()