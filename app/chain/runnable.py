from typing import TypeVar, Generic

Input = TypeVar("Input")
Output = TypeVar("Output")

class Runnable(Generic[Input, Output]):
    

    def invoke(self, input: Input) -> Output:
        raise NotImplementedError
    
    def __or__(self, other):
        return RunnableSequence(self, other)
    

class RunnableSequence(Runnable):

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def invoke(self, input):
        first_result = self.first.invoke(input)
        return self.second.invoke(first_result)