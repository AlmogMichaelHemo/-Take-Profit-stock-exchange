from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
import pyqtgraph as pg
import datetime, pickle
from TPclient_plot import ask_for_stock_excel

# colors object
RED_RGB = QColor(247, 181, 186)
GREEN_RGB = QColor(198, 245, 201)
BLUE_RGB = QColor(183, 211, 247)
GREY_RGB = QColor(187, 188, 189)
BUY_ORDER_RGB = QColor(243, 202, 136)
SELL_ORDER_RGB = QColor(251, 250, 174)

# path to folder to save the excel files
PATH_EXCEL = "C:\\Users\\User\\Desktop\\TPclient_folder\\"

# path to the folder that all the backgrounds in it
PATH_SIMPLE = "C:\\Users\\User\\Desktop\\פרוייקט בסייבר\\picturs\\"


class StockForBuyWidget:
    """
    Class that create widget for the stocks scroll area in "stock market" tab.
    """
    def __init__(self, scrollaera_content, vertical, stock_info, socket, plot_params_boxes): # stock_info = ticker, name, price, change, index, market cap
        """
        constructor of stock widget in market tab.
        """
        self.socket = socket

        self.scrollaera_content = scrollaera_content
        self.vertical = vertical
        self.stock_widget = QtWidgets.QWidget(self.scrollaera_content)

        print(stock_info)
        print("\n")

        self.ticker = stock_info[0]
        self.name = "\n".join((stock_info[1]).split(" "))
        self.price = stock_info[2]
        self.change = stock_info[3]
        self.index = stock_info[4]
        self.cap = stock_info[5]

        self.plot_params_boxes = plot_params_boxes

        self.create_widget()

    def create_widget(self):
        """
        Setting the widget and designing him with the stock info.
        """
        self.stock_widget.setObjectName("stock_widget")
        self.stock_widget.setMinimumHeight(100)
        self.stock_widget.setMaximumHeight(130)

        background_color = self.stock_widget.palette()

        if self.change > 0:
            background_color.setColor(self.stock_widget.backgroundRole(),GREEN_RGB)
        elif self.change < 0:
            background_color.setColor(self.stock_widget.backgroundRole(), RED_RGB)
        else:
            background_color.setColor(self.stock_widget.backgroundRole(), BLUE_RGB)

        self.stock_widget.setPalette(background_color)
        self.stock_widget.setAutoFillBackground(True)

        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)

        self.name_label_in_stocks_widget = QtWidgets.QLabel(self.stock_widget)
        self.name_label_in_stocks_widget.setGeometry(QtCore.QRect(5, 0, 150, 100))
        self.name_label_in_stocks_widget.setFont(font)
        self.name_label_in_stocks_widget.setObjectName("name_label_in_stocks_widget")
        self.name_label_in_stocks_widget.setText(self.name)
        self.stock_price = QtWidgets.QLCDNumber(self.stock_widget)
        self.stock_price.setGeometry(QtCore.QRect(175, 10, 101, 31))
        font.setPointSize(9)
        self.stock_price.setFont(font)
        self.stock_price.setObjectName("stock_price")
        self.stock_price.display(self.price)
        self.stock_change = QtWidgets.QLCDNumber(self.stock_widget)
        self.stock_change.setGeometry(QtCore.QRect(305, 10, 101, 31))
        self.stock_change.setFont(font)
        self.stock_change.setObjectName("stock_change")
        self.stock_change.display(self.change)
        self.week_plot_radioButton = QtWidgets.QRadioButton(self.stock_widget)
        self.week_plot_radioButton.setGeometry(QtCore.QRect(435, 10, 95, 20))
        font.setPointSize(7)
        self.week_plot_radioButton.setFont(font)
        self.week_plot_radioButton.setObjectName("week_plot_radioButton")
        self.week_plot_radioButton.setText("Week")
        self.month_plot_radioButton = QtWidgets.QRadioButton(self.stock_widget)
        self.month_plot_radioButton.setGeometry(QtCore.QRect(505, 10, 95, 20))
        self.month_plot_radioButton.setFont(font)
        self.month_plot_radioButton.setObjectName("month_plot_radioButton")
        self.month_plot_radioButton.setText("Month")
        self.year_plot_radioButton = QtWidgets.QRadioButton(self.stock_widget)
        self.year_plot_radioButton.setGeometry(QtCore.QRect(435, 30, 95, 20))
        self.year_plot_radioButton.setFont(font)
        self.year_plot_radioButton.setObjectName("year_plot_radioButton")
        self.year_plot_radioButton.setText("One Year")
        self.five_years_plot_radioButton = QtWidgets.QRadioButton(self.stock_widget)
        self.five_years_plot_radioButton.setGeometry(QtCore.QRect(505, 30, 95, 20))
        self.five_years_plot_radioButton.setFont(font)
        self.five_years_plot_radioButton.setObjectName("five_years_plot_radioButton")
        self.five_years_plot_radioButton.setText("5 Years")
        self.more_info_Button = QtWidgets.QPushButton(self.stock_widget)
        self.more_info_Button.setGeometry(QtCore.QRect(175, 55, 231, 28))
        font.setPointSize(9)
        self.more_info_Button.setFont(font)
        self.more_info_Button.setObjectName("more_info_Button")
        self.more_info_Button.setText("More Info")
        self.more_info_Button.clicked.connect(lambda: self.ask_for_more_stock_info_func())
        self.plot_Button = QtWidgets.QPushButton(self.stock_widget)
        self.plot_Button.setGeometry(QtCore.QRect(455, 55, 93, 28))
        self.plot_Button.setFont(font)
        self.plot_Button.setObjectName("plot_Button")
        self.plot_Button.setText("Plot")
        self.plot_Button.clicked.connect(lambda: self.plot_stock_func())
        self.buy_orders_comboBox = QtWidgets.QComboBox(self.stock_widget)
        self.buy_orders_comboBox.setGeometry(QtCore.QRect(580, 30, 101, 22))
        self.buy_orders_comboBox.setObjectName("buy_orders_comboBox")
        self.buy_orders_comboBox.setFont(font)
        self.buy_orders_comboBox.addItems([ "MARKET","LIMIT", "STOP LOSS", "STOP LIMIT", "AON", "IOC", "BUY ABOVE", "FOK"])
        self.choose_label = QtWidgets.QLabel(self.stock_widget)
        self.choose_label.setGeometry(QtCore.QRect(590, 10, 91, 16))
        font.setPointSize(7)
        self.choose_label.setFont(font)
        self.choose_label.setObjectName("choose_label")
        self.choose_label.setText("Choose buy order")
        self.buy_Button = QtWidgets.QPushButton(self.stock_widget)
        self.buy_Button.setGeometry(QtCore.QRect(580, 55, 101, 28))
        font.setPointSize(9)
        self.buy_Button.setFont(font)
        self.buy_Button.setObjectName("buy_Button")
        self.buy_Button.setText("Buy")
        self.buy_Button.clicked.connect(lambda: self.buy_stock_func(self.buy_orders_comboBox.currentText()))

        self.vertical.addWidget(self.stock_widget)

    def ask_for_more_stock_info_func(self):
        """
        Asking from the server for more info about the stock and creating a "more info" window.
        """
        self.socket.send("more_stock_info".encode())
        self.socket.send(pickle.dumps([self.index, self.ticker]))
        more_info_list = pickle.loads(self.socket.recv(4000))
        self.more_info_widget = InformationWidget(more_info_list)
        self.more_info_widget.show()

    def plot_stock_func(self):
        """
        First step for open a matplotlib graph for the stock history with the time period
        and the parameters that were chosen by the user.
        """
        end_date = datetime.date.today()

        if self.week_plot_radioButton.isChecked():
            start_date = end_date - datetime.timedelta(days=7)

        elif self.month_plot_radioButton.isChecked():
            start_date = end_date - datetime.timedelta(days=30)

        elif self.year_plot_radioButton.isChecked():
            start_date = end_date - datetime.timedelta(days=365)

        elif self.five_years_plot_radioButton.isChecked():
            start_date = end_date - datetime.timedelta(days=365*5)

        else: start_date = end_date - datetime.timedelta(days=5)


        plot_parameters_list = ([self.plot_params_boxes[0].isChecked(),
                                self.plot_params_boxes[1].isChecked(),
                                self.plot_params_boxes[2].isChecked(),
                                self.plot_params_boxes[3].isChecked(),
                                self.plot_params_boxes[4].isChecked(),
                                 self.plot_params_boxes[5].isChecked()])

        ask_for_stock_excel(self.socket, self.ticker, start_date, end_date, plot_parameters_list)

    def buy_stock_func(self, order_type):
        """
        Creating order window for the stock with the order type that was chosen in the combo box.
        """
        self.order_widget = OrderWindow(None, order_type, self.name, self.ticker,
                                         self.price, self.index, self.socket, 550)
        self.order_widget.show()


