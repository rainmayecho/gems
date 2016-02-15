import itertools, sys, signal

def flatten(l):
    return [item for sublist in l for item in sublist]

class Field(object):
    def __init__(self, num_players, stagger=None):
        self.NUM_PLAYERS = num_players
        self.stagger = stagger
        self.names = {}
        self.BASE_GEMS = []
        self.G = {}
        self.field = []
        self.player_rolls = []
        self.player_one_shots = [[] for _ in xrange(num_players)]
        self.pending_merge_list = []
        self.real_merge_list = []

        self._init_field()
        self._init_graph()
        self._run()

    def _init_field(self):
        self.BASE_GEMS = flatten([[g+q for q in '12345'] for g in 'BDYERGQP'])
        with open('constants.txt', 'r') as f:
            for line in f:
                k, v = line.strip().split('=')
                self.names[k] = v

    def _init_graph(self):
        for v in self.BASE_GEMS:
            self.G[v] = set()

        with open('gem_list.txt', 'r') as f:
            for line in f:
                k, v = line.strip().split(':')
                self.G[k] = set(v.split(','))

    def _run(self):
        try:
            while True:
                self._input_round(self.stagger)
                if not self.stagger:
                    self.show_merges()
                self._make_selections()
                self._make_merges()
                print self.field
        except Exception as e:
            print e
            print 'Bye.'

    def _input_round(self, stagger):
        for i in xrange(self.NUM_PLAYERS):
            self.player_rolls.append(raw_input('P%i Rolls: ' %(i+1)).upper().split(' '))
            if self.stagger:
                self.show_merges(i)

    def _make_selections(self):
        for i in xrange(self.NUM_PLAYERS):
            options = self.player_rolls[i] + self.player_one_shots[i]
            print options
            s = raw_input('P%i: Select Gem or Merge\n%s' %(i + 1, ''.join(['[%i] %s\n' %(j+1, self.get_gem_name(gem)) for j, gem in enumerate(options)])))
            try:
                self.field.append(options[int(s)-1])
            except Exception as e:
                print e
                self.field.append(options[0])
            self.player_one_shots[i] = []

    def _make_merges(self):
        for gem in self.pending_merge_list:
            reqs = self.G[gem]
            if set(reqs).issubset(self.field):
                r = raw_input('Merge %s? You will consume %s. [y/n]' %(gem, ', '.join([self.get_gem_name(req) for req in reqs])))
                if r.lower() == 'y':
                    for req in reqs:
                        self.field.remove(req)
                    self.field.append(gem)
        self.pending_merge_list = []
        self.player_rolls = []

    def get_gem_name(self, alias):
        try:
          g, q = alias
        except ValueError:
          return alias
        return '%s %s' %(self.names[q], self.names[g])

    def show_merges(self, player=None):
        WIDTH = 40
        header_text = 'Available Merges'
        header = '%s%s%s' %(' '*((WIDTH-len(header_text))/2), header_text, ' '*((WIDTH-len(header_text))/2))
        print header
        print '+%s+' %('-'*(WIDTH-2))
        l = WIDTH-7
        for gem, reqs in self.G.items():
            if gem in self.BASE_GEMS:
                continue
            rolls = [list(e) for e in itertools.product(*self.player_rolls)]
            p = False
            n = []
            one_shots = 0
            for r in rolls:
                field = self.field + r
                _p = reqs.issubset(field)
                p |= _p
                if _p:
                    n += min([field.count(req) for req in reqs]),
            for i, player_roll in enumerate(self.player_rolls):
                if reqs.issubset(player_roll):
                    if i < player:
                      continue
                    p = True
                    self.player_one_shots[i].append(gem)
                    one_shots = len(flatten(self.player_one_shots))
            if p:
                self.pending_merge_list.append(gem)
                print '%s %s%s(%i) %s' %('|', gem, ' '*(l-len(gem)), max([one_shots, min(n or [0])]), '|')
                print '+%s+' %('-'*(WIDTH-2))


field = ['B1', 'D1', 'Y1', 'B1', 'D1', 'Y1', 'G4', 'R3', 'P2']
pending = ['R5', 'D5', 'Y3', 'D3', 'B4']
F = Field(3, True)
