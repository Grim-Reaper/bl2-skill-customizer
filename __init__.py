from Mods.ModMenu import RegisterMod

from .SkillCustomizer import SkillCustomizer
from .Options import Options


RegisterMod(SkillCustomizer(Options))
