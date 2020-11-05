from enum import Enum, unique

@unique
class InvalidSplitReason(Enum):
    """
    Private class to store possible invalid reasons
    """
    ALPHA_MERGE =          'p-value greater than alpha merge'
    MIN_CHILD_NODE_SIZE =  'splitting would create nodes with less than the minimum child ' \
                           'node size'
    MAX_DEPTH =            'the max depth has been reached'
    MIN_PARENT_NODE_SIZE = 'the minimum parent node size threshold has been reached'
    PURE_NODE =            'the node only contains single category respondents'
    NODE_NOT_EXHAUSTIVE =  'the node is not exhaustive'

    def __str__(self):
        """
        Returns the string representation of the string.

        Args:
            self: (todo): write your description
        """
        return self.value
