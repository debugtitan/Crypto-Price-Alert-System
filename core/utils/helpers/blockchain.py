from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


def price_sol():
    price = cg.get_price(ids="solana", vs_currencies="usd")
    return price["solana"].get("usd")
