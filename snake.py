
import time
import random
import curses

score = 0
delay = 0

def CheckGamelose (stdscr, h, w, length):
    x = w//2
    y = h//2
    if length [0][0] in [w-1, 0] or length [0][1] in [h-1, 0] or length[0] in length[1:]:
        stdscr.clear()
        stdscr.addstr (y, x - len("You Lose"), "You Lose")
        stdscr.addstr (y +1, x - len("You Lose"), "Score: " + str (score))
        stdscr.refresh()
        time.sleep(3)         
        return 0
    return 1

def ModeInit(stdscr, x, y):
    global delay
    menu = ["Hard", "Nomal", "Easy"]
    position = 0
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    stdscr.addstr (y - 3, x - 10//2, "GAME SNAKE")   
    while (True):         
        key = stdscr.getch()  
        for i in range (0, len(menu)):
            if i+1 == position:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr (y + i, x - 3, menu[i],curses.color_pair(1))   
                stdscr.attroff(curses.color_pair(1))

            else:
                stdscr.addstr (y + i, x - 3, menu[i])
        if key == curses.KEY_DOWN:
            position += 1
        elif key == curses.KEY_UP:
            position -= 1
        elif key in [curses.KEY_ENTER, ord('\n')]:
            if position == 1:
                delay = 0.05
            elif position == 2:
                delay = 0.1
            elif position == 3:
                delay = 0.2                                
            break

        if position > 3:
            position = 1
        if position < 1:
            position = 3
        stdscr.refresh()  

def main(stdscr):
    global score
    curses.curs_set(0)
    curses.noecho()
    stdscr.border(0)
    stdscr.keypad(1)
    stdscr.timeout(50)
    h, w = stdscr.getmaxyx()
    x = w//2
    y = h//2
    head = [x,y]
    length = [[x,y],[x+1,y], [x+2, y]]
    point_x = random.randint(2, w-2)
    point_y = random.randint (2, h-2)
    xxx = -1
    yyy = 0
    ModeInit (stdscr, x, y)
    while (CheckGamelose(stdscr, h, w, length)):
        stdscr.clear()   
        stdscr.border('#', '#', '#', '#', '#', '#', '#', '#')
        stdscr.addch(point_y, point_x, "*")
        CheckGamelose (stdscr, h, w, length)
        for i in range (0, len (length)):
            stdscr.addch (length [i][1], length [i][0], 'o')      
        key = stdscr.getch()
        if key == curses.KEY_RIGHT and xxx != -1:
            xxx = 1
            yyy = 0
        elif key == curses.KEY_LEFT and xxx != 1:
            xxx = -1 
            yyy = 0
        elif key == curses.KEY_DOWN and yyy != -1:
            xxx = 0
            yyy = 1
        elif key == curses.KEY_UP and yyy != 1:
            xxx = 0
            yyy = -1

        head[1] += yyy
        head[0] += xxx 
        if length [0][0] == point_x and length [0][1] == point_y:
            score += 1 
            point_x = random.randint(2, w-2)
            point_y = random.randint (2, h-2)
            length.insert(0, list (head))
            head[1] += yyy
            head[0] += xxx 

        length.insert(0, list (head))
        last = length.pop()
        stdscr.refresh()
        time.sleep(delay)
    curses.endwin()
curses.wrapper(main)
