from ursina import *
app = Ursina()

def update():
    if held_keys['a']:
        test_square.x -= 4 * time.dt

test_square = Entity(model = 'cube', color =  color.red)


app.run()