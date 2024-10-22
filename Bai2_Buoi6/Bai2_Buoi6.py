import cv2
import numpy as np
from tkinter import filedialog, Tk, Label, Button, Frame
from PIL import Image, ImageTk


def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        process_image(img)


def process_image(img):
    # Làm mờ toàn bộ ảnh
    blurred = cv2.GaussianBlur(img, (15, 15), 0)

    # Trích xuất cạnh bằng Canny
    edges = cv2.Canny(img, threshold1=30, threshold2=100)

    # Tạo mặt nạ cho xương
    mask = np.zeros_like(img)
    mask[edges > 0] = 255  # Giữ lại các cạnh

    # Làm nét chỉ cho phần xương
    sharpened = cv2.addWeighted(img, 1.5, blurred, -0.5, 0)

    # Kết hợp ảnh: giữ xương nét và làm mờ các phần khác
    result = np.where(mask == 255, sharpened, blurred)

    # Tạo mặt nạ cho biên
    border_mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)

    # Kết hợp ảnh lại: giữ lại phần biên của xương với nét rõ hơn
    final_result = np.where(border_mask == 255, sharpened, result)

    # Hiển thị ảnh gốc và ảnh đã xử lý
    show_images(img, final_result)


def show_images(original, processed):
    # Chuyển đổi từ định dạng OpenCV sang định dạng PIL
    original_img = Image.fromarray(original)
    processed_img = Image.fromarray(processed)

    # Tạo đối tượng ImageTk
    original_photo = ImageTk.PhotoImage(original_img)
    processed_photo = ImageTk.PhotoImage(processed_img)

    # Cập nhật nhãn để hiển thị ảnh
    original_label.config(image=original_photo)
    original_label.image = original_photo
    processed_label.config(image=processed_photo)
    processed_label.image = processed_photo


# Tạo cửa sổ chính
root = Tk()
root.title("Ứng dụng làm rõ nét đoạn xương trong X-quang")

# Khung chứa các nút
frame = Frame(root)
frame.pack()

# Nút tải ảnh
load_button = Button(frame, text="Tải ảnh X-quang", command=load_image)
load_button.pack()

# Nhãn để hiển thị ảnh
original_label = Label(root)
original_label.pack(side="left")

processed_label = Label(root)
processed_label.pack(side="right")

root.mainloop()
