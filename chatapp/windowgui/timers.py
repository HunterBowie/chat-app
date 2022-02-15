import pygame, time


class RealTimer:
    def __init__(self):
        self.reset()
    
    def start(self):
        self.start_stop_timer = time.monotonic()
    
    def get(self):
        if self.start_stop_timer == -1:
            return 0
        return int(time.monotonic()-self.start_stop_timer)
    
    def reset(self):
        self.start_stop_timer = -1
    
    def passed(self, seconds):
        return self.get() >= seconds
    

class GameTimer:
    def __init__(self):
        self.reset()
    
    def start(self):
        self.start_stop_timer = pygame.time.get_ticks()
    
    def get(self):
        if self.start_stop_timer == -1:
            return 0
        now = pygame.time.get_ticks()
        return int(now-self.start_stop_timer)
    
    def reset(self):
        self.start_stop_timer = -1
    
    def passed(self, seconds):
        return self.get() >= seconds
    




