import model

def check(username, password):
    """ Checks username and password """
    if (model.Users.selectBy(username=username, password=password).count() != 1):
        return 'Wrong username or password.'