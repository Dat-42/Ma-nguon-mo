import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.impute import SimpleImputer

# Khởi tạo các biến toàn cục
df = None  # Dữ liệu sẽ được tải lên ở đây
X_train, X_test, y_train, y_test = None, None, None, None
model = None  # Biến model để lưu mô hình được huấn luyện

# Tạo từ điển để lưu thông tin sai số của từng thuật toán
error_metrics = {}

# Hàm để tải lên file dữ liệu
def load_data():
    global df
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        df = pd.read_csv(filepath)
        # In ra thông tin dữ liệu để kiểm tra
        print(df.shape)  # In kích thước của DataFrame
        print(df.columns)  # In ra tên các cột để kiểm tra
        messagebox.showinfo("Load Data", "Data loaded successfully!")
    else:
        messagebox.showwarning("Load Data", "No file selected.")

# Hàm huấn luyện mô hình
def train_model():
    global X_train, X_test, y_train, y_test, model

    if df is None:
        messagebox.showerror("Train Error", "Please load the data first.")
        return

    # Lấy tập đặc trưng (X) và nhãn (y)
    X = df.iloc[:, :9]  # Lấy 10 cột đầu làm đặc trưng
    y = df.iloc[:, -1].values.ravel()  # Cột cuối cùng là nhãn (Performance Index hoặc nhãn khác)

    # Kiểm tra nếu cột y có dữ liệu trống hoặc thiếu
    if y.size == 0:
        messagebox.showerror("Train Error", "Target variable (y) is empty.")
        return

    # Xử lý các giá trị NaN bằng cách thay thế bằng giá trị trung bình
    imputer = SimpleImputer(strategy="mean")
    X = imputer.fit_transform(X)

    # Nếu có NaN trong y, tiến hành impute cho y
    if np.any(np.isnan(y)):
        y = imputer.fit_transform(y.reshape(-1, 1)).ravel()  # Đảm bảo y là mảng 1 chiều sau khi imputation

    # Chia dữ liệu thành tập huấn luyện và kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    # Lựa chọn thuật toán
    algorithm = selected_algorithm.get()

    # Huấn luyện mô hình dựa trên thuật toán đã chọn
    if algorithm == "KNN":
        model = KNeighborsRegressor(n_neighbors=3, p=2)
    elif algorithm == "Linear Regression":
        model = LinearRegression()
    elif algorithm == "Decision Tree":
        model = DecisionTreeRegressor()
    elif algorithm == "SVM":
        model = SVR()

    # Huấn luyện mô hình
    model.fit(X_train, y_train)

    # Tính toán sai số
    y_predict = model.predict(X_test)
    mse = mean_squared_error(y_test, y_predict)
    mae = mean_absolute_error(y_test, y_predict)
    rmse = np.sqrt(mse)

    # Lưu thông số sai số cho thuật toán
    error_metrics[algorithm] = {'MSE': mse, 'MAE': mae, 'RMSE': rmse}

    messagebox.showinfo("Training", f"Model ({algorithm}) trained successfully!")

# Hàm kiểm tra và hiển thị sai số, đồ thị
def test_model():
    if X_test is None or y_test is None:
        messagebox.showerror("Test Error", "Please train the model first.")
        return

    # Dự đoán trên tập test
    y_predict = model.predict(X_test)

    # Vẽ biểu đồ scatter
    plt.figure(figsize=(10, 6))

    # Vẽ các điểm dự đoán trên tập test
    plt.scatter(range(len(y_predict)), y_predict, label="Predicted Potability", color='blue')

    # Đánh dấu điểm mới vừa kiểm tra (giả sử dự đoán cho 1 dữ liệu cụ thể)
    plt.scatter(len(y_predict), y_predict[-1], color='red', marker='x', label="New Prediction")

    # Đặt tên cho trục và tiêu đề
    plt.xlabel("Index")
    plt.ylabel("Predicted Potability")
    plt.title("Scatter Plot of Test Predictions")

    # Thêm đường phân cách 0.5 để phân loại nước uống được hay không
    plt.axhline(0.5, color='black', linestyle='--', label="Threshold (0.5)")

    # Thêm chú thích
    plt.legend()

    # Hiển thị biểu đồ
    plt.show()

    # Hiển thị sai số
    mse = mean_squared_error(y_test, y_predict)
    mae = mean_absolute_error(y_test, y_predict)
    rmse = np.sqrt(mse)
    result_text.set(f"MSE: {mse:.2f}, MAE: {mae:.2f}, RMSE: {rmse:.2f}")

