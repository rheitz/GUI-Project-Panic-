import Tkinter

root = Tkinter.Tk()

p1y_intvar = Tkinter.IntVar()
p1y_intvar.set(300) #initialize radius
p2y_intvar = Tkinter.IntVar()
p2y_intvar.set(300) #initialize radius

#Initial paddle position and size
w=5
h=100
p1x=10
p1y=300
p2x=590
p2y=300

#Score variables
score_p1 = -200
score_p2 = 0

# Top left corner of paddle 1
p1x1 = p1x-w/2
p1y1 = p1y-h/2
# Bottom right corner of paddle 1
p1x2 = p1x+w/2
p1y2 = p1y+h/2

def check_collision(canvas_item):
    bx1, by1, bx2, by2 = canvas.coords(circle_item)
    px1, py1, px2, py2 = canvas.coords(canvas_item)
    tl_inside = is_point_inside(bx1,by1,px1,py1,px2,py2)
    br_inside = is_point_inside(bx2,by2,px1,py1,px2,py2)
    if tl_inside or br_inside:
        print("inside paddle")
        return True

    
def is_point_inside(x,y,rx1,ry1,rx2,ry2):
    if x<rx2 and x>rx1 and y<ry2 and y>ry1:
        return True
    else:
        return False

def key(event):
    print "pressed", repr(event.char)
    c = event.char
    #
    #Player 1
    if c == "q":
        p1y = p1y_intvar.get()
        p1y -= 20
        p1y1 = p1y-h/2
        p1y2 = p1y+h/2
        p1y_intvar.set(p1y)
        # Controller updating the view
        canvas.coords(paddle_1,p1x1, p1y1,p1x2, p1y2)
    if c == "a":
        p1y = p1y_intvar.get()
        p1y += 20
        p1y_intvar.set(p1y)
        # Controller updating the view
        canvas.coords(paddle_1,p1x-w/2, p1y-h/2,p1x+w/2, p1y+h/2)
    #
    #Player 2
    if c == "o":
        p2y = p2y_intvar.get()
        p2y -= 20
        p2y_intvar.set(p2y)
        # Controller updating the view
        canvas.coords(paddle_2,p2x-w/2, p2y-h/2,p2x+w/2, p2y+h/2)
    if c == "l":
        p2y = p2y_intvar.get()
        p2y += 20
        p2y_intvar.set(p2y)
        # Controller updating the view
        canvas.coords(paddle_2,p2x-w/2, p2y-h/2,p2x+w/2, p2y+h/2)
    

def callback(event):
    canvas.focus_set()
    print "clicked at", event.x, event.y

#####
# Create Model
######
speed_intvar = Tkinter.IntVar()
speed_intvar.set(3) # Initialize y coordinate
# radius and x-coordinate of circle
r = 10
x = 150
y = 150
direction = 0.5 # radians of angle in standard position, ccw from positive x axis

#frame = Frame(root, width=100, height=100)
topframe = Tkinter.Canvas(root, width=600, height=100, )
topframe.grid(row=0, column=0)

# Create and place directions for the user
title_text = Tkinter.Label(topframe, text='PANIC!', font = "Helvetica 28 bold italic")
title_text.grid(row=0, column=0)

#frame = Frame(root, width=100, height=100)
midframe = Tkinter.Canvas(root, width=600, height=100, )
midframe.grid(row=1, column=0)
# Create and place directions for the user
s1 = Tkinter.Label(midframe, text='Score 1: 0',  font = "Helvetica 12 bold")
s1.grid(row=0, column=0)
# Create and place directions for the user
speed_slider = Tkinter.Scale(midframe, from_=1, to=10, variable=speed_intvar, orient=Tkinter.HORIZONTAL,label='speed')
speed_slider.grid(row=0, column=1)
# Create and place directions for the user
s2 = Tkinter.Label(midframe, text='Score 2: 0', font = "Helvetica 12 bold")
s2.grid(row=0, column=2)


canvas = Tkinter.Canvas(root, width=600, height=600, background='#FFFFFF')
canvas.grid(row=2, column=0)
canvas.bind("<Key>", key)
canvas.bind("<Button-1>", callback)
#canvas.pack()

#c Create paddle 1

paddle_1 = canvas.create_rectangle(p1x1,p1y1,p1x2,p1y2,fill='#000000') 

paddle_2 = canvas.create_rectangle(p2x-w/2, p2y-h/2,p2x+w/2, p2y+h/2,fill='#000000') 

# Create a circle on the canvas to match the initial model
circle_item = canvas.create_oval(x-r, y-r, x+r, y+r, 
                                 outline='#000000', fill='#00FFFF')

import math
def animate():

    # Get the slider data and create x- and y-components of velocity
    velocity_x = speed_intvar.get() * math.cos(direction) # adj = hyp*cos()
    velocity_y = speed_intvar.get() * math.sin(direction) # opp = hyp*sin()
    # Change the canvas item's coordinates
    canvas.move(circle_item, velocity_x, velocity_y)
    
    # Get the new coordinates and act accordingly if ball is at an edge
    x1, y1, x2, y2 = canvas.coords(circle_item)
  
    global direction, score_p1, score_p2
      
    # Check for collision with paddle 1
    collision_1 = check_collision(paddle_1)
    collision_2 = check_collision(paddle_2)

    if collision_1 == True or collision_2 == True:
        direction = math.pi - direction # Reverse the x-component of velocity
    else:    
        # If crossing left or right of canvas
        if x2>canvas.winfo_width(): # if it goes off the right side
            score_p1 += 100
            print score_p1
            s1 = Tkinter.Label(midframe, text='Score 1: '+ str(score_p1),  font = "Helvetica 12 bold")
            s1.grid(row=0, column=0)
            #reverse direction
            direction = math.pi - direction # Reverse the x-component of velocity
        if x2<0: # if it goes off the left side
            score_p2 += 100
            print score_p2
            s2 = Tkinter.Label(midframe, text='Score 2: '+ str(score_p2), font = "Helvetica 12 bold")
            s2.grid(row=0, column=2)
            #reverse direction
            direction = math.pi - direction # Reverse the x-component of velocity 
        # If crossing top or bottom of canvas
        if y2>canvas.winfo_height() or y1<0: 
            direction = -1 * direction # Reverse the y-component of velocity
    
    # Create an event in 1 msec that will be handled by animate(),
    # causing recursion        
    canvas.after(1, animate)
# Call function directly to start the recursion
animate()

root.mainloop()