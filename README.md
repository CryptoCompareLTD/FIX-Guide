# FIX Connectivity

## Document history

<table>
	<thead> 
		<tr>
			<th>Version</th>
			<th>Date</th>
			<th>Comments</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>1</td>
			<td>25/11/2019</td>
			<td>First public version</td>
		</tr>
	</tbody>
</table>

## Introduction
CryptoCompare offers industry standard FIX connectivity based on an unmodified [FIX 4.4](https://www.fixtrading.org/standards/fix-4-4/) for market data access. Low latency live streaming trade and orderbook data is available for a number of exchanges. 

To gain access to CryptoCompare FIX connectivity, please contact us [by email.](mailto:data@cryptocompare.com)

Once access has been granted, connectivity can be established by connecting to fix.cryptocompare.com.

This document serves as a developer guide for integrating with the FIX streaming service.

## Market representations

Unlike traditional FIX venues which only provide data from one source, CryptoCompare offers market data from many different exchange venues. As such, when requesting market data subscriptions, the source venue should be supplied as part of the market identifier. A market identifier (refered to hereafter as Symbol) is comprised of an exchange or venue name with the instrument from and to parts.

Symbol format with both an Exchange and Market:
> ExchangeName\~FromSymbol\~ToSymbol

A Symbol may also contain an exchange name without a market.

> ExchangeName

## Message Flow

FIX connectivity relies on an unmodified FIX 4.4 dictionary, an API key for authentication and IP whitelisting.

The idealised message flow on connection is as follows.

| Client | Message | Direction | Server |
|---|---|---|---|
|| Logon | -> ||
|| Logon (Response) | <- ||
|| SecurityListRequest | -> ||
|| SecurityList | <- ||
|| MarketDataRequest | -> ||
|| MarketData | <- ||

On establishing a TCP connection, the connecting FIX client is expected to send a [Logon](https://www.onixs.biz/fix-dictionary/4.4/msgtype_a_65.html) message as the first message. It is expected that the [password field](https://www.onixs.biz/fix-dictionary/4.4/tagnum_554.html) of the Logon message will contain the API key.

The server will respond with a Logon should the connection be established successfully or a [LogOut](https://www.onixs.biz/fix-dictionary/4.4/msgType_5_5.html) otherwise.

Once the connection is established, to establish what Symbols are available, the client is **expected** to send a [SecurityListRequest](https://www.onixs.biz/fix-dictionary/4.4/msgtype_x_120.html) message. 

The server will respond with a [SecurityList](https://www.onixs.biz/fix-dictionary/4.4/msgType_y_121.html) message with status information in the [SecurityRequestResult](https://www.onixs.biz/fix-dictionary/4.4/tagNum_560.html) field.

SecurityList messages have 3 types:
* VALID_REQUEST (0) - The request was successful and the instrument list is attached to this message.
* INSTRUMENT_DATA_TEMPORARILY_UNAVAILABLE (4) - Backend components are currently initialising. The client should wait 2 seconds then re-send the request.
* NOT_AUTHORIZED_TO_RETRIEVE_INSTRUMENT_DATA (3) - The API key for the request was invalid. The client will need to logoff then logon with a valid API Key.

**Please note**, only a single concurrent connection is supported per API key.

Based on the Symbols returned in the SecurityList it is possible to subscribe using a [Market Data Request](https://www.onixs.biz/fix-dictionary/4.4/msgtype_v_86.html) message with Symbols formatted as per Market representations defined above.

Once a subscription has been established to a valid market, the client will receive regular [MarketD Data](https://www.onixs.biz/fix-dictionary/4.4/msgtype_w_87.html) messages.