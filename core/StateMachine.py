"""
name: StateMachine.py
author: usingnamespacestc@gmail.com
version: 1.0
create: forgotten
description:
    A state machine for checking the existence of a pattern.
    也就比字符串找子串方法快一丢丢。为了省一个join操作写了这么多代码实现了个状态机真是亏了。
"""


class StateMachine:
    class State:
        def __init__(self, condition=None):
            self.condition = condition
            self.next = None

    def __init__(self, pattern: [int]):
        self.length = len(pattern)
        self.states = []
        for condition in pattern:
            self.states.append(self.State(condition=condition))
        self.first = self.states[0]
        self.final = self.State()
        self.states.append(self.final)
        for i in range(0, self.length):
            self.states[i].next = self.states[i + 1]
        self.currentState = self.first

    def reset(self):
        self.currentState = self.first

    def feed(self, condition):
        if self.currentState.condition == condition:
            # print("next")
            self.currentState = self.currentState.next
        else:
            # print("back")
            self.reset()

    def isFinal(self):
        if self.currentState is self.final:
            self.reset()
            return True
        return False

    def perfectMatch(self, pattern):
        for condition in pattern:
            self.feed(condition)
            if self.isFinal():
                return True
        return False

    def match(self, pattern):
        res1 = self.perfectMatch(pattern)
        pattern.reverse()
        res2 = self.perfectMatch(pattern)
        return res1 or res2


if __name__ == '__main__':
    # Use case:
    testMachine = StateMachine(pattern=[0, 1, 0, 0])
    result = testMachine.perfectMatch(pattern=[1, 0, 0, 1, 0, 1])
    print(result)
    result = testMachine.match(pattern=[1, 0, 0, 1, 0, 1])
    print(result)