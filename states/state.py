class state:
    def __init__(self, gm, um, em, lm, rm, am):
        self.gm = gm
        self.um = um
        self.em = em
        self.lm = lm
        self.rm = rm
        self.am = am

    def register_onStart(self, func):
        self.onStart = func
        return func

    def register_onUpdate(self, func):
        self.onUpdate = func
        return func
