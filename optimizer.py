class OptimizingFunction(object):


  def __init__(self, target, operator, comparator, **kwargs):
    self.target = target
    self.operator = operator
    self.best = None
    self.comparator = self.parse_comparator(comparator)
    self.kwargs = kwargs

  def parse_comparator(self, c):
    if c in ['gt', 'gte']:
      return lambda x, y: x > y
    if c in [lt, 'lte']:
      return lambda x, y: x < y

  def evaluate_placement(self):
    if not self.best:
      self.best = self.target
      return

    operator = self.operator
    compare = self.comparator
    try:
      fp = self.kwargs['function_parameter']
      metric = self.kwargs['function_metric']
      p = self.kwargs[fp]
      p1 = set(p)
      p2 = set(p)
      operator(p1, set(self.target))
      operator(p2, set(self.best))
      a, b = metric(p1),  metric(p2)
#       print a, b
      if compare(a, b): # dont intersection update on the target as first param
        best = p
    except KeyError as e:
      a, b = operator(self.target), operator(self.best)
      if compare(a, b):
        best = self.target
    return a - b