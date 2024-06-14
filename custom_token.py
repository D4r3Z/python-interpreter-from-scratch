class Token:
    def __init__(self, _type: str, _value: str | None = None) -> None:
        self.type = _type
        self.value = _value

    def __repr__(self) -> str:
        return f"[type:{self.type}, value:{self.value}]" if self.value else f"[type:{self.type}]"