# Hàm dự đoán dữ liệu mới
def predict_new():
    global model  # Thêm global để đảm bảo model có thể được truy cập trong hàm
    try:
        if model is None:
            messagebox.showerror("Prediction Error", "Please train the model first.")
            return

        # Lấy dữ liệu nhập từ giao diện và chuyển thành float
        hours_studied = float(entry_hours_studied.get() or 0)
        previous_scores = float(entry_previous_scores.get() or 0)
        extracurricular_activities = float(entry_extracurricular_activities.get() or 0)
        sleep_hours = float(entry_sleep_hours.get() or 0)
        sample_question_papers_practiced = float(entry_sample_question_papers_practiced.get() or 0)
        conductivity = float(entry_conductivity.get() or 0)
        organic_carbon = float(entry_organic_carbon.get() or 0)
        trihalomethanes = float(entry_trihalomethanes.get() or 0)
        turbidity = float(entry_turbidity.get() or 0)

        # Kiểm tra giá trị âm
        inputs = [hours_studied, previous_scores, extracurricular_activities, sleep_hours,
                  sample_question_papers_practiced, conductivity, organic_carbon, trihalomethanes, turbidity]
        if any(val < 0 for val in inputs):
            raise ValueError("Input values cannot be negative.")

        # Chuẩn bị dữ liệu đầu vào
        new_student_data = pd.DataFrame([inputs],
                                        columns=['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulface',
                                                 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity'])

        # Dự đoán kết quả
        predicted_performance = model.predict(new_student_data)

        # Kiểm tra nếu giá trị dự đoán lớn hơn 0.5
        if predicted_performance[0] > 0.5:  # Nếu giá trị dự đoán lớn hơn 0.5
            messagebox.showinfo("Prediction", f"Nước uống được! Predicted Potability: 1")
        else:
            messagebox.showinfo("Prediction", f"Nước không uống được. Predicted Potability: 0")

        # Vẽ biểu đồ với điểm mới
        plt.figure(figsize=(10, 6))
        plt.scatter(range(len(y_test)), y_predict, label="Test Predictions", color='blue')  # Dự đoán cho test
        plt.scatter(len(y_test), predicted_performance, color='red', marker='x', label="New Prediction")  # Dự đoán mới
        plt.axhline(0.5, color='black', linestyle='--', label="Threshold (0.5)")
        plt.xlabel("Index")
        plt.ylabel("Predicted Potability")
        plt.title("Scatter Plot with New Prediction")
        plt.legend()
        plt.show()

    except ValueError as ve:
        messagebox.showerror("Input Error", f"Error: {ve}")


# Tạo giao diện với tkinter
root = tk.Tk()
root.title("Water Potability Predictor")

# Tạo các nút và giao diện cho các phần khác nhau
tk.Button(root, text="Load Data", command=load_data).grid(row=0, column=0)

# Tùy chọn thuật toán
selected_algorithm = tk.StringVar(value="KNN")
tk.Label(root, text="Select Algorithm:").grid(row=1, column=0)
tk.Radiobutton(root, text="KNN", variable=selected_algorithm, value="KNN").grid(row=2, column=0)
tk.Radiobutton(root, text="Linear Regression", variable=selected_algorithm, value="Linear Regression").grid(row=3, column=0)
tk.Radiobutton(root, text="Decision Tree", variable=selected_algorithm, value="Decision Tree").grid(row=4, column=0)
tk.Radiobutton(root, text="SVM", variable=selected_algorithm, value="SVM").grid(row=5, column=0)

# Nút huấn luyện mô hình
tk.Button(root, text="Train Model", command=train_model).grid(row=6, column=0)

# Nút kiểm tra mô hình
tk.Button(root, text="Test Model", command=test_model).grid(row=7, column=0)

# Các ô nhập liệu cho dữ liệu mới
tk.Label(root, text="Hours Studied:").grid(row=8, column=0)
entry_hours_studied = tk.Entry(root)
entry_hours_studied.grid(row=8, column=1)

tk.Label(root, text="Previous Scores:").grid(row=9, column=0)
entry_previous_scores = tk.Entry(root)
entry_previous_scores.grid(row=9, column=1)

tk.Label(root, text="Extracurricular Activities:").grid(row=10, column=0)
entry_extracurricular_activities = tk.Entry(root)
entry_extracurricular_activities.grid(row=10, column=1)

tk.Label(root, text="Sleep Hours:").grid(row=11, column=0)
entry_sleep_hours = tk.Entry(root)
entry_sleep_hours.grid(row=11, column=1)

tk.Label(root, text="Sample Question Papers Practiced:").grid(row=12, column=0)
entry_sample_question_papers_practiced = tk.Entry(root)
entry_sample_question_papers_practiced.grid(row=12, column=1)

tk.Label(root, text="Conductivity:").grid(row=13, column=0)
entry_conductivity = tk.Entry(root)
entry_conductivity.grid(row=13, column=1)

tk.Label(root, text="Organic Carbon:").grid(row=14, column=0)
entry_organic_carbon = tk.Entry(root)
entry_organic_carbon.grid(row=14, column=1)

tk.Label(root, text="Trihalomethanes:").grid(row=15, column=0)
entry_trihalomethanes = tk.Entry(root)
entry_trihalomethanes.grid(row=15, column=1)

tk.Label(root, text="Turbidity:").grid(row=16, column=0)
entry_turbidity = tk.Entry(root)
entry_turbidity.grid(row=16, column=1)

# Nút dự đoán
tk.Button(root, text="Predict", command=predict_new).grid(row=17, column=0)

# Label hiển thị kết quả sai số
result_text = tk.StringVar()
tk.Label(root, textvariable=result_text).grid(row=18, column=0, columnspan=2)

root.mainloop()
