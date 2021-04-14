import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


class Stats:
    def __init__(self):
        self.pos = {}

    def tick_position(self, pos: int):
        curr = self.pos.get(pos, None)
        if curr is None:
            self.pos[pos] = 1
        else:
            self.pos[pos] = curr + 1

    def show(self):
        plt.bar(list(self.pos.keys()), list(self.pos.values()))
        plt.show()

