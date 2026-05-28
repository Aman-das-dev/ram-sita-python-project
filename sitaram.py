import turtle as tu
from svgpathtools import svg2paths2
from svg.path import parse_path
from tqdm import tqdm

class sketch_from_svg:

    def __init__(self, path, scale=30):
        self.path = path
        self.scale = scale

    def hex_to_rgb(self, string):
        strlen = len(string)
        if string.startswith('#'):
            if strlen == 7:
                r = string[1:3]
                g = string[3:5]
                b = string[5:7]
            elif strlen == 4:
                r = string[1:2]*2
                g = string[2:3]*2
                b = string[3:4]*2
        elif strlen == 3:
            r = string[0:1]*2
            g = string[1:2]*2
            b = string[2:3]*2
        else:
            r = string[0:2]
            g = string[2:4]
            b = string[4:6]
        
        return int(r,16)/255, int(g,16)/255, int(b,16)/255

    def load_svg(self):
        print('Loading SVG data...')
        paths, attributes, svg_att = svg2paths2(self.path)
        self.height = float(svg_att.get("height", "1000").replace("px", ""))
        self.width = float(svg_att.get("width", "1000").replace("px", ""))

        res = []
        for i in tqdm(attributes):
            path = parse_path(i['d'])
            col = self.hex_to_rgb(i['fill'])
            n = len(list(path)) + 2
            pts = [
                (float(p.real), float(p.imag))
                for p in (path.point(i / n) for i in range(0, n + 1))
            ]
            res.append((pts, col))
        print('SVG data loaded successfully.')
        return res

    def move_to(self, x, y):
        self.pen.up()
        self.pen.goto(x, y)
        self.pen.down()

    def draw(self, retain=True):
        coordinates = self.load_svg()
        self.pen = tu.Turtle()
        self.pen.speed(0)
        tu.bgcolor("white")

        # Calculate center offset
        x_center = -self.width * self.scale / (2 * self.width)
        y_center = self.height * self.scale / (2 * self.height)

        for path_col in coordinates:
            f = True
            path, col = path_col
            self.pen.color(col)
            self.pen.begin_fill()
            for coord in path:
                x = (coord[0] / self.width) * self.scale - self.scale / 2 + x_center
                y = -(coord[1] / self.height) * self.scale + self.scale / 2 + y_center
                if f:
                    self.move_to(x, y)
                    f = False
                else:
                    self.pen.goto(x, y)
            self.pen.end_fill()

        if retain:
            tu.done()

# ✅ Centered Drawing
pen = sketch_from_svg('ram sita python project/sitaram.svg', scale=180)
pen.draw()
