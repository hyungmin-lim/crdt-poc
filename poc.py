# File to PoC the CRDT data structure
# and basic operations such as insert, delete, format.

from typing import Self
from pydantic import BaseModel
import bisect


class Action(BaseModel):
    action_type: str


class OpId(BaseModel):
    counter: int  # counter for operation
    nodeId: str  # UUID for client

    # Define null OpId
    @staticmethod
    def null():
        return OpId(counter=-1, nodeId="null")

    def __eq__(self, other):
        return self.counter == other.counter and self.nodeId == other.nodeId

    def __lt__(self, other):
        if self.counter == other.counter:
            return self.nodeId < other.nodeId
        return self.counter < other.counter

    def __hash__(self):
        return hash((self.counter, self.nodeId))

    def __repr__(self):
        return f"{self.counter}@{self.nodeId}"


class Insert(Action):
    action_type: str = "insert"
    opId: OpId  # id of the action
    afterId: OpId  # id of the character at which this character is inserted
    character: str  # actual character


class Delete(Action):
    action_type: str = "remove"
    opId: OpId  # id of the action
    deleteId: OpId  # id of the character to be removed


class Character(BaseModel):
    char: str  # character
    opId: OpId  # id of the action that inserted this character
    children: list[Self] = []  # list of characters inserted after this character
    tombstone: bool  # flag to indicate if this character is deleted

    class Config:
        arbitrary_types_allowed = True

    def __lt__(self, other):
        return self.opId < other.opId

    def __repr__(self):
        return f"{self.char}" if not self.tombstone else f"({self.char})"


class CRDT:
    def __init__(self):
        self.root_char = Character(char="", opId=OpId.null(), tombstone=False)
        self.opId_to_char: dict[OpId, Character] = {}
        self.opId_to_char[OpId.null()] = self.root_char

    def generate(self) -> list[Character]:
        # Starting from the root character, iterate through the children in reverse order
        # and generate a document, which is a list of characters
        def dfs(node: Character) -> list[Character]:
            if not node.children:
                return [node]
            document = []
            if not node.tombstone:
                document.append(node)
            for child in reversed(node.children):
                document.extend(dfs(child))
            return document

        self.characters = dfs(self.root_char)
        return self.characters

    def insert(self, action: Insert):
        if action.afterId not in self.opId_to_char:
            return
        self.opId_to_char[action.opId] = Character(
            char=action.character, opId=action.opId, tombstone=False
        )
        bisect.insort(
            self.opId_to_char[action.afterId].children, self.opId_to_char[action.opId]
        )

    def delete(self, action: Delete):
        if action.deleteId not in self.opId_to_char:
            print("Delete ID not found")
            return
        self.opId_to_char[action.deleteId].tombstone = True

    def format(self):
        return "".join([char.char for char in self.generate() if not char.tombstone])


if __name__ == "__main__":
    from tests.test_basic_op import test_CRDT_insertion_only

    print(test_CRDT_insertion_only())
