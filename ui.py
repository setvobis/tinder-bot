import json
from tkinter import *
from tkinter import messagebox
from tinder_swindler import TinderSwindler
from cooldown_manager import CooldownManager


def enable_button(button):
    """Enables button"""
    if button["state"] == "disabled":
        button["state"] = "normal"


def disable_button(button):
    """Disables button"""
    if button["state"] == "normal":
        button["state"] = "disabled"


class UsrInt:
    def __init__(self):
        self.cdm = CooldownManager()
        self.driver = None
        self.user_email = None
        self.user_password = None

        # base
        self.window = Tk()
        self.window.title("Tinder Swindler")
        self.window.config(padx=50, pady=50)
        self.window.resizable(width=False, height=False)

        # decorating window
        self.canvas = Canvas()
        self.canvas.config(width=200, height=200)
        self.lock_image = PhotoImage(file="flame.png")
        self.canvas.create_image(100, 100, image=self.lock_image)
        self.canvas.grid(column=0, row=0, columnspan=3)

        # login frame
        self.login_frame = LabelFrame(self.window, text="Facebook details", padx=10, pady=10)
        self.login_frame.grid(column=0, row=1)
        self.email_label = Label(self.login_frame, text="Email:")
        self.email_label.grid(column=0, row=1, sticky="E")
        self.email_entry = Entry(self.login_frame)
        self.email_entry.grid(column=1, row=1, columnspan=2)
        self.email_entry.focus()
        self.password_label = Label(self.login_frame, text="Password:")
        self.password_label.grid(column=0, row=2, sticky="E")
        self.password_entry = Entry(self.login_frame, show="*")
        self.password_entry.grid(column=1, row=2, columnspan=2)

        # button frame
        self.button_frame = LabelFrame(self.window, padx=21, pady=10)
        self.button_frame.grid(column=0, row=2)
        self.submit_button = Button(self.button_frame, text="Login", command=self.get_login_details)
        self.submit_button.grid(column=0, row=0, columnspan=2, padx=6, pady=5, sticky="NESW")
        self.begin_button = Button(self.button_frame, text="Begin", command=self.begin_method, state="disabled")
        self.begin_button.grid(column=0, row=1, padx=5, pady=5, sticky="NESW")
        self.cooldown_button = Button(self.button_frame, text="Check cooldown", command=self.cooldown_method,
                                      state="disabled")
        self.cooldown_button.grid(column=1, row=1, padx=5, pady=5, sticky="NESW")

        self.window.mainloop()

    def get_login_details(self):
        """Gets details provided by user, that are later used to log into Tinder.
        Does not check if details are correct."""
        if len(self.email_entry.get().strip()) == 0 or len(self.password_entry.get().strip()) == 0:
            messagebox.showwarning(message="You forgot to type email or password")
        else:
            self.user_email = self.email_entry.get().strip()
            self.user_password = self.password_entry.get().strip()
            enable_button(self.begin_button)
            enable_button(self.cooldown_button)

    def begin_method(self):
        """Starts Selenium driver's part. After its part is done, updates local database."""
        disable_button(self.begin_button)
        self.driver = TinderSwindler()
        self.driver.login(email=self.user_email, password=self.user_password)
        self.driver.swipe()
        cd_data = {self.user_email: {"date": self.driver.end_time}}
        try:
            with open('cooldown.json', mode='r') as cd_file:
                # read old data
                data = json.load(cd_file)
        except FileNotFoundError:
            with open('cooldown.json', mode='w') as cd_file:
                json.dump(cd_data, cd_file, indent=4, default=str)
        else:
            # updating
            data.update(cd_data)
            with open('cooldown.json', mode='w') as cd_file:
                # saving updated
                json.dump(data, cd_file, indent=4, default=str)

    def cooldown_method(self):
        """Checks if currently logged user has likes to spend"""
        try:
            if self.cdm.check(self.user_email):
                messagebox.showinfo(message='You can swipe')
            else:
                if self.cdm.no_cd is not None:
                    messagebox.showerror(message=f'You cannot swipe until {self.cdm.no_cd}')
                else:
                    messagebox.showwarning(message='There was no successful app runs with this email or it is '
                                                   'your first app launch, I do not know.')
        except KeyError:
            messagebox.showinfo(message='No data associated with this email address')
