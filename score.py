class Score(object):
    def __init__(self):
        self.white = 255,255,255
        self.count = 0
        self.font =pygame.font.Font('freesansbold.ttf', 20)
        self.text = self.font.render("Score : "+str(self.count),1,self.white)

    def show_score(self, screen):
        screen.blit(self.text, (5 ,5))

    def score_up(self):
        self.count += 10
        self.text = self.font.render("Score : "+str(self.count),1,self.white)
        
#create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
Enemy_group = pygame.sprite.Group()
Enemy_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


def create_Enemies():
    #generate Enemies
    for row in range(rows):
        for item in range(cols):
            enemy = Enemies(100 + item * 100, 100 + row * 70)
            Enemy_group.add(enemy)

create_Enemies()

#create player
spaceship = Spaceship(int(screen_width/ 2), screen_height - 100, 3)
spaceship_group.add(spaceship)

#score
score = Score()
            
