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


class CalculatorApp(tk.Frame):
    ''' Main Calculator Class '''

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.user_in_list = []
        self.buttons_text = calculator_button_text
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

    def configure_gui(self):
        self.master.title("Calculator")
        self.master.configure(bg='black')

    def create_calc_widgets(self):
        self.create_input_field()
        self.create_buttons()

    def create_input_field(self):
        ## this work without scrollbar

        # self.screen = tk.Text(self.master, height=5, width=30)
        # self.screen.grid(row=0, column=0, columnspan=4, sticky=tk.W + tk.E)
        # self.screen.configure(font=("Calibri", 20, "bold", "italic"),
        #                       foreground="black", background="whitesmoke")

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

    def configure_button(self, txt, r, c):
        to_write = (txt == '=')
        if (txt == 'd'):
            txt = u"\u232B"
        elif (txt == '/'):
            txt = u"\u00F7"
        key = list(calculator_button_text.keys())[
            list(calculator_button_text.values()).index(txt)
        ]

        calculator_button_text[key] = ttk.Button(self.master, text=txt,
                                                 style='style.TButton',
                                                 command=lambda: self.click(txt, to_write))
        calculator_button_text[key].grid(row=r, column=c, ipady=10, ipadx=10)
        if (key=='clear'):
            self.configure_clear_button(key)
        elif (key=='equal'):
            self.configure_equal_button(key)

    def configure_clear_button(self, k):
        calculator_button_text[k].grid(columnspan=4, sticky=tk.W + tk.E)

    def configure_equal_button(self, k):
        calculator_button_text[k].grid(columnspan=4, sticky=tk.W + tk.E)

    def click(self, cmd, new_line):
        if (cmd != '='):
            self.display_on_screen(cmd, new_line)
        else:
            self.equation = re.sub(u"\u00F7", '/', self.equation)
            self.equation = re.sub("x", '*', self.equation)
            ans = str(eval(self.equation))
            self.display_on_screen(ans, new_line)
            self.equation = ""

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



if __name__ == '__main__':
    root = tk.Tk()
    calc_gui = CalculatorApp(root)
    # Make window fixed (cannot be resized)
    root.resizable(width=False, height=False)
    root.mainloop()



