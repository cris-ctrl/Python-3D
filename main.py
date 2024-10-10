from ursina import *
app = Ursina()

class Test_cube(Entity):
    def __init__(self):
        super().__init__(
            model = 'cube',
            color = color.white,
            texture = 'white_cube',
            rotation = Vec3(45,45,45)
        )

class Test_button(Button):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'cube',
            texture = 'brick',
            color = color.blue,
            highlight_color = color.red,
            pressed_color = color.green
        )
    def input(self,key):
        if self.hovered:
            if key == 'left mouse down':
                print("Pressed!!!")

def update():
    if held_keys['a']:
        test_square.x -= 4 * time.dt

#test_square = Entity(model = 'cube', color =  color.red)
#grass = Entity(model = "quad", texture='assets/grass_side.png')

test_cube = Test_cube()
test_cube.position = Vec3(5,0,5)
test_button = Test_button()
app.run()


