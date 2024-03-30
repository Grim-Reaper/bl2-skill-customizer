import os

from unrealsdk import FindObject, LoadPackage, Log, UObject, UFunction, FStruct
from Mods.ModMenu import Game, Hook, SDKMod, ModTypes, EnabledSaveType

class SkillCustomizer(SDKMod):
    Name: str = "Skill Customizer"
    Description: str = "Customize your skills!"
    Version: str = "1.0.0"
    Author: str = "Grim Reader"
    Types: ModTypes = ModTypes.Gameplay
    SaveEnabledState: EnabledSaveType = EnabledSaveType.LoadOnMainMenu
    LocalModDir: str = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, details: dict = None):
        if details is not None:
            self.Name = details["Name"]
            self.Skills = details["Skills"]

    @Hook("WillowGame.PlayerSkillTree.Initialize")
    def InjectSkills(self, caller: UObject, function: UFunction, params: FStruct) -> bool:
        Log(f"Loading '{self.Name}' Skill Set")
        self.LoadTree(params.SkillTreeDef)
        return True

    def PreloadPackages(self) -> None:
        packages = [
            "GD_Assassin_Streaming_SF",
            "GD_Mercenary_Streaming_SF",
            "GD_Siren_Streaming_SF",
            "GD_Lilac_Psycho_Streaming_SF",
            "GD_Tulip_Mechro_Streaming_SF",
            "GD_Soldier_Streaming_SF",
        ]

        for package in packages:
            LoadPackage(package)

    def LoadTree(self, SkillTreeDef) -> None:
        index = 0
        for Branch in SkillTreeDef.Root.Children:
            self.LoadBranch(Branch, self.Skills[index])
            index = index + 1

    def LoadBranch(self, SkillTreeBranchDef, SkillDefinitions) -> None:
        self.PreloadPackages()
        HasBloodlust = False
        HasHellborn = False
        for Tier in range(6):
            TierLayout = [False, False, False]
            MaxPoints = 0
            NewSkills = []
            for Skill in range(3):
                SkillDef = self.LoadSkill(SkillDefinitions[Tier][Skill])
                if SkillDef:
                    TierLayout[Skill] = True
                    MaxPoints += SkillDef.MaxGrade
                    NewSkills.append(SkillDef)
                    HasHellborn = HasHellborn or "Hellborn" in SkillDef.GetFullName()
                    HasBloodlust = HasBloodlust or SkillDef.GetName() in ["BloodfilledGuns", "BloodyTwitch"]
            if HasBloodlust:
                NewSkills.append(FindObject("SkillDefinition", "GD_Lilac_Skills_Bloodlust.Skills._Bloodlust"))
            if HasHellborn:
                NewSkills.append(FindObject("SkillDefinition", "GD_Lilac_Skills_Hellborn.Skills.FireStatusDetector"))
                NewSkills.append(FindObject("SkillDefinition", "GD_Lilac_Skills_Hellborn.Skills.AppliedStatusEffectListener"))
            SkillTreeBranchDef.Layout.Tiers[Tier].bCellIsOccupied = TierLayout
            SkillTreeBranchDef.Tiers[Tier].Skills = NewSkills
            SkillTreeBranchDef.Tiers[Tier].PointsToUnlockNextTier = min(MaxPoints, 5)

    def LoadSkill(self, Skill):
        for prefix, values in self.SkillLists.items():
            if Skill in values:
                return FindObject("SkillDefinition", f"{prefix}.{Skill}")
        return False
        
    SkillLists = {
        "GD_Siren_Skills.Motion": ["Ward", "Accelerate", "Suspension", "KineticReflection", "Fleet", "Converge", "Inertia", "Quicken", "SubSequence", "Thoughtlock"],
        "GD_Siren_Skills.Harmony": ["MindsEye", "SweetRelease", "Restoration", "Wreck", "Elated", "Res", "Recompense", "Sustenance", "LifeTap", "Scorn"],
        "GD_Siren_Skills.Cataclysm": ["Flicker", "Foresight", "Immolate", "Helios", "ChainReaction", "CloudKill", "Backdraft", "Reaper", "BlightPhoenix", "Ruin"],
        "GD_Soldier_Skills.Guerrilla": ["DoubleUp", "LaserSight", "ScorchedEarth", "Sentry", "Able", "CrisisManagement", "Grenadier", "Onslaught", "Ready", "Willing"],
        "GD_Soldier_Skills.Gunpowder": ["Battlefront", "LongBowTurret", "Nuke", "DoOrDie", "DutyCalls", "Expertise", "Impact", "MetalStorm", "Overload", "Ranger", "Steady"],
        "GD_Soldier_Skills.Survival": ["Gemini", "Mag-Lock", "PhalanxShield", "Forbearance", "Grit", "HealthY", "LastDitchEffort", "Preparation", "Pressure", "QuickCharge"],
        "GD_Assassin_Skills.Bloodshed": ["Execute", "Grim", "ManyMustFall", "Backstab", "BeLikeWater", "Followthrough", "IronHand", "KillingBlow", "LikeTheWind", "Resurgence"],
        "GD_Assassin_Skills.Cunning": ["DeathBlossom", "Innervate", "Unforseen", "Ambush", "CounterStrike", "DeathMark", "FastHands", "Fearless", "RisingShot", "TwoFang"],
        "GD_Assassin_Skills.Sniping": ["AtOneWithTheGun", "Bore", "CriticalAscention", "HeadShot", "KillConfirmed", "Killer", "OneShotOneKill", "Optics", "Precision", "Velocity"],
        "GD_Mercenary_Skills.Brawn": ["AintGotTimeToBleed", "BusThatCantSlowDown", "ComeAtMeBro", "FistfulOfHurt", "Asbestos", "Diehard", "ImTheJuggernaut", "Incite", "JustGotReal", "OutOfBubblegum", "SexualTyrannosaurus"],
        "GD_Mercenary_Skills.Gun_Lust": ["DivergentLikness", "DownNotOut", "KeepItPipingHot", "AllIneedIsOne", "AutoLoader", "ImYourHuckleberry", "LayWaste", "LockedandLoaded", "MoneyShot", "NoKillLikeOverkill", "QuickDraw"],
        "GD_Mercenary_Skills.Rampage": ["DoubleYourFun", "GetSome", "ImReadyAlready", "KeepFiring", "LastLonger", "SteadyAsSheGoes", "YippeeKiYay", "5Shotsor6", "AllInTheReflexes", "FilledtotheBrim", "Inconceivable"],
        "GD_Lilac_Skills_Hellborn.Skills": ["BurnBabyBurn", "DelusionalDamage", "ElementalElation", "ElementalEmpathy", "FireFiend", "FlameFlare", "FuelTheFire", "NumbedNerves", "PainIsPower", "RavingRetribution", "HellfireHalitosis"],
        "GD_Lilac_Skills_Bloodlust.Skills": ["BloodOverdrive", "BloodyRevival", "BloodBath", "FuelTheBlood", "BoilingBlood", "NervousBlood", "Bloodsplosion", "BloodTrance", "BuzzAxeBombadier", "TasteOfBlood", "BloodfilledGuns", "BloodyTwitch"],
        "GD_Lilac_Skills_Mania.Skills": ["FuelTheRampage", "LightTheFuse", "ReleaseTheBeast", "EmbraceThePain", "EmptyRage", "FeedTheMeat", "PullThePin", "RedeemTheSoul", "SaltTheWound", "SilenceTheVoices", "StripTheFlesh", "ThrillOfTheKill"],
        "GD_Tulip_Mechromancer_Skills.BestFriendsForever": ["CloseEnough", "CookingUpTrouble", "FancyMathematics", "TheBetterHalf", "UnstoppableForce", "20PercentCooler", "BuckUp", "ExplosiveClap", "MadeOfSternerStuff", "PotentAsAPony", "SharingIsCaring", "UpshotRobot"],
        "GD_Tulip_Mechromancer_Skills.EmbraceChaos": ["Anarchy", "SmallerLighterFaster", "TheNthDegree", "AnnoyedAndroid", "RobotRampage", "PreshrunkCyberpunk", "Discord", "TypecastIconoclast", "RationalAnarchist", "WithClaws", "BloodSoakedShields", "DeathFromAbove"],
        "GD_Tulip_Mechromancer_Skills.LittleBigTrouble": ["ElectricalBurn", "EvilEnchantress", "InterspersedOutburst", "MorePep", "Myelin", "ShockAndAAAGGGHHH", "ShockStorm", "WiresDontTalk", "MakeItSparkle", "OneTwoBoom", "StrengthOfFiveGorillas", "TheStare"]
    }