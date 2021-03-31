import unittest
import login_register
import random

class TestRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.users = login_register.Users()

    def test_check_email(self):
        wrong_emails = [
            "123453263275",
            "145jh2kj4gk4",
            "sfdhfsh585asgd.dsag",
            "adsjfhak@gmailcom",
            "asffsgerw4trew@asf,asd",
            "!qwrqwrr@gmail.com",
            "asfsfa@1as.d",
            "",
            "@gmail.com"
        ]
        wrong_chars = ['!', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+', '`', '~', '[', '{', '_'
                       ']', '}', '\\', '|', ';', ':', '\'', '"', ',', '<', '>', '/', '?', ' ', '\t', '\n']
        for char in wrong_chars:
            wrong_emails.append(char + "mail@gmail.com")
        for email in wrong_emails:
            with self.assertRaises(login_register.WrongEmailError):
                login_register.Register.check_email(email)
        good_emails = [
            "some@gmail.com",
            "1@i.ua",
            "1a2b3c@ukr.net",
            "ABC@abc.abc"
        ]
        for email in good_emails:
            self.assertTrue(login_register.Register.check_email(email))

    def test_check_name(self):
        wrong_chars = ['!', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+', '`', '~', '[', '{', ']', '}', '\\',
                       '|', ';', ':', '\'', '"', ',', '<', '>', '/', '?', ' ', '\t', '\n', '.', '@']
        wrong_names = ["", "123456789012345678901234567890123456789012345678901", "1", "12", "123", "1234", "12345"]
        for char in wrong_chars:
            wrong_names.append(char + "namename")
        for name in wrong_names:
            with self.assertRaises(login_register.WrongNameError):
                login_register.Register.check_name(name)
        good_names = ["123456", "AbCdEf123", "12345678901234567890123456789012345678901234567890", "space_"]
        for name in good_names:
            self.assertTrue(login_register.Register.check_name(name))

    def test_check_password(self):
        wrong_passwords = ["123456789", "123456789012345678901", "aaaabbaaaa", "AAAABBAAAA", "AAAA11AAAA", "aaaa11aaaa",
                      "AAAAaaAAAA"]
        wrong_chars = ['!', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+', '`', '~', '[', '{', ']', '}', '\\',
                       '|', ';', ':', '\'', '"', ',', '<', '>', '/', '?', ' ', '\t', '\n', '.', '@', '_']
        for char in wrong_chars:
            wrong_passwords.append(char + "aB3dE6gH90")
        for password in wrong_passwords:
            with self.assertRaises(login_register.WrongPasswordError):
                login_register.Register.check_password(password)
        good_passwords = ["aB3dE6gH90", "12345678No12345678No", "0h763hGaHFD6qsf"]
        for password in good_passwords:
            self.assertTrue(login_register.Register.check_password(password))

    def test_register(self):
        self.assertEqual(login_register.Register.register("some@gmail.com", "123456", "aB3dE6gH90", self.users), "200")
        with self.assertRaises(login_register.EmailIsRegistered):
            login_register.Register.register("some@gmail.com", "123456", "aB3dE6gH90", self.users)
        with self.assertRaises(login_register.NameIsRegistered):
            login_register.Register.register("some1@gmail.com", "123456", "aB3dE6gH90", self.users)
        with self.assertRaises(login_register.WrongPasswordError):
            login_register.Register.register("some1@gmail.com", "123456", "123456789", self.users)
        with self.assertRaises(login_register.WrongNameError):
            login_register.Register.register("some1@gmail.com", "12345", "aB3dE6gH90", self.users)
        with self.assertRaises(login_register.WrongEmailError):
            login_register.Register.register("s!qwrqwrr@gmail.com", "123456", "aB3dE6gH90", self.users)

class TestLogIn(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.users = login_register.Users()
        try:
            login_register.Register.register("some@gmail.com", "123456", "aB3dE6gH90", cls.users)
        except login_register.EmailIsRegistered:
            pass

    def test_check_email(self):
        self.assertTrue(login_register.LogIn.check_email("some@gmail.com", self.users))
        with self.assertRaises(login_register.EmailIsNotRegistered):
            random_email = "@random.mail"
            for i in range(20):
                random_email = random.choice("qwertyuioplkjhgfdsazxcvbnm1234567890QWERTYUIOPLKJHGFDSAZXCVBNM.") + random_email
            for i in range(100):
                login_register.LogIn.check_email(random_email, self.users)

    def test_check_password(self):
        with self.assertRaises(login_register.WrongLogInPassword):
            login_register.LogIn.check_password("some@gmail.com", "wRONGpASSWORD1", self.users)
        self.assertTrue(login_register.LogIn.check_password("some@gmail.com", "aB3dE6gH90", self.users))

    def test_log_in(self):
        self.assertIsInstance(login_register.LogIn.log_in("some@gmail.com", "aB3dE6gH90", self.users), login_register.UserToken)
