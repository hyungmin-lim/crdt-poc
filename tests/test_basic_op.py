from poc import CRDT, OpId, Insert, Delete


def test_CRDT_insertion_only():
    crdt = CRDT()
    # Say I insert "The fox" at the beginning
    op_1 = Insert(
        opId=OpId(counter=1, nodeId="node1"), afterId=OpId.null(), character="f"
    )
    op_2 = Insert(
        opId=OpId(counter=2, nodeId="node1"), afterId=op_1.opId, character="o"
    )
    op_3 = Insert(
        opId=OpId(counter=3, nodeId="node1"), afterId=op_2.opId, character="x"
    )
    op_4 = Insert(
        opId=OpId(counter=4, nodeId="node1"), afterId=OpId.null(), character="T"
    )
    op_5 = Insert(
        opId=OpId(counter=5, nodeId="node1"), afterId=op_4.opId, character="h"
    )
    op_6 = Insert(
        opId=OpId(counter=6, nodeId="node1"), afterId=op_5.opId, character="e"
    )
    op_7 = Insert(
        opId=OpId(counter=7, nodeId="node1"), afterId=op_6.opId, character=" "
    )

    crdt.insert(op_1)
    crdt.insert(op_2)
    crdt.insert(op_3)

    assert crdt.format() == "fox"

    crdt.insert(op_4)
    crdt.insert(op_5)
    crdt.insert(op_6)
    crdt.insert(op_7)

    assert crdt.format() == "The fox"

    return crdt


def test_CRDT_insertion_deletion():
    crdt = test_CRDT_insertion_only()
    op_8 = Delete(
        opId=OpId(counter=8, nodeId="node1"), deleteId=OpId(counter=4, nodeId="node1")
    )
    crdt.delete(op_8)
    assert crdt.format() == "he fox"

    op_9 = Insert(
        opId=OpId(counter=9, nodeId="node2"), afterId=OpId.null(), character="t"
    )
    crdt.insert(op_9)
    assert crdt.format() == "the fox"


def test_CRDT_insertion_deletion_reverse():
    crdt = test_CRDT_insertion_only()
    op_8 = Insert(
        opId=OpId(counter=8, nodeId="node2"), afterId=OpId.null(), character="t"
    )
    op_9 = Delete(
        opId=OpId(counter=9, nodeId="node1"), deleteId=OpId(counter=4, nodeId="node1")
    )
    crdt.insert(op_8)
    crdt.delete(op_9)
    assert crdt.format() == "the fox"
