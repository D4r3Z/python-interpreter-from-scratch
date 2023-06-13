'''symbol table for storing variables while programm is working'''
class SymbolTable:
    def __init__(self) -> None:
        self.symbols={}
    def __del__(self):
        pass
    def get(self,name):
        value=self.symbols.get(name)
        return value
    def set(self,name,link):
        self.symbols.update({name:link})
    def remove(self,name):
        del self.symbols[name]
