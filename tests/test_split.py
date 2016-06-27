"""
Testing module for the class CHAIDSplit
"""

from setup_tests import CHAID

def test_column_name_mappings():
    """ Test column name mappings are applied correctly """
    column_names = ["a", "b", "c"]
    splits = [CHAID.CHAIDSplit(col, None, None, 1) for col in range(0, len(column_names))]

    for split in splits:
        assert split.column == str(split.column_id), 'Names should be column id when mapping not applied'
        split.name_columns(column_names)
        assert split.column == column_names[split.column_id], 'Names should correctly map to column name when mapping is applied'
