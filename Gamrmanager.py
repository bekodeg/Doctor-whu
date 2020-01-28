import tkinter
import random


def move_wrap(obj, move):
    move[0] = ((canvas.coords(obj)[0] + move[0]) % long_X) - canvas.coords(obj)[0]
    move[1] = ((canvas.coords(obj)[1] + move[1]) % long_Y) - canvas.coords(obj)[1]
    canvas.move(obj, move[0], move[1])


def do_nothing(x):
    pass


def check_move():
    if canvas.coords(player) == canvas.coords(exit):
        label.config(text="Победа!")
        master.bind("<KeyPress>", do_nothing)
    for f in fires:
        if canvas.coords(player) == canvas.coords(f):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)
    for e in enemies:
        if canvas.coords(player) == canvas.coords(e[0]):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)


def not_repeat():
    global pos
    while True:
        cords = [random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step]
        if cords not in pos:
            break
    pos.append(cords)
    return cords


def enemy_move(enemy, point):
    enemy = canvas.coords(enemy)
    player = canvas.coords(point)
    s = [player[0] - enemy[0], player[1] - enemy[1]]
    if s[0] < 0 and abs(s[0]) < long_X - enemy[0] + player[0]:
        s[0] = long_X - enemy[0] + player[0]
    elif s[0] > 0 and abs(s[0]) < long_X + enemy[0] - player[0]:
        s[0] = long_X + enemy[0] - player[0]
    if s[1] < 0 and abs(s[1]) < long_X - enemy[1] + player[1]:
        s[1] = long_X - enemy[1] + player[1]
    elif s[1] > 0 and abs(s[1]) < long_X + enemy[1] - player[1]:
        s[1] = long_X + enemy[1] - player[1]
    if (s[0] <= 2 * step) and (s[0] >= -2 * step) and (s[1] <= 2 * step) and (s[1] >= -2 * step):
        if abs(s[0]) > abs(s[1]):
            if s[0] < 0:
                return [step, 0]
            else:
                return [-step, 0]
        else:
            if enemy[1] < 0:
                return [0, step]
            else:
                return [0, -step]
    return random.choice([[step, 0], [-step, 0], [0, step], [0, -step]])


def prepare_and_start():
    global player, exit, fires, enemies, pos
    pos = []
    canvas.delete("all")
    player = canvas.create_image(not_repeat(), image=player_pic, anchor='nw')
    exit = canvas.create_image(not_repeat(), image=exit_pic, anchor='nw')
    fires = []
    for i in range(N_FIRES):
        fire = canvas.create_image(not_repeat(), image=fire_pic, anchor='nw')
        fires.append(fire)
    enemies = []
    for i in range(N_ENEMIES):
        enemy = canvas.create_image(not_repeat(), image=enemy_pic, anchor='nw')
        enemies.append((enemy, enemy_move))
    label.config(text="Найди выход!")
    master.bind("<KeyPress>", key_pressed)


def key_pressed(event):
    if event.keysym == '0':
        move_wrap(player, [random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step])
    if event.keysym == 'Up':
        move_wrap(player, [0, -step])
    elif event.keysym == 'Down':
        move_wrap(player, [0, step])
    elif event.keysym == 'Left':
        move_wrap(player, [-step, 0])
    elif event.keysym == 'Right':
        move_wrap(player, [step, 0])
    for enemy in enemies:
        direction = enemy[1](enemy[0], player)  # вызвать функцию перемещения у "врага"
        move_wrap(enemy[0], direction)  # произвести  перемещение
        check_move()


step = 60  # Размер клетки
N_X = 10
N_Y = 10   # Размер сетки
N_FIRES = 6  # Число клеток, заполненных огнем
N_ENEMIES = 4  # Число врагов
long_X = step * N_X
long_Y = step * N_Y
master = tkinter.Tk()
player_pic = tkinter.PhotoImage(file="images/doctor.gif")
exit_pic = tkinter.PhotoImage(file="images/tardis.gif")
fire_pic = tkinter.PhotoImage(file="images/fire.gif")
enemy_pic = tkinter.PhotoImage(file="images/dalek.gif")
label = tkinter.Label(master, text="Найди выход")
label.pack()
canvas = tkinter.Canvas(master, bg='#0070C0',
                        height=N_X * step, width=N_Y * step)
canvas.pack()
restart = tkinter.Button(master, text="Начать заново",
                         command=prepare_and_start)
restart.pack()
prepare_and_start()
master.mainloop()