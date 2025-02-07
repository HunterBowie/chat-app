import pygame
from .util import Colors

class Window:
    def __init__(self, screen_size):
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.max_fps = 60
        self.ui_manager = None
        self.running = False
        self.bg_color = Colors.RED
        self.flashes = []
    
    def flash(self, flash):
        flash.start()
        self.flashes.append(flash)
    
    def start(self):
        self.running = True
        while self.running:
            self.update()
        if self.ui_manager:
            self.ui_manager.stop()
        pygame.quit()


    def eventloop(self, event):
        if self.ui_manager:
            self.ui_manager.eventloop(event)

        if event.type == pygame.QUIT:
            self.running = False
    
    def update(self):
        for event in pygame.event.get():
            self.eventloop(event)
        
        if self.ui_manager:
            self.ui_manager.update()
        
        finished_flahes = []
        for flash in self.flashes:
            if flash.is_finished():
                finished_flahes.append(flash)
                continue
            flash.render(self.screen)
        
        for flash in finished_flahes:
            self.flashes.remove(flash)

        pygame.display.flip()
        self.screen.fill(self.bg_color)
        self.clock.tick(self.max_fps)

