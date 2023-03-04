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
    ) -> None:
        """
        Constructs a PBVoter object from an id, optional project information and a dictionary of votes over projects.

        Parameters:
            - id (int): The mandatory id of the voter.
            - age (int): The optional age of the voter.
            - sex (str): The optional sex of the voter ('M' or 'F').
            - neighborhood (str): The optional neighborhood of the voter.
            - voting_method (str): The optional method of voting used by the voter.
            Otherwise assumed from the parent instance.
            - votes (Dict[str, int]): A mapping from project id to cardinal utility
            that this voter derives from each project. For example, in approval
            voting, we might have {'34': 1}, meaning this voter approves project 34.
        """

        self.id = id
        self.age = age
        self.sex = sex
        self.neighborhood = neighborhood
        self.voting_method = voting_method
        self.votes = {} if not votes else votes

    def __repr__(self) -> str:
        return str(self.__dict__)
