import pygame
import sys
import random
import os

# 初始化pygame所有版块
pygame.init()
#初始化pygame的混音器
pygame.mixer.init()

# 屏幕设置
WIDTH, HEIGHT = 600, 400   #游戏窗口的长和宽
BLOCK = 20                  #组成蛇和食物的方块大小
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #指定游戏窗口大小
pygame.display.set_caption("贪吃蛇大作战")

# 字体设置（游戏中所出现的文字）黑体
font = pygame.font.SysFont("simhei", 30)

# 定义游戏中常用颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 背景图加载，让背景图和游戏窗口大小一致
start_bg = pygame.image.load("start_bg.jpg")
start_bg = pygame.transform.scale(start_bg, (WIDTH, HEIGHT))

menu_bg = pygame.image.load("menu_bg.jpg")
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

game_bg = pygame.image.load("game_bg.jpg")
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))

end_bg = pygame.image.load("end_bg.jpg")
end_bg = pygame.transform.scale(end_bg, (WIDTH, HEIGHT))

# 蛇头皮肤加载以及蛇尾的绘制（采用与蛇头颜色相近的颜色填充作为蛇尾）
skin_files = ["skin_orig.jpg", "skin_dog.jpg", "skin_rabbit.jpg", "skin_green.jpg", "skin_lion.jpg","skin_penguin.jpg"]
snake_heads = [pygame.image.load(f).convert_alpha() for f in skin_files]
snake_tail_colors = [(0, 255, 0), (139, 69, 19), (255, 182, 193), (0, 255, 128), (255, 165, 0),(135,206,250)]
skin_index = 0  # 当前选择皮肤的索引，初始为0

# 游戏背景音效和贪吃蛇死亡音效
if os.path.exists("bgm.mp3"):
    pygame.mixer.music.load("bgm.mp3")
    pygame.mixer.music.play(-1)
die_sound = pygame.mixer.Sound("die.mp3") if os.path.exists("die.mp3") else None

#创建一个时钟对象，用于控制游戏的帧率
clock = pygame.time.Clock()

# 显示各个界面文字（内容，位置，颜色）
def message(msg, x, y, color=BLACK):
    text = font.render(msg, True, color) #将文字内容渲染为 pygame 的 Surface 对象
    screen.blit(text, (x, y))  #将渲染好的文字 Surface 对象绘制到游戏窗口上

# 画蛇（snake_list是存储蛇身体每个方块位置的列表）
def draw_snake(snake_list):
    for i, segment in enumerate(snake_list):
        if i == len(snake_list) - 1:
            screen.blit(pygame.transform.scale(snake_heads[skin_index], (BLOCK, BLOCK)), segment)
        else:
            pygame.draw.rect(screen, snake_tail_colors[skin_index], (*segment, BLOCK, BLOCK))

# 随机生成食物（位置随机，数量固定）
food_list = []
def generate_food(n=10):
    global food_list    #对全局变量进行赋值操作，使用 global 关键字来声明
    food_list = [[random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK)] for _ in range(n)]

#加载最高分
def load_high():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            return int(f.read())
    return 0

#保存最高分
def save_high(score):
    if score > load_high():
        with open("highscore.txt", "w") as f:
            f.write(str(score))

