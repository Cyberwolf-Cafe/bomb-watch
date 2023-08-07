import requests
import time

public = [ 'L40rkMstF9EBf6ot','OAcNEgiQDLEqFrWN','z2yBESInhPVYyu9X','898szq7wFzqQNavI','RMnezNsDlOEWcQRT','8DSWgTc1p9qw4glE','cMVWgTHmZYwcY4bN','AaLriihrkMnmBD7L','lJp5R2YgJAj1kaeX','yKKF6ojFnKfpfvPQ','svVElBgcdg2TFDBN','P56sLMUVdJuQq5HX','C4zWLZTgXx7mxhNj','2Fu8cks7Vi90GOSv','ZsL5SsGiZdhRvX7V','s9y8GDT8Y2qFmGhm','d71EEUSkhH439YAn','5fTssuOlSzezbKel']

faction = ['RWbcb8LWxr6qHQCF']

class Fetch:
    def __init__(self, keys):
        self.keys = keys
        self.err = {key:0 for key in keys}
        self.i = 0
        self.t0 = int(time.time()) - 600
    def get(self, selections):
        delay = 0
        for j in self.keys:
            self.i += 1
            if self.i >= len(self.keys):
                self.i = 0
            key = self.keys[self.i]
            r = requests.get(f'https://api.torn.com/{selections}&key={key}').json()
            if 'error' in r:
                self.err[key] += 1
                avg = 0
                for k in self.keys:
                    avg += self.err[k]
                avg /= len(self.keys)
                if (self.err[key] - avg) > 2:
                    del self.keys[self.i] #Too many errors
                    self.i -= 1
                time.sleep(delay)
                delay = delay*2 + 10
            else:
                return r
    def revivable(self,userid):
        r = self.get(f'user/{userid}?selections=profile')
        return (r['name'],r['revivable']==1,r['status']['state'])
    def userstatus(self,userid):
        r = self.get(f'user/{userid}?selections=basic')
        return (r['name'],r['status']['state'])
    def revive_history(self):
        r = self.get(f'faction/?selections=revives&from={self.t0}')
        r = r['revives']
        if len(r) > 0:
            self.t0 = r[list(r)[0]]['timestamp'] #Get last timestamp
            print(self.t0)
        return r
            

