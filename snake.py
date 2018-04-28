'''
Dit spel is gemaakt via klasses, het kan ook zonder maar dan hebben we
globale variabelen nodig, dit zou kunnen mislopen, het staat nog niet
op punt maar het werkt al.

De snelheid van de slang is nu 10 pixels per 1/30 seconde.
Dit kan je altijd aanpassen door de slaaptijd te verkleinen.
Dit doe je onderaan bij time.sleep(1/30). Deze bevindt zich in
de while loop.

Veel plezier.

'''

import random, time
from tkinter import *

class game(object):
    def __init__(self, width=300, height=300):
        self.width = width
        self.height = height

        self.tk = Tk()
        self.tk.resizable(0,0)
        self.tk.wm_attributes('-topmost', 1)
        self.tk.title("Snake")
        self.canvas = Canvas(self.tk, width=self.width, height=self.height, bd=0, \
                             highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        
    def get_info(self):
        return (self.canvas, self.width, self.height)        
    
        
class Snake(object):
    def __init__(self, spel):
        (self.canvas, self.width, self.height) = spel.get_info()
        self.length = 4
        self.vx = 10
        self.vy = 0
        self.trail = [(random.randint(0, (self.width)/10-1)*10, \
                       random.randint(0, (self.height)/10-1)*10)]
        self.parts = [self.canvas.create_rectangle(self.trail[-1][0], \
                            self.trail[-1][1], self.trail[-1][0]+10, \
                            self.trail[-1][1]+10, fill='green')]
        self.score = 0
        self.score_label = self.canvas.create_text(5, 5, text='SCORE: %s' \
                                %(self.score), font=('Helvetica', 10), anchor=NW)

        self.running = True

        self.canvas.bind_all('<KeyPress - Up>', self.vxvy)
        self.canvas.bind_all('<KeyPress - Down>', self.vxvy)
        self.canvas.bind_all('<KeyPress - Left>', self.vxvy)
        self.canvas.bind_all('<KeyPress - Right>', self.vxvy)

    def draw(self):
        self.parts.append(self.canvas.create_rectangle(self.trail[-1][0], \
                            self.trail[-1][1], self.trail[-1][0]+10, \
                            self.trail[-1][1]+10, fill='green'))
        #print(len(self.trail))
        
        
    def move(self):
        x = self.trail[-1][0] + self.vx
        y = self.trail[-1][1] + self.vy
        self.trail.append((x*(0 <= x and x < self.width) + \
                          (self.width-10)*(x < 0), (self.height-10)*(y < 0) + \
                          y*(0 <= y and y < self.height)))
        if self.trail.count(self.trail[-1]) > 1:
            self.running = False
            
    #def delete(self):
        if len(self.trail) > self.length:
            del self.trail[0]
            a = self.parts.pop(0)
            self.canvas.delete(a)
        
            
    def vxvy(self, evt):
        key = evt.keysym
        self.vx = -10*(key == 'Left') + 20*(key == 'Left')*(self.vx == 10) + \
                  10*(key == 'Right') - 20*(key == 'Right')*(self.vx == -10)
        self.vy = -10*(key == 'Up') + 20*(key == 'Up')*(self.vy == 10) + \
                  10*(key == 'Down') - 20*(key == 'Down')*(self.vy == -10)

    def get_trail(self):
        return self.trail

    def get_score(self):
        return self.score

    def add_score(self):
        self.score += 10
        self.length += 1
        self.canvas.itemconfig(self.score_label, text='SCORE: %s' %(self.score))

#random food
def food(info, trail):
    (a, b) = trail[0]
    while (a,b) in trail:
        a = random.randint(0, info[1]/10-1)*10
        b = random.randint(0, info[2]/10-1)*10
        
    foodblok = info[0].create_rectangle(a, b, a+10, b+10, fill="red")
    
    return (a, b), foodblok

        
#initialisatie spel

spel = game()
snake = Snake(spel)
foodoncanvas = False

while 1:
        snake.move()
        if not foodoncanvas:
            foodloc, foodblok = food(spel.get_info(), snake.get_trail())
            foodoncanvas = True
        elif snake.get_trail()[0] == foodloc:
            snake.add_score()
            spel.canvas.delete(foodblok)
            foodoncanvas = False
        
        snake.draw()
        if not snake.running:
            break
        
        spel.tk.update_idletasks()
        spel.tk.update()
        time.sleep(1/30)

#indien game over
spel.canvas.create_text(150, 120, text="GAME OVER", \
                           font=("Helvetica", 30), anchor=N)
spel.canvas.create_text(150, 155, text="SCORE: %s" %(snake.get_score()),
                        font=("Helvetica", 15), anchor=N, fill='blue')
spel.canvas.update()

time.sleep(3)
spel.tk.destroy()



    
