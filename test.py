import tkinter as tk


root = tk.Tk()


image = tk.PhotoImage(file="myicons/newlogo.png")

l = tk.Label(root, image=image)
l.pack()

root.mainloop()