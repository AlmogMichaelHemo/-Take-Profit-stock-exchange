# This code is the main client side, manage all the comunication with the server and handle the user asks

import socket, sys, pickle, datetime, pytz, holidays

from PyQt5 import QtWidgets
from TPui import UiClient
from TPclient_plot import ask_for_stock_excel
from TPui_widgets import StockForBuyWidget, EmptyStockWidget, OrderWidget, NoOrdersWidget,\
    OwnedStockWidget, EmptyOwnedStockWidget, ReportWidget

# host IP adress (when the client runing at same computer as the server):
IP='127.0.0.1'

PORT= 1030
PATH_EXCEL = "C:\\Users\\User\\Desktop\\TPclient_folder\\"

STOCK_EXCHANGE_TIME_ZONE = pytz.timezone('US/Eastern')
US_HOLIDAYS = holidays.US()


class Client(UiClient):
    """
    Class that inherits from Ui_client and connecting the GUI to the server.
    """
    # def __init__(self)
    def checking_if_the_market_is_open(self):
        """
        Checking if the market (NYSE & Nasdaq) is open at this
        specific time while considering US timezone, weekends and holidays.
        If the market is closed there will be a label that inform the user about that.
        """
        now = datetime.datetime.now(STOCK_EXCHANGE_TIME_ZONE)
        open_time = datetime.time(hour = 9, minute = 30, second = 0)
        close_time = datetime.time(hour = 16, minute = 0, second = 0)

        # checking if there is a holiday now
        if now.strftime('%Y-%m-%d') in US_HOLIDAYS:
            self.close_market_label_market.hide()
            self.close_market_label_portfolio.hide()

        # checking if it is the weekend now
        elif now.date().weekday() > 4:
            self.close_market_label_market.hide()
            self.close_market_label_portfolio.hide()

        # checking if it is before 0930 or after 1600 now
        elif (now.time() < open_time) or (now.time() > close_time):
            self.close_market_label_market.hide()
            self.close_market_label_portfolio.hide()

        else:
            self.close_market_label_market.show()
            self.close_market_label_market.raise_()
            self.close_market_label_portfolio.show()
            self.close_market_label_portfolio.raise_()

    def connect_to_server(self):
        """
        Connecting to the server, making connection between sockets and ui
        """
        self.client = socket.socket()
        self.client.connect((IP, PORT))
        self.connect_buttons_to_functions()

    def connect_buttons_to_functions(self):
        """
        Connecting all the buttons to their functions and also operate the checking_if_the_market_is_open() function
        """
        self.checking_if_the_market_is_open()

        self.sign_in_Button.clicked.connect(self.sign_in_button_func)
        self.sign_up_Button.clicked.connect(self.sign_up_button_func)

        self.sign_in_in_Button.clicked.connect(self.sign_in_in_button_func)
        self.sign_up_up_Button.clicked.connect(self.sign_up_up_button_func)

        self.add_money_button.clicked.connect(self.add_money_func)
        self.plot_button_in_DJIA_widget.clicked.connect(
            lambda: self.ask_for_stock_excel('DJIA', self.start_dateEdit_in_DJIA_widget.date(), datetime.date.today()))
        self.plot_button_in_NDAQ_widget.clicked.connect(
            lambda: self.ask_for_stock_excel('^NDX', self.start_dateEdit_in_NDAQ_widget.date(), datetime.date.today()))
        self.plot_button_in_Russell_1000_widget.clicked.connect(
            lambda: self.ask_for_stock_excel('^RUI', self.start_dateEdit_in_Russell_1000_widget.date(), datetime.date.today()))
        self.plot_button_in_VIX_widget.clicked.connect(
            lambda: self.ask_for_stock_excel('^VIX', self.start_dateEdit_in_VIX_widget.date(), datetime.date.today()))
        self.plot_button_in_SP_500_widget.clicked.connect(
            lambda: self.ask_for_stock_excel('^GSPC', self.start_dateEdit_in_SP_500_widget.date(), datetime.date.today()))

        self.spec_search_Button_market.clicked.connect(self.specific_search_in_market_func)
        self.free_search_Button_market.clicked.connect(self.free_search_in_market_func)
        self.refresh_portfolio_button.clicked.connect(self.refresh_portfolio_tab)
        self.refresh_balance_button.clicked.connect(self.refresh_balance_tab)
        self.refresh_reports_button.clicked.connect(self.refresh_reports_tab)
        self.send_ask_Button.clicked.connect(self.send_request)

        self.tabWidget.currentChanged.connect(lambda: self.tab_change_checking_func())

    def sign_in_button_func(self):
        """
        "sign in" button in homepage function
        """
        self.client.send("sign_in".encode())
        self.stackedWidget.setCurrentIndex(1)

    def sign_up_button_func(self):
        """
        "sign up" button in homepage function
        """
        self.client.send("sign_up".encode())
        self.stackedWidget.setCurrentIndex(2)

    def sign_in_in_button_func(self):
        """
        "sign in" button in "sign in" page function.
        Try to get the user into the system and update him if something is wrong with the username or tha password.
        """
        self.error_label_in.setText('')
        username_entered = self.username_line_in.text()
        password_entered = self.password_line_in.text()

        if (username_entered is not None) & (password_entered is not None):
            username_and_password = pickle.dumps([username_entered, password_entered])
            self.client.send(username_and_password)
            server_permit = self.client.recv(1024).decode()

            if server_permit == "Your details have been verified by the system":
                self.client_details = pickle.loads(self.client.recv(1024))
                self.stackedWidget.setCurrentIndex(3)

            else:
                self.error_label_in.setText("Error:\n"+server_permit)
                self.error_label_in.show()

    def sign_up_up_button_func(self):
        """
        "sign up" button in homepage function
        Try to create new account for the user and update him if something is wrong with with the details he entered.
        """
        fullname_entered = self.full_name_line.text()
        mail_entered = self.mail_line.text()
        initial_amount_entered = self.initial_amount_line.text()
        username_entered = self.username_line_up.text()
        password_entered = self.password_line_up.text()

        if (not (username_entered == '')) & (not (password_entered == '')) & (not (fullname_entered  == '')) &\
                (not (mail_entered == '')) & (not (initial_amount_entered  == '')):

            if initial_amount_entered.isdigit():
                all_details = [username_entered, password_entered,fullname_entered,
                               mail_entered,int(initial_amount_entered)]
                self.client.send(pickle.dumps(all_details))
                server_permit = self.client.recv(1024).decode()

                if server_permit == "Your details have been verified by the system":
                    self.client_details = all_details
                    self.stackedWidget.setCurrentIndex(3)

                elif server_permit == "Your username is already taken, please enter a new one":
                    self.error_label_up.setText("Error:\n"+server_permit)
                    self.error_label_up.show()

            else:
                self.error_label_up.setText("Error:\nThe initial amount must be a digit")
                self.error_label_up.show()

        else:
            self.error_label_up.setText("Error:\nYou must fill all the details")
            self.error_label_up.show()

    def tab_change_checking_func(self):
        """"
        Refreshing each tab that need refreshing when the user click on him.

        index and tabs :
        0 - about us ,1 - reports ,2 - balance ,
        3 - portfolio , 4 - stock market ,5 - stock index
        """
        index = self.tabWidget.currentIndex()

        if index == 1:
            self.refresh_reports_tab()

        elif index == 2:
            self.refresh_balance_tab()

        elif index == 3:
            self.refresh_portfolio_tab()

    def refresh_balance_tab(self):
        """
        Refreshing the graphs in the balance tab
        """
        self.client.send("refresh_balance_tab".encode())
        balance_gains_losses_amount = pickle.loads(self.client.recv(1024))

        self.balance_line.clear()
        self.balance_line = self.balance_graph_widget.plot([i for i in range(len(balance_gains_losses_amount[0]))],
                                                           balance_gains_losses_amount[0]
                                       , pen ='b', symbol ='x', symbolPen ='b', symbolBrush = 0.2, name ='blue')
        self.balance_number.display((balance_gains_losses_amount[0])[-1])

        self.gains_line.clear()
        self.gains_line = self.gains_graph_widget.plot([i for i in range(len(balance_gains_losses_amount[1]))],
                                                       balance_gains_losses_amount[1]
                                     , pen ='g', symbol ='x', symbolPen ='g', symbolBrush = 0.2, name ='green')
        self.gains_number.display(sum(balance_gains_losses_amount[1]))

        self.losses_line.clear()
        self.losses_line = self.losses_graph_widget.plot([i for i in range(len(balance_gains_losses_amount[2]))],
                                                         balance_gains_losses_amount[2]
                                      , pen ='r', symbol ='x', symbolPen ='r', symbolBrush = 0.2, name ='red')
        self.losses_number.display(sum(balance_gains_losses_amount[2]))

    def refresh_reports_tab(self):
        """
        Refreshing the reports tab.
        First clearing the current reports on the scroll area and then update all the new reports.
        """
        for i in reversed(range(self.reports_verticalLayout.count())):  # clear the orders scroll area
            self.reports_verticalLayout.itemAt(i).widget().setParent(None)

        self.client.send("refresh_reports".encode())
        reports_number = int(self.client.recv(1024).decode())

        if not reports_number == 0:

            for one_report in range(reports_number):
                report_info = pickle.loads(self.client.recv(2048))
                new_widget = ReportWidget(self.reports_scrollAreaWidgetContents, self.reports_verticalLayout,
                                          report_info, self.client)
                new_widget.delete_report_Button.clicked.connect(self.refresh_reports_tab)
                self.client.send("ACK".encode())

        self.reports_scrollArea.setWidget(self.reports_scrollAreaWidgetContents)

    def refresh_portfolio_tab(self):
        """
        Operating the refresh_client_orders() and refresh_client_stocks() functions
        that refreshing the whole portfolio tab.
        """
        self.refresh_client_orders()
        self.refresh_client_stocks()

    def refresh_client_orders(self):
        """
        Refreshing the orders scroll area.
        First clearing the current orders on the scroll area and then update all the new orders.
        """
        for i in reversed(range(self.orders_portfolio_verticalLayout.count())):  # clear the orders scroll area
            self.orders_portfolio_verticalLayout.itemAt(i).widget().setParent(None)

        self.client.send("refresh_open_orders".encode())
        orders_number = int(self.client.recv(1024).decode())

        if not orders_number == 0:
            plot_params_boxes = [self.High_checkBox_portfolio, self.Low_checkBox_portfolio,
                                 self.Open_checkBox_portfolio, self.Close_checkBox_portfolio,
                                 self.AdjClose_checkBox_portfolio, self.Volume_checkBox_portfolio]

            for one_stock in range(orders_number):
                order_info = pickle.loads(self.client.recv(1024))
                new_widget = OrderWidget(self.orders_portfolio_Contents, self.orders_portfolio_verticalLayout,
                                          order_info, self.client, plot_params_boxes)
                new_widget.cancel_order_pushButton.clicked.connect(self.refresh_portfolio_tab)
                self.client.send("ACK".encode())

        else:
            new_widget = NoOrdersWidget(self.orders_portfolio_Contents, self.orders_portfolio_verticalLayout)

        self.orders_scrollArea_portfolio.setWidget(self.orders_portfolio_Contents)

    def refresh_client_stocks(self):
        """
        Refreshing the client's owned stocks scroll area.
        First clearing the current stocks on the scroll area and then update all the new client's owned stocks.
        """
        for i in reversed(range(self.stocks_portfolio_verticalLayout.count())):  # clear the orders scroll area
            self.stocks_portfolio_verticalLayout.itemAt(i).widget().setParent(None)

        self.client.send("refresh_own_stocks".encode())
        stocks_number = int(self.client.recv(1024).decode())

        if not stocks_number == 0:
            stocks_number = int(stocks_number)
            plot_params_boxes = [self.High_checkBox_portfolio, self.Low_checkBox_portfolio,
                                 self.Open_checkBox_portfolio, self.Close_checkBox_portfolio,
                                 self.AdjClose_checkBox_portfolio, self.Volume_checkBox_portfolio]

            for one_stock in range(stocks_number):
                stock_info = pickle.loads(self.client.recv(1024))
                new_widget = OwnedStockWidget(self.stocks_portfolio_Contents, self.stocks_portfolio_verticalLayout,
                                     stock_info, self.client, plot_params_boxes)
                self.client.send("ACK".encode())

        else:
            new_widget = EmptyOwnedStockWidget(self.stocks_portfolio_Contents, self.stocks_portfolio_verticalLayout)

        self.stocks_scrollArea_portfolio.setWidget(self.stocks_portfolio_Contents)

    def add_money_func(self):
        """
        Adding money to the client balance.
        """
        add_value = self.add_money_spinbox.value()

        if add_value != 0:
            self.client.send("add_money".encode())
            self.client.send(str(self.add_money_spinbox.value()).encode())
            # Ack
            self.client.recv(1024)
            self.refresh_balance_tab()

    def ask_for_stock_excel(self,ticker_name, start_date, end_date):
        """
        Ask for excel file with the stock history.
        This is the first step of creating a matplotlib graph.
        """
        parameters_list = ([self.High_checkBox_in_index_widget.isChecked(),
                            self.Low_checkBox_in_index_widget.isChecked(),
                            self.Open_checkBox_in_index_widget.isChecked(),
                            self.Close_checkBox_in_index_widget.isChecked(),
                            self.AdjClose_checkBox_in_index_widget.isChecked(),
                            self.Volume_checkBox_in_index_widget.isChecked()])

        ask_for_stock_excel(self.client, ticker_name, start_date, end_date, parameters_list)

    def getting_stocks_info_to_market_func(self,search_parameters):
        """
        Getting the stocks information to the scroll area in the
        "stock market" tab after searching for those.
        """
        self.client.send(pickle.dumps(search_parameters))
        stocks_list_length = int((self.client.recv(1024)).decode())
        self.client.send("ACK".encode())

        plot_params_boxes = [self.High_checkBox_market, self.Low_checkBox_market,
                             self.Open_checkBox_market,  self.Close_checkBox_market,
                             self.AdjClose_checkBox_market, self.Volume_checkBox_market]

        if not stocks_list_length == 0:
            for one_stock in range(stocks_list_length):
                stock_info = pickle.loads(self.client.recv(1024 * 4))
                new_widget = StockForBuyWidget(self.stocks_market_Contents, self.stocks_market_verticalLayout,
                                                  stock_info, self.client, plot_params_boxes)
                self.client.send("ACK".encode())

        else:
            new_widget = EmptyStockWidget(self.stocks_market_Contents, self.stocks_market_verticalLayout)

        self.stocks_market_scrollArea.setWidget(self.stocks_market_Contents)

    def specific_search_in_market_func(self):
        """
        Searching specific stocks by the client parameters that were
        chosen in "specific search" tab in the "stock market" tab.
        """
        for i in reversed(range(self.stocks_market_verticalLayout.count())):            # clearing the widget
            self.stocks_market_verticalLayout.itemAt(i).widget().setParent(None)

        # searching parameters - index, industry, market cap , change percentage , price
        search_parameters = [str(self.index_comboBox_spec_market.currentText())]

        if self.industry_checkBox_spec_market.isChecked():
            search_parameters.append(str(self.industry_combobox_spec_market.currentText()))

        else:
            search_parameters.append("NULL")

        if self.cap_checkBox_spec_market.isChecked():
            cap = "NULL"
            if self.small_cap_button_spec_market.isChecked():
                cap = "small_cap"
            elif self.aveg_cap_button_spec_market.isChecked():
                cap = "aveg_cap"
            elif self.big_cap_button_spec_market.isChecked():
                cap = "big_cap"
            search_parameters.append(cap)

        else:
            search_parameters.append("NULL")

        if self.change_checkBox_spec_market.isChecked():
            search_parameters.append(self.change_dial_spec_market.value())

        else:
            search_parameters.append("NULL")

        if self.price_checkBox_spec_market.isChecked():
            search_parameters.append(self.price_slider_spectab_market.value())

        else:
            search_parameters.append("NULL")

        self.client.send("specific_search_in_market".encode())
        self.getting_stocks_info_to_market_func(search_parameters)

    def free_search_in_market_func(self):
        """
        Free search for  stocks by the name that was
        chosen in "free search" tab in the "stock market" tab.
        """
        for i in reversed(range(self.stocks_market_verticalLayout.count())):            # clearing the widget
            self.stocks_market_verticalLayout.itemAt(i).widget().setParent(None)

        search_parameters = []

        if self.typed_button_free_market.isChecked():
            search_parameters = ["TYPED",self.typed_lineEdit_free_market.text()]

        else:
            search_parameters = ["LIST", self.stocks_comboBox_free_market.currentText()]

        self.client.send("free_search_in_market".encode())
        self.getting_stocks_info_to_market_func(search_parameters)

        self.stocks_market_scrollArea.setWidget(self.stocks_market_Contents)

    def send_request(self):
        """
        Sending to the server the request that was chosen by the user un "reports" tab.
        """

        if self.your_details_radioButton.isChecked():
            self.client.send("create_request".encode())
            self.client.recv(1024) # ACK
            self.client.send((self.your_details_comboBox.currentText()).encode())
            self.refresh_reports_tab()


        elif self.orders_exp_radioButton.isChecked():
            self.client.send("create_request".encode())
            self.client.recv(1024)  # ACK
            self.client.send((self.orders_exp_comboBox.currentText()).encode())
            self.refresh_reports_tab()


        elif self.stocks_info_radioButton.isChecked():
            self.client.send("create_request".encode())
            self.client.recv(1024)  # ACK
            self.client.send((self.stock_info_comboBox.currentText()).encode())
            self.refresh_reports_tab()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    client = Client(MainWindow)
    client.connect_to_server()
    MainWindow.show()
    sys.exit(app.exec_())
