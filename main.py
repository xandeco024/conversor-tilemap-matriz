import pygame

# Initialize the game
pygame.init()   

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Conversor Tilemap Matriz")

#inserir tamanho do mapa, criar superficie e criar grid

selectedPaint = 0

editArea = pygame.surface.Surface((screen.get_width()-96, screen.get_height()))

scale = 1

offset = [0,0]

class InputBox:
    def __init__(self, x, y, w, h, txt):
        self.rect = pygame.Rect(x, y, w, h)
        self.normalColor = (255, 255, 0)
        self.seletedColor = (255, 255, 255)
        self.color = self.normalColor
        self.active = False
        self.originalText = txt
        self.txt = txt

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
        pygame.draw.rect(surface, self.color, self.rect, 0, 10)
        font = pygame.font.Font(None, 32)
        text = font.render(self.txt, True, (0, 0, 0))
        surface.blit(text, (self.rect.x + 5, self.rect.y + 5))

class Button:
    def __init__(self, x, y, w, h, txt, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.normalColor = (0, 255, 0)
        self.seletedColor = (255, 255, 255)
        self.color = self.normalColor
        self.active = False
        self.txt = txt
        self.callback = callback

    def Update(self):
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            self.color = self.seletedColor

            if pygame.mouse.get_pressed()[0]:
                self.callback()

        else:
            self.color = self.normalColor

    def Draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0, 10)
        font = pygame.font.Font(None, 32)
        text = font.render(self.txt, True, (0, 0, 0))
        #display text on center of button
        surface.blit(text, (self.rect.x + self.rect.width/2 - text.get_width()/2, self.rect.y + self.rect.height/2 - text.get_height()/2))

class ToolBar:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 96, screen.get_height())
        self.color = (70, 70, 70)

    def Update(self):
        pass

    def Draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Tile:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

        self.airColor = (200, 200, 255)
        self.grassColor = (0, 255, 0)
        self.dirtColor = (139, 69, 19)

        self.color = self.airColor
        self.borderColor = (0, 0, 0)

    def Update(self):
        mouse = pygame.mouse.get_pos()
        mouse = (mouse[0] - offset[0], mouse[1] - offset[1])

        if self.rect.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                if selectedPaint == 1:
                    self.color = self.airColor

                if selectedPaint == 2:
                    self.color = self.grassColor

                if selectedPaint == 3:
                    self.color = self.dirtColor

    def Draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.rect.x + offset[0], self.rect.y + offset[1], self.rect.width, self.rect.height))
        pygame.draw.rect(surface, self.borderColor, (self.rect.x + offset[0], self.rect.y + offset[1], self.rect.width, self.rect.height), 2, 0)

class Tilemap:
    def __init__(self, w, h):
        self.tiles = []
        self.w = w
        self.h = h
        self.rows = []

        self.tileSize = 64

        for r in range(h):
            row = []
            for c in range(w):
                tile = Tile(c * self.tileSize, r * self.tileSize, self.tileSize, self.tileSize)
                row.append(tile)

            self.rows.append(row)

    def Update(self):
        for row in self.rows:
            for tile in row:
                tile.Update()

    def Draw(self, surface):
        for row in self.rows:
            for tile in row:
                tile.Draw(surface)

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

# inputMapaX = InputBox(100, 128-32, 128+64, 64, "Altura")
# group.Add(inputMapaX)

# inputMapaY = InputBox(100, 126+64, 128+64, 64, "Largura")
# group.Add(inputMapaY)

# generateTilemapBtn = Button(100, 128+64+64, 128+64, 64, "Gerar Tilemap")
# group.Add(generateTilemapBtn)

tilemap = Tilemap(20, 12)
group.Add(tilemap)

exportTilemapToFileBtn = Button(1280-128-64, 720-128, 128, 64, "Exportar", lambda: ExportTilemapToFile(tilemap))
group.Add(exportTilemapToFileBtn)

recenterBtn = Button(1280-128-64, 720-128-64-64, 128, 64, "Recenter", lambda: Recenter())
group.Add(recenterBtn)

#toolBar = ToolBar()
#group.Add(toolBar)

def Recenter():
    offset[0] = 0
    offset[1] = 0

def ExportTilemapToFile(tilemap):

    #escreve esse array num txt

    array = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
        ]
    
    output = []

    for row in tilemap.rows:
        outputRow = []
        for tile in row:
            if tile.color == tile.airColor:
                outputRow.append(0)
            if tile.color == tile.grassColor:
                outputRow.append(1)
            if tile.color == tile.dirtColor:
                outputRow.append(2)
        output.append(outputRow)

    with open("tilemap.txt", "w") as file:
        file.write("tilemap = [\n")
        for row in output:
            #if last row, place comma, else, place nothing
            if output.index(row) == len(output) - 1:
                file.write(f"    {row}\n")
            else:
                file.write(f"    {row},\n")
        file.write("]")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selectedPaint = 1

            if event.key == pygame.K_2:
                selectedPaint = 2

            if event.key == pygame.K_3:
                selectedPaint = 3

        if event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                if scale < 2:
                    scale += 0.1

                else :
                    scale = 2

            if event.y == -1:
                if scale > 0.1:
                    scale -= 0.1

                else :
                    scale = 0.1

        if event.type == pygame.MOUSEMOTION:
            if event.buttons[1]:
                offset[0] += event.rel[0]
                offset[1] += event.rel[1]

    group.Update()

    screen.fill((50, 50, 60))

    group.Draw(screen)

    pygame.display.flip()