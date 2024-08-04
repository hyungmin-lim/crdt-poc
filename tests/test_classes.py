from poc import OpId


def test_OpId():
    op_id_1 = OpId(counter=1, nodeId="node1")
    op_id_2 = OpId(counter=1, nodeId="node2")
    op_id_3 = OpId(counter=2, nodeId="node1")
    op_id_4 = OpId(counter=2, nodeId="node2")

    assert op_id_1 < op_id_2, "OpId 1 should be less than OpId 2"
    assert op_id_1 < op_id_3, "OpId 1 should be less than OpId 3"
    assert op_id_1 < op_id_4, "OpId 1 should be less than OpId 4"
    assert op_id_2 < op_id_3, "OpId 2 should be less than OpId 3"
