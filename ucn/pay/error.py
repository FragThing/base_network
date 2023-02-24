"""Pay error"""


class TranferVerifyError(Exception):
    """Verify tranfer data error"""

    def __init__(self, tranfer):
        super().__init__(tranfer)
        self.transfer = tranfer
