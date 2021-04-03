# from time import sleep
#
# class VacuumCleanerInitError(Exception):
#     pass
#
# class VacuumCleanerError(Exception):
#     pass
#
# class NoWaterError(VacuumCleanerError):
#     pass
#
# class NoBatteryChargeError(VacuumCleanerError):
#     pass
#
# class NoPlaceForGarbage(VacuumCleanerError):
#     pass
#
# class IncorrectBatteryCharge(VacuumCleanerInitError):
#     pass
#
# class IncorrectAmountOfWater(VacuumCleanerInitError):
#     pass
#
# class IncorrectGarbageBinOccupancy(VacuumCleanerInitError):
#     pass
#
# class LowBatteryCharge(Exception):
#     pass
#
#
# class VacuumCleaner:
#
#     config = {"waste_difference": 17, "water_difference": 0.3, "battery_difference_for_washing": 5,
#               "battery_difference_for_cleaning": 3, "actions_with_low_battery": 6, "max_battery_charge": 100,
#               "max_amount_of_water": 100, "max_garbage_bin_occupancy": 100, "low_battery": 20}
#
#     def __init__(self, battery_charge, amount_of_water, garbage_bin_occupancy):
#         try:
#             with open("vacuum_cleaner.conf") as config:
#                 for line in config:
#                     key = line.split()[0]
#                     value = float(line.split()[-1])
#                     self.config[key] = value
#         except FileNotFoundError:
#             print("Config is not found, using default values")
#         self.waste_difference = self.config["waste_difference"]
#         self.water_difference = self.config["water_difference"]
#         self.battery_difference_for_washing = self.config["battery_difference_for_washing"]
#         self.battery_difference_for_cleaning = self.config["battery_difference_for_cleaning"]
#         self.actions_with_low_battery = self.config["actions_with_low_battery"]
#         self.max_battery_charge = self.config["max_battery_charge"]
#         self.max_amount_of_water = self.config["max_amount_of_water"]
#         self.max_garbage_bin_occupancy = self.config["max_garbage_bin_occupancy"]
#         self.low_battery = self.config["low_battery"]
#         try:
#             self.amount_of_water = amount_of_water
#             self.garbage_bin_occupancy = garbage_bin_occupancy
#             self.battery_charge = battery_charge
#         except VacuumCleanerInitError as error:
#             print("Incorrect input params")
#             raise error
#         except LowBatteryCharge:
#             pass
#
#     @property
#     def battery_charge(self):
#         return self._battery_charge
#
#     @battery_charge.setter
#     def battery_charge(self, battery_charge):
#         if 0 <= battery_charge <= self.max_battery_charge:
#             self._battery_charge = battery_charge
#         else:
#             raise IncorrectBatteryCharge
#
#     @property
#     def amount_of_water(self):
#         return self._amount_of_water
#
#     @amount_of_water.setter
#     def amount_of_water(self, amount_of_water):
#         if 0 <= amount_of_water <= self.max_amount_of_water:
#             self._amount_of_water = amount_of_water
#         else:
#             raise IncorrectAmountOfWater
#
#     @property
#     def garbage_bin_occupancy(self):
#         return self._garbage_bin_occupancy
#
#     @garbage_bin_occupancy.setter
#     def garbage_bin_occupancy(self, garbage_bin_occupancy):
#         if 0 <= garbage_bin_occupancy <= self.max_garbage_bin_occupancy:
#             self._garbage_bin_occupancy = garbage_bin_occupancy
#         else:
#             raise IncorrectGarbageBinOccupancy
#
#     def water_using_in_washing(self):
#         try:
#             self.amount_of_water -= self.water_difference
#         except IncorrectAmountOfWater:
#             self.amount_of_water = 0
#             raise NoWaterError("Washing is not finished")
#         if self.amount_of_water == 0:
#             raise NoWaterError("Washing is finished")
#
#     def battery_using_in_washing(self):
#         try:
#             self.battery_charge -= self.battery_difference_for_washing
#         except IncorrectBatteryCharge:
#             self.battery_charge = 0
#             raise NoBatteryChargeError("Washing is not finished")
#         if self.battery_charge == 0:
#             raise NoBatteryChargeError("Washing is finished")
#         elif self.battery_charge <= self.low_battery:
#             raise LowBatteryCharge
#
#     def wash(self):
#         try:
#             self.battery_using_in_washing()
#         except LowBatteryCharge as error:
#             self.water_using_in_washing()
#             print("Wash")
#             raise error
#         self.water_using_in_washing()
#         print("Wash")
#
#     def garbage_adding_in_cleaning(self):
#         try:
#             self.garbage_bin_occupancy += self.waste_difference
#         except IncorrectGarbageBinOccupancy:
#             self.garbage_bin_occupancy = self.max_garbage_bin_occupancy
#             raise NoPlaceForGarbage("Cleaning is not finished")
#         if self.garbage_bin_occupancy == self.max_garbage_bin_occupancy:
#             raise NoPlaceForGarbage("Cleaning is finished")
#
#     def battery_using_in_cleaning(self):
#         try:
#             self.battery_charge -= self.battery_difference_for_cleaning
#         except IncorrectBatteryCharge:
#             self.battery_charge = 0
#             raise NoBatteryChargeError("Cleaning is not finished")
#         if self.battery_charge == 0:
#             raise NoBatteryChargeError("Cleaning is finished")
#         elif self.battery_charge <= self.low_battery:
#             raise LowBatteryCharge
#
#     def vacuum_cleaner(self):
#         try:
#             self.battery_using_in_cleaning()
#         except LowBatteryCharge as error:
#             self.garbage_adding_in_cleaning()
#             print("Vacuum cleaner")
#             raise error
#         self.garbage_adding_in_cleaning()
#         print("Vacuum cleaner")
#
#     def move(self):
#         cleaning_enable = True
#         washing_enable = True
#         local_actions_with_low_battery = self.actions_with_low_battery
#         while local_actions_with_low_battery > 0 and (cleaning_enable or washing_enable):
#             print(f"battery {self.battery_charge:.1f}, water {self.amount_of_water:.1f} trash, "
#                   f"{self.garbage_bin_occupancy:.1f}")
#             print("Move ---")
#             if washing_enable:
#                 try:
#                     self.wash()
#                 except LowBatteryCharge:
#                     local_actions_with_low_battery -= 1
#                 except NoWaterError as error:
#                     if error.args:
#                         print(error.args[0])
#                     print("Water is over")
#                     washing_enable = False
#                 except NoBatteryChargeError as error:
#                     print(error.args[0])
#                     print("Battery charge is over")
#                     break
#             if cleaning_enable:
#                 try:
#                     self.vacuum_cleaner()
#                 except LowBatteryCharge:
#                     local_actions_with_low_battery -= 1
#                 except NoPlaceForGarbage as error:
#                     if error.args:
#                         print(error.args[0])
#                     print("Garbage bin is full")
#                     cleaning_enable = False
#                 except NoBatteryChargeError as error:
#                     print(error.args[0])
#                     print("Battery charge is over")
#                     break
#             sleep(1)


