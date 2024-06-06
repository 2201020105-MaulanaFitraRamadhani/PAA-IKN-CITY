import pygame
import random

# Konfigurasi ukuran kanvas dan ukuran cell
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
CANVAS_MARGIN = 15  
CELL_SIZE = 24
MIN_SIZE = 70
ROAD_WIDTH = 5
EDGE_WIDTH = 10  # Lebar garis tepi putih

# Warna
GREEN = (0, 128, 0)
LIGHT_GRAY = (192, 192, 192)
WHITE = (255, 255, 255)

# Kelas Node
class Node:
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

                left_child = Node(self.x, self.y, split_x - self.x, self.height, self.level + 1)
                right_child = Node(split_x, self.y, self.width - (split_x - self.x), self.height, self.level + 1)

                # Menentukan titik belokan vertikal
                turn_x = random.randint(self.x, split_x)
                turn_y = self.y + random.randint(0, self.height)
                self.turn_point = (turn_x, turn_y)

                left_child.bottom_right = right_child.bottom_left = self.turn_point

                self.children.extend([left_child, right_child])
            elif orientation == 'horizontal' and self.height > MIN_SIZE * 2:
                split_y = self.y + random.randint(MIN_SIZE, self.height - MIN_SIZE)

                top_child = Node(self.x, self.y, self.width, split_y - self.y, self.level + 1)
                bottom_child = Node(self.x, split_y, self.width, self.height - (split_y - self.y), self.level + 1)

                # Menentukan titik belokan horizontal
                turn_x = self.x + random.randint(0, self.width)
                turn_y = random.randint(self.y, split_y)
                self.turn_point = (turn_x, turn_y)

                top_child.bottom_right = bottom_child.top_left = self.turn_point

                self.children.extend([top_child, bottom_child])

            for child in self.children:
                child.split()

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
def create_map(surface):
    root = Node(CANVAS_MARGIN, CANVAS_MARGIN, CANVAS_WIDTH - 2 * CANVAS_MARGIN, CANVAS_HEIGHT - 2 * CANVAS_MARGIN, 0)
    root.split()

    tree = BSPTree(root)
    tree_leaves = tree.get_leaves()

    for leaf in tree_leaves:
        leaf.draw_rect(surface)

    # Menggambar garis tepi putih di tepi canvas
    pygame.draw.rect(surface, WHITE, (0, 0, CANVAS_WIDTH, CANVAS_HEIGHT), EDGE_WIDTH)

# Fungsi untuk menggambar rumah
def draw_home(surface, image, position):
    surface.blit(image, position)

# Inisialisasi Pygame
pygame.init()
screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
pygame.display.set_caption("BSP Map")

## Muat gambar rumah
#home_image = pygame.image.load('objek/home.jpg')
#home_image = pygame.transform.scale(home_image, (CELL_SIZE * 2, CELL_SIZE * 2))  # Mengubah ukuran gambar sesuai kebutuhan

# Membuat peta
create_map(screen)

# Menggambar rumah di titik merah sesuai gambar yang Anda unggah
#home_positions = [
#    (150, 150),  # Koordinat titik merah pertama
#    (300, 150),  # Koordinat titik merah kedua
#    (450, 150),  # Koordinat titik merah ketiga
#    (150, 450),  # Koordinat titik merah keempat
#    (450, 450)   # Koordinat titik merah kelima
#]

# Menggambar rumah di titik-titik yang telah ditentukan
#for position in home_positions:
#    draw_home(screen, home_image, position)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()