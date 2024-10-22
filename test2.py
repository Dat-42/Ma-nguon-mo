import pygame, sys
from pygame.locals import *
import random

# Khởi tạo các thông số cho game
chieu_dai = 800  # Chiều dài cửa sổ
chieu_rong = 500  # Chiều cao cửa sổ
pygame.init()  # Khởi tạo game
w = pygame.display.set_mode((chieu_dai, chieu_rong))  # Tạo cửa sổ game
pygame.display.set_caption('Game Đá Cản - Điều khiển chim né đá')

# Tạo nền của game là 1 ảnh
anh_nen = pygame.image.load('bg2.jpg')
anh_nen = pygame.transform.scale(anh_nen, (chieu_dai, chieu_rong))

# Tạo ảnh con chim
chim = pygame.image.load('chim1.png')
chim = pygame.transform.scale(chim, (80, 70))

# Tạo ảnh tảng đá và thu nhỏ
da = pygame.image.load('nui.png')
da = pygame.transform.scale(da, (200, 200))  # Giảm kích thước đá

# Khởi tạo khung thời gian và font
FPS = 60
fpsClock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 36)

# Hàm khởi tạo lại game
def reset_game():
    global x_chim, y_chim, x_nen1, x_nen2, x_da, y_da, nen_speed, da_speed, score, game_over,x_da1,y_da1
    x_chim = 100  # Vị trí ban đầu của chim
    y_chim = chieu_rong // 2  # Chim bắt đầu ở giữa
    x_nen1 = 0  # Vị trí của nền đầu tiên
    x_nen2 = chieu_dai  # Vị trí của nền thứ hai (liên tiếp)
    x_da = chieu_dai  # Vị trí ban đầu của đá
    y_da = random.randint(100, chieu_rong - 100)  # Đá xuất hiện ngẫu nhiên theo trục y
    x_da1 = chieu_dai  # Vị trí ban đầu của đá
    y_da1 = random.randint(20, chieu_rong - 100)
    nen_speed = 5  # Tốc độ di chuyển của nền
    da_speed = 5  # Tốc độ di chuyển của đá (cùng với nền)
    score = 0
    game_over = False

# Gọi hàm reset game lúc bắt đầu
reset_game()

def draw_button(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Kiểm tra nếu chuột di chuyển qua nút
    button_color = (0, 200, 0) if x + width > mouse[0] > x and y + height > mouse[1] > y else (0, 150, 0)
    pygame.draw.rect(w, button_color, (x, y, width, height))

    # Tạo text trên nút
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
    w.blit(text_surface, text_rect)

    # Kiểm tra click chuột để kích hoạt hành động
    if click[0] == 1 and action is not None:
        action()

while True:  # Tạo vòng lặp game
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if not game_over:  # Chỉ điều khiển chim khi game chưa kết thúc
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    y_chim = max(0, y_chim - 30)  # Điều khiển chim lên
                if event.key == K_DOWN:
                    y_chim = min(chieu_rong - 70, y_chim + 30)  # Điều khiển chim xuống
                if event.key == K_LEFT:
                    x_chim = max(0, x_chim - 30)  # Điều khiển chim sang trái
                if event.key == K_RIGHT:
                    x_chim = min(chieu_dai - 80, x_chim + 30)  # Điều khiển chim sang phải

    if not game_over:
        # Vẽ ảnh nền
        w.blit(anh_nen, (x_nen1, 0))
        w.blit(anh_nen, (x_nen2, 0))

        # Di chuyển nền sang trái để tạo cảm giác di chuyển
        x_nen1 -= nen_speed
        x_nen2 -= nen_speed

        # Khi nền ra khỏi màn hình, đặt lại vị trí
        if x_nen1 <= -chieu_dai:
            x_nen1 = chieu_dai
        if x_nen2 <= -chieu_dai:
            x_nen2 = chieu_dai

        # Vẽ chim
        w.blit(chim, (x_chim, y_chim))

        # Vẽ đá
        w.blit(da, (x_da, y_da))
        w.blit(da, (x_da1, y_da1))

        # Di chuyển đá từ phải sang trái cùng với nền
        x_da -= da_speed
        x_da1-=da_speed

        # Khi đá đi hết màn hình, tạo đá mới và tăng điểm
        if x_da < -100:
            x_da = chieu_dai
            y_da = random.randint(50, chieu_rong - 100)

            score += 1  # Cộng điểm khi né được đá

            x_da1 = chieu_dai
            y_da1 = random.randint(100, chieu_rong - 20)
        # Tạo khung va chạm cho chim và đá
        chim_rect = pygame.Rect(x_chim, y_chim, 80, 70)
        da_rect = pygame.Rect(x_da, y_da, 100, 100)

        # Kiểm tra va chạm giữa chim và đá
        if chim_rect.colliderect(da_rect):
            print("Chim đã va vào đá!")
            game_over = True

        # Hiển thị điểm số
        score_text = font.render(f'Score: {score}', True, (255, 0, 0))
        w.blit(score_text, (10, 10))

    else:
        # Hiển thị thông báo thua cuộc khi game over
        game_over_text = font.render('Game Over! Ban da thua.', True, (255, 0, 0))
        w.blit(game_over_text, (chieu_dai // 2 - 150, chieu_rong // 2 - 50))

        # Vẽ nút chơi lại
        draw_button('choi lai', chieu_dai // 2 - 100, chieu_rong // 2 + 50, 200, 50, reset_game)

    pygame.display.update()
    fpsClock.tick(FPS)
