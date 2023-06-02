class Token:
    def __init__(self,type_,value_=None) -> None:
        self.type=type_
        self.value=value_
    def __repr__(self) -> str:
        return f'[type:{self.type}, value:{self.value}]' if self.value else f'[type:{self.type}]'