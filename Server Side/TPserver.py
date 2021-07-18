import threading, socket, pickle, struct, pyodbc, sys, datetime, hashlib
from TPserver_functions import create_excel_func, specific_searching_in_market_func,\
    more_info_for_stock, free_searching_in_market_func, create_buy_order, create_sell_order,\
    searching_for_clients_orders, searching_for_clients_stocks, searching_for_clients_reports,\
    get_answer_to_client_request_func, delete_a_file

from TPorders_execute import OrdersRunner

IP = '0.0.0.0'
PORT = 1030
PATH_EXCEL = "C:/Users/Almogi/Desktop/פרוייקט בסייבר/stocks_csv/"
ACCESS_DRIVER = '{Microsoft Access Driver (*.mdb, *.accdb)}'
DATABASE_FILE = r'C:\Users\Almogi\Desktop\פרוייקט בסייבר\TP_data_base.accdb'

INDEXES_TABLES = {"DowJones30": "DowJones30",
                         "S&P500": "SP500",
                         "Nasdaq100": "Nasdaq100",
                         "Russell1000": "Russell1000"}

class ServerListener(threading.Thread):
    """
    Class for the server operator to close the DB usage when he want to stop the server running
    """
    def __init__(self):
        """
        Creating the class thread so it will run with the ClientConnection and the Server in parallel
        """
        self.thread = threading.Thread.__init__(self)
        # self.excel_app = xlwings.App(visible=False)

    def run(self):
        """
        Waiting for the server operator to input "kill" and then closing the server side
        """
        server_controller = input()
        if server_controller == "kill":
            cursor.close()
            cnxn.close()
            kill_excel_app = False
            print("     -------------------- server killing ---------------------")
            sys.exit()


class Server:
    """
    Class for getting clients connect, create socket for each client and a thread class for handling their usage
    """
    def __init__(self):
        """
        Creating a thread for parallel running
        """
        self.thread = threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((IP, PORT))
        self.socket.listen()

    def get_clients(self):
        """
        Trying to start the client use and get him connect to the server
        """
        while True:
            try:
                client, client_address = self.socket.accept()
                print("\n     --------- " + str(client_address) + " got connected ---------\n")
                client_handle = ClientConnection(client)
                client_handle.start()

            except Exception as ex:
                print(ex)


