"""Pay function"""


def transfer(
    coins: list[tuple[str, int]], dest: list[tuple[str, int]]
) -> dict[str, list[tuple[int, str]]]:
    """Ledger change status"""
    coins_map = {}
    for account, num in dest:
        while num > 0:
            coin_bill_list = []
            coin, denomination = coins.pop(0)
            if num <= denomination:
                coin_bill_list.append((num, account))
            else:
                coin_bill_list.append((denomination, account))
            num -= denomination
            denomination -= num
            if denomination > 0:
                coins.insert(0, (coin, denomination))
            if coin in coins_map:
                coins_map[coin] = coins_map[coin] + coin_bill_list
            else:
                coins_map[coin] = coin_bill_list
    return coins_map
