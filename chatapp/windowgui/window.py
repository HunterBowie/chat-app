import pygame
from .util import Colors

class Window:
    def __init__(self, screen_size):
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.ui = {}
        self.running = False
        self.bg_color = Colors.RED
    
    def start(self):
        self.running = True
        while self.running:
            self.update()
        pygame.quit()
    
    def eventloop(self, event):
        for element in self.ui.values():
            element.eventloop(event)

        if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):

        for event in pygame.event.get():
            self.eventloop(event)
        
        for element in self.ui.values():
            element.render(self.screen)

        pygame.display.update()
        self.screen.fill(self.bg_color)
        self.clock.tick(self.fps)

