from bills.billshowpage import BillShowPage as bill
import tkinter as tk


if __name__ == "__main__":
    app = tk.Tk()
    app.state("zoomed")
    h = bill(app)
    h.pack(expand=1, fill="both")
    app.mainloop()