# import modules

from tkinter import *
from services.login import LoginService
from services.dashboard import DashboardService
from services.public_page import PublicPage
import const

def show_public_page():
    public_page = PublicPage(main_screen)
    public_page.show_public_page()

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("600x300")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
    global username_verify
    global password_verify
    username_verify = StringVar()
    password_verify = StringVar()
    global username_login_entry
    global password_login_entry
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, bg="#ADD8E6", command=login_verify).pack()

# Implementing event on login button

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    login_service = LoginService()

    if login_service.login(username1, password1):
        login_sucess("logged in successfully")
        const.CURRENT_USER = username1
        dashboard_obj = DashboardService(main_screen)
        dashboard_obj.show_dashboard(username1, password1)
    else:
        login_failure("Username or password incorrect")

def login_sucess(message):
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text=message).pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()

def login_failure(message):
    global login_failure_screen
    login_failure_screen = Toplevel(login_screen)
    login_failure_screen.title("Success")
    login_failure_screen.geometry("500x300")
    Label(login_failure_screen, text=message).pack()
    Button(login_failure_screen, text="OK", command=delete_login_failure).pack()



def delete_login_success():
    login_success_screen.destroy()
    login_screen.destroy()



def delete_login_failure():
    login_failure_screen.destroy()


def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("1200x800")
    main_screen.title("Burdells App")
    Label(text="Welcome to Burdells Company", bg="white", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", bg="#ADD8E6", command=login).pack()
    Label(text="").pack()
    Button(text="List Vehicles", height="2", width="30", bg="#ADD8E6", command=show_public_page).pack()
    main_screen.mainloop()


main_account_screen()