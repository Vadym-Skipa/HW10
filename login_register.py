import re
import random


class RegisterError(Exception):
    pass


class WrongEmailError(RegisterError):
    pass


class WrongNameError(RegisterError):
    pass


class WrongPasswordError(RegisterError):
    pass


class EmailIsRegistered(RegisterError):
    pass


class NameIsRegistered(RegisterError):
    pass


class LogInError(Exception):
    pass


class EmailIsNotRegistered(LogInError):
    pass


class WrongLogInPassword(LogInError):
    pass


class Users:
    def __init__(self):
        self.users = {}
        self.names = []


class Register:

    @classmethod
    def check_email(cls, email: str):
        pattern = "[a-zA-Z0-9.]+@[a-z.]+\.[a-z]+"
        empty_str, number = re.subn(pattern, "", email)
        if empty_str == "" and number == 1:
            return True
        raise WrongEmailError

    @classmethod
    def check_name(cls, name: str):
        pattern = "\w{6,50}"
        empty_str, number = re.subn(pattern, "", name)
        if empty_str == "" and number == 1:
            return True
        raise WrongNameError

    @classmethod
    def check_password(cls, password: str):
        pattern_high_case = "[A-Z]"
        pattern_low_case = "[a-z]"
        pattern_digit = "\d"
        first_str, number_of_high_case = re.subn(pattern_high_case, "", password)
        second_str, number_of_low_case = re.subn(pattern_low_case, "", first_str)
        empty_str, number_of_digit = re.subn(pattern_digit, "", second_str)
        if empty_str == "" and number_of_high_case > 0 and number_of_low_case > 0 and number_of_digit > 0 \
                and 10 <= (number_of_digit + number_of_low_case + number_of_high_case) <= 20:
            return True
        raise WrongPasswordError

    @classmethod
    def register(cls, email, name, password, users: Users):
        if cls.check_email(email) and cls.check_name(name) and cls.check_password(password):
            if email in users.users:
                raise EmailIsRegistered
            if name in users.names:
                raise NameIsRegistered
            users.users.update({email: (password, name)})
            users.names.append(name)
            return "200"
        raise RegisterError


class LogIn:

    @classmethod
    def check_email(cls, email: str, users: Users):
        if Register.check_email(email):
            if email in users.users:
                return True
        raise EmailIsNotRegistered

    @classmethod
    def check_password(cls, email: str, password: str, users: Users):
        if Register.check_password(password):
            if users.users[email][0] == password:
                return True
        raise WrongLogInPassword

    @classmethod
    def log_in(cls, email: str, password: str, users: Users):
        if cls.check_email(email, users) and cls.check_password(email, password, users):
            return UserToken()
        raise LogInError


class UserToken:
    def __init__(self):
        temp_str = ""
        number = random.randrange(50, 100)
        for i in range(number):
            temp_str += random.choice("qwertyuioplkjhgfdsazxcvbnm1234567890QWERTYUIOPLKJHGFDSAZXCVBNM")
        self.token = temp_str