class EmptyStockWidget:
    """
    Creating widget that tells that their is no stocks that found after the searching in "stock market" tab.
    """
    def __init__(self, scrollaera_content, vertical):
        """
        Constructor of empty stock widget in market tab
        """
        self.scrollaera_content = scrollaera_content
        self.vertical = vertical
        self.widget = QtWidgets.QWidget(self.scrollaera_content)
        self.create_widget()

    def create_widget(self):
        """
        Create the widget and adding the background
        """
        self.widget.setObjectName("stock_widget")
        self.widget.setMinimumHeight(130)
        self.widget.setMaximumHeight(130)

        background = QtWidgets.QLabel(self.widget)
        background.setGeometry(QtCore.QRect(0, 0, 700, 130))
        background.setPixmap(QtGui.QPixmap(PATH_SIMPLE + "empty_stock_widget_background.png"))
        background.setObjectName("background")

        self.vertical.addWidget(self.widget)


class OwnedStockWidget:
    """
    Creating widget for owned stock to "portfolio" tab
    """
    def __init__(self, scrollaera_content, vertical, stock_info, socket, plot_params_boxes):
        # stock_info = ticker, name, price, change, index, market cap
        """
        Constructor of owned stock widget in market tab
        """
        self.socket = socket

        self.scrollaera_content = scrollaera_content
        self.vertical = vertical
        self.stock_widget = QtWidgets.QWidget(self.scrollaera_content)

        self.stock_number = stock_info[0]
        self.ticker = stock_info[1]
        self.buy_date =  stock_info[2]
        self.buy_price =  stock_info[3]
        self.stock_amount = stock_info[4]
        self.sell_order = stock_info[5]

        self.name = "\n".join((stock_info[6]).split(" "))
        self.price = stock_info[7]
        self.change = stock_info[8]
        self.index = stock_info[9]

        self.plot_params_boxes = plot_params_boxes

        self.create_widget()

    def create_widget(self):
        """
        Create the widget and designing him with the stock info
        """
        self.stock_widget.setObjectName("stock_widget")
        self.stock_widget.setMinimumHeight(100)
        self.stock_widget.setMaximumHeight(100)

        background_color = self.stock_widget.palette()

        if self.change > 0:
            background_color.setColor(self.stock_widget.backgroundRole(),GREEN_RGB)
        elif self.change < 0:
            background_color.setColor(self.stock_widget.backgroundRole(), RED_RGB)
        else:
            background_color.setColor(self.stock_widget.backgroundRole(), BLUE_RGB)

        self.stock_widget.setPalette(background_color)
        self.stock_widget.setAutoFillBackground(True)

        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)

        self.name_label_in_portfolio = QtWidgets.QLabel(self.stock_widget)
        self.name_label_in_portfolio.setGeometry(QtCore.QRect(10, 0, 111, 81))
        self.name_label_in_portfolio.setFont(font)
        self.name_label_in_portfolio.setObjectName("name_label_in_stocks_widget")
        self.name_label_in_portfolio.setText(self.name)

        self.stock_price = QtWidgets.QLCDNumber(self.stock_widget)
        self.stock_price.setGeometry(QtCore.QRect(120, 10, 101, 31))
        font.setPointSize(9)
        self.stock_price.setFont(font)
        self.stock_price.setObjectName("stock_price")
        self.stock_price.display(self.price)

        self.stock_change = QtWidgets.QLCDNumber(self.stock_widget)
        self.stock_change.setGeometry(QtCore.QRect(230, 10, 101, 31))
        self.stock_change.setFont(font)
        self.stock_change.setObjectName("stock_change")
        self.stock_change.display(self.change)

        self.more_info_Button = QtWidgets.QPushButton(self.stock_widget)
        self.more_info_Button.setGeometry(QtCore.QRect(120, 60, 211, 28))
        font.setPointSize(9)
        self.more_info_Button.setFont(font)
        self.more_info_Button.setObjectName("more_info_Button")
        self.more_info_Button.setText("More Info")
        self.more_info_Button.clicked.connect(lambda: self.ask_for_more_stock_info_func())

        self.plot_label_portfolio = QtWidgets.QLabel(self.stock_widget)
        self.plot_label_portfolio.setGeometry(QtCore.QRect(460, 10, 61, 16))
        self.plot_label_portfolio.setFont(font)
        self.plot_label_portfolio.setObjectName("plot_label_portfolio")
        self.plot_label_portfolio.setText("Plot Period")

        self.plot_period_comboBox_portfolio = QtWidgets.QComboBox(self.stock_widget)
        self.plot_period_comboBox_portfolio.setGeometry(QtCore.QRect(460, 30, 61, 21))
        self.plot_period_comboBox_portfolio.setObjectName("plot_period_comboBox_portfolio")
        self.plot_period_comboBox_portfolio.setFont(font)
        self.plot_period_comboBox_portfolio.addItems(['week', 'month', 'year', '5 years'])

        self.plot_Button = QtWidgets.QPushButton(self.stock_widget)
        self.plot_Button.setGeometry(QtCore.QRect(460, 60, 61, 21))
        self.plot_Button.setFont(font)
        self.plot_Button.setObjectName("plot_Button")
        self.plot_Button.setText("Plot")
        self.plot_Button.clicked.connect(lambda: self.plot_stock_func())

        if self.sell_order:
            self.order_label_portfolio = QtWidgets.QLabel(self.stock_widget)
            self.order_label_portfolio.setGeometry(QtCore.QRect(530, 20, 100, 55))
            self.order_label_portfolio.setObjectName("order_label_portfolio")
            font.setBold(True)
            self.order_label_portfolio.setFont(font)
            self.order_label_portfolio.setText("Waiting for\n" + self.sell_order + "\norder to be\nexecuted")
            font.setBold(False)

        else:
            self.sell_label_portfolio = QtWidgets.QLabel(self.stock_widget)
            self.sell_label_portfolio.setGeometry(QtCore.QRect(540, 10, 91, 16))
            self.sell_label_portfolio.setObjectName("sell_label_portfolio")
            self.sell_label_portfolio.setFont(font)
            self.sell_label_portfolio.setText("Sell Orders")

            self.sell_orders_comboBox = QtWidgets.QComboBox(self.stock_widget)
            self.sell_orders_comboBox.setGeometry(QtCore.QRect(530, 30, 81, 22))
            self.sell_orders_comboBox.setObjectName("sell_orders_comboBox")
            self.sell_orders_comboBox.setFont(font)
            self.sell_orders_comboBox.addItems(
                ["MARKET", "LIMIT", "T/P", "STOP LOSS", "STOP LIMIT", "AON", "IOC", "FOK"])

            self.sell_Button = QtWidgets.QPushButton(self.stock_widget)
            self.sell_Button.setGeometry(QtCore.QRect(530, 60, 81, 21))
            self.sell_Button.setFont(font)
            self.sell_Button.setObjectName("sell_Button")
            self.sell_Button.setText("Sell")
            self.sell_Button.clicked.connect(lambda: self.sell_stock_func(self.sell_orders_comboBox.currentText()))


        self.details_label_portfolio = QtWidgets.QLabel(self.stock_widget)
        self.details_label_portfolio.setGeometry(QtCore.QRect(350, 14, 110, 75))
        self.details_label_portfolio.setObjectName("details_label_portfolio")
        self.details_label_portfolio.setFont(font)
        self.details_label_portfolio.setText("Buy date:\n" + self.buy_date + "\n" +
                                             "Buy price: " + str(self.buy_price) + "\n" +
                                             "Amount: " + str(self.stock_amount) + "\n" +
                                             "Value: " +  str(self.stock_amount * self.price) + "\n")

        self.vertical.addWidget(self.stock_widget)

    def ask_for_more_stock_info_func(self):
        """
        Asking from the server for more info about the stock and creating a "more info" window.
        """
        self.socket.send("more_stock_info".encode())
        self.socket.send(pickle.dumps([self.index, self.ticker]))
        more_info_list = pickle.loads(self.socket.recv(4000))
        self.more_info_widget = InformationWidget(more_info_list)
        self.more_info_widget.show()

    def plot_stock_func(self):
        """
        First step for open a matplotlib graph for the stock history with the time period
        and the parameters that were chosen by the user.
        """
        end_date = datetime.date.today()

        if self.plot_period_comboBox_portfolio.currentText() == "week":
            start_date = end_date - datetime.timedelta(days=7)

        elif self.plot_period_comboBox_portfolio.currentText() == "month":
            start_date = end_date - datetime.timedelta(days=30)

        elif self.plot_period_comboBox_portfolio.currentText() == "year":
            start_date = end_date - datetime.timedelta(days=365)

        elif self.plot_period_comboBox_portfolio.currentText() == "5 years":
            start_date = end_date - datetime.timedelta(days=365*5)

        else: start_date = end_date - datetime.timedelta(days=5)


        plot_parameters_list = ([self.plot_params_boxes[0].isChecked(),
                                self.plot_params_boxes[1].isChecked(),
                                self.plot_params_boxes[2].isChecked(),
                                self.plot_params_boxes[3].isChecked(),
                                self.plot_params_boxes[4].isChecked(),
                                self.plot_params_boxes[5].isChecked()])

        ask_for_stock_excel(self.socket, self.ticker, start_date, end_date, plot_parameters_list)

    def sell_stock_func(self, order_type):
        """
        Create an order window with the order type that were chosen by the user
        """
        self.order_widget = OrderWindow(self.stock_number, order_type, self.name, self.ticker,
                                         self.price, self.index, self.socket, self.stock_amount)
        self.order_widget.show()


