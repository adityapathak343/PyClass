from tkinter import *
from tkinter.font import Font
from tkinter import filedialog
import emailhandler
import filehandler
import mysql.connector as mc


con = mc.connect(host='localhost', user='root', password='1234', database='')
cursor = con.cursor()
cursor.execute('Create database if not exists logininfo;')
cursor.execute('Use logininfo;')

folder_path = ''
files_to_send = ()
ContactInfo = ()
RegisterVar = False
login_status = False
ClientName = ''
username = ''
password = ''
file_count_var = 0

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
    register_n_font = Font(root=register_window, family='product sans', size=10)
    head_label = Label(register_window, text='Welcome!')
    head_label.grid(row=0)
    head_label.configure(font=register_hfont)
    user_label = Label(register_window, text='Username ')
    user_label.grid(row=2)
    username_entry = Entry(register_window)
    username_entry.grid(row=2, column=2)
    user_label.configure(font=register_n_font)
    pass_label = Label(register_window, text='Password ')
    pass_label.grid(row=3)
    password_entry = Entry(register_window)
    password_entry.grid(row=3, column=2)
    pass_label.configure(font=register_n_font)
    email_label = Label(register_window, text='Email ')
    email_label.grid(row=4)
    email_entry = Entry(register_window)
    email_entry.grid(row=4, column=2)
    email_label.configure(font=register_n_font)
    name_label = Label(register_window, text='Name ')
    name_label.grid(row=5)
    name_entry = Entry(register_window)
    name_entry.grid(row=5, column=2)
    name_label.configure(font=register_n_font)
    print('data submissions successful')
    submit_button = Button(register_window, text='Register')
    submit_button.bind('<Button-1>', lambda lam_var: register(register_window, username_entry, password_entry,
                                                              name_entry, email_entry))
    submit_button.grid(row=7, column=1)
    register_window.mainloop()


def register(window, eusername, epassword, ename, eemail, lam_var=None,):
    global RegisterVar
    print(lam_var)
    uid = eusername.get()
    pwd = epassword.get()
    name = ename.get()
    email = eemail.get()
    print('function called')
    register_command = 'insert into logininfo values({}, {}, {}, {});'.format('"' + uid + '"', '"' + pwd + '"', '"'
                                                                              + name + '"', '"' + email + '"')
    cursor.execute(register_command)
    con.commit()
    RegisterVar = True
    if RegisterVar:
        window.destroy()
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


def add_contact_to_list(event):
    add_window = Tk(screenName='AddWindow')
    add_hfont = Font(root=add_window, family='product sans bold', size=18)
    add_n_font = Font(root=add_window, family='product sans', size=10)
    head_label = Label(add_window, text='Add contact')
    head_label.grid(row=0)
    head_label.configure(font=add_hfont)
    contact_name_label = Label(add_window, text='Name ')
    contact_name_label.grid(row=3)
    contact_name_entry = Entry(add_window)
    contact_name_entry.grid(row=3, column=2)
    contact_name_label.configure(font=add_n_font)
    contact_email_label = Label(add_window, text='Email ')
    contact_email_label.grid(row=4)
    contact_email_entry = Entry(add_window)
    contact_email_entry.grid(row=4, column=2)
    contact_email_label.configure(font=add_n_font)
    submit_button = Button(add_window, text='Register')
    submit_button.bind('<Button-1>', lambda lam_var: add_contact(add_window, contact_name_entry, contact_email_entry))
    submit_button.grid(row=7, column=1)
    add_window.mainloop()


def add_contact(window, e_name, e_email):
    global username
    name = e_name.get()
    email = e_email.get()
    command = 'insert into ' + username + '_contact_info values({}, {})'.format('"' + name + '"', '"' + email + '"')
    cursor.execute(command)
    con2.commit()
    window.destroy()


