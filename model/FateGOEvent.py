from typing import Literal
from datetime import datetime


class FateGOEvent:
    
    def __init__(self: object, id: int, name: str, start_date: datetime, end_date: datetime, image_path: str) -> None:
        self.id = id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.image_path = image_path
    