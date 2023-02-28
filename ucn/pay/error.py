"""Pay error"""


class TranferVerifyError(Exception):
    """Verify tranfer data error"""

    def __init__(self, tranfer):
        super().__init__(tranfer)
        self.transfer = tranfer


class CoinDataVerifyError(Exception):
    """Verify coin and bill data"""

    def __init__(self, coin_list):
        super().__init__(coin_list)
        self.coin_list = coin_list


class CoinBillRootError(Exception):
    """Verify coins from the same bill root error"""

    def __init__(self, coin_list):
        super().__init__(coin_list)
        self.coin_list = coin_list
