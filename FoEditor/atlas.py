"""
Item atlas.
All items and relevant objects/functions will be defined here.
All item data is copied/mirrored from the FoE source.

Body related things are NOT defined here! They are in body.py
"""


class Item:  # Base Item object
    def __init__(self, name_, fxStr_="", desc_="", type_=None):
        self.name = name_
        self.fxStr = fxStr_
        self.desc = desc_
        self.type = type_


class Atlas:  # This class is also used for dictionaries in the body.py classes.
    def get(self, dictionary, name):  # Returns Item object based on either ID or name.
        keys = list(dictionary.keys())

        # Try by name.
        for key in keys:
            if name == dictionary[key].name:
                return dictionary[key]

        # Try by ID.
        if name in dictionary:
            return dictionary[name]

        # All has failed, let anarchy run free.
        return None

    def id(self, dictionary, text):  # Returns Item ID based on name.
        keys = list(dictionary.keys())
        for key in keys:
            if text == dictionary[key].name:
                if "None" in key:
                    return ''
                else:
                    return key
        return None  # Doesn't cause error, but rather null values.


class Equipment:  # Defines all equipment items.
    # Format: "_id_": Item("_short name_", "_string describing effects_", "_long description_", "_subtype_")
    # Seperate with commas. _subtype_ argument only applies to armor.
    # Including an effects description and a long description is not required, but will be used to add details in the gui.

    # Defines all accessories.
    accessories = {
        "None": Item("None"),
        "book0": Item("Crude Book", "int + 2", "A heavy book on a rather dry subject. Not a very interesting read."),
        "book1": Item("Trashy Novel", "lib + 2", "A trashy hardcore romance novel of the sort terribly bored housewives might read. Features jackal-morphs heavily."),
        "bangle0": Item("Iron Bangle", "hp + 20", "A crude lump of iron, fashioned as a bangle. Provides minor protection from harm."),
        "ear0": Item("Gold Earring", "cha + 2", "A golden earring. Pretty, but not terribly useful in combat."),
        "neck0": Item("Rani's Favor", "hp + 100, spi + 5, cha + 5", "An elaborate silver necklace, gifted to you by Rani, prince of Rigard."),
        "head0": Item("Lagon's Crown", "hp + 120, lust + 80, str + 4, dex + 6, lib + 3", "A crown once belonging to the lagomorph king."),
        "cuffs0": Item("Simple Cuffs", "lust + 10, lib + 1", "Simple restraints."),
        "buckler0": Item("Iron Buckler", "hp + 30, sta + 2, spi + 1", "A crude iron buckler, designed to protect the wearer from harm."),
        "buckler1": Item("Silvered Buckler", "hp + 120, sta + 5, spi + 5", "A fine, silvered buckler to be strapped to one’s off-hand. Try not to use this as a plate or mirror."),
        "charm0": Item("Simple Charm", "spi + 2", "A simple charm that disrupts harmful energies."),
        "charm1": Item("Green Scented Candle", "spi + 2, nature + 0.5", "A small scented candle fashioned with nightshade, among other ingredients. Protects the holder from poison and other forces of nature.")
    }

    # Defines all armor.
    armor = {
        "None": Item("None", "", "", "top"),
        "None ": Item("None", "", "", "bot"),
        "chest0": Item("Leather Chest", "def 0.1, sta + 1", "A simple leather breastplate.", "top"),
        "chest1": Item("Watch Uniform", "def 0.6, sta + 4", "A Rigard city watch uniform.", "full"),
        "chest2": Item("Bronze Chest", "def 0.3, sta + 2", "A simple bronze breastplate.", "top"),
        "chest3": Item("Vine Bra", "def 0.3, sta + 2, lib + 3, cha + 2", "A vine bra.", "top"),
        "pants0": Item("Leather Pants", "def 0.1, sta + 1", "A pair of simple leather pants.", "bot"),
        "pants1": Item("Bronze Leggings", "def 0.2, sta + 2", "A pair of simple bronze leggings.", "bot"),
        "pants2": Item("Vine Panties", "def 0.3, sta + 2, lib + 3, cha + 2", "A pair of vine panties.", "bot"),
        "robe0": Item("Simple Robe", "def 0, int + 1, spi + 1", "Simple cloth robe.", "top"),
        "robe1": Item("Mage Robe", "def 0.2, int + 4, spi + 3", "Stylized magician robe.", "top"),
        "cloth0": Item("Stylized Clothes", "def 0, cha + 1, lib + 1", "Stylish clothes, with an alluring cut.", "full")
    }

    # Defines all weapons.
    weapons = {
        "None": Item("None"),
        "dag0": Item("Dagger", "atk 0.1, pierce 1, dex + 1", "A simple dagger."),
        "dag1": Item("Gol Claw", "atk 0.6, pierce 1, slash 0.5, str + 2, sta + 2, dex + 10", "A dagger fashioned out of a Gol claw."),
        "swrd0": Item("Short Sword", "atk 0.1, slash 1, str + 1", "A simple short sword."),
        "swrd1": Item("Fine Rapier", "atk 0.7, pierce 1, str + 3, dex + 10", "Krawitz\" fine rapier."),
        "swrd2": Item("Greatsword", "atk 1, slash 1, str + 4", "A large greatsword."),
        "swrd3": Item("Rapier", "atk 0.1, pierce 1, dex + 2", "A sharp rapier."),
        "swrd4": Item("Jeweled Mageblade", "atk 0.5, slash 1, fire 0.5, int + 7, spi + 3, sp + 100", "A short sword with rubies inlaid in the crossguard. Brief concentration on the part of the wielder causes the edge to erupt in flame."),
        "staff0": Item("Wooden Staff", "atk 0, blunt 1, int + 1", "A simple wooden staff."),
        "staff1": Item("Magician\"s Staff", "atk 0.2, blunt 1, int + 5, spi + 3", "A magician;s staff."),
        "staff2": Item("Old Amber Staff", "atk 0.5, blunt 0.5, thunder 0.5, int + 10, spi + 10", "A weathered staff with a knob made of amber. While old, it’s still useful as a conduit for electrical energies."),
        "whip0": Item("Leather Whip", "atk 0, slash 1, lib + 1", "A simple leather whip."),
        "whip1": Item("Vine Whip", "atk 0.2, slash 1, nature 0.5, lib + 5, cha + 3", "A whip made of vines."),
        "whip2": Item("Gol Whip", "atk 0.8, slash 1, nature 0.5, lust 0.5, lib + 9, cha + 5, lust + 100", "A whip dripping with Gol venom."),
        "spear0": Item("Oak Spear", "atk 0.2, pierce 1, def 0.2", "A shaft of treated wood with a pointed tip attached. Good for the defensive fighter in keeping your distance."),
        "spear1": Item("Halberd", "atk 0.3, pierce 0.5, slash 0.5, def 0.3", "Like a spear, but it slashes, too!"),
        "flail0": Item("Heavy Flail", "atk 0.5, blunt 0.8, pierce 0.2, def -0.1, dex + 2, str + 2", "A spiked wrecking ball on a stick for the offensively oriented. Hampers your ability to defend yourself, but grants considerable attacking momentum."),
        "hammer0": Item("Warhammer", "atk 0.6, blunt 1, dex - 1, str + 4", "Unwieldy, but learn to hold this thing right and you’ll be popping skulls like overripe fruit.")
    }

    # Defines all toys.
    toys = {
        "None": Item("None"),
        "dildo0": Item("Small Dildo", "", "About fifteen cm in length, the pleasure toy could be used by just about anyone. It is made from a slighly rubbery material."),
        "dildo1": Item("Medium Dildo", "", "About twentyfive cm in length, the pleasure toy is made for more advanced practitioners. It is made from a slighly rubbery material."),
        "dildo2": Item("Large Dildo", "", "About forty cm in length, the pleasure toy is only for the most spacious orifices. It is made from a slighly rubbery material."),
        "dildo3": Item("Thin Dildo", "", "This dildo is about twenty cm in length, but relatively thin. It is made from a slighly rubbery material."),
        "dildo4": Item("Buttplug", "", "A short, thick plug, designed for anal play. It is made from a slighly rubbery material."),
        "dildo5": Item("Large Buttplug", "", "A large, thick plug, designed for advanced anal play. It is made from a slighly rubbery material."),
        "dildo6": Item("Anal Beads", "", "A set of five small beads on a string, designed for anal play."),
        "dildo7": Item("Large Anal Beads", "", "A set of five large beads on a string, designed for advanced anal play."),
        "dildo8": Item("Equine Dildo", "", "About fifty cm in length, the pleasure toy is only for the most spacious orifices. It comes complete with a sheath and a flared head. It is made from a slighly rubbery material."),
        "dildo9": Item("Canine Dildo", "", "About thirty cm in length, the pleasure toy is only for the most spacious orifices. It comes complete with a thick knot. It is made from a slighly rubbery material."),
        "dildo10": Item("Chimera", "", "About sixty cm in length, the pleasure toy is only for the most spacious orifices. It combines the barbed head of a feline cock with the sheath of a horse and the knot of a canine. It is made from a slighly rubbery material.")
    }

    # Defines all strap-ons.
    strapons = {
        "None": Item("None"),
        "strapon0": Item("Plain Strap-on", "", "The strap-on is roughly the size and shape of an average human phallus. It is made from a slighly rubbery material. At the Base, there are straps for attatching it."),
        "strapon1": Item("Large Strap-on", "", "The strap-on is roughly the shape of a human phallus, but very large. It is made from a slighly rubbery material. At the Base, there are straps for attatching it."),
        "strapon2": Item("Equine Strap-on", "", "About forty cm in length, the pleasure toy is only for the most spacious orifices. It comes complete with a sheath and a flared head. It is made from a slighly rubbery material. At the Base, there are straps for attatching it."),
        "strapon3": Item("Canid Strap-on", "", "While not incredibly long, the dog-like strap-on is very thick. It comes complete with a knot and a pointed tip. It is made from a slighly rubbery material. At the Base, there are straps for attatching it."),
        "strapon4": Item("Chimera Strap-on", "", "About sixty cm in length, the strap-on is only for the most spacious orifices. It combines the barbed head of a feline cock with the sheath of a horse and the knot of a canine. It is made from a slighly rubbery material. At the Base, there are straps for attatching it.")
    }

atlas = Atlas()
equipment = Equipment()
