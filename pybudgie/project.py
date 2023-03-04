from typing import List


class PBProject:
    def __init__(
            self,
            id: int,
            cost: int = 0,
            name: str = '',
            categories: List[str] = None,
            targets: List[str] = None
    ) -> None:
        """
        Constructs a PBProject object from an id, cost and optional project information.

        Parameters:
            - id (int): The mandatory id of the project.
            - cost (int): The cost of the project (i.e. how much budget will it use).
            - name (str): The optional name of the project.
            - categories (List[str]): The optional categories of the project.
            - targets (List[str]): The optional target [e.g. audience] of the project.
        """

        self.id = id
        self.name = name
        self.cost = cost
        self.categories = [] if not categories else categories
        self.targets = [] if not targets else targets
    
    def __repr__(self) -> str:
        return str(self.__dict__)
