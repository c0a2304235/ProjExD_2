import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書 (押下キー：移動量タプル)
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, 5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    '''
    こうかとんRect，または，爆弾Rectの画面内外判定用の関数
    引数：こうかとんRect，または，爆弾Rect
    戻り値：横方向判定結果，縦方向判定結果 (True: 画面内/False：画面内)
    '''
    yoko, tate = True, True
    if obj_rct.left <= 0 or WIDTH <= obj_rct.right:
        yoko = False
    if obj_rct.top <= 0 or HEIGHT <= obj_rct.bottom:
        tate = False
    return yoko, tate


def bomb_control(t):
    '''
    爆弾の加速度，拡大率選択用の関数
    引数：tmr
    戻り値：加速度，拡大率の順のタプル
    '''
    accs = [a for a in range(1, 11)]
    bomb_big = [b*20 for b in range(1, 11)]
    u = t // 100
    return (accs[u], bomb_big[u])


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    tmr = 0
    rate = bomb_control(tmr)  # bomb_controlの値を受け取る変数
    # こうかとんの設定
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    # 爆弾の設定
    bomb_img = pg.Surface((20, 20))
    pg.draw.circle(bomb_img, (255, 0, 0), (10, 10), rate[1])
    bomb_img.set_colorkey((0, 0, 0))
    bomb_rct = bomb_img.get_rect()
    bomb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx = 5 * rate[0]
    vy = 5 * rate[0]


    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bomb_rct):
            print("Game Over")
            return
        screen.blit(bg_img, [0, 0]) 

        # こうかとんの描画
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        # 爆弾の描画
        bomb_rct.move_ip(vx, vy)
        screen.blit(bomb_img, bomb_rct)
        yoko, tate = check_bound(bomb_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1
        pg.display.update()
        tmr += 1
        
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
