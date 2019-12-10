"""
---
name: stepper.py
description: Stepper motor package
copyright: 2019-2019 Marcio Pessoa
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
change-log:
  2019-03-09:
  - version: 0.02
    Added: start() and stop() methods.
  2019-03-09:
  - version: 0.01
    Added: Starting a new package.
"""

import math
import pyb  # pylint: disable=import-error


class Stepper():  # pylint: disable=too-many-instance-attributes
    """
    Stepper
    """

    def __init__(self, steps, timer):
        self._version = 0.02
        self.__direction = 1
        self.__snapshot = [0, 0, 0, 0]
        self.__steps = steps
        self.__frequency = 1
        self.__counter = 0
        self.__calculate = False
        self.__unit = 0
        self.__stopped = False
        self.__update_unit()
        self.tim = pyb.Timer(timer)
        self.tim.counter(0)
        self.tim.callback(lambda t: self.__update())
        self.frequency(1000)
        self.forward()

    def stop(self):
        """
        description:
        """
        self.__stopped = True

    def start(self):
        """
        description:
        """
        self.__stopped = False

    def forward(self):
        """
        description: Set step motor moves to forward.
        """
        self.__direction = 1
        self.__update_unit()
        self.start()

    def backward(self):
        """
        description: Set step motor moves to backward.
        """
        self.__direction = -1
        self.__update_unit()
        self.start()

    def position(self):
        """
        description:
        """
        if self.__stopped:
            return self.__snapshot
        if self.__calculate:
            self.__calculate = False
            self.__counter += self.__unit
            if self.__counter >= (2 * math.pi) and self.__direction == 1:
                self.__counter = 0
            if self.__counter <= 0 and self.__direction == -1:
                self.__counter = 2 * math.pi
        if math.sin(self.__counter) <= 0:
            self.__snapshot[0] = math.fabs(math.sin(self.__counter))
            self.__snapshot[1] = 0
        elif math.sin(self.__counter) > 0:
            self.__snapshot[0] = 0
            self.__snapshot[1] = math.sin(self.__counter)
        if math.cos(self.__counter) <= 0:
            self.__snapshot[2] = math.fabs(math.cos(self.__counter))
            self.__snapshot[3] = 0
        elif math.cos(self.__counter) > 0:
            self.__snapshot[2] = 0
            self.__snapshot[3] = math.cos(self.__counter)
        return self.__snapshot

    def __update(self):
        self.__calculate = True

    def __update_unit(self):
        self.__unit = 2 * math.pi / self.__steps * self.__direction

    def frequency(self, frequency=None):
        """
        description:
        """
        if frequency is None:
            return self.__frequency
        self.__frequency = frequency
        self.tim.init(freq=self.__frequency)
        return False

    def info(self):
        """
        description:
        """
        print(
            "Counter: " + str(self.__counter) +
            ", Position: " + str(self.__snapshot))
