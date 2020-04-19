from tkinter import *
import tkinter.messagebox as tkmsg
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk, Image
import mysql.connector 
import itertools

myconnector = mysql.connector.connect(host='localhost', user='root', passwd="", database="fathom")
mycursor = myconnector.cursor()

class fathomapp(Tk):
    def __init__(self):
        super().__init__()
        self._frame = None
        self.switch_frame(signup)
        self.geometry("700x500")
        self.title("Fathom")
        print(self._frame)  #for debugging

        def donothing(self):
            pass

        menubar = Menu(self)
        usermenu = Menu(menubar, tearoff=0)
        usermenu.add_command(label="homepage", command= lambda : self.switch_frame(homepage))
        usermenu.add_command(label="request", command= lambda : self.switch_frame(request))
        usermenu.add_command(label="profile", command= lambda : self.switch_frame(profile))
        usermenu.add_separator()
        usermenu.add_command(label="signout", command= lambda : self.switch_frame(signup))
        usermenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="user", menu=usermenu)

        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=donothing)
        helpmenu.add_command(label="About...", command=donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)
        
        self.user_entry = StringVar() 
        self.pass_entry = StringVar()
        self.target = StringVar()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        print(new_frame)  #for debugging
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0,column=0)


class signup(Frame):
    def __init__(self, master):
        Frame.__init__(self, master,bg='lightblue')
        Frame.configure(self)
        
        user_entry = StringVar() 
        pass_entry = StringVar()
        Label(self, text='    ',bg="lightblue").grid(row=0,column=0) #for decoration
        Label(self, text='    ',bg="lightblue").grid(row=2,column=0) 
        Label(self, text='    ',bg="lightblue").grid(row=4,column=0)
        Label(self, text='    ',bg="lightblue").grid(row=1,column=0)
        Label(self, text='    ',bg="lightblue").grid(row=3,column=0)
        Label(self, text='    ',bg="lightblue").grid(row=1,column=4)
        Label(self, text='    ',bg="lightblue").grid(row=3,column=4)
        Label(self, text='    ',bg="lightblue").grid(row=6,column=0)
        Label(self, text='signup', font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=3, padx=50).grid(row=0,column=2)
        Label(self, text='username',font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=3, relief=RIDGE).grid(row=1,column=1)
        Label(self, text='password',font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=3, relief=RIDGE).grid(row=3,column=1)
        Entry(self, textvariable=user_entry, bg='pink').grid(row=1,column=3)
        Entry(self, textvariable=pass_entry, bg='pink').grid(row=3,column=3)
        Button(self, text='submit', font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=4, relief=GROOVE, command= lambda : self.check_existing_user(user_entry.get(), pass_entry.get())).grid(row=5,column=2)
        Button(self, text='already a user', font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=4, relief=GROOVE, command= lambda: master.switch_frame(Login), padx=10).grid(row=7,column=2)

    def check_existing_user(self, username, password):
        mycursor.execute(f" select * from accounts where username = \'{username}\' ")
        result = mycursor.fetchone()
        if result is not None :
            tkmsg.showwarning(title='signup error', message='the username already exist')
        else:
            mycursor.execute("INSERT INTO accounts(username,user_password) VALUES (%s,%s)", (username,password) )
            myconnector.commit()
            self.master.switch_frame(Login)

class Login(Frame):
    def __init__(self, master):
        Frame.__init__(self, master,bg='lightblue')
        Frame.configure(self)
        user_entry = StringVar() 
        pass_entry = StringVar()
        Label(self, text='login',font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=3).grid(row=0,column=2) #for decoration
        Label(self, text='    ',bg="lightblue").grid(row=0,column=0) #for decoration
        Label(self, text='    ',bg="lightblue").grid(row=2,column=0)
        Label(self, text='    ',bg="lightblue").grid(row=1,column=0)
        Label(self, text='    ',bg="lightblue").grid(row=3,column=0)
        Label(self, text='    ',bg="lightblue").grid(row=1,column=4)
        Label(self, text='    ',bg="lightblue").grid(row=3,column=4)
        Label(self, text='    ',bg="lightblue").grid(row=4,column=0)
        Label(self, text='    ',bg="lightblue").grid(row=6,column=0)
        Label(self, text='username',font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=5, relief=RIDGE).grid(row=1,column=1)
        Label(self, text='password',font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=5, relief=RIDGE).grid(row=3,column=1)
        Entry(self, textvariable=user_entry, bg='pink').grid(row=1,column=3)
        Entry(self, textvariable=pass_entry,bg='pink').grid(row=3,column=3)
        Button(self, text='submit', font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=5, relief=GROOVE, command= lambda : self.login(user_entry.get(), pass_entry.get())).grid(row=5,column=2)

    def login(self, username, password):
        mycursor.execute(f" select * from accounts where username = \'{username}\' and user_password = \'{password}' ")
        result = mycursor.fetchone()
        if result is None :
            tkmsg.showwarning(title='login error', message="error in username or password")
        else:
            self.master.user_entry = username
            print(self.master.user_entry)   #for debugging
            self.master.switch_frame(profile)


