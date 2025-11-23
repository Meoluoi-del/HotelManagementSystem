import random
from math import sin, cos, pi, log
from tkinter import *

# --- 1. Cấu Hình Ban Đầu ---
CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 11
HEART_COLOR = "#ff2121" # Màu đỏ Trung Quốc

# --- 2. Hàm Tạo Hình Trái Tim ---
def heart_function(t, shrir_ratio):
    """
    "Ái tâm hàm số sinh thành"
    :param shrir_ratio: phóng đại tỉ lệ
    :param t: tham số
    :return: tọa độ
    """
    # # Cơ sở hàm
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))

    # # Phóng đại
    x *= shrir_ratio
    y *= shrir_ratio

    # # Di chuyển đến trung tâm canvas
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
    
    return x, y

# --- 3. Các Hàm Hiệu Ứng Phụ ---
def curve(p):
    """
    "Tùy chỉnh hàm đường cong, điều chỉnh chu kỳ rung lắc"
    :param p: tham số
    :return: hình Sin
    # Có thể thử thay thế các hàm động khác để đạt được hiệu ứng mạnh hơn (Bezier?)
    """
    return 2 * (sin(4 * p)) / (2 * pi)

def scatter_inside(x, y, beta=0.15):
    """
    "Ngẫu nhiên nội bộ khuếch tán"
    :param x: tọa độ x
    :param y: tọa độ y
    :param beta: cường độ
    :return: tọa độ mới
    """
    ratio_x = beta * log(random.random())
    ratio_y = beta * log(random.random())
    
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    
    return int(x - dx), int(y - dy)

def shrink(x, y, ratio):
    """
    "Rung lắc"
    :param x: tọa độ x
    :param y: tọa độ y
    :param ratio: tỉ lệ
    :return: tọa độ mới
    """
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    
    return x - dx, y - dy

# --- 4. Lớp Chính `Heart` ---
class Heart:
    """
    "Ái tâm loại"
    """
    def __init__(self, generate_frame=20):
        self._points = set() # Tập hợp tọa độ điểm gốc
        self._edge_diffusion_points = set() # Tập hợp tọa độ điểm khuếch tán cạnh
        self._center_diffusion_points = set() # Tập hợp tọa độ điểm khuếch tán trung tâm
        self.all_points = {} # Tọa độ động mỗi khung hình
        
        self.build(2000)
        self.random_halo = 1000
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        # # Ái tâm điểm
        for _ in range(number):
            # Chọn t ngẫu nhiên từ 0 đến 2*pi để tạo lỗ hổng trên trái tim
            t = random.uniform(0, 2 * pi) 
            x, y = heart_function(t, IMAGE_ENLARGE)
            self._points.add((x, y))
        
        # # Ái tâm nội khuếch tán (Khuếch tán cạnh)
        point_list = list(self._points)
        for x, y in point_list:
            for _ in range(3):
                # Khuếch tán ngẫu nhiên một chút
                _x, _y = scatter_inside(x, y, 0.05) 
                self._edge_diffusion_points.add((_x, _y))
        
        # # Ái tâm nội lại khuếch tán (Khuếch tán trung tâm)
        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            _x, _y = scatter_inside(x, y, 0.17) # Khuếch tán sâu hơn
            self._center_diffusion_points.add((_x, _y))

    @staticmethod
    def calc_position(x, y, ratio):
        # Tính toán vị trí điểm ảnh cuối cùng (Ảnh 5 trong bản gốc)
        
        # Tham số ma thuật (0.520 - ý nghĩa "Tôi Yêu Em")
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520) 
        
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
        
        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * pi) # Tỷ lệ phóng đại tuần hoàn
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi))) # Bán kính quầng sáng
        
        all_points = []
        
        # # Quầng sáng
        # Tạo số lượng quầng sáng ngẫu nhiên dựa trên nhịp đập
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))
        
        heart_halo_point = set() # Tập hợp điểm quầng sáng
        for _ in range(halo_number):
            # Chọn t ngẫu nhiên để tạo lỗ hổng
            t = random.uniform(0, 2 * pi) 
            x, y = heart_function(t, IMAGE_ENLARGE + halo_radius) # Vị trí rộng hơn
            
            # Tránh điểm trùng lặp
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                # # Xử lý điểm mới
                x += random.randint(-14, 14) 
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

        # # Luân Khuếch Tán (Đường viền)
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        # # Nội dung (Khuếch tán cạnh)
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        # # Nội dung (Khuếch tán trung tâm)
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame % self.generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        # Lấy tập hợp điểm động cho khung hình hiện tại
        all_points = self.all_points[render_frame % self.generate_frame]
        
        for x, y, size in all_points:
            # Vẽ hình chữ nhật (pixel)
            render_canvas.create_rectangle(int(x), int(y), int(x + size), int(y + size), width=0, fill=HEART_COLOR)


# --- 5. Vòng Lặp Hoạt Ảnh và Chạy Chương Trình ---

def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    render_canvas.delete("all")  # Xóa toàn bộ nội dung canvas

    render_heart.render(render_canvas, render_frame)
    
    # Lặp lại hàm draw sau 160ms (tạo tốc độ khung hình)
    main.after(160, draw, main, render_canvas, render_heart, render_frame + 1) 

if __name__ == '__main__':
    root = Tk() # # Một TK
    root.title("521 Heart Code")
    root.resizable(False, False)

    # # Tạo canvas
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()

    # # Tâm
    heart = Heart() 
    
    # # Bắt đầu vẽ
    draw(root, canvas, heart) 
    
    root.mainloop()