class EmptyOwnedStockWidget:
    """
    """
    def __init__(self, scrollaera_content, vertical):
        """
        Constructor of empty owned stock widget in portfolio tab
        """
        self.scrollaera_content = scrollaera_content
        self.vertical = vertical
        self.widget = QtWidgets.QWidget(self.scrollaera_content)
        self.create_widget()

    def create_widget(self):
        """
        Create the widget and adding the background
        """
        self.widget.setObjectName("stock_widget")
        self.widget.setMinimumHeight(100)
        self.widget.setMaximumHeight(100)

        background = QtWidgets.QLabel(self.widget)
        background.setGeometry(QtCore.QRect(0, 0, 700, 100))
        background.setPixmap(QtGui.QPixmap(PATH_SIMPLE + "no_stocks_portfolio.png"))
        background.setObjectName("background")

        self.vertical.addWidget(self.widget)


class InformationWidget(QWidget):
    """
    Class that create an information window
    """
    def __init__(self, more_info_list):
        """
        Design information window for a specific stock
        """
        super().__init__()

        layout = QVBoxLayout()

        self.ticker = more_info_list[0]
        self.name = more_info_list[1]
        self.price = more_info_list[2]
        self.change = more_info_list[3]
        self.description = more_info_list[4]
        self.industry = "\n".join((more_info_list[5]).split(", "))
        self.high = more_info_list[6]
        self.low = more_info_list[7]
        self.open = more_info_list[8]
        self.close = more_info_list[9]
        self.beta = more_info_list[10]
        self.PE = more_info_list[11]
        self.employees = more_info_list[12]
        self.exchange = more_info_list[13]
        self.index = more_info_list[14]

        self.resize(615, 610)

        background = QtWidgets.QLabel(self)
        background.setGeometry(QtCore.QRect(-20, -10, 651, 631))
        background.setPixmap(QtGui.QPixmap(PATH_SIMPLE + "more_information_window_background.png"))
        background.setObjectName("background")

        font = QtGui.QFont()
        font.setFamily("Castellar")
        font.setPointSize(17)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)

        article_in_information = QtWidgets.QLabel(self)
        article_in_information.setGeometry(QtCore.QRect(170, 50, 441, 41))
        article_in_information.setFont(font)
        article_in_information.setObjectName("article_in_information")
        article_in_information.setText(self.name)

        ticker_label_in_information = QtWidgets.QLabel(self)
        ticker_label_in_information.setGeometry(QtCore.QRect(50, 160, 61, 16))
        font.setPointSize(8)
        font.setUnderline(False)
        ticker_label_in_information.setFont(font)
        ticker_label_in_information.setObjectName("ticker_label_in_information")
        ticker_label_in_information.setText("ticker")

        index_label_in_information = QtWidgets.QLabel(self)
        index_label_in_information.setGeometry(QtCore.QRect(140, 160, 51, 16))
        index_label_in_information.setFont(font)
        index_label_in_information.setObjectName("index_label_in_information")
        index_label_in_information.setText("index")

        price_label_in_information = QtWidgets.QLabel(self)
        price_label_in_information.setGeometry(QtCore.QRect(80, 240, 47, 13))
        price_label_in_information.setFont(font)
        price_label_in_information.setObjectName("price_label_in_information")
        price_label_in_information.setText("price")

        industry_label_in_information = QtWidgets.QLabel(self)
        industry_label_in_information.setGeometry(QtCore.QRect(240, 160, 71, 16))
        industry_label_in_information.setFont(font)
        industry_label_in_information.setObjectName("industry_label_in_information")
        industry_label_in_information.setText("industry")

        change_label_in_information = QtWidgets.QLabel(self)
        change_label_in_information.setGeometry(QtCore.QRect(200, 240, 71, 16))
        change_label_in_information.setFont(font)
        change_label_in_information.setObjectName("change_label_in_information")
        change_label_in_information.setText("change")

        close_label_in_information = QtWidgets.QLabel(self)
        close_label_in_information.setGeometry(QtCore.QRect(210, 300, 47, 13))
        close_label_in_information.setFont(font)
        close_label_in_information.setObjectName("close_label_in_information")
        close_label_in_information.setText("close")

        open_label_in_information = QtWidgets.QLabel(self)
        open_label_in_information.setGeometry(QtCore.QRect(80, 300, 47, 13))
        open_label_in_information.setFont(font)
        open_label_in_information.setObjectName("open_label_in_information")
        open_label_in_information.setText("open")

        low_label_in_information = QtWidgets.QLabel(self)
        low_label_in_information.setGeometry(QtCore.QRect(480, 300, 31, 16))
        low_label_in_information.setFont(font)
        low_label_in_information.setObjectName("low_label_in_information")
        low_label_in_information.setText("low")

        high_label_in_information = QtWidgets.QLabel(self)
        high_label_in_information.setGeometry(QtCore.QRect(350, 300, 47, 13))
        high_label_in_information.setFont(font)
        high_label_in_information.setObjectName("high_label_in_information")
        high_label_in_information.setText("high")

        description_label_in_information = QtWidgets.QLabel(self)
        description_label_in_information.setGeometry(QtCore.QRect(45, 360, 111, 16))
        description_label_in_information.setFont(font)
        description_label_in_information.setObjectName("description_label_in_information")
        description_label_in_information.setText("description")

        beta_label_in_information = QtWidgets.QLabel(self)
        beta_label_in_information.setGeometry(QtCore.QRect(350, 240, 47, 13))
        beta_label_in_information.setFont(font)
        beta_label_in_information.setObjectName("beta_label_in_information")
        beta_label_in_information.setText("beta")

        pe_label_in_information = QtWidgets.QLabel(self)
        pe_label_in_information.setGeometry(QtCore.QRect(480, 240, 47, 13))
        pe_label_in_information.setFont(font)
        pe_label_in_information.setObjectName("pe_label_in_information")
        pe_label_in_information.setText("P/E")

        employees_label_in_information = QtWidgets.QLabel(self)
        employees_label_in_information.setGeometry(QtCore.QRect(500, 160, 91, 16))
        employees_label_in_information.setFont(font)
        employees_label_in_information.setObjectName("employees_label_in_information")
        employees_label_in_information.setText("employees")

        exchange_label_in_information = QtWidgets.QLabel(self)
        exchange_label_in_information.setGeometry(QtCore.QRect(350, 160, 81, 16))
        exchange_label_in_information.setFont(font)
        exchange_label_in_information.setObjectName("exchange_label_in_information")
        exchange_label_in_information.setText("exchange")

        ticker_value = QtWidgets.QLabel(self)
        ticker_value.setGeometry(QtCore.QRect(50, 180, 121, 41))
        ticker_value.setObjectName("ticker_value")
        ticker_value.setText(self.ticker)

        index_value = QtWidgets.QLabel(self)
        index_value.setGeometry(QtCore.QRect(140, 180, 151, 41))
        index_value.setObjectName("index_value")
        index_value.setText(self.index)

        industry_value = QtWidgets.QLabel(self)
        industry_value.setGeometry(QtCore.QRect(240, 180, 130, 41))
        industry_value.setObjectName("industry_value")
        industry_value.setText(self.industry)

        num_font = QtGui.QFont()
        num_font.setBold(True)
        num_font.setPointSize(8)
        num_font.setWeight(70)

        price_value = QtWidgets.QLCDNumber(self)
        price_value.setGeometry(QtCore.QRect(60, 260, 81, 23))
        price_value.setObjectName("price_value")
        price_value.setFont(num_font)
        price_value.display(self.price)

        change_value = QtWidgets.QLCDNumber(self)
        change_value.setGeometry(QtCore.QRect(190, 260, 81, 23))
        change_value.setObjectName("change_value")
        change_value.setFont(num_font)
        change_value.display(self.change)


        low_value = QtWidgets.QLCDNumber(self)
        low_value.setGeometry(QtCore.QRect(460, 320, 81, 23))
        low_value.setObjectName("low_value")
        low_value.setFont(num_font)
        low_value.display(self.low)

        high_value = QtWidgets.QLCDNumber(self)
        high_value.setGeometry(QtCore.QRect(330, 320, 81, 23))
        high_value.setFont(font)
        high_value.setObjectName("high_value")
        high_value.setFont(num_font)
        high_value.display(self.high)

        close_value = QtWidgets.QLCDNumber(self)
        close_value.setGeometry(QtCore.QRect(190, 320, 81, 23))
        close_value.setObjectName("close_value")
        close_value.setFont(num_font)
        close_value.display(self.close)

        open_value = QtWidgets.QLCDNumber(self)
        open_value.setGeometry(QtCore.QRect(60, 320, 81, 23))
        open_value.setObjectName("open_value")
        open_value.setFont(num_font)
        open_value.display(self.open)

        employees_value = QtWidgets.QLabel(self)
        employees_value.setGeometry(QtCore.QRect(500, 180, 101, 41))
        employees_value.setObjectName("employees_value")
        employees_value.setFont(num_font)
        employees_value.setText(str(self.employees))

        exchange_value = QtWidgets.QLabel(self)
        exchange_value.setGeometry(QtCore.QRect(350, 180, 121, 41))
        exchange_value.setObjectName("exchange_value")
        exchange_value.setText(self.exchange)

        PE_value = QtWidgets.QLCDNumber(self)
        PE_value.setGeometry(QtCore.QRect(460, 260, 81, 23))
        PE_value.setObjectName("PE_value")
        PE_value.display(self.PE)

        beta_value = QtWidgets.QLCDNumber(self)
        beta_value.setGeometry(QtCore.QRect(330, 260, 81, 23))
        beta_value.setObjectName("beta")
        beta_value.display(self.beta)

        description_value = QtWidgets.QLabel(self)
        description_value.setGeometry(QtCore.QRect(45, 380, 551, 250))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setItalic(True)
        description_value.setFont(font)
        description_value.setObjectName("description_value")
        description_value.setText(self.description)

        self.setLayout(layout)


