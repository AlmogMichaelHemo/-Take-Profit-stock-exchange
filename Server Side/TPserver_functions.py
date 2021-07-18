import datetime, pytz, holidays, os
import pandas_datareader.data as web
import xlwings as xw

CSV_PATH = r"C:\Users\Almogi\Desktop\csv_for clients"
INDEXES_WORKBOOKS_PATH = r"C:\Users\Almogi\Desktop\indexes_workbooks"
INDEXES_TABLES = {"DowJones30": "DowJones30",
                  "S&P500": "SP500",
                  "Nasdaq100": "Nasdaq100",
                  "Russell1000": "Russell1000"}

STOCK_EXCHANGE_TIME_ZONE = pytz.timezone("US/Eastern")
US_HOLIDAYS = holidays.US()

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


def checking_if_the_market_is_open_func():
    """
    Checking if the market is open at this specific time
    """
    return True
    now = datetime.datetime.now(STOCK_EXCHANGE_TIME_ZONE)
    open_time = datetime.time(hour=9, minute=30, second=0)
    close_time = datetime.time(hour=16, minute=0, second=0)
    # checking if there is a holiday now
    if now.strftime('%Y-%m-%d') in US_HOLIDAYS:
        return False
    # checking if it is the weekend now
    elif now.date().weekday() > 4:
        return False
    # checking if it is before 0930 or after 1600 now
    elif (now.time() < open_time) or (now.time() > close_time):
        return False
    else:
        return True


def delete_a_file(file_name):
    """
    Checking if a file is exist and if he is, delete him
    """
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
        except Exception as ex:
            print(ex)


def create_excel_func(stock_info):
    """"
    Get a stock's ticker and get from the internet (yahoo finance)
    create csv file and return the path for this file
    """
    data_frame = web.DataReader(stock_info[0], 'yahoo', stock_info[1], stock_info[2])
    path = CSV_PATH + "\\" + stock_info[0] + ".csv"
    data_frame.to_csv(path)

    return path


def specific_searching_in_market_func(search_parameters):
    """
    Searching a specific search in the excel file concluding all the search parameters that were chosen
    search parameters = [index, industry, market cap, change, price]
    """
    stocks_list = []
    path = INDEXES_WORKBOOKS_PATH + "\\" +  search_parameters[0] + "_stocks_workbook.xlsm"
    try:
        # excel_app = xw.App(visible=False)
        wb = xw.Book(path)
        sht = wb.sheets['Sheet1']
        last_row = sht.range(1, 1).end('down').row

        if not search_parameters[1] == "NULL":
            for a in range(2, last_row + 1):
                if search_parameters[1] in str(sht.range("E" + str(a)).value):
                    # index in stocks_list : ticker, name, price, change, index, market cap
                    stocks_list.append([sht.range('B' + str(a)).value, sht.range('C' + str(a)).value,
                                        sht.range('F' + str(a)).value, sht.range('L' + str(a)).value * 100,  search_parameters[0],
                                        sht.range('K' + str(a)).value])
        else:
            for a in range(2, last_row + 1):
                # index in stocks_list : ticker, name, price, change, index, market cap
                stocks_list.append([sht.range('B' + str(a)).value, sht.range('C' + str(a)).value,
                                    sht.range('F' + str(a)).value, sht.range('L' + str(a)).value * 100,  search_parameters[0],
                                    sht.range('K' + str(a)).value])
        stocks_list_by_cap = []

        if not search_parameters[2] == "NULL":
            min_cap = 0
            max_cap = 0
            if search_parameters[2] == "small_cap":
                min_cap = 500 * 10 ** 6
                max_cap = 20 * 10 ** 9
            elif search_parameters[2] == "aveg_cap":
                min_cap = 20 * 10 ** 9
                max_cap = 100 * 10 ** 9
            elif search_parameters[2] == "big_cap":
                min_cap = 100 * 10 ** 9
                max_cap = 2.5 * 10 ** 12

            for b in stocks_list:
                if (min_cap < int(b[5])) and (int(b[5]) < max_cap):
                    stocks_list_by_cap.append(b)
            stocks_list = stocks_list_by_cap

        stocks_list_by_price = []

        if not search_parameters[4] == "NULL":
            for c in stocks_list:
                if (search_parameters[4] -20 < c[2]) and (c[2] < search_parameters[4] + 20):
                    stocks_list_by_price.append(c)
            stocks_list = stocks_list_by_price

        stocks_list_by_change = []

        if not  search_parameters[3] == "NULL":
            for d in stocks_list:
                if (search_parameters[3] -2 < d[3]) and (d[3] < search_parameters[3] + 2):
                    stocks_list_by_change.append(d)
            stocks_list = stocks_list_by_change

        wb.save()
        wb.close()
        # excel_app.quit()
        return stocks_list

    except Exception as ex:
        print(ex)


