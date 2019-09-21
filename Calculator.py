import tkinter as tk
from tkinter import ttk
import re

# the calculator gui text for the buttons
calculator_button_text = {
    'clear': 'C',
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'decimal': '.',
    'plus': '+',
    'minus': '-',
    'multiply': 'x',
    'divide': u"\u00F7",
    'equal': '=',
    'delete': u"\u232B"
}


def find_key_from_value(dic, val):
    return list(dic.keys())[list(dic.values()).index(val)]


class CalculatorApp(tk.Frame):
    ''' Main Calculator Class '''

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.buttons = calculator_button_text.copy()
        self.equation = ""
        self.configure_gui()
        self.create_calc_widgets()
        # in order to change the button colors (mac)
        style = ttk.Style(self.master)
        style.theme_use('clam')
        style.configure('style.TButton', foreground="firebrick", background="darkgrey",
                        font=("Arial", 20, "bold", "italic"))
        style.map('TButton',
                  foreground=[('pressed', 'blue'),
                              ('active', 'darkgreen')],
                  background=[('pressed', 'dimgrey'),
                              ('active', 'grey')])
        # button style for simulation of pressed key
        pressed_sim = ttk.Style(self.master)
        pressed_sim.theme_use('clam')
        pressed_sim.configure('pressed_style.TButton', foreground="blue", background="dimgrey",
                        font=("Arial", 20, "bold", "italic"))
        idle_sim = ttk.Style(self.master)
        idle_sim.theme_use('clam')
        idle_sim.configure('idle_style.TButton', foreground="firebrick", background="darkgrey",
                              font=("Arial", 20, "bold", "italic"))

    def configure_gui(self):
        self.master.title("Calculator")
        self.master.configure(bg='black')

    def create_calc_widgets(self):
        self.create_input_field()
        self.create_buttons()

    def create_input_field(self):
        self.screen = tk.Text(self.master, height=5, width=30)
        self.screen.grid(row=0, column=0, columnspan=4, sticky='nswe')
        self.scroll_bar = ttk.Scrollbar(self.master, command=self.screen.yview)
        self.scroll_bar.grid(row=0, column=3, sticky='nse')
        self.screen.configure(font=("Calibri", 20, "bold", "italic"),
                               foreground="black", background="whitesmoke")
        self.screen.config(yscrollcommand=self.scroll_bar.set)

    def create_buttons(self):
        button_col = 0
        button_row = 1
        text_in_row = ('C', '123d', '456-', '789x', '0.+/', '=')
        for row in text_in_row:
            for text in row:
                self.configure_button(text, button_row, button_col)
                button_col += 1
            button_col = 0
            button_row += 1

        numeric_keys = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
        for k in numeric_keys:
            self.master.bind(k, lambda event: self.numeric_keystroke_action(event))

        # special cases
        self.master.bind('.', lambda event: self.special_keystroke_action('.'))
        self.master.bind('<plus>', lambda event: self.special_keystroke_action('+'))
        self.master.bind('<minus>', lambda event: self.special_keystroke_action('-'))
        self.master.bind('<asterisk>', lambda event: self.special_keystroke_action('x'))
        self.master.bind('<slash>', lambda event: self.special_keystroke_action(u"\u00F7"))
        self.master.bind('<BackSpace>', lambda event: self.special_keystroke_action(u"\u232B"))
        self.master.bind('<Return>', lambda event: self.special_keystroke_action('='))

    def configure_button(self, txt, r, c):
        to_write = (txt == '=')
        if (txt == 'd'):
            txt = u"\u232B"
        elif (txt == '/'):
            txt = u"\u00F7"
        key = find_key_from_value(calculator_button_text, txt)

        self.buttons[key] = ttk.Button(self.master, text=txt,
                                                 style='style.TButton',
                                                 command=lambda: self.click(txt, to_write))
        self.buttons[key].grid(row=r, column=c, ipady=10, ipadx=10)
        if (key=='clear'):
            self.configure_clear_button(key)
        elif (key=='equal'):
            self.configure_equal_button(key)

    def configure_clear_button(self, k):
        self.buttons[k].grid(columnspan=4, sticky=tk.W + tk.E)

    def configure_equal_button(self, k):
        self.buttons[k].grid(columnspan=4, sticky=tk.W + tk.E)

    def click(self, cmd, new_line):
        if (cmd == '='):
            if (self.equation):
                self.equation = re.sub(u"\u00F7", '/', self.equation)
                self.equation = re.sub("x", '*', self.equation)
                ans = str(eval(self.equation))
                self.display_on_screen(ans, new_line)
                self.equation = ""
        elif (cmd == 'C'):
            self.clear_screen()
        elif (cmd == u"\u232B"):
            self.delete_char()
        else:
            self.display_on_screen(cmd, new_line)

    def display_on_screen(self, val, new_line=False):
        if (not new_line):
            self.screen.insert(tk.END, val)
            self.equation += str(val)
        else:
            self.screen.insert(tk.END, '\n')
            self.screen.insert(tk.END, val)
            self.screen.insert(tk.END, '\n')
            self.screen.yview('end')

    def clear_screen(self):
        # set equation to empty before deleting screen
        self.equation = ""
        self.screen.delete('1.0', tk.END)

    def delete_char(self):
        self.equation = self.equation[0:-1]  # delete the last element
        entire_txt = self.screen.get('1.0', tk.END)[0:-2]
        self.screen.delete('1.0', tk.END)
        self.screen.insert('1.0', entire_txt)

    # keystroke handling

    def numeric_keystroke_action(self, event):
        k = find_key_from_value(calculator_button_text, event.char)
        self.simulate_button_press(k)
        self.after(150, self.simulate_button_idle, k)
        self.click(event.char, False)

    def special_keystroke_action(self, char):
        to_write = False
        k = find_key_from_value(calculator_button_text, char)
        self.simulate_button_press(k)

        if (k == 'equal'):
            to_write = True
        elif (char == u"\u232B"):
            self.delete_char()
            self.after(150, self.simulate_button_idle, k)
            return

        self.after(150, self.simulate_button_idle, k)
        self.click(char, to_write)

    def simulate_button_press(self, key):
        self.buttons[key].configure(style='pressed_style.TButton')

    def simulate_button_idle(self, key):
        self.buttons[key].configure(style='idle_style.TButton')


if __name__ == '__main__':
    root = tk.Tk()
    calc_gui = CalculatorApp(root)
    # Make window fixed (cannot be re-sized)
    root.resizable(width=False, height=False)
    root.mainloop()



