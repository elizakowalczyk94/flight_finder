import pandas

USER_DATA_CSV = "users_data.csv"


class NewUserManager:

    def __init__(self, user_name, user_last_name, user_email):
        self.user_name = user_name
        self.user_last_name = user_last_name
        self.user_email = user_email

    def add_new_user(self):
        new_user_data = {"user_name": [self.user_name],
                         "user_last_name": [self.user_last_name],
                         "user_email": [self.user_email]}
        new_user_data_frame = pandas.DataFrame(new_user_data)
        new_user_data_frame.to_csv(USER_DATA_CSV, mode='a', index=False, header=False)
