

class ServantNoblePhantasm:
    
    def __init__(self: object, name: str, rank: str, card: str, type: str, effect: str) -> None:
        self.name = name
        self.rank = rank
        self.__card = card
        self.type = type
        self.effect = effect
    
    @property
    def card(self: object) -> str:
        card = '{0}{1}'.format(self.__card[0].upper(), self.__card[1:])
        return card
    
    @card.setter
    def card(self: object, value: str) -> None:
        self.__card = value
        