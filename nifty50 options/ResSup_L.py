import tkinter as tk

class StockAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Analysis Tool")

        # Resistance Window
        self.resistance_frame = tk.Frame(self.root)
        self.resistance_frame.pack(side=tk.LEFT, padx=10, pady=10)
        tk.Label(self.resistance_frame, text="Resistance Window").grid(row=0, columnspan=2)

        self.r1_entry = tk.Entry(self.resistance_frame)
        self.r1_entry.grid(row=1, column=1)
        tk.Label(self.resistance_frame, text="R1:").grid(row=1, column=0)

        self.r2_entry = tk.Entry(self.resistance_frame)
        self.r2_entry.grid(row=2, column=1)
        tk.Label(self.resistance_frame, text="R2:").grid(row=2, column=0)

        self.r3_entry = tk.Entry(self.resistance_frame)
        self.r3_entry.grid(row=3, column=1)
        tk.Label(self.resistance_frame, text="R3:").grid(row=3, column=0)

        tk.Button(self.resistance_frame, text="Save Resistance", command=self.save_resistance_values).grid(row=4, columnspan=2)

        # Support Window
        self.support_frame = tk.Frame(self.root)
        self.support_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        tk.Label(self.support_frame, text="Support Window").grid(row=0, columnspan=2)

        self.s1_entry = tk.Entry(self.support_frame)
        self.s1_entry.grid(row=1, column=1)
        tk.Label(self.support_frame, text="S1:").grid(row=1, column=0)

        self.s2_entry = tk.Entry(self.support_frame)
        self.s2_entry.grid(row=2, column=1)
        tk.Label(self.support_frame, text="S2:").grid(row=2, column=0)

        self.s3_entry = tk.Entry(self.support_frame)
        self.s3_entry.grid(row=3, column=1)
        tk.Label(self.support_frame, text="S3:").grid(row=3, column=0)

        tk.Button(self.support_frame, text="Save Support", command=self.save_support_values).grid(row=4, columnspan=2)

        # Enter Button
        self.enter_button = tk.Button(self.root, text="Enter", command=self.open_next_program)
        self.enter_button.pack(pady=10)

    def save_resistance_values(self):
        self.r1_value = self.r1_entry.get()
        self.r2_value = self.r2_entry.get()
        self.r3_value = self.r3_entry.get()

    def save_support_values(self):
        self.s1_value = self.s1_entry.get()
        self.s2_value = self.s2_entry.get()
        self.s3_value = self.s3_entry.get()

    def open_next_program(self):
        # Close the current window
        self.root.destroy()

        # Open a new window for the next program
        new_root = tk.Tk()
        new_root.title("Next Program Window")

        # Display the saved values
        tk.Label(new_root, text="Resistance Values:").pack()
        tk.Label(new_root, text=f"R1: {self.r1_value}").pack()
        tk.Label(new_root, text=f"R2: {self.r2_value}").pack()
        tk.Label(new_root, text=f"R3: {self.r3_value}").pack()

        tk.Label(new_root, text="Support Values:").pack()
        tk.Label(new_root, text=f"S1: {self.s1_value}").pack()
        tk.Label(new_root, text=f"S2: {self.s2_value}").pack()
        tk.Label(new_root, text=f"S3: {self.s3_value}").pack()

        new_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = StockAnalysisApp(root)
    root.mainloop()
