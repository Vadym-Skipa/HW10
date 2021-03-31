from time import sleep

class VacuumCleanerInitError(Exception):
    pass

class VacuumCleanerError(Exception):
    pass

class NoWaterError(VacuumCleanerError):
    pass

class NoBatteryChargeError(VacuumCleanerError):
    pass

class NoPlaceForGarbage(VacuumCleanerError):
    pass

class IncorrectBatteryCharge(VacuumCleanerInitError):
    pass

class IncorrectAmountOfWater(VacuumCleanerInitError):
    pass

class IncorrectGarbageBinOccupancy(VacuumCleanerInitError):
    pass

class LowBatteryCharge(Exception):
    pass


class VacuumCleaner:

    config = {"waste_difference": 17, "water_difference": 0.3, "battery_difference_for_washing": 5,
              "battery_difference_for_cleaning": 3, "actions_with_low_battery": 6, "max_battery_charge": 100,
              "max_amount_of_water": 100, "max_garbage_bin_occupancy": 100, "low_battery": 20}

    def __init__(self, battery_charge, amount_of_water, garbage_bin_occupancy):
        try:
            with open("vacuum_cleaner.conf") as config:
                for line in config:
                    key = line.split()[0]
                    value = float(line.split()[-1])
                    self.config[key] = value
        except FileNotFoundError:
            print("Config is not found, using default values")
        self.waste_difference = self.config["waste_difference"]
        self.water_difference = self.config["water_difference"]
        self.battery_difference_for_washing = self.config["battery_difference_for_washing"]
        self.battery_difference_for_cleaning = self.config["battery_difference_for_cleaning"]
        self.actions_with_low_battery = self.config["actions_with_low_battery"]
        self.max_battery_charge = self.config["max_battery_charge"]
        self.max_amount_of_water = self.config["max_amount_of_water"]
        self.max_garbage_bin_occupancy = self.config["max_garbage_bin_occupancy"]
        self.low_battery = self.config["low_battery"]
        try:
            self.amount_of_water = amount_of_water
            self.garbage_bin_occupancy = garbage_bin_occupancy
            self.battery_charge = battery_charge
        except VacuumCleanerInitError as error:
            print("Incorrect input params")
            raise error
        except LowBatteryCharge:
            pass

    @property
    def battery_charge(self):
        return self._battery_charge

    @battery_charge.setter
    def battery_charge(self, battery_charge):
        if 0 <= battery_charge <= self.max_battery_charge:
            self._battery_charge = battery_charge
        else:
            raise IncorrectBatteryCharge

    @property
    def amount_of_water(self):
        return self._amount_of_water

    @amount_of_water.setter
    def amount_of_water(self, amount_of_water):
        if 0 <= amount_of_water <= self.max_amount_of_water:
            self._amount_of_water = amount_of_water
        else:
            raise IncorrectAmountOfWater

    @property
    def garbage_bin_occupancy(self):
        return self._garbage_bin_occupancy

    @garbage_bin_occupancy.setter
    def garbage_bin_occupancy(self, garbage_bin_occupancy):
        if 0 <= garbage_bin_occupancy <= self.max_garbage_bin_occupancy:
            self._garbage_bin_occupancy = garbage_bin_occupancy
        else:
            raise IncorrectGarbageBinOccupancy

    def water_using_in_washing(self):
        try:
            self.amount_of_water -= self.water_difference
        except IncorrectAmountOfWater:
            self.amount_of_water = 0
            raise NoWaterError("Washing is not finished")
        if self.amount_of_water == 0:
            raise NoWaterError("Washing is finished")

    def battery_using_in_washing(self):
        try:
            self.battery_charge -= self.battery_difference_for_washing
        except IncorrectBatteryCharge:
            self.battery_charge = 0
            raise NoBatteryChargeError("Washing is not finished")
        if self.battery_charge == 0:
            raise NoBatteryChargeError("Washing is finished")
        elif self.battery_charge <= self.low_battery:
            raise LowBatteryCharge

    def wash(self):
        try:
            self.battery_using_in_washing()
        except LowBatteryCharge as error:
            self.water_using_in_washing()
            print("Wash")
            raise error
        self.water_using_in_washing()
        print("Wash")

    def garbage_adding_in_cleaning(self):
        try:
            self.garbage_bin_occupancy += self.waste_difference
        except IncorrectGarbageBinOccupancy:
            self.garbage_bin_occupancy = self.max_garbage_bin_occupancy
            raise NoPlaceForGarbage("Cleaning is not finished")
        if self.garbage_bin_occupancy == self.max_garbage_bin_occupancy:
            raise NoPlaceForGarbage("Cleaning is finished")

    def battery_using_in_cleaning(self):
        try:
            self.battery_charge -= self.battery_difference_for_cleaning
        except IncorrectBatteryCharge:
            self.battery_charge = 0
            raise NoBatteryChargeError("Cleaning is not finished")
        if self.battery_charge == 0:
            raise NoBatteryChargeError("Cleaning is finished")
        elif self.battery_charge <= self.low_battery:
            raise LowBatteryCharge

    def vacuum_cleaner(self):
        try:
            self.battery_using_in_cleaning()
        except LowBatteryCharge as error:
            self.garbage_adding_in_cleaning()
            print("Vacuum cleaner")
            raise error
        self.garbage_adding_in_cleaning()
        print("Vacuum cleaner")

    def move(self):
        cleaning_enable = True
        washing_enable = True
        local_actions_with_low_battery = self.actions_with_low_battery
        while local_actions_with_low_battery > 0 and (cleaning_enable or washing_enable):
            print(f"battery {self.battery_charge:.1f}, water {self.amount_of_water:.1f} trash, "
                  f"{self.garbage_bin_occupancy:.1f}")
            print("Move ---")
            if washing_enable:
                try:
                    self.wash()
                except LowBatteryCharge:
                    local_actions_with_low_battery -= 1
                except NoWaterError as error:
                    if error.args:
                        print(error.args[0])
                    print("Water is over")
                    washing_enable = False
                except NoBatteryChargeError as error:
                    print(error.args[0])
                    print("Battery charge is over")
                    break
            if cleaning_enable:
                try:
                    self.vacuum_cleaner()
                except LowBatteryCharge:
                    local_actions_with_low_battery -= 1
                except NoPlaceForGarbage as error:
                    if error.args:
                        print(error.args[0])
                    print("Garbage bin is full")
                    cleaning_enable = False
                except NoBatteryChargeError as error:
                    print(error.args[0])
                    print("Battery charge is over")
                    break
            sleep(1)


# v = VacuumCleaner(40, 5, 20)
# v.move()
