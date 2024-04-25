class Perso:
    def __init__(self, nom, pv_max=500):
        self.nom = nom
        self.pv_max = pv_max
        self.pv = pv_max
        self.x = 0 
        self.y = 0
        self.jump_height = 100 
        self.jump_time = 10 
        self.jump_count = 0

    def perdre_pv(self, degats):
        self.pv -= degats
        if self.pv <= 0:
            self.pv = 0
            print(f"{self.nom} est mort.")

    def soigner(self, soin):
        self.pv += soin
        if self.pv > self.pv_max:
            self.pv = self.pv_max

    def deplacer_haut(self):
        if self.jump_count == 0:
            self.jump_count = self.jump_time 

    def deplacer_gauche(self):
        self.x -= 10 

    def deplacer_droite(self):
        self.x += 10

    def update_jump(self, SCREEN_HEIGHT=720):
        if self.jump_count > 0:
            jump_distance = (self.jump_height * (self.jump_count / self.jump_time) ** 2) // 2
            self.y -= jump_distance
            self.jump_count -= 1
        else:
            if self.y < SCREEN_HEIGHT - 200: 
                jump_distance = (self.jump_height * ((self.jump_time - self.jump_count) / self.jump_time) ** 2) // 2
                self.y += jump_distance  
            else:
                self.jump_count = 0