import cv2
import numpy as np
from tkinter import filedialog, Tk, Button, Label, Scale, HORIZONTAL
from PIL import Image, ImageTk

# Initialize global variables
label_orig = None
label_proc = None

def apply_filter(image, kernel):
    return cv2.filter2D(image, -1, kernel)

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        global img, img_original
        img_original = cv2.imread(file_path)
        img = img_original.copy()
        show_image(img_original, img, 'Ảnh gốc', 'Ảnh sau xử lý')

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        global img, img_original
        img_original = frame
        img = img_original.copy()
        show_image(img_original, img, 'Ảnh gốc', 'Ảnh sau xử lý')

def show_image(original, processed, title_orig, title_proc):
    rgb_orig = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    rgb_proc = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
    pil_orig = Image.fromarray(rgb_orig)
    pil_proc = Image.fromarray(rgb_proc)
    tk_orig = ImageTk.PhotoImage(pil_orig)
    tk_proc = ImageTk.PhotoImage(pil_proc)
    if label_orig and label_proc:
        label_orig.config(image=tk_orig, text=title_orig)
        label_orig.image = tk_orig
        label_proc.config(image=tk_proc, text=title_proc)
        label_proc.image = tk_proc
    else:
        print("Labels are not defined")

def save_image(image):
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path:
        cv2.imwrite(file_path, image)

def apply_identity():
    kernel_identity = np.array([[0,0,0], [0,1,0], [0,0,0]])
    output = apply_filter(img, kernel_identity)
    show_image(img_original, output, 'Ảnh gốc', 'Bộ lọc gốc')

def apply_blur():
    kernel_3x3 = np.ones((3,3), np.float32) / 9.0
    output = apply_filter(img, kernel_3x3)
    show_image(img_original, output, 'Ảnh gốc', 'Bộ lọc 3x3')

def apply_sharpen():
    kernel_sharpen = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    output = apply_filter(img, kernel_sharpen)
    show_image(img_original, output, 'Ảnh gốc', 'Ảnh sắc nét')

def apply_gray():
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    show_image(img_original, cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR), 'Ảnh gốc', 'Ảnh đen trắng')

def blur_background():
    h, w = img.shape[:2]
    center_x, center_y = w // 2, h // 2
    radius = min(center_x, center_y) // 2

    # Create a circular mask
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
    mask = dist_from_center <= radius

    blurred = cv2.GaussianBlur(img, (21, 21), 0)
    output = img.copy()
    output[~mask] = blurred[~mask]
    show_image(img_original, output, 'Ảnh gốc', 'Làm mờ nền')

def remove_blemishes():
    output = cv2.fastNlMeansDenoisingColored(img, None, 30, 30, 7, 21)
    show_image(img_original, output, 'Ảnh gốc', 'Xóa khuyết điểm')

def cartoonize():
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    show_image(img_original, cartoon, 'Ảnh gốc', 'Ảnh hoạt hình')

def invert_colors():
    output = cv2.bitwise_not(img)
    show_image(img_original, output, 'Ảnh gốc', 'Đảo màu')

def edge_detection():
    edges = cv2.Canny(img, 100, 200)
    show_image(img_original, cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), 'Ảnh gốc', 'Phát hiện cạnh')

def sepia_filter():
    kernel_sepia = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    output = cv2.transform(img, kernel_sepia)
    output = np.clip(output, 0, 255)
    show_image(img_original, output, 'Ảnh gốc', 'Bộ lọc Sepia')

def adjust_brightness(val):
    value = int(val)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    output = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    show_image(img_original, output, 'Ảnh gốc', 'Điều chỉnh độ sáng')

def rotate_image(angle):
    global img
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, matrix, (w, h))
    show_image(img_original, rotated, 'Ảnh gốc', 'Ảnh xoay')

def change_colorspace():
    global img
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    show_image(img_original, cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR), 'Ảnh gốc', 'Ảnh màu HSV')

def adjust_contrast(val):
    value = int(val)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.add(l, value)
    l[l > 255] = 255
    l[l < 0] = 0
    final_lab = cv2.merge((l, a, b))
    output = cv2.cvtColor(final_lab, cv2.COLOR_LAB2BGR)
    show_image(img_original, output, 'Ảnh gốc', 'Điều chỉnh độ tương phản')
def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path:
        cv2.imwrite(file_path, img)
def change_colorspace():
    global img
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    show_image(img_original, cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR), 'Ảnh gốc', 'Ảnh màu HSV')





# Set up the main application window
root = Tk()
root.title("Ứng dụng lọc ảnh")

# Create and position labels
label_orig = Label(root)
label_orig.grid(row=0, column=1, rowspan=14, padx=10)
label_proc = Label(root)
label_proc.grid(row=0, column=2, rowspan=14, padx=10)

# Create and position buttons
btn_open = Button(root, text="Mở ảnh", command=open_image)
btn_open.grid(row=0, column=0, pady=5)

btn_capture = Button(root, text="Chụp ảnh", command=capture_image)
btn_capture.grid(row=1, column=0, pady=5)

btn_identity = Button(root, text="Áp dụng bộ lọc gốc", command=apply_identity)
btn_identity.grid(row=2, column=0, pady=5)

btn_blur = Button(root, text="Áp dụng bộ lọc 3x3", command=apply_blur)
btn_blur.grid(row=3, column=0, pady=5)

btn_sharpen = Button(root, text="Ảnh sắc nét", command=apply_sharpen)
btn_sharpen.grid(row=4, column=0, pady=5)

btn_gray = Button(root, text="Ảnh đen trắng", command=apply_gray)
btn_gray.grid(row=5, column=0, pady=5)

btn_bg_blur = Button(root, text="Làm mờ nền", command=blur_background)
btn_bg_blur.grid(row=6, column=0, pady=5)

btn_blemish = Button(root, text="Xóa khuyết điểm", command=remove_blemishes)
btn_blemish.grid(row=7, column=0, pady=5)

btn_cartoon = Button(root, text="Ảnh hoạt hình", command=cartoonize)
btn_cartoon.grid(row=8, column=0, pady=5)
btn_xa = Button(root, text="bo loc saphie", command=sepia_filter)
btn_xa.grid(row=9, column=0, pady=5)
btn_kb = Button(root, text="Ảnh màu HSV", command=change_colorspace)
btn_kb.grid(row=10, column=0, pady=5)
btn_dm = Button(root, text="Đảo màu", command=invert_colors)
btn_dm.grid(row=11, column=0, pady=5)

btn_save = Button(root, text="Luu anh", command=save_image)
btn_save.grid(row=12, column=0, pady=5)

root.mainloop()