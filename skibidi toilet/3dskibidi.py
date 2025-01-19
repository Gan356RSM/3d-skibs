from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionBox, CollisionNode, CollisionSphere
from panda3d.core import WindowProperties
import math

#using a text file to store map data allows user to create/load different levels
#remove the special case from height map, and then just increment the height by 1 in update
#add blocks to location facing (3 blocks away)
#removing blocks (exercise for the student)
#   rather than storing height in self.blocks, store a list of blocks on that x/y coordinate
#   when removing block from the game, 
def load_level(filename):
    width = 0
    elevation_map = ""
    with open(filename, "r") as f:
        for line in f:
            elevation_map += line
    
    return width, elevation_map
    
class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) #super().__init__()

        wp = WindowProperties()
        wp.setSize(320 * 4, 180 * 4) 
        base.win.requestProperties(wp)
        base.setBackgroundColor(0.7, 0.8, 1)

        self.all_blocks = []
        self.texture = loader.loadTexture('block.png')

        base.cTrav = CollisionTraverser()
        pusher = CollisionHandlerPusher()

        base.disableMouse()
        self.player = self.add_block((0, 0, 0), (0., 0., 0., 0.), False, True)
        base.camera.reparentTo(self.player)
        base.camera.setPos((0, 0, 0))

        player_cnode = CollisionNode('player')
        player_cnode.addSolid(CollisionBox((0, 0, 0), 1, 1, 1))
        player_collider = self.player.attachNewNode(player_cnode)
        base.cTrav.addCollider(player_collider, pusher)
        pusher.addCollider(player_collider, self.player)

       

        self.blocks = {} 

        self.blocks_in_pos = {}
        
        width, elevation_map = load_level("map.txt")
        width = 30
        count = 0    

        for c in elevation_map:
            if c.isdigit():
                x = count // width
                y = count % width
                self.blocks_in_pos[(x, y)] = []
                if c == '0':
                    b = self.add_block((x, y, int(c) - 1), (0.2, 0.3, 0.7, 1.0), False, False)
                    self.blocks_in_pos[(x, y)].append(b)
                else:
                    for i in range(-1, int(c)):
                        b = self.add_block((x, y, i), (0.1, 0.5, 0.1, 1.0), True, False)
                        self.blocks_in_pos[(x, y)].append(b)
                self.blocks[(x, y)] = int(c)
                count += 1

        self.keymap = {
            "forward": False,
            "backward": False, 
            "left": False,
            "right": False,
            "turn_left": False,
            "turn_right": False,
            "jump": False,
            "place_block":False,
            "delete_block":False
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
        base.accept('r', self.add_block_in_front)
        base.accept('f', self.delete_one_block)

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

        x = round(self.player.getX() + 0.5)
        y = round(self.player.getY() + 0.5)
        height = 0
        if (x, y) in self.blocks:
            height = self.blocks[(x, y)]


        #prevent player from falling below that height
        if self.player.getZ() <= height + 0.1:
            self.player.setZ(height + 0.1)
            self.velocity = 0
    
        return task.cont
    
    def add_block_in_front(self):
        rad = math.radians(base.camera.getH())
        x = int(self.player.getX() - math.sin(rad) * 2)
        y = int(self.player.getY() + math.cos(rad) * 2)
        
        if not (x,y) in self.blocks:
            height = -1
        else:
            height = self.blocks[(x, y)]
        
        self.blocks[(x, y)] = height
        
        if height <= 5:
            
            self.add_block((x, y, height), (0.1 ,0.5, 0.1, 1.0), True, False)
        
    
    def jump(self):
        
        x = round(self.player.getX() + 0.5)
        y = round(self.player.getY() + 0.5)
        height = 0
        if (x, y) in self.blocks:
            height = self.blocks[(x, y)]
            
        if self.player.getZ() < height + 0.2:
            
            self.velocity = 0.2
            self.player.setZ(height + 0.2)
        

    def move_forward(self):
        x = self.player.getX()
        y = self.player.getY()
        z = self.player.getZ()
        rad = math.radians(base.camera.getH())
        dx = -math.sin(rad) * 0.2
        dy = math.cos(rad) * 0.2
        self.player.setPos((x + dx, y + dy, z))
        
    def move_backward(self):
        x = self.player.getX()
        y = self.player.getY()
        z = self.player.getZ()
        rad = math.radians(base.camera.getH())
        dx = math.sin(rad) * 0.2
        dy = -math.cos(rad) * 0.2
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
        

    def add_block(self, pos, color, add_collider, is_player):
        block = loader.loadModel('block')
        block.setTexture(self.texture)
        block.setPos(pos)
        block.setColor(color)
        block.reparentTo(render)

        if add_collider:
            cnode = CollisionNode("test")
            cnode.addSolid(CollisionBox((0, 0, 0), 1., 1., 1.))
            collider = block.attachNewNode(cnode)
        
        if not is_player:
            self.all_blocks.append(block)

        return block
    
    def delete_one_block(self):
        rad = math.radians(base.camera.getH())
        x = int(self.player.getX() - math.sin(rad) * 2)
        y = int(self.player.getY() + math.cos(rad) * 2)
        if len(self.all_blocks) == 0:
            return
        
        blocks = self.blocks_in_pos[(x, y)]
            
        b = self.all_blocks.pop(len(blocks) - 1)
        b.detachNode()

game = Game()
game.run()

