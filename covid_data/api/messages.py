class Message():
    """
        Custom class to send error/response messages
    """
    CODE_MAP = {
        1: 'SignUp Successfully',
        2: 'Login Successful',
        3: 'Something went wrong',
        4: "First name is too short",
        5: "Last name is too short",
        6: "Name shouldn't contain number",
        7: "Read Successful",
        8: "Logout successful",
        9: "Unable to logout",
    }

    @classmethod
    def code(cls, code):
        return cls.CODE_MAP.get(code, 'Unknown')
