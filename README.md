# BÀI TẬP LỚN CẤU TRÚC RỜI RẠC  
Ứng dụng trực quan hóa và xử lý thuật toán đồ thị

## Thông tin môn học
- **Môn học**: Cấu trúc rời rạc
- **Giảng viên**: Bùi Trọng Hiếu
- **Trường**: Đại học Giao Thông Vận Tải TP. Hồ Chí Minh
- **Viện**: Khoa học Công nghệ Thông tin
- **Nhóm**: 08

---

## Mô tả đề tài
Đề tài xây dựng một **ứng dụng trực quan hóa đồ thị** nhằm hỗ trợ việc học và hiểu các thuật toán trong môn Cấu trúc rời rạc.

Chương trình được phát triển bằng **Python** kết hợp với **Tkinter**, cho phép người dùng:
- Tạo và chỉnh sửa đồ thị trực tiếp trên giao diện
- Áp dụng các thuật toán đồ thị phổ biến
- Quan sát quá trình chạy thuật toán thông qua hiệu ứng trực quan

---

## Công nghệ sử dụng
- **Ngôn ngữ**: Python
- **Thư viện giao diện**: Tkinter
- **Lưu trữ dữ liệu**: JSON
- **Kiến thức áp dụng**: Lý thuyết đồ thị, thuật toán đồ thị

---

## Chức năng chính

### Xây dựng và thao tác đồ thị
- Thêm, xóa đỉnh và cạnh bằng chuột
- Hỗ trợ:
  - Đồ thị có hướng / vô hướng
  - Đồ thị có trọng số / không trọng số
- Kéo thả đỉnh để thay đổi vị trí
- Xóa đỉnh và tự động cập nhật các cạnh liên quan

### Lưu và tải đồ thị
- Lưu đồ thị dưới dạng file JSON
- Tải lại đồ thị đã lưu để tiếp tục xử lý

### Biểu diễn đồ thị
- Ma trận kề
- Danh sách kề
- Danh sách cạnh

---

## Các thuật toán đã cài đặt

### Thuật toán cơ bản
- **BFS (Tìm kiếm theo chiều rộng)**
- **DFS (Tìm kiếm theo chiều sâu)**

### Đường đi ngắn nhất
- **Dijkstra**
- **Đường đi ngắn nhất bằng BFS (đồ thị không trọng số)**

### Tính chất đồ thị
- **Kiểm tra đồ thị hai phía (Bipartite)**

### Cây khung nhỏ nhất
- **Prim**
- **Kruskal**

### Chu trình và đường đi Euler
- **Fleury**
- **Hierholzer**

### Bài toán luồng cực đại
- **Ford–Fulkerson (phiên bản Edmonds–Karp)**

Tất cả các thuật toán đều được **mô phỏng trực quan** bằng cách thay đổi màu sắc của đỉnh và cạnh theo từng bước.

---

## Kiến trúc chương trình
Chương trình được tổ chức xoay quanh lớp chính `GraphVisualizer`, đảm nhiệm:
- Quản lý dữ liệu đồ thị
- Xử lý sự kiện giao diện người dùng
- Thực thi các thuật toán
- Hiển thị kết quả trực quan

Hệ thống gồm 3 thành phần chính:
1. Giao diện người dùng
2. Quản lý dữ liệu đồ thị
3. Xử lý thuật toán

---

## Thành viên nhóm và phân công công việc

| Họ và tên | Phần đảm nhiệm |
|---------|---------------|
| **Chúc Mạnh Cường** | Đồ thị hai phía, thuật toán Fleury |
| **Lê Trần Đăng Khoa** | Biểu diễn đồ thị, Hierholzer |
| **Ngô Vinh Phát** | BFS, DFS, Prim |
| **Võ Thái Khang** | Animation Engine, Ford–Fulkerson (một phần) |
| **Nguyễn Huỳnh Anh Tuấn** | Lưu / tải đồ thị |
| **Lê Thị Thu Nga** | Đường đi ngắn nhất, Kruskal |
| **Trần Thị Như Quỳnh** | Vẽ đồ thị |

---

## Hướng dẫn chạy chương trình
1. Cài đặt Python
2. Clone repository:
   ```bash
   git clone https://github.com/ManhCuong150206/discrete-mathematics-final-project
