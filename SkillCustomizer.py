from typing import Sequence

from unrealsdk import Log, UObject, UFunction, FStruct
from Mods import ModMenu
from Mods.ModMenu import Hook, SDKMod, ModTypes, EnabledSaveType

from .SkillManager import SkillManager as _SkillManager
from .Config import Configs
from .Options import Options


class SkillCustomizer(SDKMod):
    Name: str = "Skill Customizer"
    Description: str = "Customize your skills!"
    Version: str = "1.0.0"
    Author: str = "Grim Reader"
    Types: ModTypes = ModTypes.Gameplay
    SaveEnabledState: EnabledSaveType = EnabledSaveType.LoadOnMainMenu
    Options: Sequence[ModMenu.Options.Base]
    SkillManager: _SkillManager

    def __init__(self, options: Sequence[ModMenu.Options.Base]):
        self.Options = options
        self.SkillManager = _SkillManager()

    @Hook("WillowGame.PlayerSkillTree.Initialize")
    def InjectSkills(self, caller: UObject, function: UFunction, params: FStruct) -> bool:
        skillSetName = Options[0].CurrentValue
        if skillSetName is not None:
            Log(f"Loading '{skillSetName}' Skill Set")
            self.SkillManager.LoadTree(params.SkillTreeDef, Configs[skillSetName])
            return True
        return False