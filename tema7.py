import tkinter as tk
import random
import time

# Setări pentru fereastra tkinter
WIDTH = 600
HEIGHT = 400
DELAY = 0.05  # Viteza animației (în secunde)


# Funcția pentru algoritmul Bubble Sort
def bubble_sort(arr, update_callback):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            update_callback(arr)  # Actualizează vizualizarea la fiecare pas
            time.sleep(DELAY)


# Funcția de randomizare a secvenței
def randomize_array(size):
    return [random.randint(10, 100) for _ in range(size)]


# Funcția de actualizare a vizualizării
def update_visualization(arr, canvas):
    canvas.delete("all")  # Curăță canvas-ul înainte de fiecare actualizare
    bar_width = WIDTH // len(arr)  # Lățimea fiecărei bare
    for i, value in enumerate(arr):
        x1 = i * bar_width
        y1 = HEIGHT - value * 2  # Înalțimea barei depinde de valoarea elementului
        x2 = (i + 1) * bar_width - 1
        y2 = HEIGHT
        canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
    canvas.update()  # Actualizează canvas-ul


# Crearea aplicației
def main():
    size = 30  # numărul de elemente
    arr = randomize_array(size)

    # Crearea ferestrei principale
    root = tk.Tk()
    root.title("Vizualizare Bubble Sort")
    root.geometry(f"{WIDTH}x{HEIGHT}")

    # Crearea unui canvas pentru a desena barele
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()

    # Vizualizarea inițială
    update_visualization(arr, canvas)

    # Start Bubble Sort
    bubble_sort(arr, lambda arr: update_visualization(arr, canvas))

    # Așteptăm până când fereastra este închisă
    root.mainloop()


# Rularea aplicației
if __name__ == "__main__":
    main()
