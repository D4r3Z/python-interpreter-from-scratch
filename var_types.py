from copy import deepcopy
from ctypes import py_object
class Var_Type:
    def __init__(self,value) -> None:
        self.value=value
    def __del__(self):
        del self.value
    def notted(self):
        return Bool(1 if self.value==None else 0)
    def change_to(self,other):
        if isinstance(other,self.__class__):
            self.value=deepcopy(other.value)
            return self.__class__(self.value)
        raise Exception('ERROR ERROR')
    def ored_by(self,right):
        return Bool(int(self.value!=None or right.value!=None))
    def anded_by(self,right):
        return Bool(int(self.value!=None and right.value!=None))
    def get_comparison_eq(self, other):
        if isinstance(other, self.__class__):
            return Bool(int(self.value == other.value))
        raise Exception('ERROR ERROR')
    def get_comparison_ne(self, other):
        if isinstance(other, self.__class__):
            return Bool(int(self.value != other.value))
        raise Exception('ERROR ERROR')
    def get_comparison_lt(self, other):
        if isinstance(other, self.__class__):
            return Bool(int(self.value < other.value))
        raise Exception('ERROR ERROR')
    def get_comparison_gt(self, other):
        if isinstance(other, self.__class__):
            return Bool(int(self.value > other.value))
        raise Exception('ERROR ERROR')
    def get_comparison_lte(self, other):
        if isinstance(other, self.__class__):
            return Bool(int(self.value <= other.value))
        raise Exception('ERROR ERROR')
    def get_comparison_gte(self, other):
        if isinstance(other, self.__class__):
            return Bool(int(self.value >= other.value))
        raise Exception('ERROR ERROR')
    def added_to(self,other):
        if isinstance(other,self.__class__):
            return self.__class__(self.value+other.value)
        raise Exception('ERROR ERROR')
class Bool(Var_Type):
    def added_to(self,other):
        if isinstance(other,Bool):
            return Bool(self.value or other.value)
    def multiplied_by(self,other):
        if isinstance(other, Bool):
            return Bool(self.value and other.value)
    def is_true(self):
        return True if self.value!=0 else False
    def __repr__(self):
        return 'TRUE' if self.value else 'FALSE'

class Number(Var_Type):
    def substracted_by(self,other):
        if isinstance(other, Number):
            return self.__class__(self.value-other.value)
    def multiplied_by(self,other):
        if isinstance(other, Number):
            return self.__class__(self.value*other.value)
    def divided_by(self,other):
        if isinstance(other, Number):
            return self.__class__(self.value/other.value)
    def moded_by(self,other):
        if isinstance(other, Number):
            return self.__class__(self.value%other.value)
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Bool(int(self.value == other.value))
    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Bool(int(self.value != other.value))
    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Bool(int(self.value < other.value))
    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Bool(int(self.value > other.value))
    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Bool(int(self.value <= other.value))
    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Bool(int(self.value >= other.value))
    def added_to(self,other):
        if isinstance(other,Number):
            return self.__class__(self.value+other.value)
    def is_true(self):
        return True if self.value!=0 else False
    def __repr__(self):
        return str(self.value)
class Int(Number):
    def __init__(self, value) -> None:
        super().__init__(value)
class Float(Number):
    def __init__(self, value) -> None:
        super().__init__(value)
class String(Var_Type):
    def multiplied_by(self,other):
        if isinstance(other,Int):
            return String(self.value*other.value)
        else:
            raise Exception('Invalid operation')
    def __repr__(self):
        return f'"{self.value}"'
class Array():
    def __init__(self,elements,nodes_type):
        self.lenght=0
        self.capacity=1
        self.A=self.make_array(self.capacity)
    def get_len(self):
        return self.lenght
    def get_element(self,index):
        if not 0 <= index <self.n:
            raise IndexError('K is out of bounds!')
        return self.A[index]
    def added_to(self,other):
        other_type=other.__class__.__name__
        if self.type:
            if other_type==self.type:
                if self.n == self.capacity:
                    self._resize(2*self.capacity)
                self.elements.append(other)
        else:
            if self.n == self.capacity:
                self._resize(2*self.capacity)
            self.elements.append(other)
            self.type=other_type
        return self
    def substracted_by(self,other):
        if isinstance(other, Number):
            try:
                self.elements.pop(other.value)
            except IndexError:
                raise Exception('Index Error')
            if len(self.elements)==0:
                self.type=None
        return self.__class__(self.elements,self.type)
    def _resize(self,new_cap):
        B = self.make_array(new_cap)
        for k in range(self.n):
            B[k] = self.A[k]
             
        self.A = B
        self.capacity = new_cap
    def make_array(self,new_cap):
        return (new_cap * py_object)()
class List():
    def __init__(self,elements):
        self.elements=elements
    def added_to(self, other):
        if isinstance(other,self.__class__):
            self.elements=self.elements+other.elements
        return None
    def change_to(self,other):
        if isinstance(other,self.__class__):
            self.elements=deepcopy(other.elements)
            return self.__class__(self.elements)
    def append(self,value):
        self.elements.append(value)
        return None
    def pop(self,index):
        if 0<=index.value<len(self.elements):
            self.elements.pop(index.value)
            return None
        print('Index error: index is out of bounds')
        return None
    def get_element(self,index):
        if isinstance(index, Int):
            try:
                return self.elements[index.value]
            except IndexError:
                return None
    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'
