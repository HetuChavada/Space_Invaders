import pygame
from pygame import mixer
from pygame.locals import *
import random
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk #pip install pillow
from tkinter import messagebox
import pymysql #pip install pymysql


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

#Intialize the pygame
pygame.init()

#define
clock=pygame.time.Clock()
fps=60

screen_width = 600
screen_height = 700

#Game screen
screen=pygame.display.set_mode((screen_width,screen_height))

#Game Title
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('Resources/ufo.png')
pygame.display.set_icon(icon)

#define fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

#load sounds
explosion_fx = pygame.mixer.Sound("Resources/img_explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("Resources/img_explosion2.wav")
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("Resources/img_laser.wav")
laser_fx.set_volume(0.25)

bg_fx = pygame.mixer.Sound("Resources/background.wav")
bg_fx.set_volume(0.20)

#define game variables
rows = 5
cols = 5
Enemy_cooldown = 1000#bullet cooldown in milliseconds
last_Enemy_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0#0 is no game over, 1 means player has won, -1 means player has lost

#define colours
red=(255,0,0)
green=(0,255,0)
white = (255, 255, 255)

# load background image
bg=pygame.image.load('Resources/bg.png')

def draw_bg():
    screen.blit(bg,(0,0))


#load Exit image
exit=pygame.image.load('Resources/button_quit.png')

def draw_exibtn():
    screen.blit(exit,(260,450))

"""#load Restart image
rs=pygame.image.load('Resources/button_resume.png')

def draw_rsbtn():
    screen.blit(rs,(140,450))"""


#define function for creating text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    
#create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Resources/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()


    def update(self):
        #set movement speed
        speed = 8
        #set a cooldown variable
        cooldown = 500 #milliseconds
        game_over = 0

        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT]and self.rect.right < screen_width:
            self.rect.x += speed

        #record current time
        time_now = pygame.time.get_ticks()
        #shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        #update mask
        self.mask=pygame.mask.from_surface(self.image)
       
            #draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over


#create Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Resources/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
       
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self,Enemy_group,True):
            #score increment
            score.score_up()
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


#create Enemies class
class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Resources/alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


#create Enemy Bullets class
class Enemy_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Resources/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self,spaceship_group,False,pygame.sprite.collide_mask):
            self.kill()
            explosion2_fx.play()
            #reduce spaceship health
            spaceship.health_remaining-=1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)

#create Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"Resources/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            #add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0


    def update(self):
        explosion_speed = 3
        #update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

class Score(object):
    def __init__(self):
        self.white = 255,255,255
        self.count = 0
        self.font =pygame.font.Font('freesansbold.ttf', 20)
        self.text = self.font.render("Score : "+str(self.count),1,self.white)

    def show_score(self, screen):
        screen.blit(self.text, (5 ,5))

    def score_up(self):
        self.count += 10
        self.text = self.font.render("Score : "+str(self.count),1,self.white)
            
#create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
Enemy_group = pygame.sprite.Group()
Enemy_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


def create_Enemies():
    #generate Enemies
    for row in range(rows):
        for item in range(cols):
            enemy = Enemies(100 + item * 100, 100 + row * 70)
            Enemy_group.add(enemy)

create_Enemies()

#create player
spaceship = Spaceship(int(screen_width/ 2), screen_height - 100, 3)
spaceship_group.add(spaceship)

#score
score = Score()


