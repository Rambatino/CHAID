"""
Testing module for the class Split
"""

from setup_tests import CHAID


def test_column_name_mappings():
    """ Test column name mappings are applied correctly """
    column_names = ["a", "b", "c"]
    cols = range(0, len(column_names))
    splits = [CHAID.Split(col, None, None, 1, 0) for col in cols]

    for split in splits:
        assert split.column == str(split.column_id), 'Names should be column id when mapping not applied'
        split.name_columns(column_names)
        assert split.column == column_names[split.column_id], 'Names should correctly map to column name when mapping is applied'

