"""
Created to keep main file clean.
Most imports and functions will be found here.
"""

# Built into Python.
from webbrowser import open as web
import logging as log
from json import loads, dumps
from math import floor

# Require external lib.
from PyQt5 import QtWidgets, QtCore
from dpath import util as dpath

# Found in FoEditor folder.
from FoEditor.ui import Ui_MainWindow
from FoEditor.atlas import atlas, equipment
from FoEditor.body import body, bodypart

url = "https://github.com/PythonicMoron/FoEditor"  # Source link.
GAME_VERSION = 28  # latest game version.


# Due to the way Python 3 and PyQt5 organization works, I am forced to write everything in classes and multi-class
# hierarchy sucks, so I put everything in one very large class... God forgive me.

class Main(Ui_MainWindow):  # Contains majority of functionality.

    def initUI(self, alog):  # Massive function that prepares the ui, defines data, and connects slots.
        self.data = None  # Initialize save data var to null.
        self.alog = alog  # Advanced logging.

        # Default data structure to use in case loaded data is missing flags.
        # Note: None values should not be set in data or default_data! None should only be used to default GUI widgets!
        # These defaults are educated guesses and may not be accurate, so no harm in altering them.
        self.default_data = {
            'player': {
                'name': "", 'acc1': "", 'acc2': "", 'botarm': "", 'toparm': "", 'toy': "", 'wep': "",
                'dex': 0, 'dexG': 1, 'inte': 0, 'inteG': 1, 'lib': 0, 'libG': 1, 'sta': 0, 'staG': 1,
                'str': 0, 'strG': 1, 'spi': 0, 'spiG': 1, 'maxLust': 10, 'maxLustG': 5, 'curLust': 0,
                'maxHp': 10, 'maxHpG': 10, 'curHp': 140, 'maxSp': 10, 'maxSpG': 5, 'curSp': 90,
                'slut': 0, 'subDom': 50, 'alvl': 1, 'lvl': 1, 'slvl': 1, 'sexp': 0, 'exp': 0,
                'exp2lvl': 15, 'sxp2lvl': 30,
                'body': {
                    'fem': 0, 'tone': 0, 'mass': 0, 'weight': 62
                }
            }
        }

        log.info("Setting up UI.")
        i = 0
        l = list(equipment.accessories.keys())

        while i < len(l):  # Load accessory drop-down boxes with equipment.accessories.
            item = atlas.get(equipment.accessories, l[i])

            self.acc1.addItem(item.name)
            self.acc1.setItemData(i, item.desc, 3)

            self.acc2.addItem(item.name)
            self.acc2.setItemData(i, item.desc, 3)

            i += 1
        log.debug("Setup accessory combo boxes.")

        i = t = b = 0
        l = list(equipment.armor.keys())

        while i < len(l):  # Load and sort armor drop-down boxes with atlas.Armor.
            item = atlas.get(equipment.armor, l[i])

            if ('top' in str(item.type)) or ('full' in str(item.type)):
                self.armTop.addItem(item.name)
                self.armTop.setItemData(t, item.desc, 3)
                t += 1
            elif 'bot' in str(item.type):
                self.armBot.addItem(item.name)
                self.armBot.setItemData(b, item.desc, 3)
                b += 1
            i += 1
        log.debug("Setup armor combo boxes.")

        l = list(equipment.weapons.keys())
        i = 0

        while i < len(l):  # Load weapon drop-down box with atlas.Weapons.
            item = atlas.get(equipment.weapons, l[i])

            self.weapon.addItem(item.name)
            self.weapon.setItemData(i, item.desc, 3)

            i += 1
        log.debug("Setup weapon combo box.")

        l = list(equipment.strapons.keys())
        i = 0

        while i < len(l):  # Load toy drop-down box with atlas.Strapons.
            item = atlas.get(equipment.strapons, l[i])

            self.toy.addItem(item.name)
            self.toy.setItemData(i, item.desc, 3)

            i += 1
        log.debug("Setup toy combo box.")

        # Signal/slot work section.

        self.actionSource.triggered.connect(lambda: web(url))
        self.actionOpen.triggered.connect(self.load)
        self.actionSave.triggered.connect(self.save)

        self.acc1.highlighted['int'].connect(lambda arg: self.status(equipment.accessories, self.acc1, arg))
        self.acc2.highlighted['int'].connect(lambda arg: self.status(equipment.accessories, self.acc2, arg))
        self.armTop.highlighted['int'].connect(lambda arg: self.status(equipment.armor, self.armTop, arg))
        self.armBot.highlighted['int'].connect(lambda arg: self.status(equipment.armor, self.armBot, arg))
        self.weapon.highlighted['int'].connect(lambda arg: self.status(equipment.weapons, self.weapon, arg))
        self.toy.highlighted['int'].connect(lambda arg: self.status(equipment.strapons, self.toy, arg))

        self.characterName.textChanged['QString'].connect(lambda arg: self.setval('player/name', arg))

        self.acc1.currentIndexChanged['QString'].connect(lambda arg: self.setval('player/acc1', atlas.id(equipment.accessories, arg)))
        self.acc2.currentIndexChanged['QString'].connect(lambda arg: self.setval('player/acc2', atlas.id(equipment.accessories, arg)))
        self.armTop.currentIndexChanged['QString'].connect(lambda arg: self.setval('player/toparm', atlas.id(equipment.armor, arg)))
        self.armBot.currentIndexChanged['QString'].connect(lambda arg: self.setval('player/botarm', atlas.id(equipment.armor, arg)))
        self.weapon.currentIndexChanged['QString'].connect(lambda arg: self.setval('player/wep', atlas.id(equipment.weapons, arg)))
        self.toy.currentIndexChanged['QString'].connect(lambda arg: self.setval('player/toy', atlas.id(equipment.strapons, arg)))

        self.dex.valueChanged['int'].connect(lambda arg: self.setval('player/dex', arg))
        self.dexG.valueChanged['double'].connect(lambda arg: self.setval('player/dexG', arg))
        self.inte.valueChanged['int'].connect(lambda arg: self.setval('player/inte', arg))
        self.inteG.valueChanged['double'].connect(lambda arg: self.setval('player/inteG', arg))
        self.lib.valueChanged['int'].connect(lambda arg: self.setval('player/lib', arg))
        self.libG.valueChanged['double'].connect(lambda arg: self.setval('player/libG', arg))
        self.sta.valueChanged['int'].connect(lambda arg: self.setval('player/sta', arg))
        self.staG.valueChanged['double'].connect(lambda arg: self.setval('player/staG', arg))
        self.str.valueChanged['int'].connect(lambda arg: self.setval('player/str', arg))
        self.strG.valueChanged['double'].connect(lambda arg: self.setval('player/strG', arg))
        self.spi.valueChanged['int'].connect(lambda arg: self.setval('player/spi', arg))
        self.spiG.valueChanged['double'].connect(lambda arg: self.setval('player/spiG', arg))

        self.fem.valueChanged['double'].connect(lambda arg: self.setval('player/body/fem', arg))
        self.mTone.valueChanged['double'].connect(lambda arg: self.setval('player/body/tone', arg))
        self.slut.valueChanged['int'].connect(lambda arg: self.setval('player/slut', arg))
        self.subDom.valueChanged['int'].connect(lambda arg: self.setval('player/subDom', arg))
        self.al.valueChanged['int'].connect(lambda arg: self.setval('player/alvl', arg))
        self.mass.valueChanged['double'].connect(lambda arg: self.setval('player/body/mass', arg))
        self.weight.valueChanged['double'].connect(lambda arg: self.setval('player/body/weight', arg))

        self.mLust.valueChanged['int'].connect(lambda arg: self.setval('player/maxLust', arg))
        self.mLustG.valueChanged['int'].connect(lambda arg: self.setval('player/maxLustG', arg))
        self.lust.valueChanged['double'].connect(lambda arg: self.setval('player/curLust', arg))
        self.mHP.valueChanged['int'].connect(lambda arg: self.setval('player/maxHp', arg))
        self.mHPG.valueChanged['int'].connect(lambda arg: self.setval('player/maxHpG', arg))
        self.HP.valueChanged['int'].connect(lambda arg: self.setval('player/curHp', arg))
        self.mSP.valueChanged['int'].connect(lambda arg: self.setval('player/maxSp', arg))
        self.mSPG.valueChanged['int'].connect(lambda arg: self.setval('player/maxSpG', arg))
        self.SP.valueChanged['int'].connect(lambda arg: self.setval('player/curSp', arg))
        self.lvl.valueChanged['int'].connect(lambda arg: self.setval('player/lvl', arg))
        self.slvl.valueChanged['int'].connect(lambda arg: self.setval('player/slvl', arg))
        self.sxp2lvl.valueChanged['int'].connect(lambda arg: self.setval('player/sxp2lvl', arg))
        self.xp2lvl.valueChanged['int'].connect(lambda arg: self.setval('player/exp2lvl', arg))
        self.SXP.valueChanged['int'].connect(lambda arg: self.setval('player/sexp', arg))
        self.XP.valueChanged['int'].connect(lambda arg: self.setval('player/exp', arg))

        self.lvl.valueChanged['int'].connect(lambda arg: self.getXP2lvl(arg))
        self.slvl.valueChanged['int'].connect(lambda arg: self.getSXP2lvl(arg))

        # End signal/slot work.

        self.reset()

    # Setup complete

    def setval(self, path, val):  # Sets/creates key in data to/with value
        if self.data is None:
            log.debug("Data is empty! Ignoring changes.")
            return
        elif dpath.set(self.data, path, val):
            log.debug("Changed: '%s'.", path)
            if self.alog:
                log.debug("New value is " + str(val))
        else:
            dpath.new(self.data, path, val)
            log.debug("Created '%s'.", path)
            if self.alog:
                log.debug("New value is " + str(val))

    def getval(self, path):  # Attempts to retrieve value. Returns default value if non-existent.
        try:
            log.debug("Retrieving '%s' from save data.", path)
            val = dpath.get(self.data, path)
            if self.alog:
                log.debug("Value is " + str(val))
            try:  # Is this a number?
                val = float(val)
            except ValueError:
                pass  # Not a number.
            return val
        except KeyError:
            log.debug("Data at '%s' does not exist.", path)
            log.debug("Using default.")
            try:
                val = dpath.get(self.default_data, path)
                try:  # Can I be numerical?
                    val = float(val)
                except ValueError:
                    pass  # I can not.
                return val
            except KeyError:
                log.exception("Default not defined! Somebody fucked up.")
                return None  # This is should yield interesting results.

    def getSXP2lvl(self, slvl):  # Calculate sxp to level up.
        log.debug("Calculating sxp2lvl.")
        i = 1
        sxp = float(30)
        while i < slvl:
            sxp = float(floor(sxp * 2))
            i += 1
        self.sxp2lvl.setValue(sxp)

    def getXP2lvl(self, lvl):  # Calculate xp to level up.
        i = 1
        xp = float(15)
        while i < lvl:
            xp = float(floor(xp * 1.2))
            i += 1
        self.xp2lvl.setValue(xp)

    def status(self, dictionary, obj, i):  # Display info about currently highlighted item from combobox in the status bar.
        self.statusbar.showMessage(atlas.get(dictionary, obj.itemText(i)).fxStr)

    def load(self):  # Load JSON data from file
        log.info("Open file.")

        try:
            file = open(QtWidgets.QFileDialog.getOpenFileName()[0], 'r')
            if self.alog:
                log.debug("File path = " + str(file.name))
        except FileNotFoundError:
            log.error("Invalid file path.")
            return

        self.reset()
        inp = file.read()
        file.close()

        try:
            self.data = loads(inp)
        except (TypeError, ValueError) as err:
            self.statusbar.showMessage("Load Failed!")
            log.exception(err)
            log.error("Save file load failed!")

        # Verify that this is a FoE save and of the correct version
        ver = self.getval('version')
        if ver is None:
            log.error("No version found!")
            self.statusbar.showMessage("Not a valid save!")
            return
        elif not ver == GAME_VERSION:  # Won't stop loading, but may cause trouble.
            log.warning("Game version mismatch!")
            self.statusbar.showMessage("WARNING: Version mismatch! Game("+str(ver)+") != Editor("+str(GAME_VERSION)+")")
        else:
            self.statusbar.showMessage("Version: " + str(GAME_VERSION))

        log.debug("Game version: " + str(ver))
        log.debug("Editor version: " + str(GAME_VERSION))

        # Handle save
        log.debug("Attempting save data handle...")
        try:
            # Name - Maybe handle save name too? Some parsing work needs to be done here in the future.
            self.characterName.setText(self.getval('player/name'))

            # Accessories
            item = self.getval('player/acc1')
            for i in range(0, self.acc1.count(), 1):
                if atlas.id(equipment.accessories, self.acc1.itemText(i)) == item:
                    self.acc1.setCurrentIndex(i)
                    break

            item = self.getval('player/acc2')
            for i in range(0, self.acc2.count(), 1):
                if atlas.id(equipment.accessories, self.acc2.itemText(i)) == item:
                    self.acc2.setCurrentIndex(i)
                    break

            # Armor
            item = self.getval('player/toparm')
            for i in range(0, self.armTop.count(), 1):
                if atlas.id(equipment.armor, self.armTop.itemText(i)) == item:
                    self.armTop.setCurrentIndex(i)
                    break

            item = self.getval('player/botarm')
            for i in range(0, self.armBot.count(), 1):
                if atlas.id(equipment.armor, self.armBot.itemText(i)) == item:
                    self.armBot.setCurrentIndex(i)
                    break

            # Weapon
            item = self.getval('player/wep')
            for i in range(0, self.weapon.count(), 1):
                if atlas.id(equipment.weapons, self.weapon.itemText(i)) == item:
                    self.weapon.setCurrentIndex(i)
                    break

            # Toy
            item = self.getval('player/toy')
            for i in range(0, self.toy.count(), 1):
                if atlas.id(equipment.strapons, self.toy.itemText(i)) == item:
                    self.toy.setCurrentIndex(i)
                    break
            log.debug("Loaded equipment.")

            # Stats
            self.dex.setValue(self.getval('player/dex'))
            self.dexG.setValue(self.getval('player/dexG'))
            self.inte.setValue(self.getval('player/inte'))
            self.inteG.setValue(self.getval('player/inteG'))
            self.lib.setValue(self.getval('player/lib'))
            self.libG.setValue(self.getval('player/libG'))
            self.sta.setValue(self.getval('player/sta'))
            self.staG.setValue(self.getval('player/staG'))
            self.str.setValue(self.getval('player/str'))
            self.strG.setValue(self.getval('player/strG'))
            self.spi.setValue(self.getval('player/spi'))
            self.spiG.setValue(self.getval('player/spiG'))
            log.debug("Loaded stats.")

            # Other stats
            self.fem.setValue(self.getval('player/body/fem'))
            self.mTone.setValue(self.getval('player/body/tone'))
            self.slut.setValue(self.getval('player/slut'))
            self.subDom.setValue(self.getval('player/subDom'))
            self.al.setValue(self.getval('player/alvl'))
            self.mass.setValue(self.getval('player/body/mass'))
            self.weight.setValue(self.getval('player/body/weight'))
            log.debug("Loaded other stats.")

            # More stats
            self.mLust.setValue(self.getval('player/maxLust'))
            self.mLustG.setValue(self.getval('player/maxLustG'))
            self.lust.setValue(self.getval('player/curLust'))
            self.mHP.setValue(self.getval('player/maxHp'))
            self.mHPG.setValue(self.getval('player/maxHpG'))
            self.HP.setValue(self.getval('player/curHp'))
            self.mSP.setValue(self.getval('player/maxSp'))
            self.mSPG.setValue(self.getval('player/maxSpG'))
            self.SP.setValue(self.getval('player/curSp'))
            self.lvl.setValue(self.getval('player/lvl'))
            self.slvl.setValue(self.getval('player/slvl'))
            self.sxp2lvl.setValue(self.getval('player/sxp2lvl'))
            self.xp2lvl.setValue(self.getval('player/exp2lvl'))
            self.SXP.setValue(self.getval('player/sexp'))
            self.XP.setValue(self.getval('player/exp'))
            log.debug("Loaded more stats")

        except (KeyError, AttributeError, IndexError) as err:  # Highly unlikely for bad data to get through this.
            self.statusbar.showMessage("Error Loading Data")
            log.exception(err)
            log.error("Save data load failed!")
            self.reset()
        else:
            log.debug("Save data loaded without error.")
        return

    def save(self):  # Save JSON data to file
        log.info("Save file.")
        if self.data is None:
            self.statusbar.showMessage("No Data!")
            log.debug("Data is empty.")
            return
        try:
            file = open(QtWidgets.QFileDialog.getSaveFileName()[0], 'w+')
            if self.alog:
                log.debug("File path = " + str(file.name))
            file.write(dumps(self.data))
            file.close()
        except (FileNotFoundError, TypeError) as err:  # Should never actually trigger.
            self.statusbar.showMessage("Save Failed!")
            log.exception(err)
            log.error("Save file failed!")
        else:
            self.statusbar.showMessage("Attempted Save.")
            log.debug("Saved data to file without error.")

    def reset(self):  # Resets UI indexes.
        self.data = None

        # Layouts to iterate through.
        layouts = ['name_layout', 'job_layout', 'perk_layout', 'formLayout_6', 'formLayout_7', 'formLayout_8',
                   'formLayout_9', 'formLayout']

        for item in layouts:
            attr = getattr(self, item)
            for i in reversed(range(attr.count())):
                obj = attr.itemAt(i).widget()
                if isinstance(obj, QtWidgets.QSpinBox):
                    obj.setValue(0)
                elif isinstance(obj, QtWidgets.QDoubleSpinBox):
                    obj.setValue(0.0)
                elif isinstance(obj, QtWidgets.QComboBox):
                    obj.setCurrentIndex(-1)
                elif isinstance(obj, QtWidgets.QLineEdit):
                    obj.clear()
                elif isinstance(obj, QtWidgets.QCheckBox):
                    obj.setChecked(False)
            log.debug("Data and indexes reset.")
