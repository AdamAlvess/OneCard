import time


class Perso:
    def __init__(self, nom, image, pv_max=500, y=0):
        self.nom = nom
        self.pv_max = pv_max
        self.image = image
        self.pv = pv_max
        self.x = 0
        self.jump_height = 100
        self.jump_time = 10
        self.jump_count = 0
        self.arme = None
        self.max_jumps = 2
        self.start_y = y
        self.current_jumps = 0

    def perdre_pv(self, degats):
        self.pv -= degats
        if self.pv <= 0:
            self.pv = 0

    def soigner(self, soin):
        self.pv += soin
        if self.pv > self.pv_max:
            self.pv = self.pv_max

    def deplacer_gauche(self):
        self.x -= 20
        time.sleep(0.001)

    def deplacer_droite(self):
        self.x += 20
        time.sleep(0.001)

    def deplacer_haut(self):
        if self.jump_count == 0 and self.current_jumps < self.max_jumps:
            self.jump_count = self.jump_time
            self.current_jumps += 1

    def update_jump(self):
        if self.jump_count > 0:
            jump_distance = (self.jump_height * (self.jump_count / self.jump_time) ** 2) // 2
            self.y -= jump_distance
            self.jump_count -= 1
        else:
            if self.y < self.start_y: 
                jump_distance = (self.jump_height * ((self.jump_time - self.jump_count) / self.jump_time) ** 2) // 2
                if self.y + jump_distance > self.start_y: 
                    self.y = self.start_y
                else:
                    self.y += jump_distance
            else:
                self.jump_count = 0
                self.current_jumps = 0
