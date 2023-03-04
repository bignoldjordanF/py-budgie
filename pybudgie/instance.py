from typing import List

class PBInstance:
    def __init__(
            self,
            description: str = '',
            country: str = '',
            region: str = '',
            district: str = '',
            category: str = '',
            budget: int = 0,
    ):
        # These attributes can and should be accessed
        # directly from the object.
        self.description = description
        self.country = country
        self.region = region
        self.district = district
        self.category = category
        self.budget = budget
    
    def __str__(self):
        return str(self.__dict__)
