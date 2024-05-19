import timeit
from tabulate import tabulate


def find_coins_greedy(amount, coins):
    result = {}
    for coin in sorted(coins, reverse=True):
        if amount >= coin:
            count = amount // coin
            amount -= coin * count
            result[coin] = count
            if amount == 0:
                break
    return result


def find_min_coins(amount, coins):
    if amount == 0 or min(coins) > amount:
        return {}

    DP = [float("inf")] * (amount + 1)
    DP[0] = 0

    coin_used = [-1] * (amount + 1)

    for coin in coins:
        for i in range(coin, amount + 1):
            if DP[i - coin] + 1 < DP[i]:
                DP[i] = DP[i - coin] + 1
                coin_used[i] = coin

    result = {}
    remaining_amount = amount

    while remaining_amount > 0:
        coin = coin_used[remaining_amount]
        result[coin] = result.get(coin, 0) + 1
        remaining_amount -= coin

    return result


def print_results(fn_map, coin_values, num_iterations):
    data = []

    for name, fn in fn_map.items():
        row = [name]

        for coin in coin_values:
            row.append(timeit.timeit(lambda: fn(coin, coins), number=num_iterations))
        data.append(row)

    print(
        tabulate(
            data,
            headers=["Function", *coin_values],
            tablefmt="pipe",
            floatfmt=".5f"
        )
    )


if __name__ == "__main__":
    coins = [50, 25, 10, 5, 2, 1]

    fn_map = {
        "Функція жадібного алгоритму": find_coins_greedy,
        "Функція динамічного програмування": find_min_coins,
    }

    coin_values = [100, 500, 1000]
    num_iterations = 30

    print_results(fn_map, coin_values, num_iterations)
