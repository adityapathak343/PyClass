from tkinter import *
from tkinter.font import Font
import emailhandler
import filehandler
import mysql.connector as mc


con = mc.connect(host='localhost', user='root', password='1234', database='logininfo')
cursor = con.cursor()

RegisterVar = False
login_status = False
ClientName = ''
username = ''
password = ''

if con.is_connected():
    pass
else:
    print('Error Establishing Connection!')

emailhandler.__init__()
filehandler.__init__()


def getinfo(event):
    global RegisterVar
    register_window = Tk(screenName='RegisterWindow')
    register_hfont = Font(root=register_window, family='product sans bold', size=18)
    register_nfont = Font(root=register_window, family='product sans', size=10)
    head_label = Label(register_window, text='Welcome!')
    head_label.grid(row=0)
    head_label.configure(font=register_hfont)
    user_label = Label(register_window, text='Username ')
    user_label.grid(row=2)
    username_entry = Entry(register_window)
    username_entry.grid(row=2, column=2)
    user_label.configure(font=register_nfont)
    pass_label = Label(register_window, text='Password ')
    pass_label.grid(row=3)
    password_entry = Entry(register_window)
    password_entry.grid(row=3, column=2)
    pass_label.configure(font=register_nfont)
    email_label = Label(register_window, text='Email ')
    email_label.grid(row=4)
    email_entry = Entry(register_window)
    email_entry.grid(row=4, column=2)
    email_label.configure(font=register_nfont)
    name_label = Label(register_window, text='Name ')
    name_label.grid(row=5)
    name_entry = Entry(register_window)
    name_entry.grid(row=5, column=2)
    name_label.configure(font=register_nfont)
    print('data submissions successful')
    submit_button = Button(register_window, text='Register')
    submit_button.bind('<Button-1>', lambda eff: register(username_entry, password_entry, name_entry, email_entry, eff))
    submit_button.grid(row=7, column=1)
    if RegisterVar:
        register_window.destroy()
    else:
        pass
    register_window.mainloop()


def register(eusername, epassword, ename, eemail, eff=None,):
    global RegisterVar
    uid = eusername.get()
    pwd = epassword.get()
    name = ename.get()
    email = eemail.get()
    print('function called')
    register_command = 'insert into logininfo values({}, {}, {}, {});'.format('"'+uid+'"', '"'+pwd+'"', '"'+name+'"', '"'+email+'"')
    cursor.execute(register_command)
    con.commit()
    RegisterVar = True
    print('Registration Successful!')
    return True


def login(uid, pwd):
    global ClientName
    try:
        login_command = '''
        select pwd, name from logininfo
        where uid = "'''+uid+'''"
        ;
        '''
        cursor.execute(login_command)
        data = cursor.fetchone()
        correct_password = data[0]
        ClientName = data[1]
        if correct_password == pwd:
           return True
        else:
           return False
    except TypeError:
        print('Incorrect UserId')
        return False


def login_message(event):
    global login_status
    global username
    global password
    username = usernameEntry.get()
    password = passwordEntry.get()
    if login(username, password):
        login_status = True
        root.destroy()
    else:
        return False


def send(event):
    root.destroy()
    send_window = Tk(screenName='SendWindow')
    send_hfont = Font(root=send_window, family='product sans bold', size=18)
    send_nfont = Font(root=send_window, family='product sans', size=10)
    send_head_label = Label(send_window, text='Choose your audience:')
    send_head_label.grid(row=1, column=1)
    send_head_label.configure(font=send_hfont)
    send_info_label = Label(send_window, text='Your message will be received only by the following recipients')
    send_info_label.grid(row=2, column=1)
    send_info_label.configure(font=send_nfont)
    send_window.mainloop()

def view(event):
    root.destroy()
    view_window = Tk(screenName='ViewWindow')
    view_hfont = Font(root=view_window, family='product sans bold', size=18)
    view_nfont = Font(root=view_window, family='product sans', size=10)
    view_head_label = Label(view_window, text="Here's your stuff!")
    view_head_label.grid(row=1, column=1)
    view_head_label.configure(font=view_hfont)
    view_info_label = Label(view_window, text='Files you have received through the PyClass interface')
    view_info_label.grid(row=2, column=1)
    view_info_label.configure(font=view_nfont)
    view_window.mainloop()


# ----Login Section---- #
root = Tk(screenName='LoginScreen')
HeadingFont = Font(root=root, family='product sans bold', size=18)
NormalFont = Font(root=root, family='product sans', size=10)
HeadLabel = Label(root, text='Login')
HeadLabel.grid(row=0)
HeadLabel.configure(font=HeadingFont)
UserLabel = Label(root, text='Username ')
UserLabel.grid(row=3)
usernameEntry = Entry(root)
usernameEntry.grid(row=3, column=1)
UserLabel.configure(font=NormalFont)
PassLabel = Label(root, text='Password ')
PassLabel.grid(row=4)
passwordEntry = Entry(root)
passwordEntry.grid(row=4, column=1)
PassLabel.configure(font=NormalFont)
SubmitButton = Button(root, text='Log In')
SubmitButton.bind('<Button-1>', login_message)
SubmitButton.grid(row=6, column=1)
SubmitButton.configure(font=NormalFont)
RegisterButton = Button(root, text='Register')
RegisterButton.bind('<Button-1>', getinfo)
RegisterButton.grid(row=6, column=0)
RegisterButton.configure(font=NormalFont)
root.mainloop()
cursor.close()
if login_status:
    pass
else:
    Label(root, text='Login Failed').grid(row=5, column=2)
    raise SystemExit
# ----End of Login Section---- #

# ----Main Stuff---- #

root = Tk(screenName='interface')
HeadingFont = Font(root=root, family='product sans bold', size=18)
NormalFont = Font(root=root, family='product sans', size=10)
con2 = mc.connect(host='localhost', user='root', password='1234', database='contact_info')
WelcomeLabel = Label(root, text='Welcome Back '+ClientName+'!')
WelcomeLabel.pack()
WelcomeLabel.configure(font=HeadingFont)
SendButton = Button(root, text='Send Files')
SendButton.pack()
SendButton.bind('<Button-1>', send)
SendButton.configure(font=NormalFont)
ViewButton = Button(root, text='View Files')
ViewButton.pack()
ViewButton.bind('<Button-1>', view)
ViewButton.configure(font=NormalFont)
root.mainloop()