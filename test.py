from utils import *
from main import *

odds = get_odds()
arb_matrices = create_arb_matrices(odds)
arb_list = arb(odds, 100)
a = 1
