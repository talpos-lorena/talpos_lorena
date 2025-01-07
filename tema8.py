import tkinter as tk
import random
import time
import threading

def generate_random_array(size):
    return [random.randint(10, 300) for _ in range(size)]

def update_visualization(arr, canvas, comparisons=None):
    canvas.delete("all")
    bar_width = canvas.winfo_width() / len(arr)
    for i, height in enumerate(arr):
        color = "pink" if comparisons and i in comparisons else "blue"
        canvas.create_rectangle(i * bar_width, canvas.winfo_height() - height, (i + 1) * bar_width,
                                canvas.winfo_height(), fill=color)

def selection_sort(arr, update_func, speed, stop_signal, pause_signal):
    n = len(arr)
    for i in range(n):
        if stop_signal(): break
        min_idx = i
        comparisons = [min_idx]
        for j in range(i + 1, n):
            comparisons.append(j)
            if arr[j] < arr[min_idx]: min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        update_func(arr, comparisons)
        time.sleep(speed)
        while pause_signal.is_set(): time.sleep(0.1)

def run_sorting_algorithm(algorithm, arr, update_func, speed, stop_signal, pause_signal, canvas):
    algorithm(arr, update_func, speed, stop_signal, pause_signal)

class SortingVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.arr = generate_random_array(25)
        self.stop_flag, self.pause_flag = threading.Event(), threading.Event()
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Start", command=self.start_sorting).pack()
        self.pause_btn = tk.Button(self.root, text="Pause", command=self.toggle_pause)
        self.pause_btn.pack()
        tk.Button(self.root, text="Reset", command=self.reset_sorting).pack()

    def start_sorting(self):
        self.arr = generate_random_array(25)
        self.stop_flag.clear()
        self.pause_flag.clear()
        speed = 0.2
        threading.Thread(target=run_sorting_algorithm, args=(selection_sort, self.arr, self.update_canvas, speed, self.stop_flag.is_set, self.pause_flag, self.canvas)).start()

    def toggle_pause(self):
        self.pause_flag.set() if not self.pause_flag.is_set() else self.pause_flag.clear()
        self.pause_btn.config(text="Resume" if self.pause_flag.is_set() else "Pause")

    def reset_sorting(self):
        self.arr = generate_random_array(25)
        self.update_canvas(self.arr)

    def update_canvas(self, arr, comparisons=None):
        self.root.after(0, update_visualization, arr, self.canvas, comparisons)

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizerApp(root)
    root.mainloop()