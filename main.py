import pygame

# Initialize the game
pygame.init()   

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Conversor Tilemap Matriz")

#inserir tamanho do mapa, criar superficie e criar grid

class InputBox:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.normalColor = (255, 255, 0)
        self.seletedColor = (255, 255, 255)
        self.color = self.normalColor
        self.active = False

    def Update(self):
        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(mouse) and not self.active:
                self.active = True
                self.color = self.seletedColor
            elif not self.rect.collidepoint(mouse) and self.active:
                self.active = False
                self.color = self.normalColor

        if keys[pygame.K_RETURN] and self.active:
            self.active = False
            self.color = self.normalColor

    def Draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Group:
    def __init__(self):
        self.objects = []

    def Add(self, obj):
        self.objects.append(obj)

    def Remove(self, obj):
        self.objects.remove(obj)

    def Update(self):
        for obj in self.objects:
            if hasattr(obj, 'Update'):
                obj.Update()

    def Draw(self, surface):
        for obj in self.objects:
            if hasattr(obj, 'Draw'):
                obj.Draw(surface)

# Game Loop

group = Group()

inputMapaX = InputBox(100, 100, 140, 32)
group.Add(inputMapaX)

inputMapaY = InputBox(100, 140, 140, 32)
group.Add(inputMapaY)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    group.Update()

    screen.fill((0, 0, 0))

    group.Draw(screen)

    pygame.display.flip()