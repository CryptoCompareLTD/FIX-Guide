
# FIX API

## Message Flow

| Client | Message | Direction | Server |
|---|---|---|---|
|| Logon | -> ||
|| LogonResponse | <- ||
|| SecurityListRequest | -> ||
|| SecurityList | <- ||
|| MarketDataRequest | -> ||
|| MarketData | <- ||

SecurityList messages have 3 types:
* VALID_REQUEST - The request was successful and the instrument list is attached to this message.
* INSTRUMENT_DATA_TEMPORARILY_UNAVAILABLE - Backend components are currently initialising. The client should wait 2 seconds then re-send the request.
* NOT_AUTHORIZED_TO_RETRIEVE_INSTRUMENT_DATA - The API key for the request was invalid. The client will need to logoff then logon with a valid API Key.

SecurityList 'Symbol' field format:
> Exchange\~FromSymbol\~ToSymbol

For requesting all instruments from an exchange, simply ommit the From and To symbol fields:
> Exchange

We support two types of market data:
* Orderbook
* Trade