#开始界面函数
def show_start():
    while True:
        screen.blit(start_bg, (0, 0))
        message("点击任意键进入菜单", WIDTH//2 - 120, HEIGHT//2 + 130)
        pygame.display.update()    #不断更新游戏窗口提示
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       #如果用户点击关闭窗口按钮，则退出游戏
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:   #按任意键则返回
                return

#显示菜单页面
def show_menu():
    while True:
        screen.blit(menu_bg, (0, 0))
        message("[L] 无尽模式", WIDTH//2 - 100, HEIGHT//2 - 60)
        message("[T] 限时模式（5分钟）", WIDTH//2 - 100, HEIGHT//2 - 20)
        message("[S] 选择皮肤", WIDTH//2 - 100, HEIGHT//2 + 20)
        message("[Q] 退出游戏", WIDTH//2 - 100, HEIGHT//2 + 60)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    return "endless"
                elif event.key == pygame.K_t:
                    return "timed"
                elif event.key == pygame.K_q:
                    pygame.quit(); sys.exit()
                elif event.key == pygame.K_s:   #选择皮肤
                    show_skin_select()

#皮肤选择界面
def show_skin_select():
    global skin_index
    selecting = True
    while selecting:
        screen.fill((200, 200, 200))        #皮肤选择界面的背景填充（灰色）
        message("选择蛇头皮肤：", WIDTH//2 - 100, 30)
        for i, head in enumerate(snake_heads):
            #将每个蛇头皮肤图像缩放为 40x40 像素
            screen.blit(pygame.transform.scale(head, (40, 40)), (100 + i*90, 100))
            #在每个皮肤图像周围绘制一个黑色边框。如果当前索引 i 不等于 skin_index，边框宽度为 2 像素；如果相等，边框宽度为 4 像素，用于突出显示当前选择的皮肤
            pygame.draw.rect(screen, BLACK, (100 + i*90, 100, 40, 40), 2 if i != skin_index else 4)
        message("按数字1~6选择皮肤，ESC返回菜单", 100, 200)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,pygame.K_6]:
                    skin_index = event.key - pygame.K_1
                #按ESC退出皮肤选择界面的循环，返回菜单
                elif event.key == pygame.K_ESCAPE:
                    selecting = False

#游戏结束界面
def show_end(score):
    while True:
        screen.blit(end_bg, (0, 0))
        message(f"本局得分：{score}", WIDTH//2 - 100, HEIGHT//2 - 40)
        message(f"历史最高分：{load_high()}", WIDTH//2 - 100, HEIGHT//2)
        message("按任意键再来一局", WIDTH//2 - 100, HEIGHT//2 + 40)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

#游戏主循环
def game(mode):
    #初始化蛇的位置、移动方向、长度、得分、速度等参数
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = BLOCK, 0
    snake = [[x, y]]
    length = 3
    score = 0
    speed = 5
    paused = False
    start_ticks = pygame.time.get_ticks()
    generate_food(10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high(score)
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                #方向键控制蛇的移动
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -BLOCK, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = BLOCK, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -BLOCK
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, BLOCK
                elif event.key == pygame.K_p:        #按P键则暂停，再按P键则继续游戏
                    paused = not paused

        if paused:
            message("暂停中，按P继续", WIDTH//2 - 100, HEIGHT//2)
            pygame.display.update()
            continue
        #更新蛇的位置
        x += dx
        y += dy
        #判断蛇是否撞墙或撞到自己（屏幕的左边界，右边界，上边界，下边界，自己身体）
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or [x, y] in snake:
            if die_sound:       #如果是则播放死亡音效，保存最高分，显示游戏结束界面并返回
                die_sound.play()
            pygame.time.delay(3000) #让游戏暂停3000ms,让玩家看到自己死亡瞬间
            save_high(score)
            show_end(score)
            return
        #更新贪吃蛇的位置和长度
        snake.append([x, y])
        if len(snake) > length:
            del snake[0]
        #判断蛇是否吃到食物，吃到则移除，生成新的食物
        for f in food_list:
            if [x, y] == f:
                food_list.remove(f)
                food_list.append([random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK)])
                length += 1     #增加蛇的长度
                score += 1      #增加玩家得分
                speed = min(15, 5 + score // 5)         #适当提高蛇的速度（每增加5分，速度增1，速度上限为15）
        #绘制游戏的背景、蛇和食物
        screen.blit(game_bg, (0, 0))
        draw_snake(snake)
        for f in food_list:
            pygame.draw.circle(screen, RED, (f[0]+BLOCK//2, f[1]+BLOCK//2), BLOCK//2 - 2)

        message(f"得分：{score}", 10, 10)
        message(f"最高：{load_high()}", 10, 40)
        #选择限时模式，则进行倒计时
        if mode == "timed":
            seconds = 300 - (pygame.time.get_ticks() - start_ticks) // 1000
            message(f"限时：{seconds}s", WIDTH - 150, 10)
            #游戏结束，保存最高分，显示游戏结束界面
            if seconds <= 0:
                save_high(score)
                show_end(score)
                return
        #更新显示界面和控制帧率
        pygame.display.update()
        clock.tick(speed)

# 启动游戏
while True:
    show_start()
    mode = show_menu()
    game(mode)