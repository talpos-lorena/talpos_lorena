import tkinter as tk
import random
import time

WIDTH = 600
HEIGHT = 400
DELAY = 0.05  

def bubble_sort(arr, update_callback):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            update_callback(arr) 
            time.sleep(DELAY)

def randomize_array(size):
    return [random.randint(10, 100) for _ in range(size)]

def update_visualization(arr, canvas):
    canvas.delete("all")  
    bar_width = WIDTH // len(arr)  
    for i, value in enumerate(arr):
        x1 = i * bar_width
        y1 = HEIGHT - value * 2  
        x2 = (i + 1) * bar_width - 1
        y2 = HEIGHT
        canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
    canvas.update()  
def main():
    size = 30  
    arr = randomize_array(size)

    root = tk.Tk()
    root.title("Vizualizare Bubble Sort")
    root.geometry(f"{WIDTH}x{HEIGHT}")

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()

    update_visualization(arr, canvas)

    bubble_sort(arr, lambda arr: update_visualization(arr, canvas))

    root.mainloop()

if __name__ == "__main__":
    main()
