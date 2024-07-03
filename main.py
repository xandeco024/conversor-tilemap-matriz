import pygame

# Initialize the game
pygame.init()   

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Conversor Tilemap Matriz")

#inserir tamanho do mapa, criar superficie e criar grid

selectedPaint = 0



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
        mouse = (mouse[0] - offset[0] - 96, mouse[1] - offset[1])

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

class ToolBar:
    def __init__(self, editArea):
        self.surface = pygame.Surface((96, screen.get_height()))
        self.editArea = editArea
        self.color = (100, 100, 50)

        self.exportTilemapToFileBtn = Button(0, 720-128, 64, 32, "Exportar", lambda: ExportTilemapToFile(self.editArea.tilemap))

        self.recenterBtn = Button(0, 720-128-64-64, 64, 32, "Recenter", lambda: Recenter())

    def Update(self):
        self.exportTilemapToFileBtn.Update()
        self.recenterBtn.Update()

    def Draw(self, surface):
        self.surface.fill(self.color)
        self.surface.blit(pygame.font.Font(None, 32).render("1 - Air", True, (255, 255, 255)), (0, 0))
        self.surface.blit(pygame.font.Font(None, 32).render("2 - Grass", True, (255, 255, 255)), (0, 32))
        self.surface.blit(pygame.font.Font(None, 32).render("3 - Dirt", True, (255, 255, 255)), (0, 64))
        self.exportTilemapToFileBtn.Draw(self.surface)
        self.recenterBtn.Draw(self.surface)

        surface.blit(self.surface, (0, 0))

class EditArea:
    def __init__(self):
        self.surface = pygame.Surface((screen.get_width() - 96, screen.get_height()))
        self.color = (50, 50, 50)

        self.tilemap = Tilemap(10, 10)

        self.vScrollBar = ScrollBar(screen.get_width() - 96 - 10, 0, 10, screen.get_height(), "vertical")
        self.hScrollBar = ScrollBar(0, screen.get_height() - 10, screen.get_width() - 96, 10, "horizontal")

    def Update(self):
        self.tilemap.Update()
        self.vScrollBar.Update()
        self.hScrollBar.Update()

    def Draw(self, surface):
        self.surface.fill(self.color)
        self.tilemap.Draw(self.surface)
        self.vScrollBar.Draw(self.surface)
        self.hScrollBar.Draw(self.surface)

        surface.blit(self.surface, (96, 0))

class ScrollBar:
    def __init__(self, x, y, w, h, orientation = "vertical"):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (100, 100, 100)
        self.orientation = orientation

        self.activated = False

        if orientation == "vertical":
            self.handle = pygame.Rect(x, y, w, h/10)

        elif orientation == "horizontal":
            self.handle = pygame.Rect(x, y, w/10, h)

    def Update(self):
        mousePos = pygame.mouse.get_pos()
        mousePos = (mousePos[0] - offset[0] - 96, mousePos[1] - offset[1])

        if self.handle.collidepoint(mousePos) and pygame.mouse.get_pressed()[0]:
            self.activated = True

        if not pygame.mouse.get_pressed()[0] and self.activated:
            self.activated = False

        if self.activated:
            if self.orientation == "vertical":
                self.handle.y = mousePos[1] - self.handle.height/2

                if self.handle.y < self.rect.y:
                    self.handle.y = self.rect.y

                if self.handle.y + self.handle.height > self.rect.y + self.rect.height:
                    self.handle.y = self.rect.y + self.rect.height - self.handle.height

            elif self.orientation == "horizontal":
                self.handle.x = mousePos[0] - self.handle.width/2

                if self.handle.x < self.rect.x:
                    self.handle.x = self.rect.x
                
                if self.handle.x + self.handle.width > self.rect.x + self.rect.width:
                    self.handle.x = self.rect.x + self.rect.width - self.handle.width
                

    def Draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.handle, 0, 10)
# Game Loop

group = Group()

editArea = EditArea()
group.Add(editArea)
toolBar = ToolBar(editArea)
group.Add(toolBar)





def Recenter():
    offset[0] = 0
    offset[1] = 0

def ExportTilemapToFile(tilemap):
    
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