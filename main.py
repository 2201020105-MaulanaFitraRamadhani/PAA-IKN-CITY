import pygame
import random

# Konfigurasi ukuran kanvas dan ukuran cell
NUM_CELLS_X = 150
NUM_CELLS_Y = 150
CELL_SIZE = 24
CANVAS_WIDTH = NUM_CELLS_X * CELL_SIZE
CANVAS_HEIGHT = NUM_CELLS_Y * CELL_SIZE
VIEWPORT_WIDTH = 600
VIEWPORT_HEIGHT = 600
CANVAS_MARGIN = 0  
MIN_SIZE = 70
ROAD_WIDTH = 5
EDGE_WIDTH = 10  # Lebar garis tepi putih
DASH_LENGTH = 5  # Panjang setiap dash
GAP_LENGTH = 5   # Panjang setiap gap

# Warna
GREEN = (0, 128, 0)
LIGHT_GRAY = (192, 192, 192)
WHITE = (255, 255, 255)

# Kelas Jalan
class Jalan:
    def __init__(self, x, y, width, height, level):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cell_size = CELL_SIZE
        self.road_width = ROAD_WIDTH
        self.edge_width = EDGE_WIDTH
        self.level = level
        self.children = []

        # Menghitung koordinat sudut dalam
        self.top_left = (self.x + self.road_width, self.y + self.road_width)
        self.top_right = (self.x + self.width - self.road_width, self.y + self.road_width)
        self.bottom_right = (self.x + self.width - self.road_width, self.y + self.height - self.road_width)
        self.bottom_left = (self.x + self.road_width, self.y + self.road_width)

        # Menentukan titik untuk belokan
        self.turn_point = None

    def split(self):
        if self.width > MIN_SIZE * 2 or self.height > MIN_SIZE * 2:
            orientation = random.choice(['vertical', 'horizontal'])

            if orientation == 'vertical' and self.width > MIN_SIZE * 2:
                split_x = self.x + random.randint(MIN_SIZE, self.width - MIN_SIZE)

                left_child = Jalan(self.x, self.y, split_x - self.x, self.height, self.level + 1)
                right_child = Jalan(split_x, self.y, self.width - (split_x - self.x), self.height, self.level + 1)

                # Menentukan titik belokan vertikal
                turn_x = random.randint(self.x, split_x)
                turn_y = self.y + random.randint(0, self.height)
                self.turn_point = (turn_x, turn_y)

                left_child.bottom_right = right_child.bottom_left = self.turn_point

                self.children.extend([left_child, right_child])
            elif orientation == 'horizontal' and self.height > MIN_SIZE * 2:
                split_y = self.y + random.randint(MIN_SIZE, self.height - MIN_SIZE)

                top_child = Jalan(self.x, self.y, self.width, split_y - self.y, self.level + 1)
                bottom_child = Jalan(self.x, split_y, self.width, self.height - (split_y - self.y), self.level + 1)

                # Menentukan titik belokan horizontal
                turn_x = self.x + random.randint(0, self.width)
                turn_y = random.randint(self.y, split_y)
                self.turn_point = (turn_x, turn_y)

                top_child.bottom_right = bottom_child.top_left = self.turn_point

                self.children.extend([top_child, bottom_child])

            for child in self.children:
                child.split()

    def draw_dashed_line(self, surface, color, start_pos, end_pos, width=1, dash_length=10, gap_length=5):
        x1, y1 = start_pos
        x2, y2 = end_pos

        if x1 == x2:  # vertical dashed line
            y_coords = range(y1, y2, dash_length + gap_length)
            for y in y_coords:
                if y + dash_length > y2:
                    dash_length = y2 - y
                pygame.draw.line(surface, color, (x1, y), (x2, y + dash_length), width)
        elif y1 == y2:  # horizontal dashed line
            x_coords = range(x1, x2, dash_length + gap_length)
            for x in x_coords:
                if x + dash_length > x2:
                    dash_length = x2 - x
                pygame.draw.line(surface, color, (x, y1), (x + dash_length, y2), width)

    def draw_rect(self, surface):
        # Menggambar latar belakang hijau untuk setiap node
        pygame.draw.rect(surface, GREEN, (self.x, self.y, self.width, self.height))

        # Menggambar garis tepi putih di sekitar node
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height), self.edge_width)

        # Menggambar jalan di sekitar node
        pygame.draw.rect(surface, LIGHT_GRAY, (self.x, self.y, self.width, self.road_width))  # Atas
        pygame.draw.rect(surface, LIGHT_GRAY, (self.x, self.y + self.height - self.road_width, self.width, self.road_width))  # Bawah
        pygame.draw.rect(surface, LIGHT_GRAY, (self.x, self.y, self.road_width, self.height))  # Kiri
        pygame.draw.rect(surface, LIGHT_GRAY, (self.x + self.width - self.road_width, self.y, self.road_width, self.height))  # Kanan

        # Menggambar titik belokan
        if self.turn_point:
            pygame.draw.circle(surface, LIGHT_GRAY, self.turn_point, 3)

        # Menggambar tikungan di sepanjang garis
        if self.width > MIN_SIZE * 2 and self.height > MIN_SIZE * 2:
            pygame.draw.rect(surface, LIGHT_GRAY, (self.x, self.y, self.road_width, self.height))  # Vertikal kiri
            pygame.draw.rect(surface, LIGHT_GRAY, (self.x + self.width - self.road_width, self.y, self.road_width, self.height))  # Vertikal kanan
            pygame.draw.rect(surface, LIGHT_GRAY, (self.x, self.y, self.width, self.road_width))  # Horizontal atas
            pygame.draw.rect(surface, LIGHT_GRAY, (self.x, self.y + self.height - self.road_width, self.width, self.road_width))  # Horizontal bawah

        # Menggambar jalan di tepi-tepi petak kanvas
        pygame.draw.rect(surface, LIGHT_GRAY, (self.x - self.road_width, self.y, self.road_width, self.height))  # Tepi kiri
        pygame.draw.rect(surface, LIGHT_GRAY, (self.x + self.width, self.y, self.road_width, self.height))  # Tepi kanan
        pygame.draw.rect(surface, LIGHT_GRAY, (self.x, self.y - self.road_width, self.width, self.road_width))  # Tepi atas
        pygame.draw.rect(surface, LIGHT_GRAY, (self.x, self.y + self.height, self.width, self.road_width))  # Tepi bawah

        # Menggambar petak kecil putih di depan jalan abu-abu
        self.draw_dashed_line(surface, WHITE, (self.x + self.road_width, self.y), (self.x + self.width - self.road_width, self.y), width=1, dash_length=DASH_LENGTH, gap_length=GAP_LENGTH)  # Atas
        self.draw_dashed_line(surface, WHITE, (self.x + self.road_width, self.y + self.height), (self.x + self.width - self.road_width, self.y + self.height), width=1, dash_length=DASH_LENGTH, gap_length=GAP_LENGTH)  # Bawah
        self.draw_dashed_line(surface, WHITE, (self.x, self.y + self.road_width), (self.x, self.y + self.height - self.road_width), width=1, dash_length=DASH_LENGTH, gap_length=GAP_LENGTH)  # Kiri
        self.draw_dashed_line(surface, WHITE, (self.x + self.width, self.y + self.road_width), (self.x + self.width, self.y + self.height - self.road_width), width=1, dash_length=DASH_LENGTH, gap_length=GAP_LENGTH)  # Kanan

    def draw_home(self, surface, home_image):
        # Pastikan gambar rumah berada di dalam node hijau dengan margin dari jalan
        home_width, home_height = home_image.get_size()
        max_x = self.x + self.width - self.road_width - home_width
        min_x = self.x + self.road_width
        max_y = self.y + self.height - self.road_width - home_height
        min_y = self.y + self.road_width

        if max_x > min_x and max_y > min_y:
            home_x = random.randint(min_x, max_x)
            home_y = random.randint(min_y, max_y)
            surface.blit(home_image, (home_x, home_y))

    def draw_building(self, surface, building_image):
        # Pastikan gambar gedung berada di dalam node hijau dengan margin dari jalan
        building_width, building_height = building_image.get_size()
        max_x = self.x + self.width - self.road_width - building_width
        min_x = self.x + self.road_width
        max_y = self.y + self.height - self.road_width - building_height
        min_y = self.y + self.road_width

        if max_x > min_x and max_y > min_y:
            building_x = random.randint(min_x, max_x)
            building_y = random.randint(min_y, max_y)
            surface.blit(building_image, (building_x, building_y))

