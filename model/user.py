from flask_login import UserMixin as logMix

class User(logMix):
    name = ""
    lName = ""
    email = ""
    pNumber = ""
    role = ""
    roleID = ""

    def __init__(self, form, role):
        self.name = form[0]
        self.lName = form[1]
        self.email = form[2]
        self.pNumber = form[3]
        if role == "C":
            self.role = "Client"
        elif role == "W":
            self.role = "Worker"
        elif role == "A":
            self.role = "Admin"
        self.roleID = form[4]
    pass
    '''
    id = ""
    name = ""
    lName = ""

    def __init__(self, roles=[]):
        self.roles = set(roles)

    def set_id(self, email):
        self.id = email

    def add_role(self, role):
        self.roles.append(role)

    def add_roles(self, roles):
        for role in roles:
            self.add_role(role)

    def __repr__(self):
        return 'User %s' % self.roles

    def object(self):
        result=[]
        for role in self.roles:
            result.append(role.object())

    def get_id(self):
        print(self.id)
        return self.id

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    '''
#class Role(RoleMixin):
    #pass
