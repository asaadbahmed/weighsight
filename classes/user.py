class User:
    def __init__(self, data):
        self.authenticated = False
        self.name = data.get('name', "Asaad Ahmed")
        self.age = data.get('age', 20)
        self.goal = data.get('goal', 140)
        self.height = data.get('height', 189)
        self.gender = data.get('gender', 'M')
    
    def auth():
        print("do OAUTH0 stuff")