import unittest
import vacuum_cleaner


class TestClass(unittest.TestCase):

    def setUp(self) -> None:
        self.default_vacuum_cleaner = vacuum_cleaner.VacuumCleaner(0, 0, 0)
        self.max_vacuum_cleaner = vacuum_cleaner.VacuumCleaner(0, 0, 0)
        self.max_vacuum_cleaner.waste_difference = 1
        self.max_vacuum_cleaner.water_difference = 1
        self.max_vacuum_cleaner.battery_difference_for_washing = 1
        self.max_vacuum_cleaner.battery_difference_for_cleaning = 1
        self.max_vacuum_cleaner.actions_with_low_battery = 4
        self.max_vacuum_cleaner.max_battery_charge = 200
        self.max_vacuum_cleaner.max_amount_of_water = 100
        self.max_vacuum_cleaner.max_garbage_bin_occupancy = 100
        self.max_vacuum_cleaner.low_battery = 40
        self.max_vacuum_cleaner.battery_charge = 200
        self.max_vacuum_cleaner.amount_of_water = 100
        self.low_battery_cleaner = vacuum_cleaner.VacuumCleaner(self.default_vacuum_cleaner.low_battery,
                                                                self.default_vacuum_cleaner.max_amount_of_water, 0)
        self.no_water_cleaner = vacuum_cleaner.VacuumCleaner(self.default_vacuum_cleaner.max_battery_charge, 0, 0)
        self.full_cleaner = vacuum_cleaner.VacuumCleaner(self.default_vacuum_cleaner.max_battery_charge, 0,
                                                         self.default_vacuum_cleaner.max_garbage_bin_occupancy)

    def test_battery_charge(self):
        with self.assertRaises(vacuum_cleaner.IncorrectBatteryCharge):
            self.default_vacuum_cleaner.battery_charge = self.default_vacuum_cleaner.max_battery_charge + 1
        with self.assertRaises(vacuum_cleaner.IncorrectBatteryCharge):
            self.default_vacuum_cleaner.battery_charge = self.default_vacuum_cleaner.max_battery_charge + 0.1
        with self.assertRaises(vacuum_cleaner.IncorrectBatteryCharge):
            self.default_vacuum_cleaner.battery_charge = -1
        with self.assertRaises(vacuum_cleaner.IncorrectBatteryCharge):
            self.default_vacuum_cleaner.battery_charge = -0.1
        temp_charge = self.default_vacuum_cleaner.max_battery_charge / 2
        self.default_vacuum_cleaner.battery_charge = temp_charge
        self.assertEqual(self.default_vacuum_cleaner.battery_charge, temp_charge)

    def test_amount_of_water(self):
        with self.assertRaises(vacuum_cleaner.IncorrectAmountOfWater):
            self.default_vacuum_cleaner.amount_of_water = self.default_vacuum_cleaner.max_amount_of_water + 1
        with self.assertRaises(vacuum_cleaner.IncorrectAmountOfWater):
            self.default_vacuum_cleaner.amount_of_water = self.default_vacuum_cleaner.max_amount_of_water + 0.1
        with self.assertRaises(vacuum_cleaner.IncorrectAmountOfWater):
            self.default_vacuum_cleaner.amount_of_water = -1
        with self.assertRaises(vacuum_cleaner.IncorrectAmountOfWater):
            self.default_vacuum_cleaner.amount_of_water = -0.1
        temp_amount = self.default_vacuum_cleaner.max_amount_of_water / 2
        self.default_vacuum_cleaner.amount_of_water = temp_amount
        self.assertEqual(self.default_vacuum_cleaner.amount_of_water, temp_amount)

    def test_garbage_bin_occupancy(self):
        with self.assertRaises(vacuum_cleaner.IncorrectGarbageBinOccupancy):
            self.default_vacuum_cleaner.garbage_bin_occupancy = self.default_vacuum_cleaner.max_garbage_bin_occupancy + 1
        with self.assertRaises(vacuum_cleaner.IncorrectGarbageBinOccupancy):
            self.default_vacuum_cleaner.garbage_bin_occupancy = self.default_vacuum_cleaner.max_garbage_bin_occupancy + 0.1
        with self.assertRaises(vacuum_cleaner.IncorrectGarbageBinOccupancy):
            self.default_vacuum_cleaner.garbage_bin_occupancy = -1
        with self.assertRaises(vacuum_cleaner.IncorrectGarbageBinOccupancy):
            self.default_vacuum_cleaner.garbage_bin_occupancy = -0.1
        temp_garbage = self.default_vacuum_cleaner.max_garbage_bin_occupancy / 2
        self.default_vacuum_cleaner.garbage_bin_occupancy = temp_garbage
        self.assertEqual(self.default_vacuum_cleaner.garbage_bin_occupancy, temp_garbage)

    def test_init(self):
        params_error = [
            (-1, 1, 1),
            (-1, -1, 1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, -1),
            (1, -1, -1),
            (self.default_vacuum_cleaner.max_battery_charge+1, 1, 1),
            (self.default_vacuum_cleaner.max_battery_charge+1, self.default_vacuum_cleaner.max_amount_of_water+1, 1),
            (self.default_vacuum_cleaner.max_battery_charge+1, 1, self.default_vacuum_cleaner.max_garbage_bin_occupancy+1),
            (self.default_vacuum_cleaner.max_battery_charge+1, self.default_vacuum_cleaner.max_amount_of_water+1, self.default_vacuum_cleaner.max_garbage_bin_occupancy+1),
            (1, self.default_vacuum_cleaner.max_amount_of_water+1, 1),
            (1, 1, self.default_vacuum_cleaner.max_garbage_bin_occupancy+1),
            (-1, self.default_vacuum_cleaner.max_amount_of_water+1, self.default_vacuum_cleaner.max_garbage_bin_occupancy+1)
        ]
        for a, b, c in params_error:
            with self.subTest(a=a, b=b, c=c):
                with self.assertRaises(vacuum_cleaner.VacuumCleanerInitError):
                    vacuum_cleaner.VacuumCleaner(a, b, c)
        temp_vacuum_cleaner = vacuum_cleaner.VacuumCleaner(self.default_vacuum_cleaner.max_battery_charge/2,
                                                           self.default_vacuum_cleaner.max_amount_of_water/2,
                                                           self.default_vacuum_cleaner.max_garbage_bin_occupancy/2)
        self.assertEqual(temp_vacuum_cleaner.battery_charge, self.default_vacuum_cleaner.max_battery_charge/2)
        self.assertEqual(temp_vacuum_cleaner.amount_of_water, self.default_vacuum_cleaner.max_amount_of_water/2)
        self.assertEqual(temp_vacuum_cleaner.garbage_bin_occupancy, self.default_vacuum_cleaner.max_garbage_bin_occupancy/2)

    def test_water_using_in_washing(self):
        for i in range(99):
            self.max_vacuum_cleaner.water_using_in_washing()
        with self.assertRaises(vacuum_cleaner.NoWaterError):
            self.max_vacuum_cleaner.water_using_in_washing()

    def test_battery_using_in_washing(self):
        for i in range(159):
            self.max_vacuum_cleaner.battery_using_in_washing()
        with self.assertRaises(vacuum_cleaner.LowBatteryCharge):
            self.max_vacuum_cleaner.battery_using_in_washing()
        for i in range(39):
            try:
                self.max_vacuum_cleaner.battery_using_in_washing()
            except vacuum_cleaner.LowBatteryCharge:
                pass
        with self.assertRaises(vacuum_cleaner.NoBatteryChargeError):
            self.max_vacuum_cleaner.battery_using_in_washing()

    def test_garbage_adding_in_cleaning(self):
        for i in range(99):
            self.max_vacuum_cleaner.garbage_adding_in_cleaning()
        with self.assertRaises(vacuum_cleaner.NoPlaceForGarbage):
            self.max_vacuum_cleaner.garbage_adding_in_cleaning()

    def test_battery_using_in_cleaning(self):
        for i in range(159):
            self.max_vacuum_cleaner.battery_using_in_cleaning()
        with self.assertRaises(vacuum_cleaner.LowBatteryCharge):
            self.max_vacuum_cleaner.battery_using_in_cleaning()
        for i in range(39):
            try:
                self.max_vacuum_cleaner.battery_using_in_cleaning()
            except vacuum_cleaner.LowBatteryCharge:
                pass
        with self.assertRaises(vacuum_cleaner.NoBatteryChargeError):
            self.max_vacuum_cleaner.battery_using_in_cleaning()

    def test_wash(self):
        with self.assertRaises(vacuum_cleaner.LowBatteryCharge):
            self.low_battery_cleaner.wash()
        with self.assertRaises(vacuum_cleaner.NoBatteryChargeError):
            self.default_vacuum_cleaner.wash()
        with self.assertRaises(vacuum_cleaner.NoWaterError):
            self.no_water_cleaner.wash()

    def test_vacuum_cleaner(self):
        with self.assertRaises(vacuum_cleaner.LowBatteryCharge):
            self.low_battery_cleaner.vacuum_cleaner()
        with self.assertRaises(vacuum_cleaner.NoBatteryChargeError):
            self.default_vacuum_cleaner.vacuum_cleaner()
        with self.assertRaises(vacuum_cleaner.NoPlaceForGarbage):
            self.full_cleaner.vacuum_cleaner()
