from typing import List

from unrealsdk import Log
from Mods.ModMenu.Options import Base, Spinner

from .Config import Choices, StartingValue


Log(f"Testing load one: {StartingValue}")

_ChooseSkillSet = Spinner(
    Caption="Select Skill Set",
    Description="Choose your preferred skill set.",
    StartingValue=StartingValue,
    Choices=Choices
)

Options: List[Base] = [_ChooseSkillSet]
