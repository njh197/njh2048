import threading, queue, time, random, os
from msvcrt import getwch # Windows only

KEY_UP = 'H'
KEY_DOWN = 'P'
KEY_LEFT = 'K'
KEY_RIGHT = 'M'
dc = {'H':'up','P':'down','K':'left','M':'right'}

def nothing(*args):
    pass

callback_func = nothing

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')

def input_loop():
    try:
        global isexit
        while True:
            key = getwch()
            if key=='\x1b':
                # ESC key
                input_queue.put('esc')
            elif key=='\b':
                pass
            elif key=='\r':
                pass
            elif key=='à':
                key = getwch()
                if dc.get(key,None) is not None:
                    input_queue.put(dc[key])
                else:
                    pass
            else:
                input_queue.put(key)
    except KeyboardInterrupt:
        return None
    except Exception as e:
        print(e)

input_queue = queue.Queue()
input_thread = threading.Thread(target=input_loop)
input_thread.daemon = True
input_thread.start()

ls = [
    [1,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,1]
]
pts = 0

def update_screen():
    clear_screen()
    print("Score:", pts)
    for i in ls:
        for j in i:
            print(j, end=' ')
        print()

clear_screen()
print("Press ESC to quit")
print("Use arrow keys to move tiles")
time.sleep(2)
update_screen()
while True:
    key = input_queue.get()
    if key == 'esc':
        clear_screen()
        print("Score:",pts)
        while True:
            key = input_queue.get()
            if key == 'esc':
                clear_screen()
                break
            time.sleep(0.2)
        break
    if key == 'up':
        for j in range(4):
            ls1=[]
            for i in range(4):
                if ls[i][j]!=0:
                    ls1.append(ls[i][j])
                ls[i][j]=0
            for i in range(len(ls1)):
                ls[i][j]=ls1[i]
            for i in range(3):
                if ls[i][j]!=0 and ls[i][j]==ls[i+1][j]:
                    ls[i][j]*=2
                    ls[i+1][j]=0
                    pts+=1
            ls1=[]
            for i in range(4):
                if ls[i][j]!=0:
                    ls1.append(ls[i][j])
                ls[i][j]=0
            for i in range(len(ls1)):
                ls[i][j]=ls1[i]
        update_screen()
    elif key == 'down':
        for j in range(4):
            ls1=[]
            for i in range(4):
                if ls[i][j]!=0:
                    ls1.append(ls[i][j])
                ls[i][j]=0
            for i in range(len(ls1)):
                ls[4-len(ls1)+i][j]=ls1[i]
            for i in range(2,-1,-1):
                if ls[i][j]!=0 and ls[i][j]==ls[i+1][j]:
                    ls[i][j]*=2
                    ls[i+1][j]=0
                    pts+=1
            ls1=[]
            for i in range(4):
                if ls[i][j]!=0:
                    ls1.append(ls[i][j])
                ls[i][j]=0
            for i in range(len(ls1)):
                ls[4-len(ls1)+i][j]=ls1[i]
        update_screen()
    elif key == 'left':
        for i in range(4):
            ls1=[]
            for j in range(4):
                if ls[i][j]!=0:
                    ls1.append(ls[i][j])
                ls[i][j]=0
            for j in range(len(ls1)):
                ls[i][j]=ls1[j]
            for j in range(3):
                if ls[i][j]!=0 and ls[i][j]==ls[i][j+1]:
                    ls[i][j]*=2
                    ls[i][j+1]=0
                    pts+=1
            ls1=[]
            for j in range(4):
                if ls[i][j]!=0:
                    ls1.append(ls[i][j])
                ls[i][j]=0
            for j in range(len(ls1)):
                ls[i][j]=ls1[j]
        update_screen()
    elif key == 'right':
        for i in range(4):
            ls1=[]
            for j in range(4):
                if ls[i][j]!=0:
                    ls1.append(ls[i][j])
                ls[i][j]=0
            for j in range(len(ls1)):
                ls[i][4-len(ls1)+j]=ls1[j]
            for j in range(2,-1,-1):
                if ls[i][j]!=0 and ls[i][j]==ls[i][j+1]:
                    ls[i][j]*=2
                    ls[i][j+1]=0
                    pts+=1
            ls1=[]
            for j in range(4):
                if ls[i][j]!=0:
                    ls1.append(ls[i][j])
                ls[i][j]=0
            for j in range(len(ls1)):
                ls[i][4-len(ls1)+j]=ls1[j]
        update_screen()
    if key in ['up', 'down', 'left', 'right']:
        flag=True
        for i in range(4):
            for j in range(4):
                if ls[i][j]==0:
                    flag=False
        if flag:
            clear_screen()
            print("Game Over!")
            print("Score:",pts)
            while True:
                key = input_queue.get()
                if key == 'esc':
                    clear_screen()
                    break
                time.sleep(0.2)
            break
        empty_cells=[]
        for i in range(4):
            for j in range(4):
                if ls[i][j]==0:
                    empty_cells.append((i,j))
        cell=random.choice(empty_cells)
        if random.randint(1,3)<=2:
            ls[cell[0]][cell[1]]=1
        else:
            ls[cell[0]][cell[1]]=2
    time.sleep(0.1)
