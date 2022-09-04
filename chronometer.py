from tkinter import Tk, Label, Button, Frame, Text, messagebox


class Chrono:

    def __init__(self, is_pause=False):
        self.seconds = 0
        self.process = None
        self.is_pause = is_pause
        self.max_time = 25 * 60


class Gui:

    def __init__(self, title):
        self.root = Tk()
        self.root.title(title)
        self.root.resizable(0, 0)
        self.root.config(bd=30)
        self.time = Label(self.root, fg='black', width=20, font=("", "18"))
        self.time.pack()
        self.input_txt = None
        self.btnValidate = None

        # Windows should stay in foreground
        self.root.call('wm', 'attributes', '.', '-topmost', '1')

    def create_main_window(self):
        self.time['text'] = "00:00"
        frame = Frame(self.root)
        _btnStart = Button(frame, fg='green', text='Commencer', command=start_chronometer).grid(row=1,
                                                                                                column=1,
                                                                                                padx=2,
                                                                                                pady=5)
        _btnStop = Button(frame, fg='red', text='Arrêter', command=stop_chronometer).grid(row=1,
                                                                                          column=2,
                                                                                          padx=2,
                                                                                          pady=5)
        _btnResume = Button(frame, fg='blue', text='Réinitialiser', command=resume_chronometer).grid(row=1,
                                                                                                     column=3,
                                                                                                     padx=2,
                                                                                                     pady=5)
        _btnInput = Button(frame, fg='blue', text='Réglage', command=click_time_settings_window).grid(row=2,
                                                                                                      column=2,
                                                                                                      padx=2,
                                                                                                      pady=5)
        frame.pack()

    def create_time_settings_window(self):
        frame = Frame(self.root)
        self.input_txt = Text(self.root,
                              height=1,
                              width=5)
        self.btnValidate = Button(frame, fg='green', text='Ok', command=get_value).grid(row=1,
                                                                                        column=2,
                                                                                        padx=2,
                                                                                        pady=5)
        self.input_txt.pack()
        frame.pack()

    def main_loop(self):
        self.root.mainloop()


def display_time_in_mm_ss(time_in_seconds, max_time):
    time_to_display = max_time - time_in_seconds
    return '{:02d}:{:02d}'.format(time_to_display // 60, time_to_display % 60)


def start_chronometer():
    try:
        stop_chronometer()
    except:
        pass
    my_chronometer.process = my_gui.time.after(1000, start_chronometer)
    my_chronometer.seconds += 1

    if my_chronometer.max_time <= my_chronometer.seconds:
        my_gui.time.config(fg="red", font=("", "16"))
        my_gui.time['text'] = "Posez les stylos 🔔 !"
        stop_chronometer()
    else:
        my_gui.time.config(fg="black", font=("", "18"))
        my_gui.time['text'] = display_time_in_mm_ss(my_chronometer.seconds, my_chronometer.max_time)


def stop_chronometer():
    try:
        my_gui.time.after_cancel(my_chronometer.process)
    except:
        pass


def resume_chronometer():
    global my_gui
    stop_chronometer()
    my_chronometer.seconds = 0
    my_gui.time['text'] = display_time_in_mm_ss(my_chronometer.seconds, my_chronometer.max_time)


def get_value():
    global time_settings_window
    try:
        inp = time_settings_window.input_txt.get(1.0, "end-1c")
        time = inp.split(":")
        max_time = int(time[0]) * 60 + int(time[1])
    except:
        time_settings_window.root.withdraw()
        time_settings_window.root.deiconify()
        messagebox.showinfo('Erreur', 'Le format n\'est pas correct\n'
                                      'Le format correct est : MM:SS\n'
                                      'Le chronomètre est réglé pour 25 min.')
        max_time = 25 * 60
        my_chronometer.max_time = max_time
        return
    my_chronometer.max_time = max_time
    time_settings_window.root.destroy()


def click_time_settings_window():
    global time_settings_window
    time_settings_window = Gui(title='Réglage')
    time_settings_window.create_time_settings_window()


if __name__ == "__main__":
    my_chronometer = Chrono()
    time_settings_window = None
    my_gui = Gui(title='Chronomètre')
    my_gui.create_main_window()
    my_gui.main_loop()