def send(event):
    root.destroy()
    contact_list = []
    recipient_tuple = ()
    send_window = Tk(screenName='SendWindow')
    send_hfont = Font(root=send_window, family='product sans bold', size=18)
    send_n_font = Font(root=send_window, family='product sans', size=10)
    send_head_label = Label(send_window, text='Choose your audience:')
    send_head_label.grid(row=1)
    send_head_label.configure(font=send_hfont)
    send_info_label = Label(send_window, text='Your message will be received only by the following recipients')
    send_info_label.grid(row=2)
    send_info_label.configure(font=send_n_font)
    cursor.execute('select email from ' + username + '_contact_info;')
    contact_data = cursor.fetchall()
    check_no = 1
    current_line = 4
    var_count = 0
    for tup in contact_data:
        contact_list.append(tup[0])

    for email in contact_list:
        exec('checkbox' + str(check_no) + ' = Checkbutton(send_window, cursor="dot", text=" ' + email + ' ")')
        exec('checkbox' + str(check_no) + '.grid(row=' + str(current_line) + ')')
        exec('checkbox' + str(check_no) + '.configure(font=send_n_font)')
        exec('recipient_tuple += (checkbox' + str(check_no) + ',)')
        check_no += 1
        current_line += 1
        var_count += 1

    submit_button = Button(send_window, text='Select Files')
    submit_button.bind('<Button-1>', lambda lam_var: get_recipients(send_window, recipient_tuple))
    submit_button.grid(row=7, column=1)
    send_window.mainloop()


def get_recipients(window, recipients):
    window.destroy()
    receivers = ()
    for checkbutton in recipients:
        if checkbutton.variable == 1:
            receivers += (checkbutton.text,)
    get_files(receivers)


def get_files(recipients):
    global file_count_var
    global folder_path
    global files_to_send
    file_prompt_window = Tk(screenName='file_prompt_window')
    file_prompt_hfont = Font(root=file_prompt_window, family='product sans bold', size=18)
    file_prompt_n_font = Font(root=file_prompt_window, family='product sans', size=10)
    file_prompt_head_label = Label(file_prompt_window, text='Choose your files:')
    file_prompt_head_label.grid(row=0)
    file_prompt_head_label.configure(font=file_prompt_hfont)
    submit_button = Button(file_prompt_window, text='Select Files')
    submit_button.grid(row=2)
    submit_button.bind('<Button-1>', lambda lam_var: open_file_window())
    submit_button.configure(font=file_prompt_n_font)
    counter_label = Label(file_prompt_window, textvariable='(' + str(file_count_var) + ') files selected')
    counter_label.grid(row=4)
    counter_label.configure(font=file_prompt_n_font)
    proceed_button = Button(file_prompt_window, text='Proceed')
    proceed_button.grid(row=2, column=2)
    proceed_button.bind('<Button-1>', lambda lam_var: send_mail(file_prompt_window, recipients, files_to_send))
    proceed_button.configure(font=file_prompt_n_font)
    file_prompt_window.mainloop()


def open_file_window():
    global file_count_var
    global folder_path
    global files_to_send
    filename = filedialog.askopenfilename(initialdir="/", title="Select file")
    files_to_send += (filename,)
    if filename != '':
        file_count_var += 1


def send_mail(window, recipients, files):
    global ClientName
    print(recipients)
    files = list(files)
    emailhandler.sendmail(ClientName, recipients, files)
    window.destroy()


def view(event):
    root.destroy()
    view_window = Tk(screenName='ViewWindow')
    view_hfont = Font(root=view_window, family='product sans bold', size=18)
    view_n_font = Font(root=view_window, family='product sans', size=10)
    view_head_label = Label(view_window, text="Here's your stuff!")
    view_head_label.grid(row=1, column=0)
    view_head_label.configure(font=view_hfont)
    view_info_label = Label(view_window, text='Files you have received through the PyClass interface')
    view_info_label.grid(row=2, column=1)
    view_info_label.configure(font=view_n_font)
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
con2 = mc.connect(host='localhost', user='root', password='1234', database='')
cursor = con2.cursor()
cursor.execute('Create database if not exists ' + username + '_contact_info;')
cursor.execute('Use '+username+'_contact_info;')
cursor.execute('create table if not exists '
               + username + '_contact_info (name varchar(30) not null, email varchar(80) primary key);')
WelcomeLabel = Label(root, text='Welcome Back ' + ClientName + '!')
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
AddContactButton = Button(root, text='Add Contact')
AddContactButton.pack()
AddContactButton.bind('<Button-1>', add_contact_to_list)
AddContactButton.configure(font=NormalFont)
root.mainloop()
