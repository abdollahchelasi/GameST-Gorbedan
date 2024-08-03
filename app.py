import streamlit as st



if st.button("بازی تیم دلفین"):


    import pygame
    import pygame.mixer
    import random

    # تنظیمات اولیه
    WINDOW_WIDTH = 450
    WINDOW_HEIGHT = 500
    FPS = 60

    # رنگ‌ها
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # کلاس پرنده
    class Bird(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.image.load("ball.png")
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.velocity = 0
            self.gravity = 0.5

        def update(self):
            self.velocity += self.gravity
            self.rect.y += self.velocity

            if self.rect.top <= 0:
                self.rect.top = 0
                self.velocity = 0

            if self.rect.bottom >= WINDOW_HEIGHT:
                self.rect.bottom = WINDOW_HEIGHT
                self.velocity = 0

        def flap(self):
            self.velocity = -10

    # کلاس لوله
    class Pipe(pygame.sprite.Sprite):
        pipe_images = ["a0.png", "a1.png", "a2.png", "a3.png", "a4.png", 
                    "a5.png", "a6.png", "a7.png", "a8.png", "a9.png", 
                    "a10.png", "a11.png", "a12.png", "a13.png", "a14.png", 
                    "a15.png", "a16.png", "a17.png", "a18.png", "a19.png", 
                    "a20.png"]

        def __init__(self, x, y, is_top):
            super().__init__()
            self.image = pygame.image.load(random.choice(self.pipe_images))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y if not is_top else y - self.rect.height
            self.is_top = is_top
            self.speed = 2

        def update(self):
            self.rect.x -= self.speed

            if self.rect.right < 0:
                self.kill()

    # تابع راه‌اندازی مجدد بازی
    def restart_game():
        global bird, all_sprites, pipes, score, last_score
        pygame.mixer.music.stop()  # قطع موسیقی در هنگام ریستارت
        bird = Bird(100, WINDOW_HEIGHT // 2)
        all_sprites.empty()
        pipes.empty()
        all_sprites.add(bird)
        score = 0
        last_score = 0  # تنظیم امتیاز آخر به 0

    # تابع اصلی
    def main():
        pygame.init()
        pygame.mixer.init()  # بارگذاری کتابخانه صدا

        # بارگذاری و پخش موسیقی پس‌زمینه
        pygame.mixer.music.load("toop.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # پخش موسیقی به صورت تکراری

        # بارگذاری صداها
        score_sounds = [
            pygame.mixer.Sound("a0.mp3"),
            pygame.mixer.Sound("a1.mp3"),
            pygame.mixer.Sound("a2.mp3"),
            pygame.mixer.Sound("a6.mp3"),
        ]

        crash_sounds = [
            pygame.mixer.Sound("a4.mp3"),
        ]

        for sound in score_sounds:
            sound.set_volume(0.5)  # تنظیم میزان صدا

        for sound in crash_sounds:
            sound.set_volume(0.5)  # تنظیم میزان صدا

        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("دلفین گربدان")
        clock = pygame.time.Clock()

        # تصویر پس‌زمینه
        background = pygame.image.load("bac.jpg").convert()

        # گروه اشیاء شامل پرنده و لوله‌ها
        global all_sprites, pipes, score, last_score
        all_sprites = pygame.sprite.Group()
        pipes = pygame.sprite.Group()

        # ایجاد پرنده
        global bird
        bird = Bird(100, WINDOW_HEIGHT // 2)
        all_sprites.add(bird)

        # فاصله زمانی بین ایجاد لوله‌ها
        pipe_timer = 0
        pipe_interval = 1.5 * FPS

        game_over = False
        game_start = False
        restart_button = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 50, 100, 50)
        play_button = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 - 25, 100, 50)
        font_path = pygame.font.match_font('Arial')
        font = pygame.font.Font(font_path, 36)
        small_font = pygame.font.Font(font_path, 24)

        score = 0
        last_score = 0  # متغیر جدید برای ذخیره امتیاز در زمان باخت

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over and game_start:
                    bird.flap()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and game_over:
                        restart_game()
                        game_over = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos) and game_over:
                        restart_game()
                        game_over = False
                    if play_button.collidepoint(event.pos) and not game_start:
                        restart_game()
                        game_start = True

            if game_start:
                if not game_over:
                    # ایجاد لوله‌های جدید
                    pipe_timer += 1
                    if pipe_timer >= pipe_interval:
                        pipe_timer = 0
                        pipe_height = random.randint(100, WINDOW_HEIGHT - 200)
                        top_pipe = Pipe(WINDOW_WIDTH, pipe_height, True)
                        bottom_pipe = Pipe(WINDOW_WIDTH, pipe_height + 150, False)
                        pipes.add(top_pipe)
                        pipes.add(bottom_pipe)

                    # به‌روزرسانی اشیاء
                    all_sprites.update()
                    pipes.update()

                    # بررسی برخورد
                    if pygame.sprite.spritecollide(bird, pipes, False) or bird.rect.top <= 0 or bird.rect.bottom >= WINDOW_HEIGHT:
                        last_score = score  # ذخیره امتیاز در زمان باخت
                        game_over = True
                        pygame.mixer.music.stop()  # قطع موسیقی در هنگام باخت
                        random_crash_sound = random.choice(crash_sounds)
                        random_crash_sound.play()  # پخش صدای سقوط

                    # بررسی عبور پرنده از لوله‌ها
                    for pipe in pipes:
                        if pipe.rect.right < bird.rect.left and not hasattr(pipe, 'passed'):
                            pipe.passed = True
                            if not pipe.is_top:
                                score += 2
                                random_sound = random.choice(score_sounds)
                                pygame.mixer.stop()  # قطع صدای فعلی
                                random_sound.play()  # پخش صدای تصادفی

                    # نمایش صفحه
                    screen.blit(background, (0, 0))  # نمایش پس‌زمینه
                    all_sprites.draw(screen)
                    pipes.draw(screen)

                    # نمایش امتیاز
                    score_text = font.render(f"Soccer: {score}", True, WHITE)
                    screen.blit(score_text, (10, 10))

                    small_image = pygame.image.load("logo.png")
                    small_image = pygame.transform.scale(small_image, (40, 40))
                    screen.blit(small_image, (370, 10))

                else:
                    # منوی پایان بازی
                    screen.blit(background, (0, 0))  # نمایش پس‌زمینه
                    small_image = pygame.image.load("logo.png")
                    small_image = pygame.transform.scale(small_image, (130, 130))
                    screen.blit(small_image, (160, 40))


                    small_image = pygame.image.load("a0.png")
                    small_image = pygame.transform.scale(small_image, (50, 50))
                    screen.blit(small_image, (200, 430))


                    restart_text = small_font.render("Restart", True, BLACK)
                    pygame.draw.rect(screen, WHITE, restart_button)
                    screen.blit(restart_text, (restart_button.x + (restart_button.width // 2 - restart_text.get_width() // 2),
                                            restart_button.y + (restart_button.height // 2 - restart_text.get_height() // 2)))

                    # نمایش امتیاز آخر
                    score_text = small_font.render(f"Last Score: {last_score}", True, BLACK)
                    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, restart_button.y - 30))

            else:
                # صفحه شروع بازی
                screen.blit(background, (0, 0))  # نمایش پس‌زمینه
                pygame.draw.rect(screen, WHITE, play_button)

                imglogo = pygame.image.load("logo.png")
                imglogo = pygame.transform.scale(imglogo, (140, 140))
                screen.blit(imglogo, (160, 50))

                small_image = pygame.image.load("a0.png")
                small_image = pygame.transform.scale(small_image, (50, 50))
                screen.blit(small_image, (200, 430))

                play_text = small_font.render("Play", True, BLACK)
                screen.blit(play_text, (play_button.x + (play_button.width // 2 - play_text.get_width() // 2),
                                        play_button.y + (play_button.height // 2 - play_text.get_height() // 2)))

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

    if __name__ == "__main__":
        main()
