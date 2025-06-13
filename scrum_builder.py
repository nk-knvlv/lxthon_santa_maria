from datetime import timedelta
from .model import sprint

#TODO сделать класс синглтоном
class ScrumBuilder:
    sprint_duration: timedelta


    def __init__(self):
        pass

    def create_sprint(self, ) -> sprint:
        return sprint
