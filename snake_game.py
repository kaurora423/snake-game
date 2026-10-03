import pygame
import random
import sys

# 初始化
pygame.init()

# 游戏参数
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 180, 0)

# 窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇")
clock = pygame.time.Clock()

# 字体
font = pygame.font.SysFont("arial", 30)
small_font = pygame.font.SysFont("arial", 20)

# 方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

def draw_snake(snake):
    for segment in snake:
        x, y = segment
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, GREEN, rect)
        pygame.draw.rect(screen, DARK_GREEN, rect, 2)

def draw_food(food):
    x, y = food
    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, RED, rect)

def draw_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def generate_food(snake):
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake:
            return (x, y)

def reset_game():
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2), (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2), (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
    direction = RIGHT
    food = generate_food(snake)
    score = 0
    return snake, direction, food, score

def game_over_screen(score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = small_font.render("Press R to restart or Q to quit", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(10)

def main():
    snake, direction, food, score = reset_game()
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT

                if game_over and event.key == pygame.K_r:
                    snake, direction, food, score = reset_game()
                    game_over = False

        if not game_over:
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # 边界碰撞
            if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
                game_over = True

            # 自身碰撞
            elif new_head in snake:
                game_over = True

            else:
                snake.insert(0, new_head)

                if new_head == food:
                    score += 1
                    food = generate_food(snake)
                else:
                    snake.pop()

        screen.fill(BLACK)
        draw_grid()
        draw_food(food)
        draw_snake(snake)
        draw_score(score)

        if game_over:
            game_over_screen(score)
            snake, direction, food, score = reset_game()
            game_over = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
