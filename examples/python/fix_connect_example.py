import time
import quickfix
import quickfix44

__SOH__ = chr(1)

def messageToString(message):
    return message.toString().replace(__SOH__, "|")

def securityListRequest(sessionID):
    # https://www.onixs.biz/fix-dictionary/4.4/msgtype_x_120.html
    message = quickfix44.SecurityListRequest()
    message.setField(quickfix.SecurityReqID("TEST"))
    message.setField(quickfix.SecurityListRequestType(4))  # All securities
    return message

def marketDataRequest(sessionID):
    # https://www.onixs.biz/fix-dictionary/4.4/msgtype_v_86.html
    message = quickfix44.MarketDataRequest()
    header = message.getHeader()
    target = sessionID.getTargetCompID().getString()
    fix_version = "FIX.4.4"

    header.setField(quickfix.BeginString(fix_version))
    header.setField(quickfix.SenderCompID(target))
    header.setField(quickfix.TargetCompID("CRYPTOCOMPARE"))
    header.setField(quickfix.MsgType("V"))  # V for market data request

    message.setField(quickfix.MDReqID("TEST"))
    message.setField(quickfix.SubscriptionRequestType("0"))  # snapshots
    message.setField(quickfix.MarketDepth(1))  # Top of book
    # http://www.quickfixengine.org/quickfix/doc/html/repeating_groups.html
    group_md = quickfix44.MarketDataRequest().NoMDEntryTypes()
    group_md.setField(quickfix.MDEntryType("0"))  # Top of book
    message.addGroup(group_md)

    group_sym = quickfix44.MarketDataRequest().NoRelatedSym()
    group_sym.setField(quickfix.Symbol("coinbase~btc~usd"))
    message.addGroup(group_sym)
    return message


class Application(quickfix.Application):
    # http://www.quickfixengine.org/quickfix/doc/html/application.html
    def onCreate(self, sessionID):
        print("onCreate:")
        self.session_id = sessionID
        target = sessionID.getTargetCompID().getString()
        sender = sessionID.getSenderCompID().getString()
        print(f"target: {target}")
        print(f"sender: {sender[:5]}...{sender[-5:]}")
        return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        print("onLogon:", f"Session ID: {self.sessionID}")

        security_list_msg = securityListRequest(sessionID)
        print("security list message:", messageToString(security_list_msg))
        message = marketDataRequest(sessionID)
        print("market data requests:", messageToString(message))

        quickfix.Session.sendToTarget(security_list_msg, sessionID)
        quickfix.Session.sendToTarget(message, sessionID)
        return

    def onLogout(self, sessionID):
        print("onLogout..")
        return

    def toAdmin(self, message, sessionID):
        print("toAdmin:", messageToString(message), '\n')
        return

    def toApp(self, message, sessionID):
        print("toApp:", messageToString(message), '\n')
        return

    def fromAdmin(self, message, sessionID):
        print("fromAdmin:", messageToString(message), '\n')
        return

    def fromApp(self, message, sessionID):
        msg = messageToString(message)
        msg_type = message.getHeader().getField(quickfix.MsgType())
        if msg_type.getString() == 'y':  # https://www.onixs.biz/fix-dictionary/4.4/msgtype_y_121.html
            if "coinbase~btc~usd" in msg.lower():
                print("fromApp: Requested security data available", '\n')
                return
        print("fromApp:", msg, '\n')
        return

    def keepAlive(self):
        while True:
            time.sleep(60)


if __name__ == "__main__":
    settings = quickfix.SessionSettings("CCFIX.ini")
    app = Application()
    storeFactory = quickfix.FileStoreFactory(settings)
    logFactory = quickfix.FileLogFactory(settings)
    initiator = quickfix.SocketInitiator(app,
                                         storeFactory,
                                         settings,
                                         logFactory)
    initiator.start()
    app.keepAlive()
