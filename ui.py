import tkinter as tk
# import speed_check
import threading

class TrafficLight:
    def __init__(self, master, x):
        self.master = master
        self.current_color = 'red'

        # Create the canvas
        self.canvas = tk.Canvas(master, width=200, height=300)
        self.canvas.pack(side=tk.LEFT, padx=10)

        # Create the lights for the first traffic light
        self.red_light1 = self.canvas.create_oval(10, 10, 90, 90, fill='red')
        self.yellow_light1 = self.canvas.create_oval(10, 110, 90, 190, fill='gray')
        self.green_light1 = self.canvas.create_oval(10, 210, 90, 290, fill='gray')

        # Create a copy of the lights for the second traffic light
        self.red_light2 = self.canvas.create_oval(110, 10, 190, 90, fill='red')
        self.yellow_light2 = self.canvas.create_oval(110, 110, 190, 190, fill='gray')
        self.green_light2 = self.canvas.create_oval(110, 210, 190, 290, fill='gray')

        # Start the traffic light control for the first traffic light
        self.change_light(self.red_light1, self.green_light1)

        # Start the traffic light control for the second traffic light with a delay
        self.master.after(1000, self.change_light, self.red_light2, self.green_light2)

    def change_light(self, red_light, green_light):
        if self.current_color == 'red':
            self.canvas.itemconfig(red_light, fill='red')
            # self.canvas.itemconfig(yellow_light, fill='gray')
            self.canvas.itemconfig(green_light, fill='gray')
            self.current_color = 'green'
        elif self.current_color == 'green':
            self.canvas.itemconfig(red_light, fill='gray')
            # self.canvas.itemconfig(yellow_light, fill='gray')
            self.canvas.itemconfig(green_light, fill='green')
            self.current_color = 'yellow'
        else:
            self.canvas.itemconfig(red_light, fill='gray')
            # self.canvas.itemconfig(yellow_light, fill='yellow')
            self.canvas.itemconfig(green_light, fill='gray')
            self.current_color = 'red'

        # Schedule the next light change after 2 seconds
        self.master.after(2000, self.change_light, red_light,  green_light)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Traffic Lights")
    thread1 = threading.Thread(target=speed_check.trackMultipleObjects1)
    thread2 = threading.Thread(target=speed_check.trackMultipleObjects2)
    thread3 = threading.Thread(target=TrafficLight, args=(root, 0))
    thread4 = threading.Thread(target=speed_check.get_dynamic_values)

    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    # Create the main window
    # ...

    # Run the Tkinter event loop
    root.mainloop()