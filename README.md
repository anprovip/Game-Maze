# Maze Game

![Maze Game Logo](assets/img/icon.png)

## Giới thiệu

Maze Game là một trò chơi mê cung 2D với đồ họa đơn giản, được phát triển bằng Python với thư viện Pygame. Người chơi sẽ di chuyển trong mê cung để tìm ra lối thoát, với nhiều chế độ chơi khác nhau và độ khó đa dạng.

## Tính năng

- **Ba chế độ chơi:**
  - Chế độ 1 người: Tìm đường đi trong thời gian giới hạn
  - Chế độ 2 người: Thi đấu với người chơi khác để tìm ra đường đi trước
  - Chế độ chơi với AI: Đấu với AI để xem ai tìm ra lối thoát trước

- **Ba mức độ khó:** 
  - Dễ: Giới hạn thời gian dài
  - Trung bình: Giới hạn số bước di chuyển
  - Khó: Giới hạn cả thời gian và số bước di chuyển

- **Đa dạng thuật toán tạo mê cung:**
  - Thuật toán DFS (Depth-First Search)
  - Thuật toán Kruskal
  - Thuật toán Prim

- **Hiệu ứng đồ họa và âm thanh:**
  - Hiệu ứng tạo mê cung
  - Âm thanh nền và hiệu ứng

## Điều khiển

- **Người chơi 1:**
  - Di chuyển bằng các phím mũi tên: ↑, ↓, ←, →
  
- **Người chơi 2:**
  - Di chuyển bằng các phím W, A, S, D

- **Phím chức năng:**
  - Q: Hiển thị gợi ý đường đi (chỉ chế độ 1 người)
  - R: Tạo mới mê cung
  - ESC: Tạm dừng game

## Cài đặt

### Yêu cầu

- Python 3.6 trở lên
- Pygame 2.0.0 trở lên

### Cài đặt thư viện

```bash
# Cài đặt Pygame
pip install pygame
```

### Chạy game

```bash
# Clone repository (nếu chưa có)
git clone https://github.com/your-username/Game-Maze.git
cd Game-Maze

# Chạy game trên Windows
python src/main.py

# Chạy game trên Linux hoặc macOS
python3 src/main.py
```

## Luật chơi

- Cố gắng tìm đường đến đích bằng cách di chuyển hợp lý để lấy được kho báu của mê cung
- Không thể đi qua tường
- Chế độ 1 người: Tìm đường đi trong thời gian hoặc số bước giới hạn
- Chế độ 2 người: Ai đến đích trước sẽ thắng
- Chế độ với AI: Đua với AI để đến đích trước



## Tác giả

Nhóm 03 lớp AIAI KHMT-K63

---

*Lưu ý: Dự án này được xây dựng chủ yếu cho mục đích học tập và giải trí.*
