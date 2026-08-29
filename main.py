from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import pickle
import pygame
import math
import os
import mysql.connector as db

pygame.init()

# Detect monitor resolution for Full Screen mode
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

Text_box_complete = False
details = {}
user_records = []
user_names = []
user_ids = []

# --- DATABASE & STORAGE HELPERS ---

def init_db():
    try:
        mycon = db.connect(host='localhost', user='root', password='987654321')
        c = mycon.cursor()
        try:
            c.execute('use mechflight;')
            c.execute('select * from scores;')
        except Exception:
            c.execute('drop database if exists mechflight;')
            c.execute('create database mechflight;')
            c.execute('use mechflight;')
            c.execute('create table scores(id varchar(7), name varchar(20), highscore int);')
            mycon.commit()
        mycon.close()
    except Exception as e:
        print("Database Connection Warning (running in standalone mode if DB offline):", e)

def save_score_to_db(user_id, score):
    if not user_id:
        return
    try:
        mycon = db.connect(host='localhost', user='root', password='987654321', database='mechflight')
        c = mycon.cursor()
        c.execute('select highscore from scores where id=%s;', (user_id,))
        res = c.fetchone()
        if res is None:
            c.execute('insert into scores values (%s, %s, %s);', (user_id, details.get('NAME', 'Player'), score))
        else:
            c.execute('update scores set highscore=%s where id=%s and highscore < %s;', (score, user_id, score))
        mycon.commit()
        mycon.close()
    except Exception as e:
        print("DB update error:", e)

def fetch_highscore_db(user_id):
    if not user_id:
        return 0
    try:
        mycon = db.connect(host='localhost', user='root', password='987654321', database='mechflight')
        c = mycon.cursor()
        c.execute('select highscore from scores where id=%s;', (user_id,))
        res = c.fetchone()
        mycon.close()
        if res:
            return res[0]
    except Exception as e:
        print("DB fetch error:", e)
    return 0

def load_user_data():
    global user_records, user_names, user_ids
    user_records = []
    user_names = []
    user_ids = []
    
    if not os.path.exists('LG.dat'):
        with open('LG.dat', 'wb') as f:
            pass

    try:
        with open('LG.dat', 'rb') as f:
            while True:
                try:
                    de = pickle.load(f)
                    user_records.append(de)
                    user_names.append(de.get("NAME", ""))
                    user_ids.append(de.get("USER ID", ""))
                except EOFError:
                    break
    except Exception as e:
        print("Error loading LG.dat:", e)

# Run initial setups
init_db()
load_user_data()

# --- TKINTER LOGIN & SIGNUP SCREENS ---

def password_check(uname, passwd):
    for u in user_records:
        if uname == u.get('NAME'):
            return u.get('PASS') != passwd
    return True

