import json
import os

from Mods.ModMenu import RegisterMod

from .Loader import SkillCustomizer

mod_instance = SkillCustomizer()

if os.path.isfile(mod_instance.LocalModDir + "\\data.json"):
    with open(mod_instance.LocalModDir + "\\data.json", "r") as f:
        skillSetList = json.loads(f.read())
        for skillSet in skillSetList:
            RegisterMod(SkillCustomizer(skillSet))
else:
    with open(mod_instance.LocalModDir + "\\data.json", "w") as f:
        f.write("[]")