# Kelas BSPTree
class BSPTree:
    def __init__(self, root_node):
        self.root = root_node

    def expand_node(self):
        self.root.split()

    def get_leaves(self):
        tree_leaves = []
        traversal_order = [self.root]

        while traversal_order:
            temp = traversal_order.pop(0)
            if temp.children:
                traversal_order.extend(temp.children)
            else:
                tree_leaves.append(temp)
        return tree_leaves

# Fungsi Utama untuk Membuat Peta
def create_map(surface, home_image):
    root = Jalan(CANVAS_MARGIN, CANVAS_MARGIN, CANVAS_WIDTH - 2 * CANVAS_MARGIN, CANVAS_HEIGHT - 2 * CANVAS_MARGIN, 0)
    root.split()

    tree = BSPTree(root)
    tree_leaves = tree.get_leaves()

    for leaf in tree_leaves:
        leaf.draw_rect(surface)
        leaf.draw_home(surface, home_image)  # Gambar rumah di setiap node

    # Menggambar garis tepi putih di tepi canvas
    pygame.draw.rect(surface, WHITE, (0, 0, CANVAS_WIDTH, CANVAS_HEIGHT), EDGE_WIDTH)

# Inisialisasi Pygame
pygame.init()
screen = pygame.display.set_mode((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))
pygame.display.set_caption("IKN Map")

# Muat gambar rumah
home_image = pygame.image.load('objek/b1.png')
home_image = pygame.transform.scale(home_image, (CELL_SIZE * 10, CELL_SIZE * 5))  # Mengubah ukuran gambar sesuai kebutuhan

# Membuat peta
map_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
create_map(map_surface, home_image)

# Main loop
running = True
x_offset, y_offset = 0, 0
scroll_speed = 2
pressed_keys = set()  # Track pressed keys

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            pressed_keys.discard(event.key)

    # Update offsets based on pressed keys
    if pygame.K_LEFT in pressed_keys:
        x_offset = max(x_offset - scroll_speed, 0)
    if pygame.K_RIGHT in pressed_keys:
        x_offset = min(x_offset + scroll_speed, CANVAS_WIDTH - VIEWPORT_WIDTH)
    if pygame.K_UP in pressed_keys:
        y_offset = max(y_offset - scroll_speed, 0)
    if pygame.K_DOWN in pressed_keys:
        y_offset = min(y_offset + scroll_speed, CANVAS_HEIGHT - VIEWPORT_HEIGHT)

    # Draw the viewport
    screen.blit(map_surface, (0, 0), (x_offset, y_offset, VIEWPORT_WIDTH, VIEWPORT_HEIGHT))
    pygame.display.flip()

pygame.quit()
