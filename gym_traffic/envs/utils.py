"""
    utils.py is for miscelanious utility functions.
"""

def in_bet(x1,y1,x2,y2,px,py):
    x_truth = False
    y_truth = False
    if (x1 < px and x2 > px) or (x1 > px and x2 < px):
        x_truth = True
    if (y1 < py and y2 > py) or (y1 > py and y2 < py):
        y_truth = True
    if x_truth and y_truth:
        return True
    else:
        return False

def dist(self, pos1, pos2):
    a = pos1["x"]-pos2["x"]
    b = pos1["y"]-pos2["y"]
    crnt_dist  = (((a)**2)+((b)**2))**0.5
    return crnt_dist