class profile(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg='lightblue')
        Frame.configure(self)
        username = self.master.user_entry

        name = StringVar()
        name.set(username)
        Label(self, text="name", font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=5, relief=RIDGE).grid(row=0, column=0, sticky = W)
        Entry(self, textvariable=name, bg='pink').grid(row=0, column=1, sticky = W)
        
        mycursor.execute(fr"select img from user_profile where username = '{username}' ")
        result = mycursor.fetchone()

        img_path = StringVar()
        
        Label(self, text='enter new image path', font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=5, relief=RIDGE).grid(row=2, column=0)
        Entry(self, textvariable=img_path, bg='pink', width=40).grid(row=2, column=1, pady=7, columnspan=2)      
        print(result)   #for debugging
        if result is None:
            img = Image.open(r'C:\Users\patkar\Pictures\blank.png')
            img_path.set(r'C:\Users\patkar\Pictures\blank.png')
        else:
            img_path.set(result[0])
            img = Image.open(fr'{result[0]}')
        img = img.resize((150,150), Image.ANTIALIAS)
        mylabel = ImageTk.PhotoImage(img)
        ImageLabel = Label(self, image=mylabel)
        ImageLabel.image = mylabel
        ImageLabel.grid(row=1, column=5)

        bio = StringVar()
        bio.set("just joined tinder")
        Label(self, text="bio", font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=5, relief=RIDGE).grid(row=4, column=0)
        Entry(self, textvariable=bio, bg='pink').grid(row=4, column=1, pady=7)

        sex = StringVar()
        if username is None:
            sex.set('m')
        else:
            mycursor.execute(f"select sex from user_profile where username = \'{username}\' ")
            sex_val = mycursor.fetchone()
            sex.set(sex_val)
        Label(self, text="sex").grid(row=5, column=0)
        Radiobutton(self, text="male",bg="lightblue", variable=sex, value='m').grid(row=5, column=1)
        Radiobutton(self, text="female",bg="lightblue", variable=sex, value='f').grid(row=5, column=2, pady=7)

        interest = StringVar()
        if username is None:           
            interest.set('straight')
        else:
            mycursor.execute(f"select interest from user_profile where username = \'{username}\' ")
            interest_val = mycursor.fetchone()
            interest.set(interest_val)
        Label(self, text='interest',font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=5, relief=RIDGE).grid(row=5, column=0)
        Radiobutton(self, text="straight",bg="lightblue", variable=interest, value='straight').grid(row=6, column=1)
        Radiobutton(self, text="bi",bg="lightblue", variable=interest, value='bi').grid(row=6, column=2)

        Button(self, text='ok',font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=5, relief=GROOVE, command= lambda : self.set_bio(username, img_path.get(), sex.get(), interest.get(), bio.get()) ).grid(row=7, column=1)
        Button(self, text='home page', font=("Calibri",13,"italic"), bg="crimson", fg="pink", bd=5, relief=GROOVE,command= lambda : self.master.switch_frame(homepage) ).grid(row=8, column=4)

    def set_bio(self, username, img_path, sex, interest, bio):
        mycursor.execute(f" select * from user_profile where username = \'{username}\' ")
        present = mycursor.fetchone()
        if present is None :
            mycursor.execute("insert into user_profile(username,img,sex,interest,bio) values(%s, %s ,%s ,%s ,%s)",(username,img_path,sex,interest,bio))
            myconnector.commit()
        else:
            mycursor.execute(f" update user_profile set img = \'{img_path}\' ,bio = \'{bio}\' where username = \'{username}\' ")
            myconnector.commit()


