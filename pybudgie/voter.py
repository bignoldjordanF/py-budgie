from typing import Dict


class PBVoter:
    def __init__(
            self,
            id: int,
            age: int = -1,
            sex: str = '',
            neighborhood: str = '',
            voting_method: str = '',
            votes: Dict[str, int] = None
    ):
        self.id = id
        self.age = age
        self.sex = sex
        self.neighborhood = neighborhood
        self.voting_method = voting_method
        self.votes = {} if not votes else votes

    def __repr__(self):
        return str(self.__dict__)
