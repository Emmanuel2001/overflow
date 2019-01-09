from turtle import Turtle, Screen, Shape, Pen
from random import randint

#screen
screen = Screen()
screen.setup(1024,600)
screen.tracer(0)

#boundaries
top = screen.window_height() / 2 - 100
bottom = -screen.window_height() / 2 + 100
left   = -screen.window_width() / 2 + 50
right  = screen.window_width() / 2 - 50

#field
area = Turtle()
area.hideturtle()
area.penup()
area.goto(right, top)
area.pendown()
area.goto(left, top)
area.goto(left, bottom)
area.goto(right, bottom)
area.goto(right, top)

#ball
ball = Turtle()
ball.penup()
ball.shape("circle")        
ball.shapesize(0.65, 0.65)
ball_radius = 10 * 0.5  

#plate
L = Turtle()
R = Turtle()
L.penup()
R.penup()

#shape of plate
paddle_w_half = 10 / 2      
paddle_h_half = 40 / 2      
paddle_shape = Shape("compound")
paddle_points = ((-paddle_h_half, -paddle_w_half),
                 (-paddle_h_half, paddle_w_half),
                 (paddle_h_half, paddle_w_half),
                 (paddle_h_half, -paddle_w_half))
paddle_shape.addcomponent(paddle_points, "Blue")
screen.register_shape("paddle", paddle_shape)
L.shape("paddle")
R.shape("paddle")

L.setx(left + 10)
R.setx(right - 10)

#score
score = Turtle()
score.penup()
score.hideturtle()
score_L = 0
score_R = 0
def write_scores() :
    score.clear()
    score.goto(-screen.window_width()/4, screen.window_height()/2 - 80)
    score.write(score_L, align="center", font=("Arial", 45, "bold"))
    score.goto(screen.window_width()/4, screen.window_height()/2 - 80)
    score.write(score_R, align="center", font=("Arial", 45, "bold"))

paddle_L_move_direction = 0
paddle_R_move_direction = 0
paddle_move_vert   = 21
def L_up() :
    global paddle_L_move_direction
    paddle_L_move_direction = 1
def L_down() :
    global paddle_L_move_direction
    paddle_L_move_direction = -1
def R_up() :
    global paddle_R_move_direction
    paddle_R_move_direction = 1
def R_down() :
    global paddle_R_move_direction
    paddle_R_move_direction = -1
def L_off() :
    global paddle_L_move_direction
    paddle_L_move_direction = 0
def R_off() :
    global paddle_R_move_direction
    paddle_R_move_direction = 0
    
screen.onkeypress(L_up, "w")
screen.onkeypress(L_down, "s")
screen.onkeypress(R_up, "Up")
screen.onkeypress(R_down, "Down")
screen.onkeyrelease(L_off, "w")
screen.onkeyrelease(L_off, "s")
screen.onkeyrelease(R_off, "Up")
screen.onkeyrelease(R_off, "Down")
screen.listen()
# Ball movement
ball_move_horiz = 18           
ball_move_vert  = 12

def update_ball_position () :
    global ball_move_horiz, ball_move_vert
    if ball.ycor() + ball_radius >= top :
        ball_move_vert *= -1
    elif bottom >= ball.ycor() - ball_radius : 
        ball_move_vert *= -1
    if ball_collides_with_paddle(R) or ball_collides_with_paddle(L) :
        ball_move_horiz *= -1
    ball.setx(ball.xcor() + ball_move_horiz)
    ball.sety(ball.ycor() + ball_move_vert)

winscore= Turtle()
winscore.hideturtle()
winscore.color("Red")

def check_if_someone_scores() :
    global score_L, score_R
    if (ball.xcor() + ball_radius) >= right :   # right of ball at right of field
        score_L += 1
        write_scores()
        reset_ball()
    elif left >= (ball.xcor() - ball_radius) :  # left of ball at left of field
        score_R += 1
        write_scores()
        reset_ball()

    if score_L == 7:
        screen.clear()
        winscore.write("GAME OVER \nPlayer 1 Wins!", align="center", font=("Arial", 45, "bold"))
        global ball_move_vert, ball_move_horiz
        ball.setpos(0, 0)
        speed_horiz = 0
        speed_vert = 0
    elif score_R == 7:
        screen.clear()
        winscore.write("GAME OVER \nPlayer 2 Wins!", align="center", font=("Arial", 45, "bold"))
        global ball_move_vert, ball_move_horiz
        ball.setpos(0, 0)
        speed_horiz = 0
        speed_vert = 0

def update_paddle_positions () :
    L_new_y_pos = L.ycor() + (paddle_L_move_direction * paddle_move_vert)
    R_new_y_pos = R.ycor() + (paddle_R_move_direction * paddle_move_vert)
    if paddle_is_allowed_to_move_here (L_new_y_pos):
        L.sety( L_new_y_pos )
    if paddle_is_allowed_to_move_here (R_new_y_pos):
        R.sety( R_new_y_pos )

def paddle_is_allowed_to_move_here (new_y_pos) :
    if (bottom > new_y_pos - paddle_h_half) : # bottom of paddle below bottom of field
        return False
    if (new_y_pos + paddle_h_half > top) :    # top of paddle above top of field
        return False
    return True


def ball_collides_with_paddle (paddle) :
    x_distance = abs(paddle.xcor() - ball.xcor())
    y_distance = abs(paddle.ycor() - ball.ycor())
    overlap_horizontally = (ball_radius + paddle_w_half >= x_distance)  # either True or False
    overlap_vertically   = (ball_radius + paddle_h_half >= y_distance)  # either True or False
    return overlap_horizontally and overlap_vertically

def reset_ball() :
    global ball_move_vert, ball_move_horiz
    ball.setpos(0, 0)
    speed_horiz = randint(12,15)
    speed_vert = randint(8,10)
    direction_horiz = 1
    direction_vert = 1
    if randint(0,100) > 50 :  # 50% chance of going left instead of right
        direction_horiz = -1
    if randint(0,100) > 50 :  # 50% chance of going down instead of up
        direction_vert = -1
    ball_move_horiz = direction_horiz * speed_horiz
    ball_move_vert  = direction_vert * speed_vert


#frame
def frame () :
    check_if_someone_scores()
    update_paddle_positions()
    update_ball_position()
    screen.update()                 
    screen.ontimer(frame, framerate)
 
#start
write_scores()
framerate = 40
frame()
