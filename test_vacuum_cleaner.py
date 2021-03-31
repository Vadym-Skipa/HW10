import unittest
import vacuum_cleaner


class TestClass(unittest.TestCase):

    def setUp(self) -> None:
        self.default_vacuum_cleaner = vacuum_cleaner.VacuumCleaner(0, 0, 0)
        self.max_vacuum_cleaner = vacuum_cleaner.VacuumCleaner(self.default_vacuum_cleaner.max_battery_charge,
                                                               self.default_vacuum_cleaner.max_amount_of_water, 0)
        self.max_vacuum_cleaner.waste_difference = 1
        self.max_vacuum_cleaner.water_difference = 1
        self.max_vacuum_cleaner.battery_difference_for_washing = 1
        self.max_vacuum_cleaner.battery_difference_for_cleaning = 1
        self.max_vacuum_cleaner.actions_with_low_battery = 4
        self.max_vacuum_cleaner.max_battery_charge = 200
        self.max_vacuum_cleaner.max_amount_of_water = 100
        self.max_vacuum_cleaner.max_garbage_bin_occupancy = 100
        self.max_vacuum_cleaner.low_battery = 40
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
        with self.assertRaises(vacuum_cleaner.NoWaterError):
            for i in range(10000):
                self.max_vacuum_cleaner.water_using_in_washing()

    def test_battery_using_in_washing(self):
        with self.assertRaises(vacuum_cleaner.LowBatteryCharge):
            for i in range(10000):
                self.max_vacuum_cleaner.battery_using_in_washing()

    def test_garbage_adding_in_cleaning(self):
        with self.assertRaises(vacuum_cleaner.NoPlaceForGarbage):
            for i in range(10000):
                self.max_vacuum_cleaner.garbage_adding_in_cleaning()

    def test_battery_using_in_cleaning(self):
        with self.assertRaises(vacuum_cleaner.LowBatteryCharge):
            for i in range(10000):
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
