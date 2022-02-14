import pygame
from .util import Colors

class Window:
    def __init__(self, screen_size):
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.ui_group = None
        self.running = False
        self.bg_color = Colors.RED
    
    def start(self):
        self.running = True
        while self.running:
            self.update()
        pygame.quit()
    
    def eventloop(self, event):
        if self.ui_group:
            self.ui_group.eventloop(event)

        if event.type == pygame.QUIT:
            self.running = False
    
    def update(self):

        for event in pygame.event.get():
            self.eventloop(event)
        
        if self.ui_group:
            self.ui_group.update()

        pygame.display.update()
        self.screen.fill(self.bg_color)
        self.clock.tick(self.fps)

