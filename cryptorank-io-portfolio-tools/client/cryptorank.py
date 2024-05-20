from client.core.client import ApiClient, ApiResponse, ApiError
from utils.time import timestamp


class CryptorankClient(ApiClient):
    def __init__(self, authorization: str | None = None) -> None:
        self.authorization = authorization

        self.cryptorank_base_url = "https://api.cryptorank.io"
        self.cryptorank_allowed_methods = ["GET" ,"POST", "DELETE", "PATCH"]
        self.cryptorank_rate_limits = 1000
        self.cryptorank_header = {"Authorization": self.authorization}
        self.cryptorank_error_codes = None
        self.cryptorank_error_schema = None

        super().__init__(
            base_url=self.cryptorank_base_url,
            custom_header=self.cryptorank_header,
            allowed_methods=self.cryptorank_allowed_methods,
            rate_limits=self.cryptorank_rate_limits,
            enable_logging=True,
            save_logs=True,
            custom_error_status_codes=None,
            custom_error_schema=None,
            proxy=None,
        )


    async def coins(
            self,
            locale: str = "en",
            life_cycle: str = "traded",
    ) -> ApiResponse | ApiError:
        method = "GET"
        endpoint = "/v0/coins/"
        params = {"locale": locale, "lifeCycle": life_cycle}

        response = await self.request(method, endpoint, params)

        return response


    async def transaction(
            self,
            portfolio_id: int,
            type: str,
            base_currency_key: str,
            base_quantity: int | float,
            quote_currency_key: str,
            quote_quantity: int | float,
            usd_value: int | float,
            fee_value: int | float,
            fee_type: str, 
            alter_holdings: bool = False,
            date: int = timestamp(),
    ) -> ApiResponse | ApiError:
        method = "POST"
        endpoint = "/v0/manual-portfolio/transactions"
        json = {
            "alterHoldings": alter_holdings,
            "date": date,
            "quoteCurrencyKey": quote_currency_key,
            "feeType": fee_type,
            "baseCurrencyKey": base_currency_key,
            "portfolioId": portfolio_id,
            "type": type,
            "baseQuantity": base_quantity,
            "quoteQuantity": quote_quantity,
            "feeValue": fee_value,
            "usdValue": usd_value,
        }

        response = await self.request(method, endpoint, json=json)

        return response