class homepage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master,bg='lightblue')
        Frame.configure(self)

        user = self.master.user_entry
        mycursor.execute(f" select interest from user_profile where username = \'{user}\' ")
        user_interest = mycursor.fetchone()
        if user_interest[0] == 'straight' :
            mycursor.execute(f" select sex from user_profile where username = \'{user}\' ")
            user_sex = mycursor.fetchone()
            mycursor.execute(f" select img from user_profile where sex != \'{user_sex[0]}\' ")
            img = mycursor.fetchall()
            imgs = [path[0] for path in img] 
            self.create_slide_show(imgs)
        else:
            mycursor.execute(f" select img from user_profile where username != \'{user}\' ")
            img = mycursor.fetchall()
            imgs = [path[0] for path in img] 
            self.create_slide_show(imgs)

    def create_slide_show(self, img1, i=0):
        img = Image.open(f'{img1[i]}')
        img = img.resize((200,200), Image.ANTIALIAS)
        mylabel = ImageTk.PhotoImage(img)
        ImageLabel = Label(self, image=mylabel, bg='lightblue')
        ImageLabel.image = mylabel
        ImageLabel.grid(row=1, column=5)
        print(img1)   #for debugging

        new_img = img1[i]
        next_img = new_img.replace('\\', '\\\\')
        print(next_img)     #for debugging
        mycursor.execute(fr" select username from user_profile where img = '{next_img}' ")
        name = mycursor.fetchone()
        print(name)     #for debugging
        Label(self, text=f"{name[0]}", bg='lightblue').grid(row=3,column=5, padx=5, pady=5)

        mycursor.execute(fr" select bio from user_profile where img = '{next_img}' ")
        bio = mycursor.fetchone()
        Label(self, text=f"{bio[0]}", bg='lightblue').grid(row=4,column=5)
        Button(self, text='next', command= lambda : self.create_slide_show(img1, i=i+1)).grid(row=5, column=3)
        Button(self, text='back', command= lambda : self.create_slide_show(img1, i=i-1)).grid(row=5, column=1)
        Button(self, text='send request', command= lambda : self.send_request(name)).grid(row=5, column=2)
    
    def send_request(self, target):
        username = self.master.user_entry
        print(username, target)     #for debugging
        mycursor.execute(" insert into request(username, target, sent_request, accept) values(%s, %s, %s, %s)",(username, target[0], 1, None))
        myconnector.commit()
        tkmsg.showinfo(title='request', message='request sent')

class request(Frame):
    def __init__(self, master):
        Frame.__init__(self, master,bg='lightblue')
        Frame.configure(self)
        username = self.master.user_entry
        mycursor.execute(f" select * from request where username = \'{username}\' or target = \'{username}\' ")
        result = mycursor.fetchall()
        print(result)       #for debugging
        if result is not None:
            for (match,i) in zip( result,range(len(result)) ):
                if match[0]==username:
                    Label(self, text=f"{match[1]}", bg='lightblue').grid(row=i, column=0)
                    print(match[1])     #for debugging

                    if match[2]==1 and match[3]==1:
                        Label(self, text="accepted", bg='lightblue').grid(row=i, column=1)

                    elif match[2]==1 and match[3] is None:
                        Label(self, text="pending", bg='lightblue').grid(row=i, column=1)

                elif match[1]==username and match[2]==1 and match[3] is None:
                    Label(self, text=f"{match[0]}", bg='lightblue').grid(row=i, column=0)
                    print(match[1])     #for debugging
                    Label(self, text="sent to you", bg='lightblue').grid(row=i, column=1)
                    Button(self, text="accept request", command= lambda : self.accept(match)).grid(row=i,column=2)

                elif match[1]==username and match[2]==1 and match[3]==1:
                    Label(self, text=f"{match[0]}", bg='lightblue').grid(row=i, column=0)

        chat=StringVar()
        chat.set('enter name')
        Entry(self, textvariable=chat).grid(row=100,column=1)
        Button(self, text='open chat box', command= lambda : self.open_chatbox(chat.get())).grid(row=100,column=2)

    def accept(self, match):
        username = match[0]
        target = match[1]
        print(username,target)      #for debugging
        mycursor.execute(f" update request set accept = 1 where username=\'{username}\' and target=\'{target}\' ")
        myconnector.commit()
        tkmsg.showinfo(title=request, message="request accepted")

    def open_chatbox(self, chat):
        self.master.target = chat
        self.master.switch_frame(messages)


class messages(Frame):
    def __init__(self, master):
        Frame.__init__(self, master,bg='lightblue')
        Frame.configure(self)
        user = self.master.user_entry
        receiver = self.master.target
        print(receiver)     #for debugging
        mycursor.execute(f" select * from chatbox where ( (sender = \'{user}\' and receiver = \'{receiver}\' ) or (sender = \'{receiver}\' and receiver = \'{user}\' ))")
        result = mycursor.fetchall()
        print(result)       #for debugging
        if result is not None:
            for (message,i) in zip(result, range(len(result)) ):
                Label(self, text=f"{message[1]} :   ", fg="green", bg='lightblue').grid(row=i, column=0, pady=3)
                Label(self, text=f"{message[3]} ", bg='lightblue').grid(row=i, column=1, pady=3)
        st = ScrolledText(self, width=50, height=2)
        st.grid(row=1000, column=0)
        Button(self, text="send", command= lambda : self.send(user, receiver, st.get(0.0, END))).grid(row=1000, column=1)


    def send(self, user, receiver, msg):
        if len(msg)==1 :
            pass
        else:
            mycursor.execute(" insert into chatbox(sender, receiver, message) values(%s,%s,%s)",(user, receiver, msg))
            myconnector.commit()


if __name__ == "__main__":
    window = fathomapp()
    window.configure(bg='lightblue')
    window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
    window.mainloop()
