


# import tkinter as tk
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.cm as cm

# # Sample data
# data = [
#     ['John', '2022-01-01', 1000, 5],
#     ['Alice', '2022-02-15', 2000, 3],
#     ['Bob', '2022-03-10', 1500, 7],
#     ['Sarah', '2022-04-20', 1800, 4]
# ]

# # Select columns for display and merge customer name and date
# display_data = ['{} {}'.format(row[0], row[1]) for row in data]

# # Create the Tkinter window
# root = tk.Tk()
# root.title('Table Plot')

# # Create a Matplotlib figure
# fig = Figure(figsize=(8, 4), dpi=100)

# # Create a subplot for the table
# ax = fig.add_subplot(111)
# ax.axis('off')

# # Create the table plot
# table = ax.table(cellText=[[row] for row in display_data],
#                  colLabels=['Customer & Krar Date'],
#                  loc='center',
#                  cellLoc='center',
#                  cellColours=[[cm.Blues(0.2)] for _ in range(len(display_data))])

# # Set table properties
# table.auto_set_font_size(False)
# table.set_fontsize(12)
# table.scale(1.2, 1.2)  # Adjust the table size if needed

# # Create a FigureCanvasTkAgg instance
# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.draw()

# # Pack the canvas into the Tkinter window
# canvas.get_tk_widget().pack()

# # Start the Tkinter event loop
# root.mainloop()
