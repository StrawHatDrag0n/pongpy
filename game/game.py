import pygame
from game.paddle import Paddle
from game.ball import Ball
from game.constants import WIDTH, HEIGHT, FPS, BLACK, WHITE

class GameState:
    def __init__(self) -> None:
        self.left_score = 0
        self.left_hits = 0
        self.right_score = 0
        self.right_hits = 0

    def __str__(self) -> str:
        return f"Left Score: {self.left_score}, Left Hits: {self.left_hits}, Right Score: {self.right_score}, Right Hits: {self.right_hits}"

class Game:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.game_state = GameState()

        self.left_paddle = Paddle(10, HEIGHT//2 - 50, 10, 100)
        self.right_paddle = Paddle(WIDTH - 10 - 10, HEIGHT//2 - 50, 10, 100)
        self.ball = Ball(self.width // 2, self.height // 2, 10)
        self.score_font = pygame.font.SysFont("comicsans", 50)
        self.sprites = [self.left_paddle, self.right_paddle, self.ball]

    def draw(self):
        self.window.fill(BLACK)
        left_score_text = self.score_font.render(str(self.game_state.left_score), 1, WHITE)
        right_score_text = self.score_font.render(str(self.game_state.right_score), 1, WHITE)
        total_hits_text = self.score_font.render(str(self.game_state.left_hits + self.game_state.right_hits), 1, WHITE)

        self.window.blit(left_score_text, (self.width // 4 - left_score_text.get_width() // 2 - 50, 20))
        self.window.blit(right_score_text, (self.width * (3/4) - right_score_text.get_height() // 2 + 50, 20))
        self.window.blit(total_hits_text, (self.width / 2 - total_hits_text.get_height() // 2 + 50, 20))
        
        for sprite in self.sprites:
            sprite.draw(self.window)

    def _handle_collisions(self):
        ball, left_paddle, right_paddle = self.ball, self.left_paddle, self.right_paddle

        if ball.y + ball.radius >= self.height or ball.y - ball.radius <= 0:
            ball.y_velocity *= -1

        if ball.x_velocity > 0:
            paddle = right_paddle
            ball_x_boundary = ball.x + ball.radius
            paddle_x_boundary = paddle.x
        else:
            paddle = left_paddle
            ball_x_boundary = -1 * (ball.x - ball.radius)
            paddle_x_boundary = -1 * (paddle.x + paddle.width)

        if ball.y >= paddle.y and ball.y <= paddle.y + paddle.height and ball_x_boundary >= paddle_x_boundary:
            ball.x_velocity *= -1
            middle_y = paddle.y + paddle.height / 2
            difference_in_y = middle_y - ball.y
            reduction_factor = (paddle.height / 2) / ball.VELOCITY
            y_vel = difference_in_y / reduction_factor
            ball.y_velocity = -1 * y_vel
            if paddle is left_paddle:
                self.game_state.left_hits += 1
            else:   
                self.game_state.right_hits += 1

    def loop(self) -> GameState:
        self.ball.move()
        self._handle_collisions()
        if self.ball.x < 0:
            self.game_state.right_score += 1
            self.ball.reset()
        elif self.ball.x > WIDTH:
            self.game_state.left_score += 1
            self.ball.reset()
        return self.game_state

    def move_paddles(self, keys):
        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        if keys[pygame.K_s]:
            self.left_paddle.move_down()
        if keys[pygame.K_UP]:
            self.right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            self.right_paddle.move_down()

    @staticmethod
    def run(width=WIDTH,  height=HEIGHT, fps=FPS):
        pygame.init()
        pygame.display.set_caption("Pong")
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()

        game = Game(window, width, height)

        run_game = True
        while run_game: 
            clock.tick(fps) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_game = False
                    pygame.quit()
                    break
            keys = pygame.key.get_pressed()
            game.move_paddles(keys)
            game.loop()
            game.draw()
            pygame.display.update()

if __name__ == '__main__':
    Game.run()