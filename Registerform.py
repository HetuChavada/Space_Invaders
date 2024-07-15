from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk #pip install pillow
from tkinter import messagebox
import pymysql

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
        self.bg1=ImageTk.PhotoImage(file=r"Resources/bg3.jpg")
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

        self.txt_security=ttk.Entry(frame,textvariable=self.var_securityA,font=("times new roman",15))
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
        b2=Button(frame,image=self.photoimage1,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold") ,fg="white",bg="white")
        b2.place(x=370,y=440,width=180)

    #function Declaration
    def register_data(self):
        if self.var_fname.get()=="" or self.var_email.get()=="" or self.var_securityQ.get()=="select":
            messagebox.showerror("Error","All fields Required")
        elif self.var_pass.get()!=self.var_confirmpass.get():
             messagebox.showerror("Error","Password and confirm password must be same")
        elif self.var_check.get()==0:
             messagebox.showerror("Error","Please Agree our terms and conditions")
        else:
            conn=pymysql.connect(host="localhost",user="root",password="",db="space_invaders")
            my_cursor=conn.cursor()
            Query=("select * from register where email=%s")
            value=(self.var_email.get(),)
            my_cursor.execute(Query,value)
            row=my_cursor.fetchone()
            if row!=None:
                messagebox.showerror("Error","User already exist, Please try another email")
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
            messagebox.showinfo("Success","Register successfully")
       



        

if __name__== "__main__":
    root=Tk()
    app=Register(root)
    root.mainloop()
    
