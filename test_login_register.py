# import re
# import random
#
#
# class RegisterError(Exception):
#     pass
#
#
# class WrongEmailError(RegisterError):
#     pass
#
#
# class WrongNameError(RegisterError):
#     pass
#
#
# class WrongPasswordError(RegisterError):
#     pass
#
#
# class EmailIsRegistered(RegisterError):
#     pass
#
#
# class NameIsRegistered(RegisterError):
#     pass
#
#
# class LogInError(Exception):
#     pass
#
#
# class EmailIsNotRegistered(LogInError):
#     pass
#
#
# class WrongLogInPassword(LogInError):
#     pass
#
#
# class Users:
#     def __init__(self):
#         self.users = {}
#         self.names = []
#
#
# class Register:
#
#     @classmethod
#     def check_email(cls, email: str):
#         pattern = "[a-zA-Z0-9.]+@[a-z.]+\.[a-z]+"
#         empty_str, number = re.subn(pattern, "", email)
#         if empty_str == "" and number == 1:
#             return True
#         raise WrongEmailError
#
#     @classmethod
#     def check_name(cls, name: str):
#         pattern = "\w{6,50}"
#         empty_str, number = re.subn(pattern, "", name)
#         if empty_str == "" and number == 1:
#             return True
#         raise WrongNameError
#
#     @classmethod
#     def check_password(cls, password: str):
#         pattern_high_case = "[A-Z]"
#         pattern_low_case = "[a-z]"
#         pattern_digit = "\d"
#         first_str, number_of_high_case = re.subn(pattern_high_case, "", password)
#         second_str, number_of_low_case = re.subn(pattern_low_case, "", first_str)
#         empty_str, number_of_digit = re.subn(pattern_digit, "", second_str)
#         if empty_str == "" and number_of_high_case > 0 and number_of_low_case > 0 and number_of_digit > 0 \
#                 and 10 <= (number_of_digit + number_of_low_case + number_of_high_case) <= 20:
#             return True
#         raise WrongPasswordError
#
#     @classmethod
#     def register(cls, email, name, password, users: Users):
#         if cls.check_email(email) and cls.check_name(name) and cls.check_password(password):
#             if email in users.users:
#                 raise EmailIsRegistered
#             if name in users.names:
#                 raise NameIsRegistered
#             users.users.update({email: (password, name)})
#             users.names.append(name)
#             return "200"
#         raise RegisterError
#
#
# class LogIn:
#
#     @classmethod
#     def check_email(cls, email: str, users: Users):
#         if Register.check_email(email):
#             if email in users.users:
#                 return True
#         raise EmailIsNotRegistered
#
#     @classmethod
#     def check_password(cls, email: str, password: str, users: Users):
#         if Register.check_password(password):
#             if users.users[email][0] == password:
#                 return True
#         raise WrongLogInPassword
#
#     @classmethod
#     def log_in(cls, email: str, password: str, users: Users):
#         if cls.check_email(email, users) and cls.check_password(email, password, users):
#             return UserToken()
#         raise LogInError
#
#
# class UserToken:
#     def __init__(self):
#         temp_str = ""
#         number = random.randrange(50, 100)
#         for i in range(number):
#             temp_str += random.choice("qwertyuioplkjhgfdsazxcvbnm1234567890QWERTYUIOPLKJHGFDSAZXCVBNM")
#         self.token = temp_str



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
