import asyncio

from client.cryptorank import CryptorankClient


async def buy_coins(
        client: CryptorankClient,
        portfolio_id: int,
        buy_amount: int | float,
        buy_quote: str,
        fee_quote: str,
        min_mcap: int | float,
) -> None:
    coins = await client.coins()
    coins_list: list[dict] = coins.response.get("data")

    client.logging.info(f"Found {len(coins_list)} coins!")

    for coin in coins_list:
        coin_name = coin.get("name")
        coin_symbol = coin.get("symbol")
        coin_key = coin.get("key")
        coin_mcap = coin.get("marketCap", 0)
        coin_price = coin.get("price").get("USD")

        client.logging.info(f"{coin_symbol} ({coin_name}) coin")

        if not coin.get("isTraded"):
            client.logging.warning(f"{coin_name} is not traded, skip..")
            continue

        if min_mcap > coin_mcap:
            client.logging.warning(f"{coin_name} has less mcap than min, skip..")
            continue

        client.logging.info(f"{coin_name} is okey, buying..")
        transaction = await client.transaction(
            portfolio_id=portfolio_id,
            type="BUY",
            base_currency_key=coin_key,
            base_quantity=(buy_amount / coin_price),
            quote_currency_key=buy_quote,
            quote_quantity=buy_amount,
            usd_value=buy_amount,
            fee_value=0,
            fee_type="USD",
        )

        if transaction.status_code != 201:
            client.logging.error(f"{coin_name} buy error {transaction.error}")
            continue

        client.logging.success(f"{coin_name} buyed, next coin..")


async def main() -> None:
    authorization = "Bearer xxx"
    client = CryptorankClient(authorization)

    await buy_coins(
        client,
        portfolio_id=52921,
        buy_amount=10,
        buy_quote="united-states-dollar",
        fee_quote="USD",
        min_mcap=100_000,
    )




if __name__ == "__main__":
    asyncio.run(main())