class OrderWindow(QWidget):
    """
    Class that create an order window
    """
    def __init__(self, stock_number, order, stock_name, ticker, price, index, socket, amount):
        """
        Creating the window and fit it to the type of order that was asked by the user
        """
        super().__init__()

        self.layout = QVBoxLayout()
        self.stock = stock_name
        self.ticker = ticker
        self.price = price
        self.index = index
        self.socket = socket

        self.resize(328, 430)
        self.background_label = QtWidgets.QLabel(self)
        self.background_label.setGeometry(QtCore.QRect(0, 1, 331, 421))
        self.background_label.setPixmap(QtGui.QPixmap(PATH_SIMPLE + "order_window_background.png"))
        self.background_label.setObjectName("background_label")

        self.font = QtGui.QFont()
        self.font.setFamily("Castellar")
        self.font.setPointSize(17)
        self.font.setBold(True)
        self.font.setUnderline(True)
        self.font.setWeight(75)

        self.order_type_label = QtWidgets.QLabel(self)
        self.order_type_label.setGeometry(QtCore.QRect(140, 33, 141, 80))
        self.order_type_label.setObjectName("order_type_label")
        self.order_type_label.setFont(self.font)

        self.font.setUnderline(False)
        self.create_order_Button = QtWidgets.QPushButton(self)
        self.create_order_Button.setGeometry(QtCore.QRect(20, 353, 291, 51))
        self.create_order_Button.setObjectName("create_order_Button")
        self.create_order_Button.setText("create order")
        self.create_order_Button.setFont(self.font)

        self.font.setPointSize(8)
        self.stock_name_label = QtWidgets.QLabel(self)
        self.stock_name_label.setGeometry(QtCore.QRect(30, 191, 51, 21))
        self.stock_name_label.setObjectName("stock_name_label")
        self.stock_name_label.setText("stock:")
        self.stock_name_label.setFont(self.font)

        self.choose_label = QtWidgets.QLabel(self)
        self.choose_label.setGeometry(QtCore.QRect(30, 250, 271, 41))
        self.choose_label.setObjectName("choose_label")
        self.choose_label.setFont(self.font)

        self.price_label = QtWidgets.QLabel(self)
        self.price_label.setGeometry(QtCore.QRect(30, 221, 47, 21))
        self.price_label.setObjectName("price_label")
        self.price_label.setText("price:")
        self.price_label.setFont(self.font)

        self.num_font = QtGui.QFont()
        self.num_font.setBold(True)
        self.num_font.setPointSize(8)
        self.num_font.setWeight(70)
        self.font.setBold(False)

        self.stock_name = QtWidgets.QLabel(self)
        self.stock_name.setGeometry(QtCore.QRect(90, 191, 201, 25))
        self.stock_name.setObjectName("stock_name")
        self.stock_name.setText(self.stock)
        self.stock_name.setFont(self.font)

        self.price_lcdNumber = QtWidgets.QLCDNumber(self)
        self.price_lcdNumber.setGeometry(QtCore.QRect(90, 221, 131, 21))
        self.price_lcdNumber.setObjectName("price_lcdNumber")
        self.price_lcdNumber.display(self.price)
        self.price_lcdNumber.setFont(self.num_font)

        self.order_explanation = QtWidgets.QLabel(self)
        self.order_explanation.setGeometry(QtCore.QRect(20, 115, 290, 51))
        self.order_explanation.setObjectName("order_explanation")
        self.order_explanation.setFont(self.font)

        self.stocks_number_spinBox = QtWidgets.QSpinBox(self)
        self.stocks_number_spinBox.setGeometry(QtCore.QRect(110, 290, 101, 21))
        self.stocks_number_spinBox.setMinimum(1)
        self.stocks_number_spinBox.setMaximum(amount)
        self.stocks_number_spinBox.setObjectName("stocks_number_spinBox")
        self.stocks_number_spinBox.setFont(self.num_font)

        if not stock_number:
            self.choose_label.setText("choose how many stocks\nyou want to buy:")

        elif stock_number:
            self.choose_label.setText("choose how many stocks\nyou want to sell:")

        if order == "MARKET":
            self.create_market_order(stock_number)
        elif order == "LIMIT":
            self.create_limit_order(stock_number)
        elif order == "STOP LOSS":
            self.create_stop_loss_order(stock_number)
        elif order == "STOP LIMIT":
            self.create_stop_limit_order(stock_number)
        elif order == "AON":
            self.create_aon_order(stock_number)
        elif order == "IOC":
            self.create_ioc_order(stock_number)
        elif order == "BUY ABOVE":
            self.create_buy_above_order()
        elif order == "FOK":
            self.create_fok_order(stock_number)
        elif order == "T/P":
            self.create_take_profit_order(stock_number)

    def create_market_order(self, stock_number):
        """
       Creating an buy or sell "market" order, the simplest order
        """
        self.order_type_label.setText("MARKET\nORDER")
        self.order_explanation.setText("A market order is an order to buy"
                                       "\nor sell a stock at the market's"
                                       "\ncurrent best available price")

        if not stock_number:
            self.create_order_Button.clicked.connect((lambda: self.create_buy_order_function("BUY-MARKET")))
        else:
            self.create_order_Button.clicked.connect((lambda: self.create_sell_order_function("SELL-MARKET", stock_number)))

        self.setLayout(self.layout)

    def create_limit_order(self, stock_number):
        """
       Creating an buy or sell "limit" order, this order limit the buy price
        """
        self.order_type_label.setText("LIMIT\nORDER")

        self.limit_label = QtWidgets.QLabel(self)
        self.limit_label.setGeometry(QtCore.QRect(30, 320, 101, 21))
        self.limit_label.setObjectName("limit_label")
        self.font.setBold(True)
        self.limit_label.setFont(self.font)

        self.max_limit_spinBox = QtWidgets.QSpinBox(self)
        self.max_limit_spinBox.setGeometry(QtCore.QRect(135, 320, 101, 21))
        self.max_limit_spinBox.setObjectName("max_limit_spinBox")
        self.max_limit_spinBox.setFont(self.num_font)

        self.order_explanation.setText("A limit order is an order to"
                                       "\nbuy or sell a stock at a "
                                       "\nspecific price or better")

        if not stock_number:
            self.limit_label.setText("max limit :")
            self.max_limit_spinBox.setMinimum(0)
            self.max_limit_spinBox.setMaximum(self.price)
            self.create_order_Button.clicked.connect((lambda: self.create_buy_order_function("BUY-LIMIT")))
        else:
            self.limit_label.setText("min limit :")
            self.max_limit_spinBox.setMinimum(self.price)
            self.max_limit_spinBox.setMaximum(self.price + 550)
            self.create_order_Button.clicked.connect((lambda: self.create_sell_order_function("SELL-LIMIT", stock_number)))

        self.setLayout(self.layout)

    def create_stop_loss_order(self, stock_number):
        """
        Creating an buy or sell "stop loss" order, this order limit the loss of the possible transaction
        """
        self.font.setPointSize(10)
        self.font.setBold(True)
        self.order_type_label.setText("STOP\nLOSS\nORDER")
        self.font.setPointSize(8)
        self.font.setBold(False)
        self.order_explanation.setText(
            "A stop-loss order remains dormant"
            "\nuntil a certain minimum is passed "
            "\nprice and under it.")

        self.limit_label = QtWidgets.QLabel(self)
        self.limit_label.setGeometry(QtCore.QRect(30, 320, 101, 21))
        self.limit_label.setObjectName("limit_label")
        self.limit_label.setText("stop price :")
        self.font.setBold(True)
        self.limit_label.setFont(self.font)

        self.min_limit_spinBox = QtWidgets.QSpinBox(self)
        self.min_limit_spinBox.setGeometry(QtCore.QRect(130, 320, 101, 21))
        self.min_limit_spinBox.setObjectName("min_limit_spinBox")
        self.min_limit_spinBox.setFont(self.num_font)

        if not stock_number:
            self.min_limit_spinBox.setMinimum(1)
            self.min_limit_spinBox.setMaximum(self.price)
            self.create_order_Button.clicked.connect((lambda: self.create_buy_order_function("BUY-STOPLOSS")))
        else:
            self.min_limit_spinBox.setMinimum(1)
            self.min_limit_spinBox.setMaximum(self.price)
            self.create_order_Button.clicked.connect((lambda: self.create_sell_order_function("SELL-STOPLOSS", stock_number)))

        self.setLayout(self.layout)

    def create_stop_limit_order(self, stock_number):
        """
        Creating an buy or sell "stop limit" order, this order combines stop loss and limit orders
        """
        self.font.setPointSize(10)
        self.font.setBold(True)
        self.order_type_label.setText("STOP\nLIMIT\nORDER")
        self.font.setPointSize(8)
        self.font.setBold(False)
        self.order_explanation.setText(
            "stop-limit order is a conditional trade"
            "\nthat combine the features of a stop-loss"
            "\nwith those of a limit order"
            "\nto mitigate risk")

        self.choose_label.setGeometry(QtCore.QRect(30, 240, 271, 41))
        self.stocks_number_spinBox.setGeometry(QtCore.QRect(120, 275, 101, 21))

        self.stop_label = QtWidgets.QLabel(self)
        self.stop_label.setGeometry(QtCore.QRect(30, 305, 101, 21))
        self.stop_label.setObjectName("limit_label")
        self.stop_label.setText("stop price :")
        self.font.setBold(True)
        self.stop_label.setFont(self.font)

        self.stop_limit_spinBox = QtWidgets.QSpinBox(self)
        self.stop_limit_spinBox.setGeometry(QtCore.QRect(120, 305, 101, 21))
        self.stop_limit_spinBox.setObjectName("stop_limit_spinBox")
        self.stop_limit_spinBox.setFont(self.num_font)

        self.limit_label = QtWidgets.QLabel(self)
        self.limit_label.setGeometry(QtCore.QRect(30, 330, 101, 21))
        self.limit_label.setObjectName("limit_label")
        self.font.setBold(True)
        self.limit_label.setFont(self.font)

        self.max_limit_spinBox = QtWidgets.QSpinBox(self)
        self.max_limit_spinBox.setGeometry(QtCore.QRect(120, 330, 101, 21))
        self.max_limit_spinBox.setObjectName("max_limit_spinBox")
        self.max_limit_spinBox.setFont(self.num_font)

        if not stock_number:
            self.limit_label.setText("max limit :")
            self.stop_limit_spinBox.setMinimum(self.price)
            self.stop_limit_spinBox.setMaximum(self.price + 3500)
            self.max_limit_spinBox.setMinimum(self.stop_limit_spinBox.value())
            self.max_limit_spinBox.setMaximum(self.stop_limit_spinBox.value() + 3500)
            self.create_order_Button.clicked.connect((lambda: self.create_buy_order_function("BUY-STOPLIMIT")))
        else:
            self.limit_label.setText("limit :")
            self.max_limit_spinBox.setMinimum(1)
            self.max_limit_spinBox.setMaximum(self.price + 3500)
            self.stop_limit_spinBox.setMinimum(1)
            self.stop_limit_spinBox.setMaximum(self.price)
            self.create_order_Button.clicked.connect(
                (lambda: self.create_sell_order_function("SELL-STOPLIMIT", stock_number)))

        self.setLayout(self.layout)

    def create_aon_order(self, stock_number):
        """
        Creating an buy or sell "AON" (all-or-none) order, this order apply the transaction only if it can be a full one
        """
        self.order_type_label.setText("AON\nORDER")
        self.order_explanation.setText("An All-Or-None (AON) order is an order"
                                       "\nto buy a stock that must be executed"
                                       "\nin its entirety, or not"
                                       "\nexecuted at all. ")
        if not stock_number:
            self.create_order_Button.clicked.connect((lambda: self.create_buy_order_function("BUY-AON")))
        else:
            self.create_order_Button.clicked.connect((lambda: self.create_sell_order_function("SELL-AON", stock_number)))

        self.setLayout(self.layout)

    def create_ioc_order(self, stock_number):
        """
        Creating an buy or sell "IOC" (immediately-or-cancel) order, this order try to execute the order once,
        if the transaction wasn't made the order is canceled.
        """
        self.order_type_label.setText("IOC\nORDER")
        self.order_explanation.setText("An Immediate-Or-Cancel (IOC) order is an"
                                       "\norder to buy or sell a stock that must"
                                       "\nbe executed immediately. Any portion"
                                       "\nof an IOC order that cannot be filled "
                                       "\nimmediately will be cancelled.")
        if not stock_number:
            self.create_order_Button.clicked.connect((lambda: self.create_buy_order_function("BUY-IOC")))
        else:
            self.create_order_Button.clicked.connect((lambda: self.create_sell_order_function("SELL-IOC", stock_number)))

        self.setLayout(self.layout)

    def create_buy_above_order(self):
        """
        Creating an buy "Buy Above" order, this order buys the stock if the price is getting higher.
        The main reason for buying in more expensive price is that when the price rise up there
        is a chance it will raise more.
        """
        self.order_type_label.setText("BUY\nABOVE\nORDER")
        self.create_order_Button.clicked.connect((lambda: self.create_buy_order_function("BUY-BUYABOVE")))
        self.order_explanation.setText("A market order is an order to buy"
                                       "\na stock at the market's current"
                                       "\nbest available price")
        self.setLayout(self.layout)

        self.choose_label.setGeometry(QtCore.QRect(30, 240, 271, 41))
        self.stocks_number_spinBox.setGeometry(QtCore.QRect(120, 275, 101, 21))

        self.limit_label = QtWidgets.QLabel(self)
        self.limit_label.setGeometry(QtCore.QRect(30, 305, 101, 21))
        self.limit_label.setObjectName("limit_label")
        self.limit_label.setText("limit price :")
        self.font.setBold(True)
        self.limit_label.setFont(self.font)

        self.max_limit_label = QtWidgets.QLabel(self)
        self.max_limit_label.setGeometry(QtCore.QRect(30, 330, 101, 21))
        self.max_limit_label.setObjectName("max_limit_label")
        self.max_limit_label.setText("max limit :")
        self.max_limit_label.setFont(self.font)

        self.limit_spinBox = QtWidgets.QSpinBox(self)
        self.limit_spinBox.setGeometry(QtCore.QRect(120, 305, 101, 21))
        self.limit_spinBox.setMinimum(self.price)
        self.limit_spinBox.setMaximum(3500)
        self.limit_spinBox.setObjectName("limit_spinBox")
        self.limit_spinBox.setFont(self.num_font)

        self.max_limit_spinBox = QtWidgets.QSpinBox(self)
        self.max_limit_spinBox.setGeometry(QtCore.QRect(120, 330, 101, 21))
        self.max_limit_spinBox.setMinimum(self.limit_spinBox.value())
        self.max_limit_spinBox.setMaximum(3500)
        self.max_limit_spinBox.setObjectName("max_limit_spinBox")
        self.max_limit_spinBox.setFont(self.num_font)

        self.setLayout(self.layout)

    def create_fok_order(self, stock_number):
        """
        Creating an buy or sell "FOK" (fill-or-kill) order, this order has a time period for being alive
        """
        self.order_type_label.setText("FOK\nORDER")
        self.order_explanation.setText("Fill-or-Kill(FOK) order it mandates that"
                                       "\nthe entire order size be traded and in"
                                       "\na very short time period. If neither"
                                       "\nconditions met, the order is canceled")

        self.minutes_label = QtWidgets.QLabel(self)
        self.minutes_label.setGeometry(QtCore.QRect(30, 320, 101, 21))
        self.minutes_label.setObjectName("limit_label")
        self.minutes_label.setText("live minutes:")
        self.font.setBold(True)
        self.minutes_label.setFont(self.font)

        self.minutes_spinBox = QtWidgets.QSpinBox(self)
        self.minutes_spinBox.setGeometry(QtCore.QRect(135, 320, 101, 21))
        self.minutes_spinBox.setMinimum(1)
        self.minutes_spinBox.setMaximum(100)
        self.minutes_spinBox.setObjectName("minutes_spinBox")
        self.minutes_spinBox.setFont(self.num_font)

        if not stock_number:
            self.create_order_Button.clicked.connect((lambda: self.create_buy_order_function("BUY-FOK")))
        else:
            self.create_order_Button.clicked.connect((lambda: self.create_sell_order_function("SELL-FOK", stock_number)))


        self.setLayout(self.layout)

    def create_take_profit_order(self, stock_number):
        """
        Creating an sell "T/P" (Take Profit) order, this order can be executed
        only if the client made a profit out of it.
        """
        self.order_type_label.setText("Take\nProfit\nORDER")

        self.limit_label = QtWidgets.QLabel(self)
        self.limit_label.setGeometry(QtCore.QRect(30, 320, 101, 21))
        self.limit_label.setObjectName("limit_label")
        self.font.setBold(True)
        self.limit_label.setFont(self.font)

        self.min_limit_spinBox = QtWidgets.QSpinBox(self)
        self.min_limit_spinBox.setGeometry(QtCore.QRect(135, 320, 101, 21))
        self.min_limit_spinBox.setObjectName("min_limit_spinBox")
        self.min_limit_spinBox.setFont(self.num_font)
        self.min_limit_spinBox.setMinimum(self.price + 1)
        self.min_limit_spinBox.setMaximum(self.price + 550)

        self.order_explanation.setText("A \n order (T/P) is "
                                       "\na type of limit order that "
                                       "\nspecifies the exact price at"
                                       "\nwhich to close out an open "
                                       "\nposition for a profit.")

        self.limit_label.setText("min limit :")
        self.create_order_Button.clicked.connect(
            (lambda: self.create_sell_order_function("SELL-TAKEPROFIT", stock_number)))

        self.setLayout(self.layout)

    def create_buy_order_function(self, order_type):
        """
        Sending the buy order that was made by the user with the parameters every type of order needs
        """
        self.socket.send("create_order".encode())
        if order_type == "BUY-MARKET":
            # transaction_parameters = [order type, ticker, index, stocks number, "no_necessary_params" ]
            transaction_parameters = [order_type, self.ticker, self.index,  self.stocks_number_spinBox.value(), "no_necessary_params" ]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "BUY-LIMIT":
            # transaction_parameters = [order type, ticker, index, stocks number, maximum limit ]
            transaction_parameters = [order_type, self.ticker, self.index,  self.stocks_number_spinBox.value(),
                                      str(self.max_limit_spinBox.value())]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "BUY-STOPLOSS":
            # transaction_parameters = [order type, ticker, index, stocks number, minimum limit ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(),
                                      str(self.min_limit_spinBox.value())]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "BUY-STOPLIMIT":
            # transaction_parameters = [order type, ticker, index, stocks number, stop price "-" maximum limit ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(),
                                      str(self.stop_limit_spinBox.value()) + "-" + str(self.max_limit_spinBox.value())]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "BUY-AON":
            # transaction_parameters = [order type, ticker, index, stocks number, "no_necessary_params" ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(),
                                      "no_necessary_params"]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "BUY-IOC":
            # transaction_parameters = [order type, ticker, index, stocks number, number of execution cycles ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(), "not necessary"]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "BUY-BUYABOVE":
            # transaction_parameters = [order type, ticker, index, stocks number, limit "-" maximum limit ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(),
                                      str(self.limit_spinBox.value()) + "-" + str(self.max_limit_spinBox.value())]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "BUY-FOK":
            # transaction_parameters = [order type, ticker, index, stocks number, "no_necessary_params" ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(),
                                      str( self.minutes_spinBox.value())]
            self.socket.send(pickle.dumps(transaction_parameters))

        self.close()

    def create_sell_order_function(self, order_type, stock_number):
        """
        Sending the sell order that was made by the user with the parameters every type of order needs
        """
        self.socket.send("create_order".encode())
        if order_type == "SELL-MARKET":
            # transaction_parameters = [order type, ticker, index, stocks number, "no_necessary_params" ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(),
                                      "no_necessary_params", stock_number]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "SELL-LIMIT":
            # transaction_parameters = [order type, ticker, index, stocks number, maximum limit ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(),
                                      str(self.max_limit_spinBox.value()), stock_number]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "SELL-STOPLOSS":
            # transaction_parameters = [order type, ticker, index, stocks number, minimum limit ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(),
                                      str(self.min_limit_spinBox.value()), stock_number]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "SELL-STOPLIMIT":
            # transaction_parameters = [order type, ticker, index, stocks number, stop price "-" maximum limit ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(),
                                      str(self.stop_limit_spinBox.value()) + "-" + str(self.max_limit_spinBox.value()),
                                      stock_number]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "SELL-AON":
            # transaction_parameters = [order type, ticker, index, stocks number, "no_necessary_params" ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(),
                                      "no_necessary_params", stock_number]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "SELL-IOC":
            # transaction_parameters = [order type, ticker, index, stocks number, number of execution cycles ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(),
                                      "not necessary", stock_number]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "SELL-FOK":
            # transaction_parameters = [order type, ticker, index, stocks number, "no_necessary_params", stock_number ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(),
                                      str(self.minutes_spinBox.value()), stock_number]
            self.socket.send(pickle.dumps(transaction_parameters))
        elif order_type == "SELL-TAKEPROFIT":
            # transaction_parameters = [order type, ticker, index, stocks number, "no_necessary_params", stock_number ]
            transaction_parameters = [order_type, self.ticker, self.index, self.stocks_number_spinBox.value(),
                                     str(self.min_limit_spinBox.value()), stock_number]
            self.socket.send(pickle.dumps(transaction_parameters))

        self.close()


