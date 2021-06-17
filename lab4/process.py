import random


class Process:
    pages: int
    assigned_pages: int
    priority: int

    def __init__(self, pages, priority):
        self.priority = priority
        self.pages = pages

    def __lt__(self, other):
        return other.priority < self.priority  # This is a little of a hack

    def __repr__(self):
        return f"Proc(frames: {self.pages}, priority: {self.priority})"

    @property
    def is_faulted(self):
        return self.pages > self.assigned_pages

    @property
    def overflow_amount(self):
        assert self.is_faulted
        return self.pages - self.assigned_pages

    @staticmethod
    def gen_data(amount: int, max_page: int):
        res = []
        for i in range(amount):
            res.append(Process(random.randint(1, max_page), random.randint(1, amount)))
        return res
