# This code is running in the back of the server all the time.
# It looking for open buy or sell orders in the database and checks if they are possible to execute.
# If they do, the orders executed and the information created by the process (money gain/loss or no changes) are saved in the database.

import time, datetime, threading
import xlwings as xw
from TPserver_functions import checking_if_the_market_is_open_func

INDEXES_WORKBOOKS_PATH = r"C:\Users\Almogi\Desktop\indexes_workbooks"
TIME_SPACE = 60.0

# excel columns list :
#    A - stock           B - ticker
#    C - name            D - description
#    E - industry        F - price
#    G - high            H - low
#    I - open            J - close
#    K - market cap      L - change
#    M - beta            N - volume
#    O - P/E             P - employees
#    Q - Exchange

INDEXES_TABLES = {"DowJones30": 'DowJones30',
                  "S&P500": 'SP500',
                  "Nasdaq100": 'Nasdaq100',
                  "Russell1000": 'Russell1000'}


class OrdersRunner(threading.Thread):
    """
    Class that try to execute all the open sell and buy orders every one minute.
    This class has a function for each order type and for updating the data base.
    """
    def __init__(self, cursor):
        """
        Creating a thread so the class can run in parallel with the server.
        """
        self.thread = threading.Thread.__init__(self)
        self.cursor = cursor

    def run(self):
        """
        This function running until the program stop.
        Every minute that passed the while loop start a new iteration.
        """
        stop = False
        while not stop:
            try:
                # if checking_if_the_market_is_open_func():
                if True:
                    print("     ~~~~~~~~~~ order runner is coming back to work ~~~~~~~~~~")
                    for index in INDEXES_TABLES:
                        self.execute_orders(index, INDEXES_TABLES.get(index) + "_orders_table")
                else:
                    time.sleep(TIME_SPACE)
            except Exception as exc:
                if "Attempt to use a closed cursor" in str(exc):
                    stop = True
                else:
                    print("\norder execute error :")
                    print(exc)
                    time.sleep(3)

            finally:
                print("     ~~~~~~~~~ order runner is sleeping for a minute ~~~~~~~~~")
                time.sleep(TIME_SPACE)

    def execute_orders(self, index, orders_table_name):
        """
        Getting the name of open orders table and trying to execute all the open orders in it.
        """
        self.cursor.execute("SELECT order_number, order_type, order_creator_key, order_date,"
                            " ticker, stocks_number, order_info, owned_stock_number FROM " + orders_table_name)
        orders_list = list(self.cursor.fetchall())

        if orders_list:
            path = INDEXES_WORKBOOKS_PATH + "\\" + index + "_stocks_workbook.xlsm"
            # excel_app = xw.App(visible = False)
            wb = xw.Book(path)
            sht = wb.sheets['Sheet1']

            for one_order in orders_list:
                if one_order[1] == "BUY-MARKET":
                    self.buy_market_func(one_order, index, sht)
                elif one_order[1] == "BUY-LIMIT":
                    self.buy_limit_func(one_order, index, sht)
                elif one_order[1] == "BUY-STOPLOSS":
                    self.buy_stop_loss_func(one_order, index, sht)
                elif one_order[1] == "BUY-STOPLIMIT":
                    self.buy_stop_limit_func(one_order, index, sht)
                elif one_order[1] == "BUY-AON":
                    self.buy_aon_func(one_order, index, sht)
                elif one_order[1] == "BUY-IOC":
                    self.buy_ioc_func(one_order, index, sht)
                elif one_order[1] == "BUY-BUYABOVE":
                    self.buy_buy_above_func(one_order, index, sht)
                elif one_order[1] == "BUY-FOK":
                    self.buy_fok_func(one_order, index, sht)
                elif one_order[1] == "SELL-MARKET":
                    self.sell_market_func(one_order, index, sht)
                elif one_order[1] == "SELL-LIMIT":
                    self.sell_limit_func(one_order, index, sht)
                elif one_order[1] == "SELL-STOPLOSS":
                    self.sell_stop_loss_func(one_order, index, sht)
                elif one_order[1] == "SELL-STOPLIMIT":
                    self.sell_stop_limit_func(one_order, index, sht)
                elif one_order[1] == "SELL-AON":
                    self.sell_aon_func(one_order, index, sht)
                elif one_order[1] == "SELL-IOC":
                    self.sell_ioc_func(one_order, index, sht)
                elif one_order[1] == "SELL-TAKEPROFIT":
                    self.sell_take_profit_func(one_order, index, sht)
                elif one_order[1] == "SELL-FOK":
                    self.sell_fok_func(one_order, index, sht)

            wb.save()
            wb.close()
            # excel_app.quit()

    def seacrching_stock_price_in_excel_file(self, sht, ticker):
        """
        Getting stock's ticker and return the current price
        """
        last_row = sht.range(1, 1).end('down').row

        for a in range(2, last_row + 1):
            if ticker == str(sht.range("B" + str(a)).value):
                stock_price = sht.range('F' + str(a)).value
                return stock_price

    def buy_market_func(self, one_order, index, sht):
        """
        Trying to execute buy "market" order, this order is buying the stock at any price
        """
        stock_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
        # stock_for_buy_list = order_creator_key, ticker, index, today date,price, stocks_amount
        stock_for_buy_list = [one_order[2], one_order[4], index, str(datetime.date.today()), stock_price, one_order[5]]

        full_price = stock_for_buy_list[4] * one_order[5]
        self.cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?", one_order[2])
        current_amount = self.cursor.fetchone()[0]

        if current_amount >= full_price:
            self.update_users_table(current_amount - full_price, one_order[2])
            self.update_balance_table(current_amount - full_price, one_order[2])
            self.update_owned_stocks_table(stock_for_buy_list, index)
            self.delete_order(one_order[0], index)

        elif one_order[5] > 1:
            possible_amount = int(current_amount/stock_for_buy_list[4])
            if possible_amount != 0:
                stock_for_buy_list[5] = possible_amount
                full_price = stock_for_buy_list[4] * stock_for_buy_list[5]
                self.update_users_table(current_amount - full_price, one_order[2])
                self.update_balance_table(current_amount - full_price, one_order[2])
                self.update_owned_stocks_table(stock_for_buy_list, index)
                self.update_order_stocks_amount(one_order[0], index, one_order[5] - possible_amount)

    def buy_limit_func(self, one_order, index, sht):
        """
        Trying to execute buy "limit" order,
        this order buying is the stock only if the price is equal or less than the limit
        """
        stock_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
        # stock_for_buy_list = order_creator_key, ticker, index, today date,price, stocks_amount
        stock_for_buy_list = [one_order[2], one_order[4], index, str(datetime.date.today()), stock_price, one_order[5]]
        limit = int(one_order[6])

        if stock_for_buy_list[4] <= limit:
            full_price = stock_for_buy_list[4] * one_order[5]
            self.cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?", one_order[2])
            current_amount = self.cursor.fetchone()[0]

            if current_amount >= full_price:
                self.update_users_table(current_amount - full_price, one_order[2])
                self.update_balance_table(current_amount - full_price, one_order[2])
                self.update_owned_stocks_table(stock_for_buy_list, index)
                self.delete_order(one_order[0], index)

            elif one_order[5] > 1:
                possible_amount = int(current_amount / stock_for_buy_list[4])
                if possible_amount != 0:
                    stock_for_buy_list[5] = possible_amount
                    full_price = stock_for_buy_list[4] * stock_for_buy_list[5]
                    self.update_users_table(current_amount - full_price, one_order[2])
                    self.update_balance_table(current_amount - full_price, one_order[2])
                    self.update_owned_stocks_table(stock_for_buy_list, index)
                    self.update_order_stocks_amount(one_order[0], index, one_order[5] - possible_amount)

    def buy_stop_loss_func(self, one_order, index, sht):
        """
        Trying to execute buy "stop loss" order, this order is buying the stock at his minimum limit
        """
        current_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])

        if current_price <= int(one_order[6]):
            order_type = "BUY-MARKET"
            self.cursor.execute("INSERT INTO " + INDEXES_TABLES.get(index) + "_orders_table "
                                "(order_type,order_creator_key, order_date, ticker, stocks_number, order_info)"
                                " VALUES(?,?,?,?,?,?)", order_type, one_order[2], str(datetime.date.today()),
                                one_order[4], one_order[5], "no necessary")

            self.delete_order(one_order[0], index)

    def buy_stop_limit_func(self, one_order, index, sht):
        """
        Trying to execute buy "stop limit" order,
        this order is creating a limit order if the price is lower than the stop price
        """
        current_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])

        if current_price <= int(((one_order[6]).split("-"))[0]):
            order_type = "BUY-LIMIT"
            self.cursor.execute("INSERT INTO " + INDEXES_TABLES.get(index) + "_orders_table "
                                "(order_type,order_creator_key, order_date, ticker, stocks_number, order_info)"
                                " VALUES(?,?,?,?,?,?)"
                                , order_type, one_order[2], str(datetime.date.today()),
                                one_order[4], one_order[5], ((one_order[6]).split("-"))[1])

            self.delete_order(one_order[0], index)

    def buy_aon_func(self, one_order, index, sht):
        """
        Trying to execute buy "AON" (all-or-none) order,
        this order try to buy all the stocks that the order ask for.
        If the transaction couldn't made it all the order is canceled.
        """
        stock_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
        # stock_for_buy_list = order_creator_key, ticker, index, today date,price, stocks_amount
        stock_for_buy_list = [one_order[2], one_order[4], index, str(datetime.date.today()), stock_price, one_order[5]]

        full_price = stock_for_buy_list[4] * one_order[5]
        self.cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?", one_order[2])
        current_amount = self.cursor.fetchone()[0]

        if current_amount >= full_price:
            self.update_users_table(current_amount - full_price, one_order[2])
            self.update_balance_table(current_amount - full_price, one_order[2])
            self.update_owned_stocks_table(stock_for_buy_list, index)
            self.delete_order(one_order[0], index)

    def buy_ioc_func(self, one_order, index, sht):
        """
        Trying to execute buy "IOC" (immediately-or-cancel) order,
        this order is trying to buy a stock, if the transaction cant be made once the whole order is canceled
        """
        stock_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
        # stock_for_buy_list = order_creator_key, ticker, index, today date,price, stocks_amount
        stock_for_buy_list = [one_order[2], one_order[4], index, str(datetime.date.today()), stock_price, one_order[5]]

        full_price = stock_for_buy_list[4] * one_order[5]
        self.cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?", one_order[2])
        current_amount = self.cursor.fetchone()[0]

        if current_amount >= full_price:
            self.update_users_table(current_amount - full_price, one_order[2])
            self.update_balance_table(current_amount - full_price, one_order[2])
            self.update_owned_stocks_table(stock_for_buy_list, index)
            self.delete_order(one_order[0], index)

        else:
            self.delete_order(one_order[0], index)

    def buy_buy_above_func(self, one_order, index, sht):
        """
        Trying to execute buy "Buy Above" order,
        this order is buying the stock only if the price is equal or higher than the limit
        """
        stock_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
        # stock_for_buy_list = order_creator_key, ticker, index, today date,price, stocks_amount
        stock_for_buy_list = [one_order[2], one_order[4], index, str(datetime.date.today()), stock_price, one_order[5]]

        min_limit = int(((one_order[6]).split("-"))[0])
        max_limit = int(((one_order[6]).split("-"))[1])

        full_price = stock_for_buy_list[4] * one_order[5]
        self.cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?", one_order[2])
        current_amount = self.cursor.fetchone()[0]
        if min_limit <= int(stock_for_buy_list[4]) <= max_limit:
            if current_amount >= full_price:
                self.update_users_table(current_amount - full_price, one_order[2])
                self.update_balance_table(current_amount - full_price, one_order[2])
                self.update_owned_stocks_table(stock_for_buy_list, index)
                self.delete_order(one_order[0], index)

            elif one_order[5] > 1:
                possible_amount = int(current_amount / stock_for_buy_list[4])
                if possible_amount != 0:
                    stock_for_buy_list[5] = possible_amount
                    full_price = stock_for_buy_list[4] * stock_for_buy_list[5]
                    self.update_users_table(current_amount - full_price, one_order[2])
                    self.update_balance_table(current_amount - full_price, one_order[2])
                    self.update_owned_stocks_table(stock_for_buy_list, index)
                    self.update_order_stocks_amount(one_order[0], index, one_order[5] - possible_amount)

    def buy_fok_func(self, one_order, index, sht):
        """
        Trying to execute buy "FOK" (fill-or-kill) order,
        this order is trying to purchase a stock only for specific time period, either the order is canceld
        """
        live_minutes = int(one_order[6])

        if live_minutes > 0:
            self.cursor.execute("UPDATE " + INDEXES_TABLES.get(index) + "_orders_table SET order_info = ? "
                                "WHERE order_number = ?", str(live_minutes - 1), one_order[0])

            stock_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
            # stock_for_buy_list = order_creator_key, ticker, index, today date,price, stocks_amount
            stock_for_buy_list = [one_order[2], one_order[4], index, str(datetime.date.today()), stock_price,
                                  one_order[5]]

            full_price = stock_for_buy_list[4] * one_order[5]
            self.cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?", one_order[2])
            current_amount = self.cursor.fetchone()[0]

            if current_amount >= full_price:
                self.update_users_table(current_amount - full_price, one_order[2])
                self.update_balance_table(current_amount - full_price, one_order[2])
                self.update_owned_stocks_table(stock_for_buy_list, index)
                self.delete_order(one_order[0], index)

        else:
            self.delete_order(one_order[0], index)

    def sell_market_func(self, one_order, index, sht):
        """
        Trying to execute sell "market" order, this order sell the owned stock at the current price in the market
        """
        stock_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
        # stock_for_buy_list = order_creator_key, ticker, index, today date,price, stocks_amount
        stock_for_buy_list = [one_order[2], one_order[4], index, str(datetime.date.today()), stock_price, one_order[5]]

        full_price = stock_for_buy_list[4] * one_order[5]
        self.cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?", one_order[2])
        current_amount = self.cursor.fetchone()[0]

        self.update_users_table(current_amount + full_price, one_order[2])
        self.update_balance_table(current_amount + full_price, one_order[2])
        self.update_gains_or_losses(one_order[7], one_order[5], full_price, one_order[2], index)
        self.delete_order(one_order[0], index)

        self.cursor.execute(
            "SELECT stock_amount FROM " + INDEXES_TABLES.get(index) + "_owned_stocks_table "
            "WHERE stock_number = ?", one_order[7])
        full_stock_amount = self.cursor.fetchone()[0]

        if full_stock_amount == one_order[5]:
            self.delete_owned_stock(one_order[7], index)

        else:
            new_stocks_amount = full_stock_amount - one_order[5]
            self.update_owned_stock_amount_and_order(one_order[7], index, new_stocks_amount)
            self.delete_sell_order_from_owned_stock(one_order[7], index)

    def sell_limit_func(self,one_order, index, sht):
        """
        Trying to execute sell "limit" order, this order sell the owned stock only when the price reach the limit
        """
        limit = int(one_order[6])
        stock_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
        # stock_for_buy_list = order_creator_key, ticker, index, today date,price, stocks_amount
        stock_for_buy_list = [one_order[2], one_order[4], index, str(datetime.date.today()), stock_price, one_order[5]]

        if stock_for_buy_list[4] >= limit:
            full_price = stock_for_buy_list[4] * one_order[5]
            self.cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?", one_order[2])
            current_amount = self.cursor.fetchone()[0]
            self.update_users_table(current_amount + full_price, one_order[2])
            self.update_balance_table(current_amount + full_price, one_order[2])
            self.update_gains_or_losses(one_order[7], one_order[5], full_price, one_order[2], index)
            self.delete_order(one_order[0], index)
            self.cursor.execute(
                "SELECT stock_amount FROM " + INDEXES_TABLES.get(index) + "_owned_stocks_table "
                                                                          "WHERE stock_number = ?", one_order[7])
            full_stock_amount = self.cursor.fetchone()[0]
            if full_stock_amount == one_order[5]:
                self.delete_owned_stock(one_order[7], index)

            else:
                new_stocks_amount = full_stock_amount - one_order[5]
                self.update_owned_stock_amount_and_order(one_order[7], index, new_stocks_amount)
                self.delete_sell_order_from_owned_stock(one_order[7], index)

    def sell_stop_loss_func(self,one_order, index, sht):
        """
        Trying to execute sell "stop loss" order,
        this order sell the owned stock when the price getting lower than the minimum limit
        """
        limit = int(one_order[6])
        stock_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
        # stock_for_buy_list = order_creator_key, ticker, index, today date,price, stocks_amount
        stock_for_buy_list = [one_order[2], one_order[4], index, str(datetime.date.today()), stock_price, one_order[5]]

        if stock_for_buy_list[4] <= limit:
            full_price = stock_for_buy_list[4] * one_order[5]
            self.cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?", one_order[2])
            current_amount = self.cursor.fetchone()[0]

            self.update_users_table(current_amount + full_price, one_order[2])
            self.update_balance_table(current_amount + full_price, one_order[2])
            self.update_gains_or_losses(one_order[7], one_order[5], full_price, one_order[2], index)
            self.delete_order(one_order[0], index)

            self.cursor.execute(
                "SELECT stock_amount FROM " + INDEXES_TABLES.get(index) + "_owned_stocks_table "
                                                                          "WHERE stock_number = ?", one_order[7])
            full_stock_amount = self.cursor.fetchone()[0]

            if full_stock_amount == one_order[5]:
                self.delete_owned_stock(one_order[7], index)
            else:
                new_stocks_amount = full_stock_amount - one_order[5]
                self.update_owned_stock_amount_and_order(one_order[7], index, new_stocks_amount)
                self.delete_sell_order_from_owned_stock(one_order[7], index)

    def sell_stop_limit_func(self,one_order, index, sht):
        """
        Trying to execute sell "stop limit" order,
        this order create limit order if the price is lower than the stop price
        """
        current_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
        stop_price = int(((one_order[6]).split("-"))[0])
        limit_price = ((one_order[6]).split("-"))[1]

        if current_price <= stop_price:
            order_type = "SELL-LIMIT"
            self.cursor.execute("INSERT INTO " + INDEXES_TABLES.get(index) + "_orders_table"
                                "(order_type,order_creator_key, order_date, ticker, stocks_number, order_info,"
                                                                             "owned_stock_number)"
                                " VALUES(?,?,?,?,?,?,?)"
                                , order_type, one_order[2], str(datetime.date.today()),
                                one_order[4], one_order[5], limit_price,one_order[7])

            self.delete_order(one_order[0], index)

    def sell_aon_func(self,one_order, index, sht):
        """
        Trying to execute sell "AON" (all-or-none) order, this order try to sell all the stocks,
        if the transaction cant be made full the order is canceled
        """
        stock_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
        # stock_for_buy_list = order_creator_key, ticker, index, today date,price, stocks_amount
        stock_for_buy_list = [one_order[2], one_order[4], index, str(datetime.date.today()), stock_price, one_order[5]]

        full_price = stock_for_buy_list[4] * one_order[5]
        self.cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?", one_order[2])
        current_amount = self.cursor.fetchone()[0]

        self.update_users_table(current_amount + full_price, one_order[2])
        self.update_balance_table(current_amount + full_price, one_order[2])
        self.update_gains_or_losses(one_order[7], one_order[5], full_price, one_order[2], index)
        self.delete_order(one_order[0], index)

        self.cursor.execute(
            "SELECT stock_amount FROM " + INDEXES_TABLES.get(index) + "_owned_stocks_table "
                                                                      "WHERE stock_number = ?", one_order[7])
        full_stock_amount = self.cursor.fetchone()[0]

        if full_stock_amount == one_order[5]:
            self.delete_owned_stock(one_order[7], index)
        else:
            new_stocks_amount = full_stock_amount - one_order[5]
            self.update_owned_stock_amount_and_order(one_order[7], index, new_stocks_amount)
            self.delete_sell_order_from_owned_stock(one_order[7], index)

    def sell_ioc_func(self,one_order, index, sht):
        """
        Trying to execute sell "IOC" (immediately-or-canceled) order,
        this order try to sell the stocks once, if the transaction can't be made the order is canceled
        """
        stock_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
        # stock_for_buy_list = order_creator_key, ticker, index, today date,price, stocks_amount
        stock_for_buy_list = [one_order[2], one_order[4], index, str(datetime.date.today()), stock_price, one_order[5]]

        full_price = stock_for_buy_list[4] * one_order[5]
        self.cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?", one_order[2])
        current_amount = self.cursor.fetchone()[0]
        try:
            self.update_users_table(current_amount + full_price, one_order[2])
            self.update_balance_table(current_amount + full_price, one_order[2])
            self.update_gains_or_losses(one_order[7], one_order[5], full_price, one_order[2], index)
            self.delete_order(one_order[0], index)

            self.cursor.execute(
                "SELECT stock_amount FROM " + INDEXES_TABLES.get(index) + "_owned_stocks_table "
                                                                          "WHERE stock_number = ?", one_order[7])
            full_stock_amount = self.cursor.fetchone()[0]

            if full_stock_amount == one_order[5]:
                self.delete_owned_stock(one_order[7], index)
            else:
                new_stocks_amount = full_stock_amount - one_order[5]
                self.update_owned_stock_amount_and_order(one_order[7], index, new_stocks_amount)
                self.delete_sell_order_from_owned_stock(one_order[7], index)

        except:
            self.delete_sell_order_from_owned_stock(one_order[7], index)
            self.delete_order(one_order[0], index)

    def sell_fok_func(self,one_order, index, sht):
        """
        Trying to execute sell "FOK" (fill-or-kill) order,
        this order can be alive for a specific period of time,
        If it can't be executed inn this time the order is canceled
        """
        live_minutes = int(one_order[6])

        if live_minutes > 0:
            self.cursor.execute("UPDATE " + INDEXES_TABLES.get(index) + "_orders_table SET order_info = ? "
                                "WHERE order_number = ?", str(live_minutes - 1), one_order[0])

            stock_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
            # stock_for_buy_list = order_creator_key, ticker, index, today date,price, stocks_amount
            stock_for_buy_list = [one_order[2], one_order[4], index, str(datetime.date.today()), stock_price,
                                  one_order[5]]

            full_price = stock_for_buy_list[4] * one_order[5]
            self.cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?",
                                one_order[2])
            current_amount = self.cursor.fetchone()[0]

            self.update_users_table(current_amount + full_price, one_order[2])
            self.update_balance_table(current_amount + full_price, one_order[2])
            self.update_gains_or_losses(one_order[7], one_order[5], full_price, one_order[2], index)
            self.delete_order(one_order[0], index)

            self.cursor.execute(
                "SELECT stock_amount FROM " + INDEXES_TABLES.get(index) + "_owned_stocks_table "
                                                                          "WHERE stock_number = ?", one_order[7])
            full_stock_amount = self.cursor.fetchone()[0]

            if full_stock_amount == one_order[5]:
                self.delete_owned_stock(one_order[7], index)
            else:
                new_stocks_amount = full_stock_amount - one_order[5]
                self.update_owned_stock_amount_and_order(one_order[7], index, new_stocks_amount)
                self.delete_sell_order_from_owned_stock(one_order[7], index)
        else:
            self.delete_order(one_order[0], index)
            self.delete_sell_order_from_owned_stock(one_order[7], index)

    def sell_take_profit_func(self,one_order, index, sht):
        """
        Trying to execute sell "T/P" (Take-Profit) order,
        this order sell the stock only if the transaction will make the profit that the client asked for
        """
        stock_price = self.seacrching_stock_price_in_excel_file(sht, one_order[4])
        # stock_for_buy_list = order_creator_key, ticker, index, today date,price, stocks_amount
        stock_for_buy_list = [one_order[2], one_order[4], index, str(datetime.date.today()), stock_price,one_order[5]]
        limit = int(one_order[6])

        if stock_for_buy_list[4] >= limit:
            full_price = stock_for_buy_list[4] * one_order[5]
            self.cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?", one_order[2])
            current_amount = self.cursor.fetchone()[0]

            self.update_users_table(current_amount + full_price, one_order[2])
            self.update_balance_table(current_amount + full_price, one_order[2])
            self.update_gains_or_losses(one_order[7], one_order[5], full_price, one_order[2], index)
            self.delete_order(one_order[0], index)

            self.cursor.execute(
                "SELECT stock_amount FROM " + INDEXES_TABLES.get(index) + "_owned_stocks_table "
                                                                          "WHERE stock_number = ?",one_order[7])
            full_stock_amount = self.cursor.fetchone()[0]

            if full_stock_amount == one_order[5]:
                self.delete_owned_stock(one_order[7], index)
            else:
                new_stocks_amount = full_stock_amount - one_order[5]
                self.update_owned_stock_amount_and_order(one_order[7], index, new_stocks_amount)
                self.delete_sell_order_from_owned_stock(one_order[7], index)

    def update_owned_stocks_table(self, stock_for_buy_list, index):
        """
        When a buy order had been executed this function create an owned stocks line in owned stocks table
        """
        self.cursor.execute(
            "INSERT INTO " + index + "_owned_stocks_table(owner_key, ticker, buy_date, buy_price, stock_amount)"
            " VALUES(?,?,?,?,?)", stock_for_buy_list[0],stock_for_buy_list[1],stock_for_buy_list[3],
            stock_for_buy_list[4],stock_for_buy_list[5])

    def delete_owned_stock(self, stock_number, index):
        """
        When a sell order had been executed this function delete the sold stock from the owned stocks table
        """
        try:
            self.cursor.execute("DELETE * FROM " + INDEXES_TABLES.get(index) +
                                "_owned_stocks_table WHERE stock_number = ?", stock_number)

        except Exception as ex:
            print("delete error:\n")
            print(ex)

    def update_users_table(self, new_amount, order_creator_key):
        """
        When a buy or sell order had been executed this function
        add or lower the balance of the client in the users table
        """
        self.cursor.execute("UPDATE users_table SET initial_amount = ? WHERE user_key_number = ?", new_amount,
                            order_creator_key)

    def update_balance_table(self, new_amount, order_creator_key):
        """
        This function update the balance graph after a change in the balance number
        """
        self.cursor.execute("SELECT balance_y FROM balance_history_table WHERE (user_key_number = ?)",
                            order_creator_key)
        balance_str = self.cursor.fetchone()[0] + "," + str(int(new_amount))
        self.cursor.execute("UPDATE balance_history_table SET balance_y = ? WHERE user_key_number = ?",
                            balance_str, order_creator_key)

    def update_gains_or_losses(self, owned_stock_number, stocks_amount, full_price, order_creator_key, index):
        """
        This function checking is the sell order gained or lost money, for each case the function updating the graph
        """
        self.cursor.execute("SELECT buy_price FROM " + INDEXES_TABLES.get(index) +
                            "_owned_stocks_table WHERE stock_number = ?", owned_stock_number)
        buy_price = int(stocks_amount * self.cursor.fetchone()[0])
        buy_and_sell_remainder = full_price - buy_price

        if buy_and_sell_remainder > 0:
            self.cursor.execute("SELECT gains_y FROM balance_history_table WHERE (user_key_number = ?)",
                                order_creator_key)
            gains_str = self.cursor.fetchone()[0] + "," + str(buy_and_sell_remainder)
            self.cursor.execute("UPDATE balance_history_table SET gains_y = ? WHERE user_key_number = ?",
                                gains_str, order_creator_key)

        elif buy_and_sell_remainder < 0:
            self.cursor.execute("SELECT losses_y FROM balance_history_table WHERE (user_key_number = ?)",
                                order_creator_key)
            losses_str = self.cursor.fetchone()[0] + "," + str(-1 * buy_and_sell_remainder)
            self.cursor.execute("UPDATE balance_history_table SET losses_y = ? WHERE user_key_number = ?",
                                losses_str, order_creator_key)

    def delete_order(self, order_number, index):
        """
        This function is deleting an order after it was executed
        """
        try:
            self.cursor.execute("DELETE * FROM " + INDEXES_TABLES.get(index) +
                                "_orders_table WHERE order_number = ?", order_number)
        except Exception as ex:
            print("delete error:\n")
            print(ex)

    def update_order_stocks_amount(self, order_number, index, new_amount):
        """
        This function update an buy order if it wasn't executed fully
        """
        try:
            self.cursor.execute("UPDATE " + INDEXES_TABLES.get(index) +
                                "_orders_table SET stocks_number = ? WHERE order_number = ?", new_amount, order_number)
        except Exception as w:
            print("update error:\n")
            print(w)

    def update_owned_stock_amount_and_order(self, stock_number, index, new_amount):
        """
        This function update an owned stock stocks number and the sell order
        when the sell order wasn't executed fully.
        """
        try:
            self.cursor.execute("UPDATE " + INDEXES_TABLES.get(index) +
                                "_owned_stocks_table SET stock_amount = ?, sell_order = ? WHERE stock_number = ?"
                                , new_amount, None, stock_number)
        except Exception as w:
            print("update error:\n")
            print(w)

    def delete_sell_order_from_owned_stock(self, stock_number, index):
        """
        This order deleting the open order that was made on an owned stock
        """
        self.cursor.execute("UPDATE " + INDEXES_TABLES.get(index) + "_owned_stocks_table SET sell_order = ?"
                            " WHERE stock_number = ?", None, stock_number)
