class MySetting:
    def __init__(self, request):
        self.session = request.session
        self.setting = request.session.get('myset')
        if not self.setting:
            self.setting = request.session['myset'] = {'bgc': '#151817', 'frc': '#eee'}

    def avazkon(self, bgc, frc):
        self.setting['bgc'] = bgc
        self.setting['frc'] = frc
        self.session.modified = True
