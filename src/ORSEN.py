from src.textunderstanding import InputDecoder
from . import Logger
from src.dbo.user import DBOUser
from src.models.user import User
class ORSEN:

    def __init___(self):
        super().__init__()
        # Database access
        self.dbo_user = DBOUser('users', User)

    """ A part of me tells me na we need to have a different method for getting input para mabilis na lang ayusin soon pag sa iba gagamitin."""
    def get_input(self):
        user_input = input()
        return user_input

    def login_signup(self):
        print("Hi! Do you have an account? (Y/N)")
        user_input = input()

        if user_input == "Y":  # login
            self.login()
        else:
            self.signup()
        print(curr_user)

    def login(self):
        # ask for user details
        is_done = False

        while not is_done:
            print("What's your username?")
            name = input()
            print("What's is the secret code?")
            code = input()

            temp_user = self.dbo_user.get_specific_user(name, code)

            if temp_user is None:
                print("I don't think that's right. Can you try again?")

            else:
                # store user
                self.set_global_curr_user(temp_user)
                print("Hi! Welcome back ", name)
                is_done = True

    def signup(self):
        print("What's your username?")
        name = input()
        print("What's is the secret code?")
        code = input()

        self.set_global_curr_user(self.dbo_user.add_user(User(-1, name, code)))

    def login_signup_automatic(self):
        print("What's your name?")
        name = self.get_input()

        user_list = self.dbo_user.get_user_by_name('name')
        if user_list is not []:
            print("Do we have a secret code?")
            has_code_answer = self.get_input()
            has_code = False

            if has_code_answer.lower() == "y" or has_code_answer.lower() == "yes":
                print("What is the secret code?")
                input_code = self.get_input()
                temp_user = self.dbo_user.get_specific_user(name, input_code)

            else:
                # has_code_answer.lower() == "n" or has_code_answer.lower() == "no":
                print("Alright then let's make one! What should it be?")
                input_code = self.get_input()
                temp_user = self.dbo_user.add_user(User(-1, name, input_code))

            self.set_global_curr_user(temp_user)
            print("Alright %s, let's make a story. You start!")


    def set_global_curr_user(self, user):
        global curr_user
        curr_user = user

    def execute_text_understanding(self, input):
        result = InputDecoder.annotate_input(input)
        print("Printing result")
        print(result)

    def start_conversation(self):
        # Initialize loggers
        Logger.setup_loggers()

        print("Input text")














