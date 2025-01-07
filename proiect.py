import tkinter as tk
import threading
import random
import time

def generate_random_array(size):
    return [random.randint(10, 300) for _ in range(size)]

def update_visualization(arr, canvas, comparisons=None):
    canvas.delete("all")
    bar_width = canvas.winfo_width() / len(arr)

    for i, height in enumerate(arr):
        color = "purple" if comparisons and i in comparisons else "pink"
        canvas.create_rectangle(i * bar_width, canvas.winfo_height() - height, (i + 1) * bar_width,
                                canvas.winfo_height(), fill=color)

def bubble_sort(arr, update_func, speed, stop_signal, pause_signal):
    n = len(arr)
    for i in range(n):
        if stop_signal():
            break
        for j in range(0, n - i - 1):
            comparisons = [j, j + 1]
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            update_func(arr, comparisons)
            time.sleep(speed)

            while pause_signal.is_set():
                time.sleep(0.1)

def insertion_sort(arr, update_func, speed, stop_signal, pause_signal):
    for i in range(1, len(arr)):
        if stop_signal():
            break
        key = arr[i]
        j = i - 1
        comparisons = [j]
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            comparisons.append(j)
        arr[j + 1] = key
        update_func(arr, comparisons)
        time.sleep(speed)

        while pause_signal.is_set():
            time.sleep(0.1)

def selection_sort(arr, update_func, speed, stop_signal, pause_signal):
    n = len(arr)
    for i in range(n):
        if stop_signal():
            break
        min_idx = i
        comparisons = [min_idx]
        for j in range(i + 1, n):
            comparisons.append(j)
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        update_func(arr, comparisons)
        time.sleep(speed)

        while pause_signal.is_set():
            time.sleep(0.1)

def run_sorting_algorithm(algorithm, arr, update_func, speed, stop_signal, pause_signal, canvas):
    algorithm(arr, update_func, speed, stop_signal, pause_signal)

def update_with_canvas(arr, canvas, app, comparisons=None):
    app.root.after(0, update_visualization, arr, canvas, comparisons)

class SortingVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.arr = generate_random_array(50)
        self.speed = 0.05
        self.stop_sorting_flag = threading.Event()
        self.pause_signal = threading.Event()

        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()

        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        self.algorithm_menu = tk.OptionMenu(self.root, self.algorithm_var, "Bubble Sort", "Insertion Sort",
                                            "Selection Sort")
        self.algorithm_menu.pack()

        self.speed_scale = tk.Scale(self.root, from_=0.01, to=0.5, resolution=0.01, orient="horizontal", label="Viteză")
        self.speed_scale.set(self.speed)
        self.speed_scale.pack()

        self.size_scale = tk.Scale(self.root, from_=5, to_=100, orient="horizontal", label="Număr de elemente")
        self.size_scale.set(50)
        self.size_scale.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_sorting)
        self.start_button.pack()

        self.pause_button = tk.Button(self.root, text="Pauză", command=self.pause_sorting)
        self.pause_button.pack()

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_sorting)
        self.reset_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_sorting)
        self.stop_button.pack()

        self.randomize_button = tk.Button(self.root, text="Randomize", command=self.randomize_array)
        self.randomize_button.pack()

        self.sorting_thread = None
        self.is_paused = False

    def start_sorting(self):
        self.arr = generate_random_array(self.size_scale.get())
        self.update_visualization()
        self.stop_sorting_flag.clear()
        self.pause_signal.clear()
        self.is_paused = False
        selected_algorithm = self.algorithm_var.get()

        def update_func(arr, comparisons):
            update_with_canvas(arr, self.canvas, self, comparisons)

        if selected_algorithm == "Bubble Sort":
            self.sorting_thread = threading.Thread(target=run_sorting_algorithm, args=(
            bubble_sort, self.arr, update_func, self.speed_scale.get(), self.stop_sorting_flag.is_set,
            self.pause_signal, self.canvas))
        elif selected_algorithm == "Insertion Sort":
            self.sorting_thread = threading.Thread(target=run_sorting_algorithm, args=(
            insertion_sort, self.arr, update_func, self.speed_scale.get(), self.stop_sorting_flag.is_set,
            self.pause_signal, self.canvas))
        elif selected_algorithm == "Selection Sort":
            self.sorting_thread = threading.Thread(target=run_sorting_algorithm, args=(
            selection_sort, self.arr, update_func, self.speed_scale.get(), self.stop_sorting_flag.is_set,
            self.pause_signal, self.canvas))

        self.sorting_thread.start()

    def stop_sorting(self):
        self.stop_sorting_flag.set()

    def pause_sorting(self):
        if self.pause_signal.is_set():
            self.pause_signal.clear()
            self.pause_button.config(text="Pauză")
        else:
            self.pause_signal.set()
            self.pause_button.config(text="Reluare")

    def reset_sorting(self):
        self.arr = generate_random_array(self.size_scale.get())
        self.update_visualization()

    def randomize_array(self):
        self.arr = generate_random_array(self.size_scale.get())
        self.update_visualization()

    def update_visualization(self):
        self.root.after(0, update_visualization, self.arr, self.canvas)

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizerApp(root)
    root.mainloop()