class ClientConnection(threading.Thread):
    """
    Class for handling the client and take care of him
    """
    def __init__(self, client):
        """
        Creating the thread so the class can run in parallel
        """
        threading.Thread.__init__(self)
        self.client = client
        self.current_client_key = None

    def run(self):
        """
        Trying to make the first step in connecting the client to the system
        """
        try:
            connection_use = self.client.recv(1024).decode()   # checking if the client clicked 'sign in' or 'sign up'
            if connection_use == "sign_in":
                self.sign_in_client()
            elif connection_use == "sign_up": # while the "sign up" client is connected
                self.sign_up_client()

        except Exception as ex:
            print("      --- the connection was forcibly closed by the client ---")

    def sign_in_client(self):
        """
        Deal with sighing in process
        """
        while True:  # while the "sign in" client is connected
            username_and_password = self.client.recv(1024)
            username_and_password = pickle.loads(username_and_password)
            # checking if the username is exist in the database and return the correct password
            cursor.execute("SELECT password FROM users_table WHERE (username = ?)", username_and_password[0])
            password = cursor.fetchone()

            if not password:
                self.client.send("The username you entered is not exist in the system".encode())

            elif password[0] == hashlib.md5((username_and_password[1]).encode()).hexdigest():
                self.client.send("Your details have been verified by the system".encode())
                # saving the current client key number
                cursor.execute("SELECT user_key_number FROM users_table WHERE (username = ?)", username_and_password[0])
                self.current_client_key = cursor.fetchone()[0]
                print("     ------------ " + username_and_password[0] + " got connected into the system ------------")
                # sending all client details to the client from the database
                cursor.execute("SELECT username, password, fullname, mail, initial_amount"
                               " FROM users_table WHERE (user_key_number = ?)", self.current_client_key)
                self.client.send(pickle.dumps(list(cursor.fetchone())))
                break
            else:
                self.client.send("The details you entered do not match each other".encode())

        self.client_handling()

    def sign_up_client(self):
        """
        Deal with sighing up process
        """
        while True:
            # while the "sign up" client is connected
            all_details = self.client.recv(1024)
            all_details = pickle.loads(all_details)
            cursor.execute("SELECT username FROM users_table WHERE username = ?", all_details[0])
            # checking if the client username is already used
            check_username_existence = cursor.fetchone()
            if check_username_existence:
                self.client.send("Your username is already taken, please enter a new one".encode())
            else:
                break

        # adding user to the database
        cursor.execute(
            "INSERT INTO users_table(username,password,fullname,mail,initial_amount)"
            " VALUES(?,?,?,?,?)", all_details[0], hashlib.md5((all_details[1]).encode()).hexdigest(),
            all_details[2], all_details[3], all_details[4])

        self.client.send("Your details have been verified by the system".encode())
        print("     ------------ " + all_details[0] + " got connected into the system ------------")

        cursor.execute("SELECT user_key_number FROM users_table WHERE (username = ?)", all_details[0])
        self.current_client_key = cursor.fetchone()[0]
        # create a line for the client in the blance history table
        cursor.execute(
            "INSERT INTO balance_history_table(user_key_number, balance_y, gains_y, losses_y)"
            " VALUES(?,?,?,?)", self.current_client_key, all_details[4], "0", "0")

        self.create_report("TEXT", all_details[0].upper() + " welcome to 'Take Profit Stock Exchange'",
                           "Hey,"
                           "\nThank you for choosing to practice on our platform,"
                           "\nour goal is to let you to learn about the stock market in the easiest and safest way."
                           "\nOur platform provides reliable and up to date information so that you can study the "
                           "\nstocks market in depth and without risks."
                           "\nFor more information and explanations go to the About Us page."
                           "\nGood luck! and don't forget to take profit...")

        self.client_handling()

    def client_handling(self):
        """
        Handling the client requests.
        Every request from the client start with the name of the client action and then
        the asked request is applied by a specific function.
        """
        while True:
            try:
                client_ask = self.client.recv(1024).decode()

                if client_ask == "refresh_balance_tab":
                    self.refresh_balance_tab()
                elif client_ask == "add_money":
                    self.add_money()
                elif client_ask == "stock_excel":
                    self.send_stock_excel()
                elif client_ask == "specific_search_in_market":
                    self.specific_searching()
                elif client_ask == "free_search_in_market":
                    self.free_searching()
                elif client_ask == "more_stock_info":
                    self.more_stock_info()
                elif client_ask == "create_order":
                    self.create_order()
                elif client_ask == "refresh_open_orders":
                    self.refresh_open_orders()
                elif client_ask == "refresh_own_stocks":
                    self.refresh_own_stocks()
                elif client_ask == "refresh_reports":
                    self.refresh_reports()
                elif client_ask == "delete_buy_order":
                    self.delete_buy_order()
                elif client_ask == "delete_sell_order":
                    self.delete_sell_order()
                elif client_ask == "create_request":
                    self.create_request()
                elif client_ask == "delete_report":
                    self.delete_report()

            except Exception as ex:
                cursor.execute("SELECT username FROM users_table WHERE user_key_number = ?", self.current_client_key)
                print("     ------------------- " + cursor.fetchone()[0] + " got disconnected ------------------")
                self.client.close()
                break

    def refresh_balance_tab(self):
        """
        Refreshing the client's balance tab with three different pyqt graphs
        """
        cursor.execute("SELECT balance_y,gains_y,losses_y FROM balance_history_table WHERE (user_key_number = ?)",
                       self.current_client_key)
        balance_gains_losses_amount = list(cursor.fetchone())

        for i in range(len(balance_gains_losses_amount)):
            save_list = balance_gains_losses_amount[i].split(',')
            for g in range(len(save_list)):
                save_list[g] = int(float(save_list[g]))
            balance_gains_losses_amount[i] = save_list[-10:]

        balance_gains_losses_amount.append(balance_gains_losses_amount[0][-1])
        self.client.send(pickle.dumps(balance_gains_losses_amount))

    def refresh_open_orders(self):
        """
        Refreshing the open orders that the client have and sending them one by one
        """
        all_open_orders = searching_for_clients_orders(self.current_client_key, cursor)
        self.client.send((str(len(all_open_orders))).encode())  # sending how many open orders were found
        for one_order in all_open_orders:
            self.client.send(pickle.dumps(one_order))
            self.client.recv(1024)  # ACK

    def refresh_own_stocks(self):
        """
        Refreshing the client's owned stocks and sending them one by one
        """
        owned_stocks = searching_for_clients_stocks(self.current_client_key, cursor)
        self.client.send((str(len(owned_stocks))).encode())  # sending how many owned stocks were found
        for one_order in owned_stocks:
            self.client.send(pickle.dumps(one_order))
            self.client.recv(1024)  # ACK

    def refresh_reports(self):
        """
        Refreshing the clint's reports and sending them one by one
        """
        all_reports = searching_for_clients_reports(self.current_client_key, cursor)
        self.client.send((str(len(all_reports))).encode())  # sending how many open orders were found
        for one_report in all_reports:
            self.client.send(pickle.dumps(one_report))
            self.client.recv(1024)  # ACK

    def add_money(self):
        """
        Adding money for the client in the users_table and in the balance_table
        """
        add_value = int(self.client.recv(1024).decode())
        cursor.execute("SELECT initial_amount FROM users_table WHERE user_key_number = ?", self.current_client_key)
        current_amount = cursor.fetchone()[0]
        cursor.execute("UPDATE users_table SET initial_amount = ? WHERE user_key_number = ?", (current_amount+add_value,
                                                                                               self.current_client_key))
        cursor.execute("SELECT balance_y FROM balance_history_table WHERE (user_key_number = ?)",
                       self.current_client_key)
        balance_str = cursor.fetchone()[0] + "," + str(current_amount+add_value)
        cursor.execute("UPDATE balance_history_table SET balance_y = ? WHERE user_key_number = ?",
                       balance_str, self.current_client_key)
        self.client.send('Ack'.encode())

    def send_stock_excel(self):
        """
        Sending for the client an excel file with stock history, this file will be use for matplotlib graph.
        The file is sending in packs and not all by once.
        After sending the function delte the file from the computer.
        """
        stock_info = pickle.loads(self.client.recv(1024))
        path_excel = create_excel_func(stock_info)
        with open(path_excel, 'rb') as file:
            data = file.read()
        size = len(data)
        self.client.sendall(struct.pack('>Q', size) + data)
        delete_a_file(path_excel)

    def specific_searching(self):
        """
        Get a specific search parameters and search stocks that matched those parameters
        and then sending the stocks to the client one by one.
        """
        search_parameters = pickle.loads(self.client.recv(1024)) # index ,industry , market cap , change , price
        stocks_list = specific_searching_in_market_func(search_parameters)
        self.client.send((str(len(stocks_list))).encode())# sending  how many stocks were found
        self.client.recv(1024) # ACK

        for one_stock in stocks_list:
            self.client.send(pickle.dumps(one_stock))
            self.client.recv(1024) # ACK

    def free_searching(self):
        """
        Get a free search parameters and search stocks that matched those parameters
        and then sending the stocks to the client one by one.
        """
        search_parameters = pickle.loads(self.client.recv(1024))  # search type (TYPED/LIST) ,search line
        stocks_list = free_searching_in_market_func(search_parameters)
        self.client.send((str(len(stocks_list))).encode())  # sending how many stocks were found
        self.client.recv(1024)  # ACK

        for one_stock in stocks_list:
            self.client.send(pickle.dumps(one_stock))
            self.client.recv(1024)  # ACK

    def more_stock_info(self):
        """
        Get a stock's ticker and get more information about that stock,
        and finally sending the info to the client
        """
        index_and_ticker = pickle.loads(self.client.recv(1024))
        more_info = more_info_for_stock(index_and_ticker[0], index_and_ticker[1])
        self.client.send(pickle.dumps(more_info))

    def create_order(self):
        """
        Creating an open order with the parameters that were entered by the client
        """
        # transaction_parameters = [order type, ticker, index, stocks number, more_params/no_necessary_params]
        transaction_parameters = pickle.loads(self.client.recv(1024))
        # transaction_parameters = [order type, creator key, date, ticker,index,
        #                           stocks number, more_params/no_necessary_params]
        transaction_parameters.insert(1, self.current_client_key)
        transaction_parameters.insert(2, str(datetime.date.today()))

        buy_or_sell_and_type = (transaction_parameters[0]).split("-")
        transaction_parameters[0] = buy_or_sell_and_type[1]

        if buy_or_sell_and_type[0] == "BUY":
            create_buy_order(transaction_parameters, cursor)

        elif buy_or_sell_and_type[0] == "SELL":
            create_sell_order(transaction_parameters, cursor)

    def delete_buy_order(self):
        """
        Delete an open buy order that the client ask for canceling it from the open orders table
        """
        try:
            order_number = int((self.client.recv(1024)).decode())
            self.client.send("ACK".encode())
            order_index = str((self.client.recv(1024)).decode())
            cursor.execute("DELETE * FROM " + INDEXES_TABLES.get(order_index) +
                           "_orders_table WHERE order_number = ?", order_number)
            cursor.execute("DELETE * FROM " + INDEXES_TABLES.get(order_index) +
                           "_orders_table WHERE order_number = ?", order_number)
        except Exception as ex:
            print(ex)

    def delete_sell_order(self):
        """
        Delete an open sell order that the client ask for canceling it from
        the open orders table and from the owned stocks open order table
        """
        try:
            order_number = int((self.client.recv(1024)).decode())
            self.client.send("ACK".encode())
            order_index = str((self.client.recv(1024)).decode())

            cursor.execute("SELECT owned_stock_number FROM " + INDEXES_TABLES.get(order_index) +
                           "_orders_table WHERE order_number = ?", order_number)
            owned_stock_number = int(cursor.fetchone()[0])

            cursor.execute("UPDATE " + INDEXES_TABLES.get(order_index) + "_owned_stocks_table SET sell_order = ? WHERE stock_number = ?",
                           None, owned_stock_number)

            cursor.execute("DELETE * FROM " + INDEXES_TABLES.get(order_index) +
                           "_orders_table WHERE order_number = ?", order_number)
            cursor.execute("DELETE * FROM " + INDEXES_TABLES.get(order_index) +
                           "_orders_table WHERE order_number = ?", order_number)
        except Exception as ex:
            print(ex)

    def create_report(self, report_type, article, content):
        """
        Creating a report that was asked by the client and adding it to the reports table
        """
        try:
            now_time = str(datetime.datetime.strftime(datetime.datetime.now(), "%H:%M   %D"))
            cursor.execute("INSERT INTO reports_table(report_type,client_addressee_number,article,[time],content)"
                           " VALUES (?, ?, ?, ?, ?)", report_type, self.current_client_key, article, now_time, content)
        except Exception as a:
            print(a)

    def delete_report(self):
        """
        Delete a report from the reports table
        """
        self.client.send("ACK".encode())
        report_number = int(self.client.recv(1024).decode())
        cursor.execute("DELETE * FROM reports_table WHERE report_number = ?", report_number)
        cursor.execute("DELETE * FROM reports_table WHERE report_number = ?", report_number)

    def create_request(self):
        """
        Getting the client ask for a new report and answering it
        """
        self.client.send("ACK".encode())
        client_ask = self.client.recv(1024).decode()
        report_details = get_answer_to_client_request_func(self.current_client_key, cursor, client_ask)
        report_type = report_details[0]
        report_article = report_details[1]
        report_content = report_details[2]

        self.create_report(report_type, report_article, report_content)


if __name__ == '__main__':
    listener = ServerListener()
    listener.start()

    # connecting to the database
    cnxn = pyodbc.connect(driver=ACCESS_DRIVER, dbq=DATABASE_FILE, autocommit=True)
    cursor = cnxn.cursor()
    print("     ----------------- connected to database ----------------- ")

    order_runner = OrdersRunner(cursor)
    order_runner.start()

    server = Server()
    server.get_clients()


