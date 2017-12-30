# Modules paths
# Packages
import pickle
from collections import namedtuple

import numpy as np

from xmas_happiness_engine.data_input.O.outloc import OUTLOC

Memory = namedtuple('Memory', 'date messages')

# Loading memories
memories = pickle.load(open((OUTLOC+'/memories.pd'), 'rb'))

attempt = []
for memory in memories:

    attempt.append(len(memory.messages))
    print(memory.messages[0]['author'],memory.messages[0]['message'])

print(np.mean(attempt))
print(sorted(attempt, reverse=True))
