import pygame, time


class RealTimer:
    def __init__(self):
        self.start_time = -1
        self.stop_time = -1
    
    def start(self):
        self.reset()
    
    def get(self):
        if self.start_time == -1:
            return 0
        if self.stop_time == -1:
            return time.monotonic()-self.start_time

        return self.stop_time-self.start_time
    
    def reset(self):
        self.start_time = time.monotonic()
        self.stop_time = -1

    def stop(self):
        self.stop_time = time.monotonic()
    
    def passed(self, seconds):
        return self.get() >= seconds
    
    def __repr__(self):
        return f"time: {self.get()}"
    

class GameTimer:
    def __init__(self):
        self.reset()
    
    def start(self):
        self.start_time = pygame.time.get_ticks()
    
    def get(self):
        if self.start_time == -1:
            return 0
        now = pygame.time.get_ticks()
        return int(now-self.start_time)
    
    def reset(self):
        self.start_time = -1
    
    def passed(self, seconds):
        return self.get() >= seconds
    

    




