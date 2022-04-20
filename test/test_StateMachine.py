from core.StateMachine import StateMachine


class TestClass:
    def test_state_machine(self):
        testMachine = StateMachine(pattern=[0, 1, 0, 0])
        result = testMachine.perfectMatch(pattern=[1, 0, 0, 1, 0, 1])
        assert result is False
        result = testMachine.match(pattern=[1, 0, 0, 1, 0, 1])
        assert result is True
