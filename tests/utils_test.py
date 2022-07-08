import sys

sys.path.append("../snakey")

from hypothesis import assume, given
from hypothesis.strategies import lists, sets, tuples, integers, composite, sampled_from

position_strategy = tuples(integers(min_value=0), integers(min_value=0))
positions_strategy = lists(position_strategy, min_size=1)
