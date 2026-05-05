import os
import json
from typing import Sequence


_IsLoaded: bool = False

Choices: Sequence[str] = []
Configs: dict = {}
StartingValue: str = None


if not _IsLoaded:
    dir = os.path.dirname(os.path.realpath(__file__))
    if os.path.isfile(dir + "\\data.json"):
        with open(dir + "\\data.json", "r") as f:
            skillSetList = json.loads(f.read())
            for skillSet in skillSetList:
                Choices.append(skillSet["Name"])
                Configs[skillSet["Name"]] = skillSet["Skills"]
    else:
        with open(dir + "\\data.json", "w") as f:
            f.write("[]")
            _IsLoaded = True

if StartingValue is None:
    dir = os.path.dirname(os.path.realpath(__file__))
    if os.path.isfile(dir + "\\data.json"):
        with open(dir + "\\settings.json", "r") as f:
            settings = json.loads(f.read())
            if settings["Options"] is not None and settings["Options"]["Select Skill Set"] is not None:
                StartingValue = settings["Options"]["Select Skill Set"]

if StartingValue is None:
    StartingValue = "Insane Gaige"

