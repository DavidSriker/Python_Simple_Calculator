import tkinter as tk
from tkinter import ttk

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
    'plus': '+',
    'minus': '-',
    'multiply': 'x',
    'divide': '/',
    'equal': '='
}


class CalculatorAppearance(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.buttons_text = calculator_button_text
        self.configure_gui()
        self.create_calc_widgets()
        # in order to change the button colors
        ttk.Style().configure('red/black.TButton', foreground='red', background='black',
                              font=("Arial", 20, "bold"))


    def configure_gui(self):
        self.master.title("Calculator")
        self.master.configure(bg='black')

    def create_calc_widgets(self):
        self.create_input_field()
        self.create_buttons()

    def create_input_field(self):
        display = tk.StringVar()
        self.user_in = tk.Entry(self.master, textvariable=display)
        self.user_in.grid(row=0, column=0, ipady=10, ipadx=10, columnspan=4, sticky=tk.W + tk.E)
        self.user_in.configure(font=("Arial", 20, "bold"))
        self.user_in.insert(0, "0")

    def create_buttons(self):
        button_col = 0
        button_row = 1
        text_in_row = ('C', '123+', '456-', '789x', '0=/')
        for row in text_in_row:
            for text in row:
                self.configure_button(text, button_row, button_col)
                button_col += 1
            button_col = 0
            button_row += 1

    def configure_button(self, txt, r, c):
        key = list(calculator_button_text.keys())[
            list(calculator_button_text.values()).index(txt)
        ]
        calculator_button_text[key] = ttk.Button(self.master, text=txt,
                                                 style='red/black.TButton')
        calculator_button_text[key].grid(row=r, column=c, ipady=10, ipadx=10)
        if (key=='clear'):
            self.configure_clear_button(key)
        elif (key=='equal'):
            self.configure_equal_button(key)
        elif (key=='divide'):
            self.configure_divide_button(key)


    def configure_clear_button(self, k):
        calculator_button_text[k].grid(columnspan=4, sticky=tk.W + tk.E)

    def configure_equal_button(self, k):
        calculator_button_text[k].grid(columnspan=2, sticky=tk.W + tk.E)

    def configure_divide_button(self, k):
        calculator_button_text[k].grid(column=3)



if __name__=='__main__':
    root = tk.Tk()
    calc_gui = CalculatorAppearance(root)
    root.mainloop()
