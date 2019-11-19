
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

Security list messages have 3 types:
* VALID_REQUEST - The request was successful and the instrument list is attached to this message.
* INSTRUMENT_DATA_TEMPORARILY_UNAVAILABLE - Backend components are currently initialising. The client should wait 2 seconds then re-send the request.
* NOT_AUTHORIZED_TO_RETRIEVE_INSTRUMENT_DATA - The API key for the request was invalid. The client will need to logoff then logon with a valid API Key.

We support two types of market data:
* Orderbook
* Trade