class OrderWidget:
    """
    Class for the open orders that were made by the user in "portfolio" tab
    """
    def __init__(self, scrollaera_content, vertical, order_info, socket, plot_params_boxes): # order_info =
        """
        Constructor of orders widgets in the "portfolio" tab
        """
        self.socket = socket

        self.scrollaera_content = scrollaera_content
        self.vertical = vertical
        self.plot_params_boxes = plot_params_boxes
        self.order_widget = QtWidgets.QWidget(self.scrollaera_content)

        self.order_number = order_info[0]
        self.order_type = order_info[1]
        self.order_date = order_info[2]
        self.order_ticker = order_info[3]
        self.order_stocks_number = order_info[4]
        self.order_more_info = order_info[5]
        self.order_index = order_info[6]

        self.create_widget()

    def create_widget(self):
        """
        Create the widget and designing it with the order info
        """
        self.order_widget.setObjectName("order_widget")
        self.order_widget.setMinimumHeight(121)
        self.order_widget.setMaximumHeight(121)

        background_color = self.order_widget.palette()

        buy_or_sell = ((self.order_type).split("-"))[0]
        type = ((self.order_type).split("-"))[1]

        if buy_or_sell == "BUY":
            background_color.setColor(self.order_widget.backgroundRole(),BUY_ORDER_RGB)
        elif buy_or_sell == "SELL":
            background_color.setColor(self.order_widget.backgroundRole(), SELL_ORDER_RGB)

        self.order_widget.setPalette(background_color)
        self.order_widget.setAutoFillBackground(True)

        self.order_type_label = QtWidgets.QLabel(self.order_widget)
        self.order_type_label.setGeometry(QtCore.QRect(10, 10, 131, 51))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.order_type_label.setFont(font)
        self.order_type_label.setObjectName("order_type_label")
        self.order_type_label.setText(buy_or_sell + "\n" + type)

        self.order_info_label = QtWidgets.QLabel(self.order_widget)
        self.order_info_label.setGeometry(QtCore.QRect(110, 12, 120, 61))
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(30)
        font.setPointSize(8)
        self.order_info_label.setFont(font)
        self.order_info_label.setObjectName("order_info_label")
        self.order_info_label.setText("parameters:\n" + self.order_more_info +
                                      "\ndate: " + self.order_date +
                                      "\nstocks number: " + str(self.order_stocks_number))

        self.cancel_order_pushButton = QtWidgets.QPushButton(self.order_widget)
        self.cancel_order_pushButton.setGeometry(QtCore.QRect(250, 12, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.cancel_order_pushButton.setFont(font)
        self.cancel_order_pushButton.setObjectName("cancel_order_pushButton")
        self.cancel_order_pushButton.setText("cancel\norder")
        self.cancel_order_pushButton.clicked.connect(lambda: self.cancel_order())

        self.stock_name_in_order = QtWidgets.QLabel(self.order_widget)
        self.stock_name_in_order.setGeometry(QtCore.QRect(10, 70, 91, 51))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.stock_name_in_order.setFont(font)
        self.stock_name_in_order.setObjectName("stock_name_in_order")
        self.stock_name_in_order.setText(self.order_ticker)

        self.index_in_order = QtWidgets.QLabel(self.order_widget)
        self.index_in_order.setGeometry(QtCore.QRect(120, 70, 101, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.index_in_order.setFont(font)
        self.index_in_order.setObjectName("index_in_order")
        self.index_in_order.setText(self.order_index)

        self.plot_comboBox_in_order = QtWidgets.QComboBox(self.order_widget)
        self.plot_comboBox_in_order.setGeometry(QtCore.QRect(250, 70, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.plot_comboBox_in_order.setFont(font)
        self.plot_comboBox_in_order.addItems(['week', 'month', 'year', '5 year'])
        self.plot_comboBox_in_order.setObjectName("plot_comboBox_in_order")

        self.plot_pushButton_in_order = QtWidgets.QPushButton(self.order_widget)
        self.plot_pushButton_in_order.setGeometry(QtCore.QRect(250, 90, 61, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.plot_pushButton_in_order.setFont(font)
        self.plot_pushButton_in_order.setObjectName("plot_pushButton_in_order")
        self.plot_pushButton_in_order.setText("plot")
        self.plot_pushButton_in_order.clicked.connect(self.plot_graph)

        self.more_info_Button_in_order = QtWidgets.QPushButton(self.order_widget)
        self.more_info_Button_in_order.setGeometry(QtCore.QRect(120, 90, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.more_info_Button_in_order.setFont(font)
        self.more_info_Button_in_order.setObjectName("pushButton")
        self.more_info_Button_in_order.setText("more info")
        self.more_info_Button_in_order.clicked.connect(self.ask_for_more_stock_info_func)

        self.vertical.addWidget(self.order_widget)

    def cancel_order(self):
        """
        Cancel the order if the user asked for it
        """
        if ((self.order_type).split("-"))[0] == 'BUY':
            self.socket.send("delete_buy_order".encode())

        elif ((self.order_type).split("-"))[0] == 'SELL':
            self.socket.send("delete_sell_order".encode())

        self.socket.send((str(self.order_number)).encode())
        self.socket.recv(1024)  # ACK
        self.socket.send((self.order_index).encode())

    def plot_graph(self):
        """
        First step for open a matplotlib graph for the stock history with the time period
        and the parameters that were chosen by the user.
        """

        plot_bool_list = [ x.isChecked() for x in self.plot_params_boxes]
        end_date = datetime.date.today()

        if self.plot_comboBox_in_order.currentText() == 'week':
            start_date = end_date - datetime.timedelta(days=7)

        elif self.plot_comboBox_in_order.currentText() == 'month':
            start_date = end_date - datetime.timedelta(days=30)

        elif self.plot_comboBox_in_order.currentText() == 'year':
            start_date = end_date - datetime.timedelta(days=365)

        elif self.plot_comboBox_in_order.currentText() == '5 year':
            start_date = end_date - datetime.timedelta(days=365 * 5)

        ask_for_stock_excel(self.socket, self.order_ticker, start_date, end_date,  plot_bool_list)

    def ask_for_more_stock_info_func(self):
        """
        Asking from the server for more info about the order's stock and creating a "more info" window.
        """
        self.socket.send("more_stock_info".encode())
        self.socket.send(pickle.dumps([self.order_index, self.order_ticker]))
        more_info_list = pickle.loads(self.socket.recv(4000))
        self.more_info_widget = InformationWidget(more_info_list)
        self.more_info_widget.show()


class NoOrdersWidget:
    """
    Create a widget when there is no open orders
    """
    def __init__(self, scrollaera_content, vertical):
        """
        Constructor of no orders widget in "portfolio" tab
        """
        self.scrollaera_content = scrollaera_content
        self.vertical = vertical
        self.create_widget()

    def create_widget(self):
        """
        Create the widget and designing it with the background
        """
        self.widget = QtWidgets.QWidget(self.scrollaera_content)
        self.widget.setObjectName("stock_widget")
        self.widget.setMinimumHeight(121)
        self.widget.setMaximumHeight(121)

        background = QtWidgets.QLabel(self.widget)
        background.setGeometry(QtCore.QRect(0, 0, 711, 121))
        background.setPixmap(QtGui.QPixmap(PATH_SIMPLE + "no_orders_widget.png"))
        background.setObjectName("background")

        self.vertical.addWidget(self.widget)


class ReportWidget:
    """
    Creating a report widget that was made by the server
    """
    def __init__(self, scrollaera_content, vertical, report_details, socket): # stock_info = ticker, name, price, change, index, market cap
        """
        Constructor of the report in the "reports" tab
        """
        self.socket = socket

        self.scrollaera_content = scrollaera_content
        self.vertical = vertical

        self.report_number = report_details[0]
        self.report_type = report_details[1]
        self.article = report_details[2]
        self.time = report_details[3]
        self.content = report_details[4]

        self.create_widget()

    def create_widget(self):
        """
        Creating the basic of the widget and designing it with the report info
        """
        self.report_widget = QtWidgets.QWidget(self.scrollaera_content)
        self.report_widget.setObjectName("report_widget")
        self.report_widget.setMinimumHeight(170)
        self.report_widget.setMaximumHeight(170)

        background_color = self.report_widget.palette()
        background_color.setColor(self.report_widget.backgroundRole(), GREY_RGB)
        self.report_widget.setPalette(background_color)
        self.report_widget.setAutoFillBackground(True)

        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)

        self.report_article_label = QtWidgets.QLabel(self.report_widget)
        self.report_article_label.setGeometry(QtCore.QRect(10, 0, 481, 41))
        self.report_article_label.setFont(font)
        self.report_article_label.setObjectName("report_article_label")
        self.report_article_label.setText(self.article)

        font.setPointSize(9)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)

        self.report_time_label = QtWidgets.QLabel(self.report_widget)
        self.report_time_label.setGeometry(QtCore.QRect(510, 10, 121, 20))
        font = QtGui.QFont()
        font.setItalic(True)
        font.setUnderline(False)
        self.report_time_label.setFont(font)
        self.report_time_label.setObjectName("report_time_label")
        self.report_time_label.setText(self.time)

        self.delete_report_Button = QtWidgets.QPushButton(self.report_widget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setUnderline(False)
        self.delete_report_Button.setFont(font)
        self.delete_report_Button.setObjectName("delete_report_Button")
        self.delete_report_Button.setText("DELETE")
        self.delete_report_Button.clicked.connect(lambda: self.delete_report_func())

        if self.report_type == "TEXT":
            self.create_text_report()

        elif self.report_type == "GRAPH":
            self.create_graph_report()

        self.vertical.addWidget(self.report_widget)

    def create_text_report(self):
        """
        Creating a text report with the report information
        """
        self.report_widget.setMinimumHeight(240)
        self.report_widget.setMaximumHeight(240)

        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setWeight(75)
        font.setPointSize(9)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)

        self.report_content_label = QtWidgets.QLabel(self.report_widget)
        self.report_content_label.setGeometry(QtCore.QRect(10, 42, 601, 141))
        self.report_content_label.setFont(font)
        self.report_content_label.setObjectName("report_content_label")
        self.report_content_label.setText(self.content)

        self.delete_report_Button.setGeometry(QtCore.QRect(510, 200, 111, 31))

    def create_graph_report(self):
        """
        Creating a graph report with the report graphing information
        """
        self.report_widget.setMinimumHeight(210)
        self.report_widget.setMaximumHeight(210)

        self.content = self.content.split(",")
        y_list = [float(i) for i in self.content]
        x_list = [i for i in range(len(self.content))]

        self.losses_graph_widget = pg.PlotWidget(self.report_widget)
        self.losses_graph_widget.setGeometry(QtCore.QRect(10, 42, 491, 151))
        self.losses_line = self.losses_graph_widget.plot(x_list, y_list, pen ='r', symbol ='x',
                                                         symbolPen ='r', symbolBrush = 0.2, name ='red')

        self.delete_report_Button.setGeometry(QtCore.QRect(510, 170, 111, 31))

    def delete_report_func(self):
        """
        asking the server to delete the report if the user asked so
        """
        self.socket.send("delete_report".encode())
        self.socket.recv(1024)  # ACK
        self.socket.send((str(self.report_number)).encode())