def launch_auth_flow():
    global details
    auth_success = False

    root = Tk()
    root.title("Mechflight - Authentication")
    root.geometry("1200x650")
    try:
        root.state('zoomed')
    except Exception:
        pass

    bg_photo = None
    try:
        img_bg = Image.open("lgbg.jpg")
        bg_photo = ImageTk.PhotoImage(img_bg)
        bg_label = Label(root, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.pack(fill="both", expand="yes")
    except Exception:
        root.configure(bg="black")

    welcome_frame = Frame(root, bg="black")
    login_frame = Frame(root, bg="black")
    signup_frame = Frame(root, bg="black")

    def show_frame(frame_to_show):
        welcome_frame.place_forget()
        login_frame.place_forget()
        signup_frame.place_forget()

        frame_w = 500
        frame_h = 580 if frame_to_show == signup_frame else 500
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        x = (screen_w // 2) - (frame_w // 2)
        y = (screen_h // 2) - (frame_h // 2)
        frame_to_show.place(x=x, y=y, width=frame_w, height=frame_h)

    # --- 1. WELCOME FRAME ---
    w_caption = Label(welcome_frame, text="MECHFLIGHT", font=("Impact", 40), fg="white", bg="black")
    w_caption.place(relx=0.5, y=80, anchor="center")

    w_sub = Label(welcome_frame, text="Choose an option to continue", font=("Arial", 14), fg="grey", bg="black")
    w_sub.place(relx=0.5, y=160, anchor="center")

    w_login_btn = Button(welcome_frame, text="Login", font=("Impact", 22), fg="white", bg="blue", bd=0, cursor="hand2",
                         command=lambda: show_frame(login_frame))
    w_login_btn.place(relx=0.5, y=260, width=350, height=60, anchor="center")

    w_signup_btn = Button(welcome_frame, text="Sign Up", font=("Impact", 22), fg="white", bg="darkgreen", bd=0, cursor="hand2",
                          command=lambda: show_frame(signup_frame))
    w_signup_btn.place(relx=0.5, y=360, width=350, height=60, anchor="center")

    # --- 2. LOGIN FRAME ---
    l_caption = Label(login_frame, text="Welcome Warrior!!", font=("Impact", 30), fg="white", bg="black")
    l_caption.place(x=50, y=30)

    l_uname_lbl = Label(login_frame, text="Username", font=("Arial", 13, "bold"), fg="grey", bg="black")
    l_uname_lbl.place(x=70, y=120)
    l_uname_entry = Entry(login_frame, highlightthickness=2, relief=FLAT, font=("Arial", 13))
    l_uname_entry.place(x=75, y=145, width=350, height=35)

    l_pass_lbl = Label(login_frame, text="Password", font=("Arial", 13, "bold"), fg="grey", bg="black")
    l_pass_lbl.place(x=70, y=210)
    l_pass_entry = Entry(login_frame, highlightthickness=2, relief=FLAT, font=("Arial", 13), show="•")
    l_pass_entry.place(x=75, y=235, width=350, height=35)

    def do_login():
        nonlocal auth_success
        uname = l_uname_entry.get().strip()
        passwd = l_pass_entry.get().strip()
        if not uname or not passwd:
            messagebox.showerror("Error", "All fields are required", parent=root)
        elif uname not in user_names:
            messagebox.showerror("Error", "Username not found", parent=root)
        elif password_check(uname, passwd):
            messagebox.showerror("Error", "Incorrect password", parent=root)
        else:
            for u in user_records:
                if uname == u['NAME']:
                    details.clear()
                    details.update(u)
            messagebox.showinfo("Welcome", "Hey\nWelcome Back!!")
            auth_success = True
            root.destroy()

    l_btn = Button(login_frame, text="Login", bg="blue", fg="white", bd=0, font=("Impact", 18), cursor="hand2", command=do_login)
    l_btn.place(x=75, y=320, width=350, height=50)

    l_back_btn = Button(login_frame, text="< Back", font=("Impact", 14), fg="white", bg="grey", cursor="hand2",
                        command=lambda: show_frame(welcome_frame))
    l_back_btn.place(x=75, y=400, width=350, height=40)

    # --- 3. SIGNUP FRAME ---
    s_caption = Label(signup_frame, text="Get Ready Warrior!!", font=("Impact", 30), fg="white", bg="black")
    s_caption.place(x=35, y=25)

    s_uname_lbl = Label(signup_frame, text="Username", font=("Arial", 12, "bold"), fg="grey", bg="black")
    s_uname_lbl.place(x=70, y=95)
    s_uname_entry = Entry(signup_frame, highlightthickness=2, relief=FLAT, font=("Arial", 12))
    s_uname_entry.place(x=75, y=120, width=350, height=35)

    s_pass_lbl = Label(signup_frame, text="Password", font=("Arial", 12, "bold"), fg="grey", bg="black")
    s_pass_lbl.place(x=70, y=170)
    s_pass_entry = Entry(signup_frame, highlightthickness=2, relief=FLAT, font=("Arial", 12), show="•")
    s_pass_entry.place(x=75, y=195, width=350, height=35)

    s_cpass_lbl = Label(signup_frame, text="Confirm Password", font=("Arial", 12, "bold"), fg="grey", bg="black")
    s_cpass_lbl.place(x=70, y=245)
    s_cpass_entry = Entry(signup_frame, highlightthickness=2, relief=FLAT, font=("Arial", 12), show="•")
    s_cpass_entry.place(x=75, y=270, width=350, height=35)

    s_email_lbl = Label(signup_frame, text="Email", font=("Arial", 12, "bold"), fg="grey", bg="black")
    s_email_lbl.place(x=70, y=320)
    s_email_entry = Entry(signup_frame, highlightthickness=2, relief=FLAT, font=("Arial", 12))
    s_email_entry.place(x=75, y=345, width=350, height=35)

    def do_signup():
        nonlocal auth_success
        global Text_box_complete
        uname = s_uname_entry.get().strip()
        passwd = s_pass_entry.get().strip()
        cpasswd = s_cpass_entry.get().strip()
        email = s_email_entry.get().strip()

        if not uname or not passwd or not cpasswd or not email:
            messagebox.showerror("Error", "All fields are required", parent=root)
        elif uname in user_names:
            messagebox.showerror("Error", "Username already exists", parent=root)
        elif passwd != cpasswd:
            messagebox.showerror("Error", "Password and Confirm Password must be the same", parent=root)
        else:
            details.clear()
            details["NAME"] = uname
            details["EMAIL ID"] = email
            details["PASS"] = passwd

            while True:
                uid_char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                uid = "#" + "".join(random.choices(uid_char, k=6))
                if uid not in user_ids:
                    details["USER ID"] = uid
                    break

            try:
                with open("LG.dat", "ab") as f:
                    pickle.dump(details, f)
            except Exception as e:
                print("Error saving to LG.dat:", e)

            user_records.append(details.copy())
            user_names.append(details["NAME"])
            user_ids.append(details["USER ID"])

            try:
                mycon = db.connect(host='localhost', user='root', password='987654321', database='mechflight')
                c = mycon.cursor()
                c.execute('insert into scores values (%s, %s, 0);', (details['USER ID'], details['NAME']))
                mycon.commit()
                mycon.close()
            except Exception as e:
                print("DB Signup Error:", e)

            messagebox.showinfo("Finished", "Registered successfully")
            Text_box_complete = False
            auth_success = True
            root.destroy()

    s_btn = Button(signup_frame, text="Confirm", bg="blue", fg="white", bd=0, font=("Impact", 18), cursor="hand2", command=do_signup)
    s_btn.place(x=75, y=410, width=350, height=50)

    s_back_btn = Button(signup_frame, text="< Back", font=("Impact", 14), fg="white", bg="grey", cursor="hand2",
                        command=lambda: show_frame(welcome_frame))
    s_back_btn.place(x=75, y=480, width=350, height=40)

    show_frame(welcome_frame)

    root.mainloop()
    return auth_success

# --- PYGAME HELPER FUNCTIONS ---

def set_fullscreen_mode():
    return pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

def load_font(name, size):
    try:
        return pygame.font.Font(name, size)
    except Exception:
        return pygame.font.SysFont('arial', size)

def text_single(s, x, y, c, f_size, color=(255, 0, 0)):
    font = load_font('ARCADE.TTF', f_size)
    i = font.render(s, True, color)
    c.blit(i, (x, y))

def is_button_clicked(rect, events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(event.pos):
                return True
    return False

def is_mouse_hovering(rect):
    return rect.collidepoint(pygame.mouse.get_pos())

def button_draw(s, c, f_size, r, C, e=True, events=None):
    font = load_font('perfect-dark-brk/pdark.ttf', f_size)
    b_text = font.render(s, True, C)
    b_rec = b_text.get_rect(center=r.center)
    if e:
        if is_mouse_hovering(r):
            pygame.draw.rect(c, (80, 80, 80), r, 0, 5)
        else:
            pygame.draw.rect(c, (0, 0, 0), r, 0, 5)
        pygame.draw.rect(c, (255, 255, 255), r, 1, 5)
        c.blit(b_text, b_rec)

    if e and events is not None:
        return is_button_clicked(r, events)
    return False

# --- PYGAME SCREENS ---

def player_profile():
    screen = set_fullscreen_mode()
    pygame.display.set_caption('Mechflight - Profile')
    clock = pygame.time.Clock()

    profileimg = pygame.transform.scale(pygame.image.load('profile photo1.png'), (220, 220))
    profile_rec = profileimg.get_rect(center=(screen_width / 4, screen_height / 2))

    backimg = pygame.transform.scale(pygame.image.load('back1.jpeg'), (50, 50))
    b_rec = backimg.get_rect()
    back = pygame.rect.Rect(0, 0, 100, 50)
    back.bottomleft = (20, screen_height - 20)
    b_rec.midleft = back.midright

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "home"

        screen.fill((10, 20, 30))
        pygame.draw.rect(screen, (20, 30, 40), (screen_width / 2 - 50, 0, screen_width / 2, screen_height), 0, 10)
        pygame.draw.rect(screen, (255, 255, 255), (screen_width / 2 - 50, 0, screen_width / 2, screen_height), 5, 10)
        screen.blit(profileimg, profile_rec)

        Y = 80
        for key in details:
            pygame.draw.rect(screen, (50, 60, 70), (screen_width / 2 - 30, Y, screen_width / 2 - 40, 70), 0, 10)
            pygame.draw.rect(screen, (80, 90, 100), (screen_width / 2 - 30, Y, screen_width / 2 - 40, 70), 3, 10)
            val = "••••••••" if key == "PASS" else str(details[key])
            text = f"{key}: {val}"
            text_single(text, screen_width / 2 - 10, Y + 20, screen, 30, (255, 255, 255))
            Y += 95

        if button_draw('BACK', screen, 22, back, 'grey', True, events):
            return "home"
        screen.blit(backimg, b_rec)

        pygame.display.flip()
        clock.tick(60)
    return "home"

def loading_screen():
    screen = set_fullscreen_mode()
    pygame.display.set_caption('Mechflight - Loading')
    clock = pygame.time.Clock()

    t = 0
    w1 = pygame.transform.scale(pygame.image.load("sprite1.png"), (60, 60))
    w2 = pygame.transform.scale(pygame.image.load("sprite2.png"), (60, 60))
    w3 = pygame.transform.scale(pygame.image.load("sprite3.png"), (60, 60))
    w4 = pygame.transform.scale(pygame.image.load("sprite4.png"), (60, 60))
    walk_sprites = [w1, w2, w3, w4]

    rec = pygame.rect.Rect(screen_width / 4, screen_height / 2, 30, 30)
    rg = pygame.rect.Rect(screen_width / 4, screen_height / 2 + 60, screen_width / 2, 3)
    speed = 6
    img_sprite = walk_sprites[0]

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "home"

        t += 2
        if t == 20:
            img_sprite = walk_sprites[1]
        elif t == 40:
            img_sprite = walk_sprites[2]
        elif t == 60:
            img_sprite = walk_sprites[3]
            t = 0

        rec.x += speed

        if rec.x + 60 > 3 * screen_width / 4:
            return "game"

        screen.fill((10, 20, 30))
        pygame.draw.rect(screen, (255, 255, 255), rg)
        screen.blit(img_sprite, rec)

        pygame.display.flip()
        clock.tick(60)
    return "game"

def game():
    screen = set_fullscreen_mode()
    pygame.display.set_caption('Mechflight')
    clock = pygame.time.Clock()
    fps = 60
    g_limit = screen_height - 110

    pd = {'roll': 0, 'roll1': 0, 'obs': 6, 'p_change': 5, 'dead': False, 'times': 0, 'e0': 0, 'jump': False,
          'draw': True, 'score': 0, 'sc_d': 0, 'hs': 0}
    font = load_font('ARCADE_N.TTF', 36)

    def draw_score():
        st = f'SCORE:{pd["score"]}'
        text = font.render(st, True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect(topleft=(20, 20))
        screen.blit(text, textRect)

    # BG MAPPING (Full Screen Dynamic Scaling)
    back = pygame.transform.scale(pygame.image.load("back6.jpg"), (screen_width, g_limit))
    ground = pygame.transform.scale(pygame.image.load("ground.jpg"), (screen_width, 130))
    back_width = back.get_width()
    ground_width = ground.get_width()
    tiles = math.ceil(screen_width / back_width) + 3
    tiles1 = math.ceil(screen_width / ground_width) + 3

    def bg_move():
        # Dino-game style difficulty scaling (smoothly increases speed as score goes up)
        current_speed = min(18, 6 + (pd['score'] * 0.025))
        pd['obs'] = current_speed
        sky_speed = current_speed * 0.4

        for i in range(tiles):
            screen.blit(back, (i * back_width - pd['roll1'], 0))
        for j in range(tiles1):
            screen.blit(ground, (j * ground_width - pd['roll'], g_limit))

        if not pd['dead']:
            pd['roll1'] += sky_speed
            pd['roll'] += current_speed

            if pd['roll1'] >= back_width:
                pd['roll1'] = 0
            if pd['roll'] >= ground_width:
                pd['roll'] = 0

    # PLAYER SPRITES & RECT
    p_x = 80
    p_y = g_limit - 85
    p_rec = pygame.Rect(p_x + 10, p_y + 10, 65, 65)

    w1 = pygame.transform.scale(pygame.image.load("sprite1.png"), (85, 90))
    w2 = pygame.transform.scale(pygame.image.load("sprite2.png"), (85, 90))
    w3 = pygame.transform.scale(pygame.image.load("sprite3.png"), (85, 90))
    w4 = pygame.transform.scale(pygame.image.load("sprite4.png"), (85, 90))
    f0 = pygame.transform.scale(pygame.image.load("sprite5.png"), (90, 130))
    f1 = pygame.transform.scale(pygame.image.load("sprite6.png"), (90, 130))
    f2 = pygame.transform.scale(pygame.image.load("sprite7.png"), (90, 130))
    f3 = pygame.transform.scale(pygame.image.load("sprite8.png"), (90, 130))
    e1 = pygame.transform.scale(pygame.image.load("explosion1.png"), (90, 90))
    e2 = pygame.transform.scale(pygame.image.load("explosion2.png"), (90, 90))
    
    walk_anim = [w1, w2, w3, w4]
    fly_anim = [f0, f2, f1, f3]
    expl_anim = [e1, e2]
    current_p_img = walk_anim[0]

    # OBSTACLES SPACING
    img_ob = pygame.image.load("obstacles.png").convert_alpha()
    img_ob = pygame.transform.rotate(img_ob, 90)
    ob_w = 130
    ob_h = 65
    ob_img = pygame.transform.scale(img_ob, (ob_w, ob_h))

    n = 5
    obs = []
    obs_hitbox = []

    for i in range(n):
        spawn_x = screen_width + i * 360 + random.randint(0, 100)
        spawn_y = random.randint(120, g_limit - ob_h - 10)
        rect = pygame.Rect(spawn_x, spawn_y, ob_w, ob_h)
        hitbox = pygame.Rect(spawn_x + 10, spawn_y + 10, ob_w - 20, ob_h - 20)
        obs.append(rect)
        obs_hitbox.append(hitbox)

    def p_move():
        nonlocal current_p_img
        keys = pygame.key.get_pressed()
        if not pd['dead']:
            if p_rec.y >= p_y:
                p_rec.y = p_y
                pd['jump'] = False

            if keys[pygame.K_SPACE] and p_rec.y > 50:
                pd['jump'] = True
                p_rec.y -= pd['p_change']
            elif p_rec.y < p_y:
                p_rec.y += 4  # gravity fall

            if p_rec.x < screen_width // 4:
                p_rec.x += 2

            for i in range(n):
                if obs_hitbox[i].colliderect(p_rec):
                    pd['dead'] = True

        if pd['draw']:
            screen.blit(current_p_img, (p_rec.x - 10, p_rec.y - 10))

    def update_obstacles():
        if not pd['dead']:
            for i in range(n):
                obs[i].x -= pd['obs']
                obs_hitbox[i].x -= pd['obs']

                if obs[i].right < 0:
                    max_x = max(o.x for o in obs)
                    new_x = max(screen_width, max_x + 320 + random.randint(0, 100))
                    r = random.random()
                    if r < 0.4:
                        y = g_limit - ob_h
                    elif r < 0.75:
                        y = random.randint(180, g_limit - 200)
                    else:
                        y = random.randint(60, 180)

                    obs[i].topleft = (new_x, y)
                    obs_hitbox[i].topleft = (new_x + 10, y + 10)

                screen.blit(ob_img, obs[i])
        else:
            for i in range(n):
                screen.blit(ob_img, obs[i])

    # RETRY MODAL RECTS (FULL SCREEN CENTERED)
    re_rect = pygame.rect.Rect(0, 0, 480, 340)
    re_rect.center = (screen_width / 2, screen_height / 2)
    retry_btn_rect = pygame.rect.Rect(screen_width / 2 - 90, screen_height / 2 + 80, 180, 55)
    close_btn_rect = pygame.rect.Rect(0, 0, 45, 45)
    close_btn_rect.topright = re_rect.topright

    retry_text = font.render('Try again', True, (255, 255, 255))
    retry_text_rect = retry_text.get_rect(center=(screen_width / 2, screen_height / 2 - 80))

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "home"

        clock.tick(fps)
        pd['times'] += 2

        if not pd['dead']:
            anim_list = fly_anim if pd['jump'] else walk_anim
            if pd['times'] == 20:
                current_p_img = anim_list[1]
                pd['score'] += 1
            elif pd['times'] == 40:
                current_p_img = anim_list[2]
                pd['score'] += 1
            elif pd['times'] >= 60:
                current_p_img = anim_list[3]
                pd['score'] += 1
                pd['times'] = 0
        else:
            if pd['e0'] < 3:
                if pd['times'] == 30:
                    current_p_img = expl_anim[1]
                elif pd['times'] >= 60:
                    current_p_img = expl_anim[0]
                    pd['e0'] += 1
                    pd['times'] = 0
            else:
                current_p_img = walk_anim[0]
                pd['draw'] = False
                if pd['sc_d'] == 0:
                    user_id = details.get('USER ID', '')
                    save_score_to_db(user_id, pd['score'])
                    pd['hs'] = max(pd['score'], fetch_highscore_db(user_id))
                    pd['sc_d'] += 1

        screen.fill((211, 211, 211))

        bg_move()
        update_obstacles()
        p_move()
        draw_score()

        if not pd['draw']:
            pygame.draw.rect(screen, (0, 0, 0), re_rect, 0, 12)
            pygame.draw.rect(screen, (255, 255, 255), re_rect, 3, 12)
            screen.blit(retry_text, retry_text_rect)

            hss = f'HIGHSCORE: {pd["hs"]}'
            text_single(hss, screen_width / 2 - 140, screen_height / 2, screen, 36, (255, 255, 0))

            if button_draw('RETRY', screen, 30, retry_btn_rect, 'white', True, events):
                return "game"
            if button_draw('X', screen, 30, close_btn_rect, 'white', True, events):
                return "home"

        pygame.display.flip()

    return "home"

def open_home():
    global Text_box_complete

    screen = set_fullscreen_mode()
    pygame.display.set_caption('Mechflight - Home')
    clock = pygame.time.Clock()

    font = load_font('ARCADE_N.TTF', 85)
    hd = font.render('MECHFLIGHT', True, (255, 255, 255))
    h_rec = hd.get_rect(center=(screen_width / 2, screen_height / 2 - 60))
    h_speed = 1
    up = True

    nme = details.get('NAME', 'Player')
    profileimg = pygame.transform.scale(pygame.image.load('profile photo1.png'), (60, 60))
    profile_rec = profileimg.get_rect(topleft=(screen_width / 4, 30))

    Player_profile = pygame.rect.Rect(30, 30, screen_width / 4, 60)
    Start = pygame.rect.Rect(0, 0, 280, 90)
    Start.center = (screen_width / 2, 3 * screen_height / 4 + 40)

    Text_box = pygame.rect.Rect(0, screen_height - 200, screen_width, 200)
    Next = pygame.rect.Rect(screen_width - 140, screen_height - 70, 120, 55)
    j = 0
    script_idx = 0

    script_lines = []
    try:
        with open('Script.txt', 'r') as f:
            script_lines = [line.strip() for line in f if line.strip()]
    except Exception:
        script_lines = ["Hello! Welcome to Mechflight!", "Created by Class 12 students.", "Thank You for downloading!"]

    if not script_lines:
        script_lines = ["Welcome to Mechflight!"]

    D = script_lines[0]

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"

        screen.fill((20, 30, 40))

        if not Text_box_complete and script_idx < len(script_lines):
            pygame.draw.rect(screen, (0, 0, 0), Text_box)
            pygame.draw.rect(screen, (255, 255, 255), Text_box, 2)
            
            # Display typewriter text
            text_single(D[0:j], 50, screen_height - 150, screen, 38, (255, 255, 255))
            if j < len(D):
                j += 1

            if button_draw('Next', screen, 26, Next, (255, 215, 0), True, events):
                script_idx += 1
                if script_idx < len(script_lines):
                    D = script_lines[script_idx]
                    j = 0
                else:
                    Text_box_complete = True
        else:
            Text_box_complete = True

            if button_draw(nme, screen, 28, Player_profile, (255, 215, 0), True, events):
                return "profile"
            screen.blit(profileimg, profile_rec)

            if button_draw('Start', screen, 40, Start, (255, 215, 0), True, events):
                return "loading"

            # Title float animation
            if h_rec.y > screen_height / 2 - 100 and up:
                h_rec.y -= h_speed
            else:
                up = False
                if h_rec.y < screen_height / 2 - 20:
                    h_rec.y += h_speed
                else:
                    up = True
            screen.blit(hd, h_rec)

        pygame.display.flip()
        clock.tick(60)

    return "quit"

# --- MAIN RUNNER ---

def main():
    if not launch_auth_flow():
        print("User exited login/signup.")
        return

    current_screen = "home"
    while current_screen != "quit":
        if current_screen == "home":
            current_screen = open_home()
        elif current_screen == "profile":
            current_screen = player_profile()
        elif current_screen == "loading":
            current_screen = loading_screen()
        elif current_screen == "game":
            current_screen = game()
        else:
            break

    pygame.quit()

if __name__ == "__main__":
    main()

