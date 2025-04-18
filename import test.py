import pygame, math, time, os

pygame.mixer.init()
pygame.init()

# 화면 크기 설정
w = 1600
h = int(w * (9 / 16))  # 정수로 변환

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Rhythm Game Test")

clock = pygame.time.Clock()

# 루프 제어 변수
main = True
ingame = True

# 키 상태
keys = [0, 0, 0, 0]      # 애니메이션용 키 값 (0.0 ~ 1.0)
keyset = [0, 0, 0, 0]    # 실제 눌린 키 상태 (0 또는 1)

maxframe = 60  # 최대 FPS
fps = 0

gst = time.time()
Time = time.time() - gst

ty = 0
tst = Time

t1 = []
t2 = []
t3 = []
t4 = []

#font 파일 들고오기
Capth = os.path.dirname(__file__)  # 현재 파일의 절대 경로
Fpath = os.path.join("font")
rate = "READY"

# 인게임으로 부르기
ingame_font_rate = pygame.font.Font(os.path.join(Fpath, "PermanentMarker-Regular.ttf"), int(w / 23)) # 폰트 파일 불러옴 및 크기

music_path = pygame.mixer.music.load(r"C:/Temp/pygame.re/song/audio/PUPA.mp3") # 노래 불러들임 (ogg파일이면 더 좋음)
pygame.mixer.music.set_volume(1) # 사운드 볼륨 크기 (낮으면 낮을수록 소리도 작게들림)
pygame.mixer.music.play() #노래 실행 (play (-1)을 하면 노래 무한 반복)

#랜더링 작업
rate_text = ingame_font_rate.render(str(rate), False, (225, 225, 255))

# 입력 키
def sum_note(n):
    if n == 1: 
       ty = 0
       tst = Time + 2
       t1.append([ty, tst])
    if n == 2:
        ty = 0
        tst = Time + 2
        t2.append([ty, tst])
    if n == 3:
        ty = 0
        tst = Time + 2
        t3.append([ty, tst])
    if n == 4:
        ty = 0
        tst = Time + 2
        t4.append([ty, tst])

speed = 3

notesumt = 0

a = 0
aa = 0

spin = 0

combo = 0
combo_effect = 0
combo_effect2 = 0
miss_anim = 0
last_combo = 0

score = 0

fever_mode = False

max_combo = 80

combo_time = Time + 1

rate_data = [0, 0, 0, 0] 

# 소환 딜레이
note_times = [
    [2.4, 3.2, 4.7, 7.1, 9.0, 9.4, 10.2, 11.58, 12.1, 12.3, 13.0, 14.5, 14.7, 15.0, 16.2],  # 1번 라인
    [2.1, 2.3, 2.7, 3.2, 4.4, 4.6, 4.8, 5.2, 6.8, 7.0, 7.2, 7.4, 7.8, 9.2, 9.5, 9.7, 10.5, 10.7, 10.9, 11.1, 11.3, 11.54, 12.0, 12.3, 13.0, 13.4, 13.9, 14.4, 14.7, 15.4, 15.5, 15.9, 16.1, 16.3],  # 2번 라인
    [2, 2.2, 2.8, 4.3, 4.5, 4.9, 5.1, 5.4, 6.7, 6.9, 7.3, 7.5, 7.8, 9.3, 9.6, 9.8, 10.4, 10.6, 10.8, 11.0, 11.2, 11.4, 11.52, 11.8, 12.5, 13.2, 13.5, 13.7, 14.2, 15.4, 15.5, 15.9, 16.0, 16.4, 16.6],  # 3번 라인
    [3.0, 5.0, 5.4, 7.6, 9.1, 10.2, 11.5, 11.8, 12.8, 13.5, 14.2, 14.6, 15.2, 16.5]   ]# 4번 라인
 
