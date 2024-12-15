from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionNode, CollisionSphere, CollisionBox, WindowProperties
from random import randint
import math

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        wp = WindowProperties()
        base.win.requestProperties(wp)

        base.setBackgroundColor(0, 0, 0)

        base.cTrav = CollisionTraverser()
        pusher = CollisionHandlerPusher()

        base.camLens.setFov(70)
        
        self.texture = loader.loadTexture("block.png")
        
        
        for i in range(49):
            for j in range(49):   
                self.add_block((j, i, -2), (1, 1, 1 ,1), False)

        for i in range(5):
            for j in range(i * 2 + 4):
                for k in range(i * 2 + 4):
                    self.add_block((j - i + 25, k - i + 25, 5 - i - 2), (1, 1, 1 ,1), True)

        base.disableMouse()

        '''
        for i in range(14):
            for j in range(18):   
                self.add_block((j - 9, i - 7, 2), (1, 1, 1 ,1), False)   

        for i in range(5):
            for j in range(18):   
                self.add_block((j - 9, 7, i - 2), (1, 1, 1 ,1), True) 

        for i in range(5):
            for j in range(18):   
                self.add_block((j - 9, -7, i - 2), (1, 1, 1 ,1), True) 
        
        for i in range(5):
            for j in range(18):   
                self.add_block((9, j - 9, i - 2), (1, 1, 1 ,1), True) 

        for i in range(5):
            for j in range(18):   
                self.add_block((-9, j - 9, i - 2), (1, 1, 1 ,1), True) 
        '''

        #self.add_block((0, 20, -1), (0.5, 0.5, 0.5, 1))
        #self.add_block((0, 20, 0), (0.5, 0.5, 0.5, 1))
        self.player = self.add_block((1, 1, 0), (0., 0., 0., 0.), False)  
        
        player_cnode = CollisionNode('player')
        player_cnode.addSolid(CollisionBox((0, 0, 0), 1, 1, 1))
        player_collider = self.player.attachNewNode(player_cnode)
        base.cTrav.addCollider(player_collider, pusher)
        pusher.addCollider(player_collider, self.player)

        

        base.camera.reparentTo(self.player)
        base.camera.setPos((0, 0, 0))
        
        self.keymap = {
            "forward": False,
            "backward": False, 
            "left": False,
            "right": False,
            "turn_left": False,
            "turn_right": False,
            "jump": False
        }

        base.accept('w', self.update_keymap, ["forward", True])
        base.accept('w-up', self.update_keymap, ["forward", False])
        base.accept('s', self.update_keymap, ["backward", True])
        base.accept('s-up', self.update_keymap, ["backward", False])
        base.accept('a', self.update_keymap, ["left", True])
        base.accept('a-up', self.update_keymap, ["left", False])
        base.accept('d', self.update_keymap, ["right", True])
        base.accept('d-up', self.update_keymap, ["right", False])
        base.accept('q', self.update_keymap, ["turn_left", True])
        base.accept('q-up', self.update_keymap, ["turn_left", False])
        base.accept('e', self.update_keymap, ["turn_right", True])
        base.accept('e-up', self.update_keymap, ["turn_right", False])
        base.accept('space', self.jump)

        taskMgr.add(self.update_game, "update")
        self.velocity = 0
        
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
        if self.keymap["turn_left"]:
            self.turn_left()
        if self.keymap["turn_right"]:
            self.turn_right()

        self.velocity -= 0.01
        self.player.setZ(self.player.getZ() + self.velocity)

        if self.player.getZ() <= 0:
            self.player.setZ(0)
    
        return task.cont

    def jump(self):

        self.velocity = 0.2
        

    def move_forward(self):
        x = self.player.getX()
        y = self.player.getY()
        z = self.player.getZ()
        rad = math.radians(base.camera.getH())
        dx = -math.sin(rad) * 0.1
        dy = math.cos(rad) * 0.1
        self.player.setPos((x + dx, y + dy, z))
        
    def move_backward(self):
        x = self.player.getX()
        y = self.player.getY()
        z = self.player.getZ()
        rad = math.radians(base.camera.getH())
        dx = math.sin(rad) * 0.1
        dy = -math.cos(rad) * 0.1
        self.player.setPos((x + dx, y + dy, z))
        
    def move_left(self):
        x = self.player.getX()
        y = self.player.getY()
        z = self.player.getZ()
        rad = math.radians(base.camera.getH() - 90)
        dx = math.sin(rad) * 0.1
        dy = -math.cos(rad) * 0.1
        self.player.setPos((x + dx, y + dy, z))
        
    def move_right(self):
        x = self.player.getX()
        y = self.player.getY()
        z = self.player.getZ()
        rad = math.radians(base.camera.getH() - 90)
        dx = -math.sin(rad) * 0.1
        dy = math.cos(rad) * 0.1
        self.player.setPos((x + dx, y + dy, z))

    def turn_left(self):
        h = base.camera.getH()
        base.camera.setH(h + 1)

    def turn_right(self):
        h = base.camera.getH()
        base.camera.setH(h - 1)
         
    def add_block(self, pos, color, add_collider):
        block = loader.loadModel("block")
        block.setTexture(self.texture)
        block.setPos(pos)
        block.setColor(color)
        block.reparentTo(render)

        if add_collider:
            cnode = CollisionNode("block")
            cnode.addSolid(CollisionBox((0, 0, 0), 1, 1, 1))
            collider = block.attachNewNode(cnode)

        return block
        

game = Game()
game.run()

