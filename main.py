import tkinter as tk
from tkinter import Canvas, Scrollbar, Button
from PIL import Image, ImageDraw, ImageTk
import random

# Constants
CANVAS_WIDTH = 1510  # Adjusted for 150x150 cells (each cell is 10x10 pixels)
CANVAS_HEIGHT = 1510
MIN_SIZE = 150
VIEWPORT_MARGIN = -10  # Margin around the viewport


#def create_placeholder_buildings():
#    # Big building (10x5)
#    big_building = Image.new("RGB", (100, 50), "blue")
#    big_building.save("big_building.png")
#
#    # Medium building (5x3)
#    medium_building = Image.new("RGB", (50, 30), "red")
#    medium_building.save("medium_building.png")
#
#    # Small building (2x2)
#    small_building = Image.new("RGB", (20, 20), "yellow")
#    small_building.save("small_building.png")
#
#    # House (1x2)
#    house = Image.new("RGB", (10, 20), "green")
#    house.save("house.png")
#
#create_placeholder_buildings()

# Jalan Class (BSP Node)
class Jalan:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = None
        self.right = None

    def split(self):
        if self.width > 2 * MIN_SIZE or self.height > 2 * MIN_SIZE:
            if self.width > self.height:
                split_line = random.randint(MIN_SIZE, self.width - MIN_SIZE)
                self.left = Jalan(self.x, self.y, split_line, self.height)
                self.right = Jalan(self.x + split_line, self.y, self.width - split_line, self.height)
            else:
                split_line = random.randint(MIN_SIZE, self.height - MIN_SIZE)
                self.left = Jalan(self.x, self.y, self.width, split_line)
                self.right = Jalan(self.x, self.y + split_line, self.width, self.height - split_line)
            self.left.split()
            self.right.split()

    def draw_rect(self, draw, image):
        green_area = (self.x + 10, self.y + 10, self.x + self.width - 10, self.y + self.height - 10)
        draw.rectangle(green_area, fill="green", outline="white", width=2)  # White stroke
        self.draw_roads(draw)
        self.place_buildings(draw, image, green_area)

    def draw_roads(self, draw):
        road_width = 10
        dash_distance = 0  # Distance from edge of road to dashed line

        # Top road
        draw.rectangle((self.x, self.y, self.x + self.width, self.y + road_width), fill="gray")
        self.draw_dashed_line(draw, (self.x, self.y + dash_distance), (self.x + self.width, self.y + dash_distance))

        # Bottom road
        draw.rectangle((self.x, self.y + self.height - road_width, self.x + self.width, self.y + self.height), fill="gray")
        self.draw_dashed_line(draw, (self.x, self.y + self.height - dash_distance), (self.x + self.width, self.y + self.height - dash_distance))

        # Left road
        draw.rectangle((self.x, self.y, self.x + road_width, self.y + self.height), fill="gray")
        self.draw_dashed_line(draw, (self.x + dash_distance, self.y), (self.x + dash_distance, self.y + self.height))

        # Right road
        draw.rectangle((self.x + self.width - road_width, self.y, self.x + self.width, self.y + self.height), fill="gray")
        self.draw_dashed_line(draw, (self.x + self.width - dash_distance, self.y), (self.x + self.width - dash_distance, self.y + self.height))

    def draw_dashed_line(self, draw, start, end):
        dash_length = 10
        gap_length = 10
        x1, y1 = start
        x2, y2 = end
        total_length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        dashes = int(total_length // (dash_length + gap_length))
        for i in range(dashes):
            start_dash = (
                x1 + (x2 - x1) * (i * (dash_length + gap_length)) / total_length,
                y1 + (y2 - y1) * (i * (dash_length + gap_length)) / total_length,
            )
            end_dash = (
                x1 + (x2 - x1) * ((i * (dash_length + gap_length) + dash_length)) / total_length,
                y1 + (y2 - y1) * ((i * (dash_length + gap_length) + dash_length)) / total_length,
            )
            draw.line([start_dash, end_dash], fill="white", width=2)

    def place_buildings(self, draw, image, green_area):
        building_images = {
            "big_building": Image.open("objek/b1.png"),
            "medium_building": Image.open("objek/b2.png"),
            "small_building": Image.open("objek/b3.png"),
            "house": Image.open("objek/b4.png")
        }
        
        placements = {
            "big_building": (100, 50),
            "medium_building": (50, 30),
            "small_building": (20, 20),
            "house": (10, 20)
        }
        
        placed_rectangles = []

        def can_place(new_rect):
            min_gap = 20  # Minimum gap between buildings
            for rect in placed_rectangles:
                if (
                    new_rect[0] < rect[2] + min_gap and new_rect[2] > rect[0] - min_gap and
                    new_rect[1] < rect[3] + min_gap and new_rect[3] > rect[1] - min_gap
                ):
                    return False
            return True

        def try_place(building_key, count):
            width, height = placements[building_key]
            margin = 10
            for _ in range(count):
                for _ in range(100):  # Try 100 times to place the building
                    x = random.randint(green_area[0] + margin, green_area[2] - width - margin)
                    y = random.randint(green_area[1] + margin, green_area[3] - height - margin)
                    new_rect = (x, y, x + width, y + height)
                    if can_place(new_rect):
                        placed_rectangles.append(new_rect)
                        image.paste(building_images[building_key], (x, y))
                        break

        # Place buildings with the specified ranges
        try_place("big_building", random.randint(1, 1))
        try_place("medium_building", random.randint(4, 4))
        try_place("small_building", random.randint(10, 20))
        try_place("house", random.randint(10, 20))

def create_map():
    # Create a blank canvas
    image = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    # Create the root node and split it
    root = Jalan(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
    root.split()

    # Collect all leaf nodes
    nodes = [root]
    leaves = []
    while nodes:
        node = nodes.pop()
        if node.left and node.right:
            nodes.append(node.left)
            nodes.append(node.right)
        else:
            leaves.append(node)

    # Draw the map sections
    for leaf in leaves:
        leaf.draw_rect(draw, image)

    return image

def update_map(canvas, image):
    map_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=map_image)
    canvas.image = map_image  # Keep reference to avoid garbage collection

def redesign_map(canvas):
    image = create_map()
    update_map(canvas, image)
    # Scroll to the margin position
    canvas.xview_moveto(VIEWPORT_MARGIN / (CANVAS_WIDTH + 2 * VIEWPORT_MARGIN))
    canvas.yview_moveto(VIEWPORT_MARGIN / (CANVAS_HEIGHT + 2 * VIEWPORT_MARGIN))


def main():
    root = tk.Tk()
    root.title("City Map with BSP")

    canvas_frame = tk.Frame(root)
    canvas_frame.pack(fill=tk.BOTH, expand=True)

    hbar = Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
    hbar.pack(side=tk.BOTTOM, fill=tk.X)
    vbar = Scrollbar(canvas_frame, orient=tk.VERTICAL)
    vbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas = Canvas(canvas_frame, width=800, height=600, scrollregion=(-VIEWPORT_MARGIN, -VIEWPORT_MARGIN, CANVAS_WIDTH + VIEWPORT_MARGIN, CANVAS_HEIGHT + VIEWPORT_MARGIN))
    canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    hbar.config(command=canvas.xview)
    vbar.config(command=canvas.yview)
    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

    redesign_button = Button(root, text="Redesign Map", command=lambda: redesign_map(canvas))
    redesign_button.pack()

    # Initial map design
    image = create_map()
    update_map(canvas, image)
    # Scroll to the margin position
    canvas.xview_moveto(VIEWPORT_MARGIN / (CANVAS_WIDTH + 2 * VIEWPORT_MARGIN))
    canvas.yview_moveto(VIEWPORT_MARGIN / (CANVAS_HEIGHT + 2 * VIEWPORT_MARGIN))


    root.mainloop()

if __name__ == "__main__":
    main()