class mainwindow(pygame.sprite.Sprite):
    def __init__(self):
        countdown=3
        last_count = pygame.time.get_ticks()
        last_Enemy_shot = pygame.time.get_ticks()
        game_over = 0#0 is no game over, 1 means player has won, -1 means player has lost
        #Game Loop
        run=True
        while run:
            clock.tick(fps)
            #background
            draw_bg()
            bg_fx.play()
            if countdown == 0:
                #create random alien bullets
                #record current time
                time_now = pygame.time.get_ticks()
                #shoot
                if time_now - last_Enemy_shot > Enemy_cooldown and len(Enemy_bullet_group) < 5 and len(Enemy_group) > 0:
                    attacking_Enemy = random.choice(Enemy_group.sprites())
                    Enemy_bullet = Enemy_Bullets(attacking_Enemy.rect.centerx, attacking_Enemy.rect.bottom)
                    Enemy_bullet_group.add(Enemy_bullet)
                    last_Enemy_shot = time_now
                #check if all the aliens have been killed
                if len(Enemy_group) == 0:
                    game_over = 1
                if game_over == 0:
                    #update spaceship
                    game_over = spaceship.update()
                    #update sprite groups
                    bullet_group.update()
                    Enemy_group.update()
                    Enemy_bullet_group.update()
                else:
                    if game_over == -1:
                        draw_text('GAME OVER! ', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
                        #draw restart Icon
                        draw_exibtn()
                        #draw Exit Icon
                        #draw_rsbtn()
                    if game_over == 1:
                        draw_text('YOU WIN!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
                        #draw restart Icon
                        draw_exibtn()
                        #draw Exit Icon
                        #draw_rsbtn()
            if countdown > 0:
                draw_text('GET READY!', font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
                draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
                count_timer = pygame.time.get_ticks()
                if count_timer - last_count > 1000:
                    countdown -= 1
                    last_count = count_timer
            #update explosion group
            explosion_group.update()
            #draw sprite groups
            spaceship_group.draw(screen)
            bullet_group.draw(screen)
            Enemy_group.draw(screen)
            Enemy_bullet_group.draw(screen)
            explosion_group.draw(screen)
            score.show_score(screen)
            #event handlers
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # press r to restart
                        #main()
                        run=False
                        break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # press Q to quit
                        run= False
                        break
            pygame.display.update()
        pygame.quit()
        

"""if __name__== "__main__":
    app= mainwindow()"""
    

def main():
    win=Tk()
    app=Login_window(win)
    win.mainloop()

class Login_window:
    def __init__(self,root):
        self.root=root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")

        #create background image
        self.bg=ImageTk.PhotoImage(file=r"Resources/darkbg.jpg")
        lbl_bg=Label(self.root,image=self.bg)
        lbl_bg.place(x=0,y=0,relwidth=1,relheight=1)

        #create left image
        self.bg1=ImageTk.PhotoImage(file=r"Resources/bg3.jpg")
        lbl_bg1=Label(self.root,image=self.bg1)
        lbl_bg1.place(x=420,y=80,width=470,height=460)
        
    
        #create Frame
        frame=Frame(self.root,bg="white")
        frame.place(x=120,y=80,width=360,height=460)

        img1=Image.open(r"Resources/user (2).png")
        img1=img1.resize((100,100),Image.Resampling.LANCZOS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        lblimg1=Label(image=self.photoimage1,bg="white",borderwidth=0)
        lblimg1.place(x=250,y=85,width=100,height=100)

        username=lbl=Label(frame,text="Username",font=("times new roman",15,"bold"),fg="black",bg="white")
        username.place(x=70,y=150)

        self.txtuser=ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txtuser.place(x=40,y=180,width=270)

        password=lbl=Label(frame,text="Password",font=("times new roman",15,"bold"),fg="black",bg="white")
        password.place(x=70,y=230)

        self.txtpass=ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txtpass.place(x=40,y=260,width=270)
        self.txtpass.config(show="*")

        img2=Image.open(r"Resources/user (2).png")
        img2=img2.resize((25,25),Image.Resampling.LANCZOS)
        self.photoimage2=ImageTk.PhotoImage(img2)
        lblimg2=Label(image=self.photoimage2,bg="white",borderwidth=0)
        lblimg2.place(x=165,y=230,width=25,height=25)

        img3=Image.open(r"Resources/pass.png")
        img3=img3.resize((25,25),Image.Resampling.LANCZOS)
        self.photoimage3=ImageTk.PhotoImage(img3)
        lblimg3=Label(image=self.photoimage3,bg="white",borderwidth=0)
        lblimg3.place(x=165,y=310,width=25,height=25)

        #Login button
        loginbtn=Button(frame,command=self.login,text="Login",font=("times new roman",15,"bold"),bd=3,relief=RIDGE,fg="White",bg="red",activeforeground="white",activebackground="red")
        loginbtn.place(x=110,y=315,width=120,height=35)

         #register button
        registerbtn=Button(frame,text="New user Register",command=self.register_window,font=("times new roman",12,"bold"),borderwidth=0,fg="black",bg="white",activeforeground="black",activebackground="white")
        registerbtn.place(x=15,y=370,width=160)

        #forgetpass button
        forgetbtn=Button(frame,text="Forget Password",command=self.forget_password_window,font=("times new roman",12,"bold"),borderwidth=0,fg="black",bg="white",activeforeground="black",activebackground="white")
        forgetbtn.place(x=10,y=400,width=160)

    #Register  button function
    def register_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)

    def login(self):
        if self.txtuser.get()=="" or  self.txtpass.get()=="":
            messagebox.showerror("Error","All fields Required",parent=self.root)
        else:
            conn=pymysql.connect(host="localhost",user="root",password="",db="space_invaders")
            my_cursor=conn.cursor()
            my_cursor.execute("select * from register where email=%s and password=%s",
                               (
                                  self.txtuser.get(),
                                  self.txtpass.get()
                                ))
            row=my_cursor.fetchone()
            #print(row)
            if row==None:
                messagebox.showerror("Error","Invalid Usernsme & password",parent=self.root)
            else:
                open_main=messagebox.askyesno("YesNo","Do you want to play",parent=self.root)
                self.root.destroy()
                if open_main>0:
                   #self.new_window=Toplevel(self.root)
                    app= mainwindow()
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()


    #reset password
    def reset_pass(self):
        if self.combo_security_Q.get()=="select":
            messagebox.showerror("Error,","Select security Question",parent=self.root2)
        elif self.txt_security.get()=="":
            messagebox.showerror("Error","Please enter the answer",parent=self.root2)
        elif  self.txt_newpass.get()=="":
             messagebox.showerror("Error","Please enter the New password",parent=self.root2)
        else:
            conn=pymysql.connect(host="localhost",user="root",password="",db="space_invaders")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s and securityQ=%s and securityA=%s")
            value=(self.txtuser.get(),self.combo_security_Q.get(),self.txt_security.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row==None:
                 messagebox.showerror("Error","Please enter the correct Answer",parent=self.root2)
            else:
                query=("update register set password=%s where email=%s")
                value=(self.txt_newpass.get(),self.txtuser.get())
                my_cursor.execute(query,value)

                conn.commit()
                conn.close()
                messagebox.showinfo("Info","Your password has been reset,please login new password",parent=self.root2)
                self.root2.destroy()
                
    
    #forget password window
    def forget_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please enter the email address to reset password",parent=self.root)
        else:
            conn=pymysql.connect(host="localhost",user="root",password="",db="space_invaders")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.txtuser.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            #print(row)
            if row==None:
                messagebox.showerror("Error","Please enter the valid user name",parent=self.root)
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forget password")
                self.root2.geometry("340x450+610+170")

                l=Label(self.root2,text="Forget password",font=("times new roman",20,"bold") , bg="white",fg="red")
                l.place(x=0,y=10,relwidth=1)
                
                #Security Questions
                security_Q=Label(self.root2,text="select security", font=("times new roman",15,"bold") , bg="white",fg="black")
                security_Q.place(x=50,y=80)
                #Combobox
                self.combo_security_Q=ttk.Combobox(self.root2,font=("times new roman",15,"bold") ,state="readonly")
                self.combo_security_Q["values"]=("select","Your birth place","Your friend name","Tour pet name")
                self.combo_security_Q.place(x=50,y=110,width=250)
                self.combo_security_Q.current(0)

                #security Answer
                security_A=Label(self.root2,text="security Answer", font=("times new roman",15,"bold") ,fg="black",bg="white")
                security_A.place(x=50,y=150)

                self.txt_security=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.txt_security.place(x=50,y=180,width=250)

                new_password=Label(self.root2,text="New password",font=("times new roman",15,"bold") ,fg="black",bg="white")
                new_password.place(x=50,y=220)

                self.txt_newpass=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.txt_newpass.place(x=50,y=250,width=250)
                
                btn=Button(self.root2,text="Reset",command=self.reset_pass,font=("times new roman",15,"bold"),fg="white",bg="green")
                btn.place(x=100,y=290)

  
class Register:
    def __init__(self,root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1600x900+0+0")

        #variables
        self.var_fname=StringVar()        
        self.var_lname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_securityQ=StringVar()
        self.var_securityA=StringVar()
        self.var_pass=StringVar()
        self.var_confirmpass=StringVar()
        #check button
        self.var_check=IntVar()

         #create background image
        self.bg=ImageTk.PhotoImage(file=r"Resources/darkbg.jpg")
        lbl_bg=Label(self.root,image=self.bg)
        lbl_bg.place(x=0,y=0,relwidth=1,relheight=1)

        #create left image
        self.bg1=ImageTk.PhotoImage(file=r"Resources/bg2.jpg")
        lbl_bg1=Label(self.root,image=self.bg1)
        lbl_bg1.place(x=50,y=100,width=470,height=550)

         #create Frame
        frame=Frame(self.root,bg="white")
        frame.place(x=520,y=100,width=800,height=550)

        #Register Label
        register_lbl=Label(frame,text="Register Here", font=("times new roman",25,"bold"), fg="darkgreen"  , bg="white")
        register_lbl.place(x=20,y=20)

        #Label & Entry
        #row 1
        #First name
        fname=Label(frame,text="First Name", font=("times new roman",15,"bold") , bg="white")
        fname.place(x=50,y=100)

        fname_entry=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15,"bold"))
        fname_entry.place(x=50,y=130,width=250)

         #Last name
        l_name=Label(frame,text="Last Name", font=("times new roman",15,"bold") , bg="white",fg="black")
        l_name.place(x=370,y=100)

        self.txt_lname=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15))
        self.txt_lname.place(x=370,y=130,width=250)

        #row 2
        #Contact no
        contact=Label(frame,text="Contact No", font=("times new roman",15,"bold") , bg="white",fg="black")
        contact.place(x=50,y=170)

        self.txt_contact=ttk.Entry(frame,textvariable=self.var_contact,font=("times new roman",15))
        self.txt_contact.place(x=50,y=200,width=250)

        #Email
        email=Label(frame,text="Email", font=("times new roman",15,"bold") , bg="white")
        email.place(x=370,y=170)

        self.txt_email=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",15))
        self.txt_email.place(x=370,y=200,width=250)

        #row 3
        #Security Questions
        security_Q=Label(frame,text="select security", font=("times new roman",15,"bold") , bg="white",fg="black")
        security_Q.place(x=50,y=240)

        #Combobox
        self.combo_security_Q=ttk.Combobox(frame,textvariable=self.var_securityQ,font=("times new roman",15,"bold") ,state="readonly")
        self.combo_security_Q["values"]=("select","Your birth place","Your friend name","Tour pet name")
        self.combo_security_Q.place(x=50,y=270,width=250)
        self.combo_security_Q.current(0)

        #security Answer
        security_A=Label(frame,text="security Answer", font=("times new roman",15,"bold") ,fg="black",bg="white")
        security_A.place(x=370,y=240)

        self.txt_security=ttk.Entry(frame,textvariable=self.var_securityA,font=("times new roman",15,"bold"))
        self.txt_security.place(x=370,y=270,width=250)

        #row 4
        #password
        paswd=Label(frame,text="Password", font=("times new roman",15,"bold") ,fg="black",bg="white")
        paswd.place(x=50,y=310)

        self.txt_paswd=ttk.Entry(frame,textvariable=self.var_pass,font=("times new roman",15))
        self.txt_paswd.place(x=50,y=340,width=250)

          # confirm password
        confirm_paswd=Label(frame,text=" Confirm Password", font=("times new roman",15,"bold") ,fg="black",bg="white")
        confirm_paswd.place(x=370,y=310)

        self.txt_confirm_paswd=ttk.Entry(frame,textvariable=self.var_confirmpass,font=("times new roman",15))
        self.txt_confirm_paswd.place(x=370,y=340,width=250)

        #check Button
        checkbtn= Checkbutton(frame,variable=self.var_check,text="I Agree the terms  and conditions",font=("times new roman",12,"bold"),onvalue=1,offvalue=0)
        checkbtn.place(x=50,y=380)

        #buttons
        img1=Image.open(r"Resources/register.png")
        img1=img1.resize((180,50),Image.Resampling.LANCZOS)
        self.photoimage=ImageTk.PhotoImage(img1)
        b1=Button(frame,image=self.photoimage,command=self.register_data,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold") ,fg="white",bg="white")
        b1.place(x=50,y=440,width=180)

         #buttons
        img2=Image.open(r"Resources/login.png")
        img2=img2.resize((180,50),Image.Resampling.LANCZOS)
        self.photoimage1=ImageTk.PhotoImage(img2)
        b2=Button(frame,image=self.photoimage1,command=self.return_login,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold") ,fg="white",bg="white")
        b2.place(x=370,y=440,width=180)

    #function Declaration
    def register_data(self):
        if self.var_fname.get()=="" or self.var_email.get()=="" or self.var_securityQ.get()=="select":
            messagebox.showerror("Error","All fields Required",parent=self.root)
        elif self.var_pass.get()!=self.var_confirmpass.get():
             messagebox.showerror("Error","Password and confirm password must be same",parent=self.root)
        elif self.var_check.get()==0:
             messagebox.showerror("Error","Please Agree our terms and conditions",parent=self.root)
        else:
            conn=pymysql.connect(host="localhost",user="root",password="",db="space_invaders")
            my_cursor=conn.cursor()
            Query=("select * from register where email=%s")
            value=(self.var_email.get(),)
            my_cursor.execute(Query,value)
            row=my_cursor.fetchone()
            if row!=None:
                messagebox.showerror("Error","User already exist, Please try another email",parent=self.root)
            else:
                my_cursor.execute("insert into register values(%s,%s,%s,%s,%s,%s,%s)",
                                       (
                                           self.var_fname.get(),
                                           self.var_lname.get(),
                                           self.var_contact.get(),
                                           self.var_email.get(),
                                           self.var_securityQ.get(),
                                           self.var_securityA.get(),
                                           self.var_pass.get()
                                        ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Register successfully",parent=self.root)

    def return_login(self):
        self.root.destroy()

        

if __name__== "__main__":
    main()
    