def free_searching_in_market_func(search_parameters):
    """
    Searching a free search in the excel file
    search parameters = [Typed/List, stock_name]
    """
    workbooks_list = ["DowJones30", "Nasdaq100", "S&P500", "Russell1000"]

    search_type = search_parameters[0]
    stock_name = search_parameters[1]

    stocks_list = []

    try:
        if search_type == "TYPED":
            found = False
            stock_name = stock_name.upper()

            for index in workbooks_list:
                if not found:
                    path = INDEXES_WORKBOOKS_PATH + "\\" + index + "_stocks_workbook.xlsm"
                    wb = xw.Book(path)
                    sht = wb.sheets['Sheet1']
                    last_row = sht.range(1, 1).end('down').row

                    for a in range(2, last_row + 1):
                        if stock_name in str(sht.range("C" + str(a)).value):
                            # index in stocks_list : ticker, name, price, change, index, market cap
                            stocks_list.append([sht.range('B' + str(a)).value, sht.range('C' + str(a)).value,
                                                sht.range('F' + str(a)).value, sht.range('L' + str(a)).value * 100,
                                                index,
                                                sht.range('K' + str(a)).value])
                            found = True

                    wb.save()
                    wb.close()
                    # excel_app.kill()
                else:
                    break

        elif search_type == "LIST":

            stock_name = stock_name.split("~")
            index = stock_name[1]
            stock_name = stock_name[0]

            path = INDEXES_WORKBOOKS_PATH + "\\" + index + "_stocks_workbook.xlsm"
            wb = xw.Book(path)
            sht = wb.sheets['Sheet1']
            last_row = sht.range(1, 1).end('down').row

            for a in range(2, last_row + 1):
                if stock_name in str(sht.range("C" + str(a)).value):
                    # index in stocks_list : ticker, name, price, change, index, market cap
                    stocks_list.append([sht.range('B' + str(a)).value, sht.range('C' + str(a)).value,
                                        sht.range('F' + str(a)).value, sht.range('L' + str(a)).value * 100, index,
                                        sht.range('K' + str(a)).value])

            wb.save()
            wb.close()

        return stocks_list

    except:
        pass


def more_info_for_stock(index, ticker):
    """
    Getting stock's ticker and searching for more information about the stock and his public company
    """
    path = INDEXES_WORKBOOKS_PATH + "\\" + index + "_stocks_workbook.xlsm"
    try:
        wb = xw.Book(path)
        sht = wb.sheets['Sheet1']
        last_row = sht.range(1, 1).end('down').row

        more_info_list = []
        # ticker, name, price, change, description,
        # industry, high, low, open, close,
        # beta, volume, PE, employees, Exchange, index

        for a in range(2, last_row + 1):
            if ticker == str(sht.range("B" + str(a)).value):
                more_info_list = [ticker, sht.range('C' + str(a)).value,
                                  sht.range('F' + str(a)).value, sht.range('L' + str(a)).value * 100,
                                  description_fix(sht.range('D' + str(a)).value),
                                  industry_fix(sht.range('E' + str(a)).value),
                                  sht.range('G' + str(a)).value, sht.range('H' + str(a)).value,
                                  sht.range('I' + str(a)).value, sht.range('J' + str(a)).value,
                                  sht.range('M' + str(a)).value, sht.range('O' + str(a)).value,
                                  sht.range('P' + str(a)).value, sht.range('Q' + str(a)).value, index]
                break

        wb.save()
        wb.close()

        return more_info_list
    except:
        pass


