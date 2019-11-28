def _try_parse(val: str) -> int:
    try:
        return int(val)
    except ValueError:
        return None

class Action:
    def __init__(self, operator: str, value: int):
        self.operator = operator
        self.value = value

    @staticmethod
    def deserialize(message: str) -> "Action":
        op = message[0]
        val = _try_parse(message[1:])
        if op in ['+', '-', '='] and val is not None:
            return Action(op, val)
        return None

    def serialize(self) -> str:
        return f"{self.operator[0]}{self.value}"

    def __repr__(self) -> str:
        return f"<Action: op='{self.operator}', val='{self.value}'>"