def rating(n):
    global combo, miss_anim, last_combo, combo_effect, combo_effect2, combo_time, rate, score, fever_mode
    # 피버모드드
    if combo >=  max_combo:
        fever_mode = True
    else:
        fever_mode = False
        
    multiplier = 2 if fever_mode else 1
    # 점수 입력 및 판정 방식
    if abs((h/12) * 9 - rate_data[n - 1] < 950 * speed * (h / 900) and (h / 12) * 9 - rate_data[n - 1] >= 200 * speed * (h / 900)):
        last_combo = combo
        miss_anim = 1
        combo = 0
        combo_effect = 0.2
        combo_time = Time + 1 
        combo_effect2 = 1.3
        rate = "WORST"
        score += 0
    if abs((h/12) * 9 - rate_data[n - 1]) < 200 * speed * (h / 900) and abs((h / 12) * 9 - rate_data[n - 1]) >= 100 * speed * (h / 900):
        last_combo = combo
        miss_anim = 1
        combo = 0
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "BAD"
        score += 0
    if abs((h/12) * 9 - rate_data[n - 1]) < 100 * speed * (h / 900) and abs((h / 12) * 9 - rate_data[n - 1]) >= 50 * speed * (h / 900):
        combo += 1
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "GOOD"
        score += 50 * multiplier
    if abs((h/12) * 9 - rate_data[n - 1]) < 50 * speed * (h / 900) and abs((h / 12) * 9 - rate_data[n - 1]) >= 15 * speed * (h / 900):
        combo += 1
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "GREAT"
        score += 70  * multiplier
    if abs((h/12) * 9 - rate_data[n - 1]) < 15 * speed * (h / 900) and abs((h / 12) * 9 - rate_data[n - 1]) >= 0 * speed * (h / 900):
        combo += 1
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "PERFECT"
        score += 100 * multiplier
        
