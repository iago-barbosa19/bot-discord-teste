

class ServantSkill:
    
    def __init__(self: object, name: str, effect: str, cooldown: int = 0) -> None:
        self.name = name
        self.effect = effect
        self.cooldown = cooldown
        
    def __str__(self: object) -> str:
        return f'Nome: {self.name} - Efeito: {self.effect} - Cooldown: {self.cooldown}'