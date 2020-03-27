import os, sys
import threading
import pyautogui, datetime
import win32gui, pickle, sqlite3
from pynput.mouse import Listener
import keyboard
import time

killswitch = False
conn = sqlite3.connect('packs.db')
c = conn.cursor()
class Bot:
    global killswitch
    def __init__(self,window):
        self.hwnd = win32gui.FindWindow(None, window)
        self.mail = None
        
    def pos(self):
        try:
            rect = win32gui.GetWindowRect(self.hwnd)
            x,y = rect[0], rect[1]
            w,h = rect[2]-x, rect[3]-y  #1206 686
            return x,y,w,h
        except:
            return False
        
    def execute(self,id):
        if self.hwnd == 0:
            print('Fenster nicht gefunden')
            return False
        c.execute('SELECT name,WW,WH FROM packages WHERE id=' + str(id))
        name,ww,wh = c.fetchone()
        try:
            win32gui.SetForegroundWindow(self.hwnd)
        except:
            print('SetForeground Failed')
        data = pickle.load(open(name+'.p','rb'))
        starttime = data[0][2]
        for action in data:
            time.sleep(action[2]-starttime)
            starttime = action[2]
            x,y,w,h = self.pos()
            XFaktor = w / ww
            YFaktor = h / wh
            mx,my = action[0] * XFaktor, action[1] * YFaktor
            pyautogui.click(x + mx,y + my)
            
class record:
    global killswitch
    def __init__(self,window):
        self.window = window
        self.hwnd = win32gui.FindWindow(None, window)
        self.data = []
        self.record = False

    def pos(self):
        try:
            rect = win32gui.GetWindowRect(self.hwnd)
            x,y = rect[0], rect[1]
            w,h = rect[2]-x, rect[3]-y
            return x,y,w,h
        except:
            return False
    
    def list(self):
        print('ID   |  NAME')
        print('----------')
        conn = sqlite3.connect('packs.db')
        c = conn.cursor()
        packs = []
        for row in c.execute('SELECT * FROM packages'):
            packs.append(row)
        return packs
            
    def save(self,name):
        if self.data != []:
            #try:
            conn = sqlite3.connect('packs.db')
            c = conn.cursor()
            if self.pos() != False:
                x,y,w,h = self.pos()
            else:
                print('cant get width and hight')
                return False
            id = 1
            for row in c.execute('SELECT * FROM packages'):
                id+=1
            zeit = str(datetime.datetime.now().time())
            zeit1 = zeit.replace(':','-')[:8]
            c.execute('INSERT INTO packages VALUES ({},"{}","{}",{},"{}",{},{})'.format(id,name,zeit1,len(self.data),self.window,w,h))
            conn.commit()
            pickle.dump(self.data, open(name+'.p','wb'))
            print(name, 'gespeichert')
            return True
            #except:
            #    print('Fehler beim Speichern von', name)
            #    return False
        else:
            print('Data is empty')
            return False
        
    def on_click(self,x,y,button,pressed):
        global killswitch
        if killswitch:
            return False
        if self.pos() != False:
            x1,y1,w,h = self.pos()
            x = (x - x1)
            y = (y - y1)
        else:
            print('Problem with finding {}(s) position. Stopping.'.format(self.window))
            killswitch = True
            return False
        if str(button) == 'Button.right' and not pressed:
            if self.record == False:
                self.record = True
                print('Start Recording..')
                self.data.append([x,y,time.perf_counter()])
                print('x:{}|y:{}|t:0sek.'.format(x,y))
                return
            if self.record:
                self.record = False
                print('Recording beendet..')
                self.data.pop(0)
                killswitch = True
                zeit = str(datetime.datetime.now().time())
                zeit1 = zeit.replace(':','-')
                name = 'Saving {} Actions...'.format(len(self.data))
                print(name, '--> self.Data')
                return self.data
        if self.record:
            if str(button) == 'Button.left' and pressed:
                self.data.append([x,y,time.perf_counter()])
                print('x:{}|y:{}|t:{}sek.'.format(x,y,(self.data[len(self.data)-1][2]) - (self.data[len(self.data)-2][2])))

    def listen(self):
        try:
            win32gui.SetForegroundWindow(self.hwnd)
        except:
            print('SetForeground Failed')
        global killswitch
        with Listener(on_click=self.on_click) as listener:
            listener.join()
            if killswitch:
                return False
            if keyboard.is_pressed('q'):
                return True
      
try:
    c.execute('CREATE TABLE packages (id INT,name TEXT,time DATE, actions INT, window TEXT, WW INT, WH INT)')
    conn.commit()
except:
    pass

if __name__ == '__main__':
        
    if len(sys.argv) == 2:
        arg1 = sys.argv[1]
        if arg1 == 'list':
            pack = record('').list()
            for row in pack:
                print('{} | {}'.format(row[0], row[1]))
    elif len(sys.argv) == 3:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        if arg1 == '-b':
            c.execute('SELECT name, window FROM packages WHERE id=' + arg2)
            name,window = c.fetchone()
            idlebot = Bot(window)
            print('Bot executing ({}) on Window:{}'.format(name,window))
            idlebot.execute(arg2)
    elif len(sys.argv) == 4:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
        if arg1 == '-r':
            rec = record(arg2)
            rec.listen()
            rec.save(arg3)
    else:
        print('python idleBot.py list --> Show list of records.')
        print('python idleBot.py [-b] [RECORD ID]')
        print(' ^--> -b to use the Bot class to execute records.\n')
        print('python idleBot.py [-r] "[WINDOW NAME]" "[RECORD FILE NAME]"')
        print(' ^--> -r record something.\n')
        print('Example: idleBot.py -b 1234')
        print('         idleBot.py -r Bluestacks TakeLoot')
    
    
conn.commit()