from datetime import timedelta
from typing import Optional, Self, Union, List


#TODO сделать класс синглтоном
class ScrumBuilder:
    sprint_duration: timedelta
    scrumbuilder: Optional[Self] = None

    def __new__(cls, *args, **kwargs):
        """
        Create the singleton ScrumBuilder
        :param args:
        :param kwargs:
        """
        if ScrumBuilder.scrumbuilder is None:
            ScrumBuilder.scrumbuilder = super().__new__(args, kwargs)
        return ScrumBuilder.scrumbuilder


    def __init__(self,
                 task_name: str,
                 task_description: str,
                 task_developers: Union[List[str], str],
                 task_deadline: str):
        pass

