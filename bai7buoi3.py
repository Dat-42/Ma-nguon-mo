import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, diff
import cv2  # OpenCV để hỗ trợ xử lý ảnh

# Hàm để mở file ảnh
def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        img_resized = cv2.resize(img, (250, 250))  # Định lại kích thước ảnh để hiển thị trong GUI
        display_image(img_resized)
        edge_image = edge_detection(img_resized)
        display_edge_image(edge_image)

# Hàm để hiển thị ảnh gốc trong GUI
def display_image(image):
    image_display = ImageTk.PhotoImage(image=Image.fromarray(image))
    original_image_label.config(image=image_display)
    original_image_label.image = image_display

# Hàm để thực hiện tách biên
def edge_detection(image):
    edges = cv2.Canny(image, 100, 200)  # Tách biên sử dụng thuật toán Canny
    return edges

# Hàm để hiển thị ảnh tách biên
def display_edge_image(image):
    plt.figure(figsize=(5, 5))
    plt.imshow(image, cmap='gray')
    plt.title('Edge Detected Image')
    plt.show()

# Thiết lập giao diện GUI
root = tk.Tk()
root.title("Edge Detection Application")

# Nút mở ảnh
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack(pady=10)

# Nhãn để hiển thị ảnh gốc
original_image_label = tk.Label(root)
original_image_label.pack()

# Chạy ứng dụng
root.mainloop()
