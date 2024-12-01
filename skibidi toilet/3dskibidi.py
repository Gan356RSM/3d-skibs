from direct.showbase.ShowBase import ShowBase
from random import randint
import math

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.texture = loader.loadTexture("block.png")
        
        #for i in range(28):
            #for j in range(36):   
                #self.add_block((j - 18, 20, i - 14), (j*0.01, j*0.01, j*0.01 ,1))
        self.add_block((0, 20, 0), (0.5, 0.5, 0.5, 1))
        self.player = self.add_block((0, 0, 0), (0., 0., 0., 0.))  
        base.camera.reparentTo(self.player)
        base.camera.setPos((0, 0, 0))
        
        self.keymap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False
        }
        
        base.accept('w', self.update_keymap, ["forward", True])
        base.accept('w-up', self.update_keymap, ["forward", False])
        base.accept('s', self.update_keymap, ["backward", True])
        base.accept('s-up', self.update_keymap, ["backward", False])
        base.accept('a', self.update_keymap, ["left", True])
        base.accept('a-up', self.update_keymap, ["left", False])
        base.accept('d', self.update_keymap, ["right", True])
        base.accept('d-up', self.update_keymap, ["right", False])
        
        taskMgr.add(self.update_game, "update")
        
    def update_keymap(self, key, value):
        self.keymap[key] = value
        print(self.keymap)

    def update_game(self, task):
        if self.keymap["forward"]:
            self.move_forward()
        if self.keymap["backward"]:
            self.move_backward()
        if self.keymap["left"]:
            self.move_left()
        if self.keymap["right"]:
            self.move_right()

    
        return task.cont
    
    def move_forward(self):
        x = self.player.getX()
        y = self.player.getY()
        rad = math.radians(self.player.getH())
        dx = -math.sin(rad) * 0.1
        dy = math.cos(rad) * 0.1
        self.player.setPos((x + dx, y + dy, 0))
        
    def move_backward(self):
        x = self.player.getX()
        y = self.player.getY()
        rad = math.radians(self.player.getH())
        dx = math.sin(rad) * 0.1
        dy = -math.cos(rad) * 0.1
        self.player.setPos((x + dx, y + dy, 0))
        
    def move_left(self):
        x = self.player.getX()
        y = self.player.getY()
        rad = math.radians(self.player.getH() + 90)
        dx = math.sin(rad) * 0.1
        dy = -math.cos(rad) * 0.1
        self.player.setPos((x + dx, y + dy, 0))
        
    def move_right(self):
        x = self.player.getX()
        y = self.player.getY()
        rad = math.radians(self.player.getH() + 90)
        dx = -math.sin(rad) * 0.1
        dy = math.cos(rad) * 0.1
        self.player.setPos((x + dx, y + dy, 0))
         
    def add_block(self, pos, color):
        block = loader.loadModel("block")
        block.setTexture(self.texture)
        block.setPos(pos)
        block.setColor(color)
        block.reparentTo(render)
        return block
        

game = Game()
game.run()