while main:
    while ingame:
         
        if len(t1) > 0:
            rate_data[0] = t1[0][0]
        if len(t2) > 0:
            rate_data[1] = t2[0][0]
        if len(t3) > 0:
            rate_data[2] = t3[0][0]
        if len(t4) > 0:
            rate_data[3] = t4[0][0]
            
        # 소환 타이밍
        Time = time.time() - gst
        for i in range(4):  # i = 0~3 (라인 번호)
           if len(note_times[i]) > 0 and Time > note_times[i][0]:
               sum_note(i + 1)  # sum_note는 1~4라인 번호를 받는 함수니까 i+1
               note_times[i].pop(0)  # 해당 시간 제거
        
        # FPS 계산
        fps = clock.get_fps()
            
        ingame_font_combo = pygame.font.Font(os.path.join(Fpath, "PermanentMarker-Regular.ttf"), int((w / 38) * combo_effect2))
        combo_text = ingame_font_combo.render(str(combo), False, (255, 255, 255,))
        combo_text.set_alpha(128)
        
        rate_text = ingame_font_rate.render(str(rate), False, (225, 225, 255,128))
        rate_text = pygame.transform.scale(rate_text, (int(w / 110 * len(rate) * combo_effect2), int((w / 58 * combo_effect * combo_effect2))))
        
        ingame_font_miss = pygame.font.Font(os.path.join(Fpath, "PermanentMarker-Regular.ttf"), int((w / 38 * miss_anim)))
        miss_text = ingame_font_miss.render(str(last_combo), False, (255, 0, 0))
        
        if fps == 0:
            fps = maxframe

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    keyset[0] = 1
                    if len(t1) > 0:
                        if t1[0][0] > h / 3:
                            rating(1)
                            t1.pop(0)
                if event.key == pygame.K_f:
                    keyset[1] = 1
                    if len(t2) > 0:
                        if t2[0][0] > h / 3:
                            rating(2)
                            t2.pop(0)
                if event.key == pygame.K_j:
                    keyset[2] = 1
                    if len(t3) > 0:
                        if t3[0][0] > h / 3:
                            rating(3)
                            t3.pop(0)
                if event.key == pygame.K_k:
                    keyset[3] = 1
                    if len(t4) > 0:
                        if t4[0][0] > h / 3:
                            rating(4)
                            t4.pop(0)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    keyset[0] = 0
                if event.key == pygame.K_f:
                    keyset[1] = 0
                if event.key == pygame.K_j:
                    keyset[2] = 0
                if event.key == pygame.K_k:
                    keyset[3] = 0

        # 키 애니메이션 값 업데이트
        for i in range(4):
            keys[i] += (keyset[i] - keys[i]) / (2 * (maxframe / fps))

        # 화면 초기화
        screen.fill((0, 0, 0))

        # 가운데 기어 배경
        pygame.draw.rect(screen, (0, 0, 0), (w / 2 - w / 8, -int(w / 100), w / 4, h + int(w / 50)))

        # 키별 애니메이션 막대 (4개)
        for i in range(4):
            for j in range(7):
                brightness = 200 - ((200 / 7) * j)
                color = (brightness, brightness, brightness)
                pygame.draw.rect(
                    screen,
                    color,
                    (
                        w / 2 - w / 8 + (w / 16) * i + w / 32 - (w / 32) * keys[i],
                        (h / 12) * 9 - (h / 30) * keys[i] * j,
                        w / 16 * keys[i],
                        (h / 35) / j if j != 0 else 0  # j가 0일 경우 나눗셈 에러 방지
                    )
                )
         # 텍스쳐의 움직임을 정해주는 코드       
        if Time > combo_time:
            combo_effect += (0 - combo_effect) / (7 * (maxframe / fps))
        if Time < combo_time:
            combo_effect += (1 - combo_effect) / (7 * (maxframe / fps))
            
        combo_effect2 += (2 - combo_effect2) / (7 * (maxframe / fps))
        
        miss_anim += (4 - miss_anim) / (14 * (maxframe / fps))
        
        # 기어 테두리
        pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 8, -int(w / 100), w / 4, h + int(w / 50)), int(w / 100))
        
        for tile_data in t1:
            tile_data[0] = 0 - (h / 12) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900)
            pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 8, tile_data[0] - h / 100, w / 16, h / 50))
            if tile_data[0] > h - (h / 9):
              last_combo = combo
              miss_anim = 1
              combo = 0
              combo_effect = 0.2
              combo_time = Time + 1
              combo_effect2 = 1.3
              rate = "MISS"
              t1.remove(tile_data)
                
        for tile_data in t2:
            tile_data[0] = 0 - (h / 12) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900)
            pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 16, tile_data[0] - h / 100, w / 16, h / 50))
            if tile_data[0] > h - (h / 9):
              last_combo = combo
              miss_anim = 1
              combo = 0
              combo_effect = 0.2
              combo_time = Time + 1
              combo_effect2 = 1.3
              rate = "MISS"
              t2.remove(tile_data)
                
        for tile_data in t3:
            tile_data[0] = 0 - (h / 12) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900)
            pygame.draw.rect(screen, (255, 255, 255), (w / 2, tile_data[0] - h / 100, w / 16, h / 50))
            if tile_data[0] > h - (h / 9):
              last_combo = combo
              miss_anim = 1
              combo = 0
              combo_effect = 0.2
              combo_time = Time + 1
              combo_effect2 = 1.3
              rate = "MISS"
              t3.remove(tile_data)
                
        for tile_data in t4:
            tile_data[0] = 0 - (h / 12) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900)
            pygame.draw.rect(screen, (255, 255, 255), (w / 2 + w / 16, tile_data[0] - h / 100, w / 16, h / 50))
            if tile_data[0] > h - (h / 9):
              last_combo = combo
              miss_anim = 1
              combo = 0
              combo_effect = 0.2
              combo_time = Time + 1
              combo_effect2 = 1.3
              rate = "MISS"
              t4.remove(tile_data)
        
       # 판정 선
        pygame.draw.rect(screen, (0, 0, 0), (w / 2 - w / 8, (h / 12) * 9, w / 4, h / 2))
        pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 8, (h / 12) * 9, w / 4, h / 2), int(h / 100))
    
       # 키 디자인
        pygame.draw.rect(screen, (255 - 100 * keys[0],255 - 100 * keys[0], 255 - 100 * keys[0]), (w / 2 - w / 9, (h / 24) * 19 + (h / 48) * keys[0], w / 27, h / 8), int(h / 150))
        pygame.draw.rect(screen, (255 - 100 * keys[3],255 - 100 * keys[3], 255 - 100 * keys[3]), (w / 2 + w / 13.5, (h / 24) * 19 + (h / 48) * keys[3], w / 27, h / 8), int(h / 150))
       # 스핀 디자인
        pygame.draw.circle(screen, (150, 150, 150), (w / 2, (h / 24) * 21), (w / 20), int(h / 200))
        pygame.draw.line(screen, (150, 150, 150), (w / 2 - math.sin(spin) * 25 * (w / 1600), (h / 24) * 21 - math.cos(spin) * 25 * (w / 1600)), (w / 2 + math.sin(spin) * 25 * (w / 1600), (h / 24) * 21 + math.cos(spin) * 25 * (w / 1600)), int(w / 400))
        spin += (speed / 20 * (maxframe / fps))

       # 키 디자인
        pygame.draw.rect(screen, (255 - 100 * keys[1], 255 - 100 * keys[1], 255 - 100 * keys[1]), (w / 2 - w / 18, (h / 48) * 39 + (h / 48) * keys[1], w / 27, h / 8))
        pygame.draw.rect(screen, (0,0, 0), (w / 2 - w / 18, (h / 48) * 43 + (h / 48) * (keys[1] * 1.2), w / 27, h / 64), int(h / 150))
        pygame.draw.rect(screen, (50,50, 50), (w / 2 - w / 18, (h / 48) * 39 + (h / 48) * keys[1], w / 27, h / 8), int(h / 150))
       # 키 디자인
        pygame.draw.rect(screen, (255 - 100 * keys[2], 255 - 100 * keys[2], 255 - 100 * keys[2]), (w / 2 + w / 58, (h / 48) * 39 + (h / 48) * keys[2], w / 27, h / 8))
        pygame.draw.rect(screen, (0,0, 0), (w / 2 + w / 58, (h / 48) * 43 + (h / 48) * (keys[2] * 1.2), w / 27, h / 64), int(h / 150))
        pygame.draw.rect(screen, (50,50, 50), (w / 2 + w / 58, (h / 48) * 39 + (h / 48) * keys[2], w / 27, h / 8), int(h / 150))
       # 게이지 바 디자인
        gauge_x = w / 2.418 + w / 5 + 20
        gauge_y = (h / 6) * 3        
        gauge_height = (h / 12) * 6   
        gauge_width = 20
        
        pygame.draw.rect(screen, (80, 80, 80), (gauge_x, gauge_y, gauge_width, gauge_height))
        
        filled_height = gauge_height * min(combo / max_combo, 1.0)
        if fever_mode:
            gauge_color = (255, 100, 100)  # 피버 모드일 때 노란색
        else:
            gauge_color = (100, 255, 100)  # 일반 초록색
        pygame.draw.rect(screen, (gauge_color), (gauge_x, gauge_y + gauge_height - filled_height, gauge_width, filled_height))
        pygame.draw.rect(screen, (255, 255, 255), (gauge_x, gauge_y, gauge_width, gauge_height), 2)
        # miss 판정정
        miss_text.set_alpha(255 - (255 / 4) * miss_anim)
        
        #폰트를 화면에 그리기
        screen.blit(combo_text, (w / 2 - combo_text.get_width() / 2, (h / 12) * 4 - combo_text.get_height() / 2))
        screen.blit(rate_text, (w / 2 - rate_text.get_width() / 2, (h / 12) * 8 - rate_text.get_height() / 2))
        screen.blit(miss_text, (w / 2 - miss_text.get_width() / 2, (h / 12) * 4 - miss_text.get_height() / 2))
        
        #점수 폰트 띄우기
        score_font = pygame.font.Font(os.path.join(Fpath, "PermanentMarker-Regular.ttf"), int (w / 35))
        score_text = score_font.render(f"Score: {score}", False, (255, 255, 100))
        screen.blit(score_text, (20,20))
    
        
        # 화면 업데이트
        pygame.display.flip()
        
       
        # FPS 제한
        clock.tick(maxframe)
        