def description_fix(description):
    """
    Getting the one-line description and turn it to an orderly paragraph
    """
    description = description.split(". ")
    new_desc = []

    for line in description:
        words = (line).split(" ")

        if (20 < len(words)) and (len(words) < 30):
            new_desc.append(" ".join(words[0:8]))
            new_desc.append(" ".join(words[8:17]))
            new_desc.append(" ".join(words[17:len(words) - 1]))

        elif (30 < len(words)) and (len(words) < 40):
            new_desc.append(" ".join(words[0:8]))
            new_desc.append(" ".join(words[8:17]))
            new_desc.append(" ".join(words[17:26]))
            new_desc.append(" ".join(words[26:len(words) - 1]))

        elif (40 < len(words)) and (len(words) < 50):
            new_desc.append(" ".join(words[0:8]))
            new_desc.append(" ".join(words[8:17]))
            new_desc.append(" ".join(words[17:26]))
            new_desc.append(" ".join(words[26:35]))
            new_desc.append(" ".join(words[35:len(words) - 1]))

        elif (50 < len(words)) and (len(words) < 60):
            new_desc.append(" ".join(words[0:8]))
            new_desc.append(" ".join(words[8:17]))
            new_desc.append(" ".join(words[17:26]))
            new_desc.append(" ".join(words[26:35]))
            new_desc.append(" ".join(words[35:44]))
            new_desc.append(" ".join(words[44:len(words) - 1]))

        elif (65 < len(words)) and (len(words)):
            new_desc.append(" ".join(words[0:8]))
            new_desc.append(" ".join(words[8:17]))
            new_desc.append(" ".join(words[17:26]))
            new_desc.append(" ".join(words[26:35]))
            new_desc.append(" ".join(words[35:44]))
            new_desc.append(" ".join(words[44:55]))
            new_desc.append(" ".join(words[55:len(words) - 1]))

        else:
            new_desc.append(" ".join(words))

    description = "\n".join(new_desc)
    return description


def industry_fix(industry):
    """
    Getting the one-line industry name and turn it to a little orderly paragraph
    """
    industry = industry.split(" ")
    new_industry = []

    for i in range(len(industry)):
        appended = False
        if not (i+2 > len(industry)):
            if industry[i+1] == "&":
                appended = True
                new_industry.append(industry[i] + " &")
            elif not industry[i] == "&":
                new_industry.append(industry[i])
                appended = True
        if (not industry[i] == "&") and (not appended):
            new_industry.append(industry[i])

    industry = "\n".join(new_industry)
    return industry


def create_buy_order(transaction_parameters, cursor):
    """
    Adding new buy order to the open orders table
    transaction_parameters = [order type, creator key, date, ticker ,index, stocks number,
    more_params/no_necessary_params]
    """
    try:
        order_type = "BUY-" + transaction_parameters[0]
        order_creator_key = transaction_parameters[1]
        order_date = transaction_parameters[2]
        ticker = transaction_parameters[3]
        index = transaction_parameters[4]
        stocks_number = int(transaction_parameters[5])
        order_info = str(transaction_parameters[6])

        cursor.execute("INSERT INTO " + INDEXES_TABLES.get(index) + "_orders_table (order_type,order_creator_key,"
                       "order_date,ticker,stocks_number,order_info) VALUES(?,?,?,?,?,?)"
                       , order_type, order_creator_key, order_date, ticker, stocks_number, order_info)
    except Exception as a:
        print(a)


