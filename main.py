import customtkinter as ctk
import tkinter as tk
import re

BASE_WIDTH = 450
BASE_HEIGHT = 200


def print_size(item):
    print(item.winfo_width(), item.winfo_height())


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Apple Purchase History Calculator")
        self.geometry(f"{BASE_WIDTH}x{BASE_HEIGHT}")

        self.counter_rows = []
        self.total_label = ctk.CTkLabel(self, text="Total spent: £0")
        self.total_label.pack(pady=20)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=20)

        self.add_button = ctk.CTkButton(self.button_frame, text="Add price counter", command=self.add_counter)
        self.add_button.pack(pady=20, side=tk.LEFT, padx=10)

        self.remove_button = ctk.CTkButton(self.button_frame, text="Remove price counter", command=self.remove_counter, fg_color="red")
        self.remove_button.pack(pady=20, side=tk.LEFT, padx=10)

        self.canvas_frame = ctk.CTkScrollableFrame(self)
        self.canvas_height = 0
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def add_counter(self):

        counter_row = CounterRow(self.canvas_frame, callback=self.update_total, cindex=len(self.counter_rows) + 1)
        counter_row.pack(pady=10, anchor=tk.CENTER, side="top")
        self.counter_rows.append(counter_row)

        if len(self.counter_rows) <= 10:
            # Update the height of the canvas
            self.canvas_height += 49  # Adjust this value as needed
            self.geometry(f"{BASE_WIDTH}x{BASE_HEIGHT + self.canvas_height}")

            self.update()
        self.update_total()

    def remove_counter(self):
        if not self.counter_rows:
            return

        self.counter_rows[-1].destroy()
        self.counter_rows.pop()

        if len(self.counter_rows) < 10:
            # Update the height of the canvas
            self.canvas_height -= 49
            if self.canvas_height < 0:
                self.canvas_height = 0
            self.geometry(f"{int(BASE_WIDTH)}x{int(BASE_HEIGHT + self.canvas_height)}")
            self.update()
        self.update_total()

    def update_total(self):
        if not self.counter_rows:
            return

        total = sum(row.get_total() for row in self.counter_rows)
        self.total_label.configure(text=f"Total spent: £{total:.2f}")


class CounterRow(ctk.CTkFrame):
    def __init__(self, master=None, callback=None, **kwargs):
        counter_index = kwargs.pop("cindex", 1)
        super().__init__(master, **kwargs)

        self.callback = callback

        ctk.CTkLabel(self, text=f"{counter_index}.").pack(side=tk.LEFT, padx=10)

        self.last_cost = ""
        self.last_counter = "0"

        self.lbl_cost = ctk.CTkLabel(self, text="Cost: £")
        self.lbl_cost.pack(side=tk.LEFT)
        self.cost_var = ctk.StringVar()
        self.cost_var.trace_add("write", self.on_value_change)
        self.cost_entry = ctk.CTkEntry(self, textvariable=self.cost_var)
        self.cost_entry.pack(side=tk.LEFT, padx=10)

        self.lbl_count = ctk.CTkLabel(self, text="#")
        self.lbl_count.pack(side=tk.LEFT)
        self.counter_var = ctk.StringVar(self)
        self.counter_var.trace_add("write", self.on_value_change)
        self.counter_entry = ctk.CTkEntry(self, textvariable=self.counter_var, width=40)
        self.counter_entry.pack(side=tk.LEFT, padx=10)
        self.counter_var.set("0")

        self.counter_plus = ctk.CTkButton(self, text="+", command=self.increment, width=30)
        self.counter_plus.pack(side=tk.LEFT, padx=10)

        self.counter_minus = ctk.CTkButton(self, text="-", command=self.decrement, width=30)
        self.counter_minus.pack(side=tk.LEFT, padx=10)

    def increment(self):
        counter_num = self.counter_var.get()
        if counter_num == "":
            counter_num = 0
        self.counter_var.set(str(int(counter_num) + 1))
        self.on_value_change()

    def decrement(self):
        counter_num = self.counter_var.get()
        if counter_num == "":
            return
        if int(counter_num) == 0:
            return
        self.counter_var.set(str(int(self.counter_var.get()) - 1))
        self.on_value_change()

    def on_value_change(self, *args):
        if self.callback:
            self.callback()

        current_cost = self.cost_var.get()
        current_counter = self.counter_var.get()

        if current_cost == "":
            self.cost_var.set("")
        elif current_cost.count(".") > 1 or re.search(r"[^0-9.]+", current_cost) is not None:
            self.cost_var.set(self.last_cost)
        else:
            self.last_cost = self.cost_var.get()

        if current_counter == "":
            self.counter_var.set("0")
        elif not re.search(r"^[0-9]+$", self.counter_var.get()):
            self.counter_var.set(self.last_counter)
        else:
            self.last_counter = self.counter_var.get()

        self.cost_var.set(self.cost_var.get().lstrip("0"))
        self.counter_var.set(self.counter_var.get().lstrip("0"))
        if self.counter_var.get() == "":
            self.counter_var.set("0")

    def get_total(self):
        try:
            cost = float(self.cost_var.get())
            counter = int(self.counter_var.get())
            return cost * counter
        except ValueError:
            return 0


if __name__ == "__main__":
    ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode("System")
    app = Application()
    app.mainloop()
