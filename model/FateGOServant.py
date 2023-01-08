from typing import Literal
from model.FateGOServantNoblePhantasm import ServantNoblePhantasm
from model.FateGOServantSkill import ServantSkill


class Servant:
    
    def __init__(self: object, name: str, servant_class: str, rarity: int, cost: int, attributes: dict, cards: tuple, traits: tuple, skills: Literal['tuple', 'ServantSkill'], noble_phantasm: ServantNoblePhantasm, passive_skills: Literal['tuple', 'ServantSkill'], servant_url_image: str):
        self.name: str = name
        self.servant_class: str = servant_class
        self.rarity: int = rarity
        self.cost: int = cost
        self.attributes: dict = attributes
        self.cards: tuple = cards
        self.traits: tuple = traits
        self.skills: Literal['tuple', 'ServantSkill'] = skills
        self.noble_phantasm: ServantNoblePhantasm = noble_phantasm
        self.passive_skills: Literal['tuple', 'ServantSkill'] = passive_skills
        self.servant_url_image: str = servant_url_image

    @property
    def s_class(self: object) -> str:
        servant_class = '{0}{1}'.format(self.servant_class[0].upper(), self.servant_class[1:])
        return servant_class
    
    @property
    def basic_infos(self: object) -> str:
        content = f'**Classe:** {self.s_class}\n\n**Raridade:** {self.rarity}\n\n**Custo:** {self.cost}'
        return content
    
    @classmethod
    def factory(self: object, **kwargs):
        from model import ServantNoblePhantasm, ServantSkill
        
        servant_skills = tuple( ServantSkill(name = skill['name'],
                                             effect = skill['detail'],
                                             cooldown = skill['coolDown'][-1])
                                for skill in kwargs['skills'])
        
        servant_passive_skills = tuple( ServantSkill(name = skill['name'],
                                                     effect = skill['detail'])
                                        for skill in kwargs['passive_skills'])
        

        traits = tuple(trait['name'] for trait in kwargs['traits'])
        
        servant_noble_phantasm = ServantNoblePhantasm(  name = kwargs['noble_phantasm']['name'],
                                                        rank = kwargs['noble_phantasm']['rank'],
                                                        card = kwargs['noble_phantasm']['card'],
                                                        type = kwargs['noble_phantasm']['type'],
                                                        effect = kwargs['noble_phantasm']['detail'])

        return self(name = kwargs['servant_name'],
                    servant_class = kwargs['servant_class'],
                    rarity = kwargs['rarity'],
                    cost = kwargs['cost'],
                    attributes = kwargs['attributes'],
                    cards = kwargs['cards'],
                    traits = traits,
                    skills = servant_skills,
                    noble_phantasm = servant_noble_phantasm,
                    passive_skills = servant_passive_skills,
                    servant_url_image = kwargs['servant_url_image'])
        