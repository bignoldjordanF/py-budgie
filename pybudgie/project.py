from typing import List


class PBProject:
    def __init__(
            self,
            id: int,
            name: str = '',
            cost: int = 0,
            categories: List[str] = None,
            targets: List[str] = None
    ):
        self.id = id
        self.name = name
        self.cost = cost
        self.categories = [] if not categories else categories
        self.targets = [] if not targets else targets
    
    def __repr__(self):
        return str(self.__dict__)