def create_sell_order(transaction_parameters, cursor):
    """
     Adding new sell order to the open orders table and update the owned stocks table
    transaction_parameters = [order type, creator key, date, ticker ,index,
     stocks number, more_params/no_necessary_params]
    """
    try:
        order_type = "SELL-" + transaction_parameters[0]
        order_creator_key = transaction_parameters[1]
        order_date = transaction_parameters[2]
        ticker = transaction_parameters[3]
        index = transaction_parameters[4]
        stocks_number = int(transaction_parameters[5])
        order_info = str(transaction_parameters[6])
        owned_stock_number = transaction_parameters[7]

        cursor.execute("INSERT INTO " + INDEXES_TABLES.get(index) + "_orders_table (order_type,order_creator_key,"
                       "order_date,ticker,stocks_number,order_info,owned_stock_number) VALUES(?,?,?,?,?,?,?)"
                       , order_type, order_creator_key, order_date, ticker, stocks_number, order_info, owned_stock_number)

        cursor.execute("UPDATE " + INDEXES_TABLES.get(index) + "_owned_stocks_table SET sell_order = ?"
                       " WHERE stock_number = ?", order_type, owned_stock_number)

    except Exception as a:
        print(a)


def searching_for_clients_orders(client_key_number, cursor):
    """
    Searching all client's open orders and return a list with all of them
    """
    orders_list = []

    for index in INDEXES_TABLES:
        cursor.execute("SELECT order_number,order_type,order_date,ticker,stocks_number,order_info FROM "
                        + INDEXES_TABLES.get(index) + "_orders_table WHERE order_creator_key = ?", client_key_number)
        for order in list(cursor.fetchall()):
            order = list(order)
            order.append(index)
            orders_list.append(order)
    return orders_list


def searching_for_clients_stocks(client_key_number, cursor):
    """
    Searching all client's owned stocks, getting their new price and change and return a list with all of them
    """
    clients_stocks = []
    for index in INDEXES_TABLES:
        cursor.execute("SELECT stock_number,ticker,buy_date,buy_price,stock_amount,sell_order FROM " +
                       INDEXES_TABLES.get(index) + "_owned_stocks_table WHERE owner_key = ?", client_key_number)
        owned_stocks = list(cursor.fetchall())

        if owned_stocks:
            path = INDEXES_WORKBOOKS_PATH + "\\" + index + "_stocks_workbook.xlsm"
            wb = xw.Book(path)
            sht = wb.sheets['Sheet1']
            last_row = sht.range(1, 1).end('down').row

            for stock in owned_stocks:
                stock = list(stock)
                for a in range(2, last_row + 1):
                    if stock[1] == str(sht.range("B" + str(a)).value):
                        stock.append(sht.range('C' + str(a)).value)
                        stock.append(sht.range('F' + str(a)).value)
                        stock.append(sht.range('L' + str(a)).value * 100)
                        stock.append(index)
                        clients_stocks.append(stock)
                        break
            wb.save()
            wb.close()
    return clients_stocks


def searching_for_clients_reports(client_key_number, cursor):
    """
    Searching all client's reports and return a list with all of them
    """
    cursor.execute("SELECT report_number, report_type, article, time, content FROM "
                   "reports_table WHERE client_addressee_number = ?", client_key_number)
    reports_list = list(cursor.fetchall())[::-1]
    return reports_list


def get_answer_to_client_request_func(client_key_number, cursor, client_ask):
    """
    Getting the client's request and return the answer of each type of request
    """
    if client_ask == "get balance history":
        cursor.execute("SELECT balance_y FROM balance_history_table WHERE user_key_number = ?", client_key_number)
        report_details = ["GRAPH", "Balance History", str(cursor.fetchone()[0])]

    elif client_ask == "get gains history":
        cursor.execute("SELECT gains_y FROM balance_history_table WHERE user_key_number = ?", client_key_number)
        report_details = ["GRAPH", "Gains History", str(cursor.fetchone()[0])]

    elif client_ask == "get losses history":
        cursor.execute("SELECT losses_y FROM balance_history_table WHERE user_key_number = ?", client_key_number)
        report_details = ["GRAPH", "Losses History", str(cursor.fetchone()[0])]

    else:
        cursor.execute("SELECT full_explanation FROM concepts_explanations WHERE client_ask = ?", client_ask)
        report_details = ["TEXT", client_ask, cursor.fetchone()[0]]

    return report_details