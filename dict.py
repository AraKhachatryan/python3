#!/usr/bin/python3

class My_list:

    def __init__(self, length = 1):
        self.ml = [ [None for value in range(2)] for key in range(length) ]

    def __str__(self):
        return str(self.ml)

    def __add__(self, other):
        tmp = My_list(len(self.ml) + len(other.ml))
        tmp.ml = self.ml + other.ml
        return tmp

    def __setitem__(self, key, value):
        for index, pair in enumerate(self.ml):
            if pair[0] == key:
                self.ml[index][1] = value
                break
            elif pair[0] == None:
                self.ml[index] = [key, value]
                break
            else:
                self.ml += [[key, value]]
                break

    def __getitem__(self, key):
        for index, pair in enumerate(self.ml):
            if pair[0] == key:
                return self.ml[index][1]

    def reverse(self):
        self.ml = self.ml[::-1]



first = My_list()
first["ab"] = "bbbbbb"
first["cd"] = "dddddd"
first["ab"] = "cccccc"
first["xy"] = "xyyyyy"
print(first)
print('the value of "xy"', first["xy"])

second = My_list()
second[3] = 5
second[4] = 45
tmp = first + second
print(tmp)
