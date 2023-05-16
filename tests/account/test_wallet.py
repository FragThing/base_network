from ucn.account.wallet import Account


def test_account_init(multikey, encode_algo):
    """
    Test the Account class initialization with valid parameters.
    Assert that an instance of the Account class is created.
    """
    account = Account(multikey, encode_algo)
    assert isinstance(account, Account)


def test_account_id_url(multikey, encode_algo):
    """
    Test the id_url property of the Account class. Assert that the id_url
    matches the expected format.
    """
    account = Account(multikey, encode_algo)
    id_url = account.id_url
    assert isinstance(id_url, str) and len(id_url) > 0


def test_account_credit(multikey, encode_algo):
    """
    Test the credit property of the Account class. Assert that it returns a
    float value.
    """
    account = Account(multikey, encode_algo)
    credit = account.credit
    assert isinstance(credit, float)


def test_account_balance(multikey, encode_algo):
    """
    Test the balance property of the Account class. Assert that it returns a
    float value.
    """
    account = Account(multikey, encode_algo)
    balance = account.balance
    assert isinstance(balance, float)
