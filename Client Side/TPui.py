# This code is defining the whole  basic UI that the client's side will see and use 

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import datetime

# path for the backgrounds pictures
PATH_SIMPLE = "C:\\Users\\User\\Desktop\\picturs\\"

class UiClient():
    def __init__(self, MainWindow):
        """
        Creating the client window, setting all the tabs, the backgrounds and the objects.
        """
        MainWindow.resize(1042, 650)
        MainWindow.setWindowTitle("Take Profit")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)         # creating the stack widget
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1041, 651))

        # ---------- homepage ----------

        self.home_page = QtWidgets.QWidget()                                      # creating the homepage widget

        font = QtGui.QFont()                                                      # font for "sign in" and "sign up" buttons
        font.setFamily("Castellar")
        font.setPointSize(25)
        font.setWeight(70)
        font.setBold(True)

        self.sign_in_Button = QtWidgets.QPushButton(self.home_page)               # "sign  in" button in homepage
        self.sign_in_Button.setGeometry(QtCore.QRect(230, 460, 281, 81))
        self.sign_in_Button.setFont(font)
        self.sign_in_Button.setText("SIGN IN")

        self.sign_up_Button = QtWidgets.QPushButton(self.home_page)               # "sign up" button in homepage
        self.sign_up_Button.setGeometry(QtCore.QRect(530, 460, 281, 81))
        self.sign_up_Button.setFont(font)
        self.sign_up_Button.setText("SIGN UP")

        self.home_background = QtWidgets.QLabel(self.home_page)                   # set homepage background
        self.home_background.setGeometry(QtCore.QRect(-50, 0, 1101, 687))
        self.home_background.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"home_background.png"))

        self.home_background.raise_()
        self.sign_in_Button.raise_()
        self.sign_up_Button.raise_()
        self.stackedWidget.addWidget(self.home_page)

        # ---------- sign in page ----------

        self.sign_in_page = QtWidgets.QWidget()                                   # creating the "sign in" page widget

        self.sign_in_background = QtWidgets.QLabel(self.sign_in_page)             # set "sign in" background
        self.sign_in_background.setGeometry(QtCore.QRect(-30, -30, 1161, 731))
        self.sign_in_background.setAutoFillBackground(False)
        self.sign_in_background.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"signing_background.png"))

        font.setFamily("Arial")                                                   # font for "username" and "password" lines
        font.setPointSize(9)
        font.setWeight(50)

        self.username_line_in = QtWidgets.QLineEdit(self.sign_in_page)            # "username" line in "sign in" page
        self.username_line_in.setGeometry(QtCore.QRect(410, 280, 211, 31))
        self.username_line_in.setFont(font)
        self.username_line_in.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Israel))

        self.password_line_in = QtWidgets.QLineEdit(self.sign_in_page)            # "password" line in "sign in" page
        self.password_line_in.setGeometry(QtCore.QRect(410, 350, 211, 31))
        self.password_line_in.setFont(font)
        self.password_line_in.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Israel))

        font.setFamily("Castellar")                                               # font for "username","password" labels and "sign in" button
        font.setPointSize(12)
        font.setWeight(75)

        self.username_label_in = QtWidgets.QLabel(self.sign_in_page)              # "username" label in "sign in" page
        self.username_label_in.setGeometry(QtCore.QRect(460, 240, 121, 41))
        self.username_label_in.setFont(font)
        self.username_label_in.setText("USERNAME")

        self.password_label_in = QtWidgets.QLabel(self.sign_in_page)              # "password" label in "sign in" page
        self.password_label_in.setGeometry(QtCore.QRect(460, 310, 121, 41))
        self.password_label_in.setFont(font)
        self.password_label_in.setText("PASSWORD")

        self.error_label_in = QtWidgets.QLabel(self.sign_in_page)                 # error label for problems with client's details
        self.error_label_in.setGeometry(QtCore.QRect(80, 460, 700, 151))
        self.error_label_in.setFont(font)


        self.sign_in_in_Button = QtWidgets.QPushButton(self.sign_in_page)         # "sign in" button in "sign in" page
        self.sign_in_in_Button.setGeometry(QtCore.QRect(420, 440, 191, 61))
        font.setPointSize(20)
        self.sign_in_in_Button.setFont(font)
        self.sign_in_in_Button.setText("SIGN IN")

        self.stackedWidget.addWidget(self.sign_in_page)

        # ---------- sign up page ----------

        self.sign_up_page = QtWidgets.QWidget()                                    # creating the "sign up" page widget

        self.sign_up_background = QtWidgets.QLabel(self.sign_up_page)              # set "sign up" background
        self.sign_up_background.setGeometry(QtCore.QRect(-30, -30, 1161, 731))
        self.sign_up_background.setAutoFillBackground(False)
        self.sign_up_background.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"signing_background.png"))

        font.setFamily("Arial")                                                    # font for all lines
        font.setPointSize(9)
        font.setWeight(50)

        self.full_name_line = QtWidgets.QLineEdit(self.sign_up_page)               # "full name" line in "sign up" page
        self.full_name_line.setGeometry(QtCore.QRect(410, 230, 211, 31))
        self.full_name_line.setFont(font)

        self.mail_line = QtWidgets.QLineEdit(self.sign_up_page)                    # "mail" line in "sign up" page
        self.mail_line.setGeometry(QtCore.QRect(410, 290, 211, 31))
        self.mail_line.setFont(font)

        self.initial_amount_line = QtWidgets.QLineEdit(self.sign_up_page)          # "initial amount" line in "sign up" page
        self.initial_amount_line.setGeometry(QtCore.QRect(410, 350, 211, 31))
        self.initial_amount_line.setFont(font)

        self.username_line_up = QtWidgets.QLineEdit(self.sign_up_page)             # "username" line in "sign up" page
        self.username_line_up.setGeometry(QtCore.QRect(410, 410, 211, 31))
        self.username_line_up.setFont(font)

        self.password_line_up = QtWidgets.QLineEdit(self.sign_up_page)             # "password" line in "sign up" page
        self.password_line_up.setGeometry(QtCore.QRect(410, 470, 211, 31))
        self.password_line_up.setFont(font)

        font.setFamily("Castellar")                                                # font for labels and "sign up" button in "sign up" page
        font.setPointSize(12)
        font.setWeight(75)

        self.fullname_label = QtWidgets.QLabel(self.sign_up_page)                  # "full name" label in "sign up" page
        self.fullname_label.setGeometry(QtCore.QRect(460, 200, 121, 41))
        self.fullname_label.setFont(font)
        self.fullname_label.setText("FULL NAME")

        self.mail_address_label = QtWidgets.QLabel(self.sign_up_page)              # "mail" label in sign "up page"
        self.mail_address_label.setGeometry(QtCore.QRect(440, 260, 151, 41))
        self.mail_address_label.setFont(font)
        self.mail_address_label.setText("MAIL ADDRESS")

        self.initial_amount_label = QtWidgets.QLabel(self.sign_up_page)            # "initial amount" label in "sign up" page
        self.initial_amount_label.setGeometry(QtCore.QRect(430, 320, 181, 41))
        self.initial_amount_label.setFont(font)
        self.initial_amount_label.setText("INITIAL AMOUNT")

        self.username_label_up = QtWidgets.QLabel(self.sign_up_page)               # "username" label in "sign up" page
        self.username_label_up.setGeometry(QtCore.QRect(460, 380, 121, 41))
        self.username_label_up.setFont(font)
        self.username_label_up.setText("USERNAME")

        self.password_label_up = QtWidgets.QLabel(self.sign_up_page)               # "password" label in "sign up" page
        self.password_label_up.setGeometry(QtCore.QRect(460, 440, 121, 41))
        self.password_label_up.setFont(font)
        self.password_label_up.setText("PASSWORD")

        self.error_label_up = QtWidgets.QLabel(self.sign_up_page)                  # error label for problems with client's details
        self.error_label_up.setGeometry(QtCore.QRect(20, 520, 700, 151))
        self.error_label_up.setFont(font)

        self.sign_up_up_Button = QtWidgets.QPushButton(self.sign_up_page)          # "sign up" button in "sign up" page
        self.sign_up_up_Button.setGeometry(QtCore.QRect(420, 520, 191, 61))
        font.setPointSize(20)
        self.sign_up_up_Button.setFont(font)
        self.sign_up_up_Button.setText("SIGN UP")

        self.stackedWidget.addWidget(self.sign_up_page)

        # -- TakeProfit inside page --

        self.inside_page = QtWidgets.QWidget()
        self.tabWidget = QtWidgets.QTabWidget(self.inside_page)
        self.tabWidget.setGeometry(QtCore.QRect(0, -1, 1031, 621))

        font.setFamily("Castellar")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)

        # tab 1 -------- about us

        self.about_tab = QtWidgets.QWidget()
        self.background_tab_1 = QtWidgets.QLabel(self.about_tab)
        self.background_tab_1.setGeometry(QtCore.QRect(0, -40, 1081, 691))
        self.background_tab_1.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"about_us_tab_background.png"))

        self.about_us_label = QtWidgets.QLabel(self.about_tab)
        self.about_us_label.setGeometry(QtCore.QRect(20, 232, 411, 341))
        font.setUnderline(False)
        self.about_us_label.setFont(font)
        self.about_us_label.setText("“Take Profit Stock Exchange” is a practice\n"
                                    "platform for day trading, our goal is to\n"
                                    "let you learn about the stock market in\n"
                                    "the easiest and safest way.\n"
                                    "\nOur platform provides reliable and up to\n"
                                    "date information so that you can study\n"
                                    "stocks market in depth and without risks.\n"
                                    "We also provide friendly user service so\n"
                                    "you can learn the market world in the\n"
                                    "best way.\n"
                                    "\nIn this page you can learn how to use the\n"
                                    "platform and what each tab is for.")
        self.about_us_label.setObjectName("about_us_label")
        font.setUnderline(True)

        self.about_us_explanations_tab_widget = QtWidgets.QTabWidget(self.about_tab)
        self.about_us_explanations_tab_widget.setGeometry(QtCore.QRect(460, 219, 551, 354))
        self.about_us_explanations_tab_widget.setObjectName("about_us_explanations_tab_widget")

        self.reports_exp = QtWidgets.QWidget()
        self.reports_exp.setObjectName("reports_exp")
        self.reports_exp_label = QtWidgets.QLabel(self.reports_exp)
        self.reports_exp_label.setGeometry(QtCore.QRect(0, 0, 571, 331))
        self.reports_exp_label.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"reports_exp_label.png"))
        self.reports_exp_label.setObjectName("reports_exp_label")
        self.about_us_explanations_tab_widget.addTab(self.reports_exp, "reports")

        self.balance_exp = QtWidgets.QWidget()
        self.balance_exp.setObjectName("balance_exp")
        self.balance_exp_label = QtWidgets.QLabel(self.balance_exp)
        self.balance_exp_label.setGeometry(QtCore.QRect(0, 0, 571, 331))
        self.balance_exp_label.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"balance_exp_label.png"))
        self.balance_exp_label.setObjectName("balance_exp_label")
        self.about_us_explanations_tab_widget.addTab(self.balance_exp, "balance")

        self.portfolio_exp = QtWidgets.QWidget()
        self.portfolio_exp.setObjectName("portfolio_exp")
        self.portfolio_exp_label = QtWidgets.QLabel(self.portfolio_exp)
        self.portfolio_exp_label.setGeometry(QtCore.QRect(0, 0, 571, 331))
        self.portfolio_exp_label.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"portfolio_exp_label.png"))
        self.portfolio_exp_label.setObjectName("portfolio_exp_label")
        self.about_us_explanations_tab_widget.addTab(self.portfolio_exp, "portfolio")

        self.stock_market_exp = QtWidgets.QWidget()
        self.stock_market_exp.setObjectName("stock_market_exp")
        self.stock_market_exp_label = QtWidgets.QLabel(self.stock_market_exp)
        self.stock_market_exp_label.setGeometry(QtCore.QRect(0, 0, 571, 331))
        self.stock_market_exp_label.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"stock_market_exp_label.png"))
        self.stock_market_exp_label.setObjectName("stock_market_exp_label")
        self.about_us_explanations_tab_widget.addTab(self.stock_market_exp, "stock market")

        self.indexes_exp = QtWidgets.QWidget()
        self.indexes_exp.setObjectName("indexes_exp")
        self.indexes_exp_label = QtWidgets.QLabel(self.indexes_exp)
        self.indexes_exp_label.setGeometry(QtCore.QRect(0, 0, 571, 331))
        self.indexes_exp_label.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"indexes_exp_label.png"))
        self.indexes_exp_label.setObjectName("indexes_exp_label")
        self.about_us_explanations_tab_widget.addTab(self.indexes_exp, "indexes")

        self.tabWidget.addTab(self.about_tab, "     About Us     ")

        # tab 2 -------- reports

        self.reports_tab = QtWidgets.QWidget()
        self.background_tab_2 = QtWidgets.QLabel(self.reports_tab)
        self.background_tab_2.setGeometry(QtCore.QRect(0, 0, 1031, 611))
        self.background_tab_2.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"reports_tab_background.png"))

        self.refresh_reports_button = QtWidgets.QPushButton(self.reports_tab)
        self.refresh_reports_button.setGeometry(QtCore.QRect(970, 10, 41, 31))
        self.refresh_reports_button.setObjectName("refresh_reports_button")
        font.setPointSize(7)
        font.setUnderline(False)
        font.setFamily('Californian FB')
        font.setBold(False)
        font.setWeight(40)
        self.refresh_reports_button.setFont(font)
        self.refresh_reports_button.setText("refresh\npage")

        self.reports_scrollArea = QtWidgets.QScrollArea(self.reports_tab)
        self.reports_scrollArea.setGeometry(QtCore.QRect(340, 230, 671, 341))
        self.reports_scrollArea.setWidgetResizable(True)
        self.reports_scrollArea.setObjectName("reports_scrollArea")

        self.reports_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.reports_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 649, 339))
        self.reports_scrollAreaWidgetContents.setObjectName("reports_scrollAreaWidgetContents")
        self.reports_verticalLayout = QtWidgets.QVBoxLayout(self.reports_scrollAreaWidgetContents)
        self.reports_verticalLayout.setObjectName("reports_verticalLayout")

        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)

        self.reports_label = QtWidgets.QLabel(self.reports_tab)
        self.reports_label.setGeometry(QtCore.QRect(350, 200, 251, 20))
        self.reports_label.setFont(font)
        self.reports_label.setObjectName("reports_label")
        self.reports_label.setText("Reports")

        self.requests_label = QtWidgets.QLabel(self.reports_tab)
        self.requests_label.setGeometry(QtCore.QRect(50, 240, 231, 20))
        font.setUnderline(True)
        self.requests_label.setFont(font)
        self.requests_label.setObjectName("requests_label")
        self.requests_label.setText("Requests")

        self.your_details_radioButton = QtWidgets.QRadioButton(self.reports_tab)
        self.your_details_radioButton.setGeometry(QtCore.QRect(20, 270, 16, 17))
        self.your_details_radioButton.setObjectName("your_details_radioButton")

        self.orders_exp_radioButton = QtWidgets.QRadioButton(self.reports_tab)
        self.orders_exp_radioButton.setGeometry(QtCore.QRect(20, 440, 16, 17))
        self.orders_exp_radioButton.setObjectName("orders_exp_radioButton")

        self.stocks_info_radioButton = QtWidgets.QRadioButton(self.reports_tab)
        self.stocks_info_radioButton.setGeometry(QtCore.QRect(20, 360, 16, 17))
        self.stocks_info_radioButton.setObjectName("stocks_info_radioButton")

        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)

        self.report_your_details_title = QtWidgets.QLabel(self.reports_tab)
        self.report_your_details_title.setGeometry(QtCore.QRect(40, 270, 101, 21))
        self.report_your_details_title.setFont(font)
        self.report_your_details_title.setObjectName("report_your_details_title")
        self.report_your_details_title.setText("Your Details")

        self.stock_info_report_ask_title = QtWidgets.QLabel(self.reports_tab)
        self.stock_info_report_ask_title.setGeometry(QtCore.QRect(40, 350, 171, 31))
        self.stock_info_report_ask_title.setFont(font)
        self.stock_info_report_ask_title.setObjectName("stock_info_report_ask_title")
        self.stock_info_report_ask_title.setText("Stock Market Concepts")

        self.orders_exp_report_ask_title = QtWidgets.QLabel(self.reports_tab)
        self.orders_exp_report_ask_title.setGeometry(QtCore.QRect(40, 430, 161, 31))
        self.orders_exp_report_ask_title.setFont(font)
        self.orders_exp_report_ask_title.setObjectName("orders_exp_report_ask_title")
        self.orders_exp_report_ask_title.setText("Orders explanations")

        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)

        self.orders_exp_comboBox = QtWidgets.QComboBox(self.reports_tab)
        self.orders_exp_comboBox.setGeometry(QtCore.QRect(30, 464, 211, 31))
        self.orders_exp_comboBox.setObjectName("orders_exp_comboBox")
        self.orders_exp_comboBox.setFont(font)
        self.orders_exp_comboBox.addItems(["market order", "limit order", "take profit order", "stop loss order", "stop limit order",
                                           "AON order", "IOC order", "buy above order", "FOK order"])

        self.your_details_comboBox = QtWidgets.QComboBox(self.reports_tab)
        self.your_details_comboBox.setGeometry(QtCore.QRect(30, 300, 211, 31))
        self.your_details_comboBox.setObjectName("your_details_comboBox")
        self.your_details_comboBox.setFont(font)
        self.your_details_comboBox.addItems(["get balance history", "get gains history", "get losses history"])

        self.stock_info_comboBox = QtWidgets.QComboBox(self.reports_tab)
        self.stock_info_comboBox.setGeometry(QtCore.QRect(30, 385, 211, 31))
        self.stock_info_comboBox.setObjectName("stock_info_comboBox")
        self.stock_info_comboBox.setFont(font)
        self.stock_info_comboBox.addItems(["what is the stock market?", "what is a stock?",
                                           "when the market is open?",
                                           "what is a ticker symbol?", "what is 'high'?", "what is 'low'?", "what is 'open'?",
                                           "what is 'close'?", "what is 'adjusted close'?", "what is 'change'?",
                                           "what is 'market cap'?", "what is 'volume'?", "what is 'beta'?",
                                           "what is 'P/E'?", "what is an index fund?", "what is DowJones30 index?",
                                           "what is S&P 500 index?", "what is Nasdaq100 index?",
                                           "what is Russel 1000 index?"])

        self.send_ask_Button = QtWidgets.QPushButton(self.reports_tab)
        self.send_ask_Button.setGeometry(QtCore.QRect(174, 550, 61, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.send_ask_Button.setFont(font)
        self.send_ask_Button.setObjectName("send_ask_Button")
        self.send_ask_Button.setText("SEND")

        self.tabWidget.addTab(self.reports_tab, "     Reports     ")

        # tab 3 -------- balance, gains and losses

        self.gains_and_losses_tab = QtWidgets.QWidget()
        self.background_tab_ = QtWidgets.QLabel(self.gains_and_losses_tab)
        self.background_tab_.setGeometry(QtCore.QRect(0, 0, 1031, 611))
        self.background_tab_.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"gains_and_losses_tab_background.png"))

        self.refresh_balance_button = QtWidgets.QPushButton(self.gains_and_losses_tab)
        self.refresh_balance_button.setGeometry(QtCore.QRect(970, 10, 41, 31))
        self.refresh_balance_button.setObjectName("refresh_balance_button")
        font.setPointSize(7)
        font.setFamily('Californian FB')
        font.setBold(False)
        font.setWeight(40)
        self.refresh_balance_button.setFont(font)
        self.refresh_balance_button.setText("refresh\npage")

        font = QtGui.QFont()
        font.setPointSize(15)

        self.balance_label = QtWidgets.QLabel(self.gains_and_losses_tab)
        self.balance_label.setGeometry(QtCore.QRect(440, 230, 111, 41))
        self.balance_label.setFont(font)
        self.balance_label.setText("balance")

        self.gains_label = QtWidgets.QLabel(self.gains_and_losses_tab)
        self.gains_label.setGeometry(QtCore.QRect(145, 230, 111, 41))
        self.gains_label.setFont(font)
        self.gains_label.setText("gains")

        self.losses_label = QtWidgets.QLabel(self.gains_and_losses_tab)
        self.losses_label.setGeometry(QtCore.QRect(800, 230, 111, 41))
        self.losses_label.setFont(font)
        self.losses_label.setText("losses")

        self.gains_number = QtWidgets.QLCDNumber(self.gains_and_losses_tab)
        self.gains_number.setGeometry(QtCore.QRect(120, 270, 121, 51))

        self.losses_number = QtWidgets.QLCDNumber(self.gains_and_losses_tab)
        self.losses_number.setGeometry(QtCore.QRect(775, 270, 121, 51))

        self.balance_number = QtWidgets.QLCDNumber(self.gains_and_losses_tab)
        self.balance_number.setGeometry(QtCore.QRect(430, 270, 121, 51))

        x = [1,1]
        y = [1,1]

        self.losses_graph_widget = pg.PlotWidget(self.gains_and_losses_tab)
        self.losses_graph_widget.setGeometry(QtCore.QRect(700, 330, 311, 241))
        self.losses_line = self.losses_graph_widget.plot(x,y)

        self.balance_graph_widget = pg.PlotWidget(self.gains_and_losses_tab)
        self.balance_graph_widget.setGeometry(QtCore.QRect(360, 330, 311, 241))
        self.balance_line = self.balance_graph_widget.plot(x,y)

        self.gains_graph_widget = pg.PlotWidget(self.gains_and_losses_tab)
        self.gains_graph_widget.setGeometry(QtCore.QRect(20, 330, 311, 241))
        self.gains_line = self.gains_graph_widget.plot(x,y)

        self.add_money_button = QtWidgets.QPushButton(self.gains_and_losses_tab)
        self.add_money_button.setGeometry(QtCore.QRect(555, 300, 61, 21))
        font.setPointSize(10)
        font.setUnderline(False)
        self.add_money_button.setFont(font)
        self.add_money_button.setText("+")

        self.add_money_spinbox = QtWidgets.QSpinBox(self.gains_and_losses_tab)
        self.add_money_spinbox.setGeometry(QtCore.QRect(555, 275, 61, 21))
        font.setItalic(True)
        font.setPointSize(10)
        font.setWeight(50)
        self.add_money_spinbox.setFont(font)
        self.add_money_spinbox.setMaximum(200)

        self.tabWidget.addTab(self.gains_and_losses_tab, "     balance     ")

        # tab 4 -------- portfolio

        self.portfolio_tab = QtWidgets.QWidget()
        self.background_tab_4 = QtWidgets.QLabel(self.portfolio_tab)
        self.background_tab_4.setGeometry(QtCore.QRect(0, 0, 1031, 611))
        self.background_tab_4.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"portfolio_tab_background.png"))

        self.close_market_label_portfolio = QtWidgets.QLabel(self.portfolio_tab)
        self.close_market_label_portfolio.setGeometry(QtCore.QRect(540, 30, 361, 91))
        self.close_market_label_portfolio.setObjectName("close_market_label_portfolio")
        self.close_market_label_portfolio.setPixmap(QtGui.QPixmap(PATH_SIMPLE + "the_market_is_close_label.png"))

        self.details_label_portfolio = QtWidgets.QLabel(self.portfolio_tab)
        self.details_label_portfolio.setGeometry(QtCore.QRect(380, 205, 711, 20))
        font.setPointSize(14)
        self.details_label_portfolio.setFont(font)
        self.details_label_portfolio.setObjectName("details_label_portfolio")
        self.details_label_portfolio.setText("Name       price       change                    plot    orders")

        self.open_orders_label_portfolio = QtWidgets.QLabel(self.portfolio_tab)
        self.open_orders_label_portfolio.setGeometry(QtCore.QRect(110, 205, 160, 20))
        self.open_orders_label_portfolio.setFont(font)
        self.open_orders_label_portfolio.setObjectName("details_label_portfolio")
        self.open_orders_label_portfolio.setText("open orders")

        font = QtGui.QFont()
        font.setFamily("Californian FB")
        font.setBold(True)
        font.setUnderline(False)
        font.setItalic(False)
        font.setWeight(75)

        self.High_checkBox_portfolio = QtWidgets.QCheckBox(self.portfolio_tab)
        self.High_checkBox_portfolio.setGeometry(QtCore.QRect(715, 140, 70, 17))
        self.High_checkBox_portfolio.setFont(font)
        self.High_checkBox_portfolio.setObjectName("High_checkBox_portfolio")
        self.High_checkBox_portfolio.setText("High")

        self.Low_checkBox_portfolio = QtWidgets.QCheckBox(self.portfolio_tab)
        self.Low_checkBox_portfolio.setGeometry(QtCore.QRect(715, 160, 70, 17))
        self.Low_checkBox_portfolio.setFont(font)
        self.Low_checkBox_portfolio.setObjectName("Low_checkBox_portfolio")
        self.Low_checkBox_portfolio.setText("Low")

        self.Open_checkBox_portfolio = QtWidgets.QCheckBox(self.portfolio_tab)
        self.Open_checkBox_portfolio.setGeometry(QtCore.QRect(770, 140, 70, 17))
        self.Open_checkBox_portfolio.setFont(font)
        self.Open_checkBox_portfolio.setObjectName("Open_checkBox_portfolio")
        self.Open_checkBox_portfolio.setText("Open")

        self.Close_checkBox_portfolio = QtWidgets.QCheckBox(self.portfolio_tab)
        self.Close_checkBox_portfolio.setGeometry(QtCore.QRect(770, 160, 70, 17))
        self.Close_checkBox_portfolio.setFont(font)
        self.Close_checkBox_portfolio.setObjectName("Close_checkBox_portfolio")
        self.Close_checkBox_portfolio.setText("Close")

        self.Volume_checkBox_portfolio = QtWidgets.QCheckBox(self.portfolio_tab)
        self.Volume_checkBox_portfolio.setGeometry(QtCore.QRect(825, 140, 101, 17))
        self.Volume_checkBox_portfolio.setFont(font)
        self.Volume_checkBox_portfolio.setObjectName("Volume_checkBox_portfolio")
        self.Volume_checkBox_portfolio.setText("Volume")

        self.AdjClose_checkBox_portfolio = QtWidgets.QCheckBox(self.portfolio_tab)
        self.AdjClose_checkBox_portfolio.setGeometry(QtCore.QRect(825, 160, 111, 17))
        self.AdjClose_checkBox_portfolio.setFont(font)
        self.AdjClose_checkBox_portfolio.setObjectName("AdjClose_checkBox_portfolio")
        self.AdjClose_checkBox_portfolio.setText("Adj Close")

        self.refresh_portfolio_button = QtWidgets.QPushButton(self.portfolio_tab)
        self.refresh_portfolio_button.setGeometry(QtCore.QRect(970, 10, 41, 31))
        self.refresh_portfolio_button.setObjectName("refresh_portfolio_button")
        font.setPointSize(7)
        font.setBold(False)
        font.setWeight(40)
        self.refresh_portfolio_button.setFont(font)
        self.refresh_portfolio_button.setText("refresh\npage")

        self.plot_settings_label_portfolio = QtWidgets.QLabel(self.portfolio_tab)
        self.plot_settings_label_portfolio.setGeometry(QtCore.QRect(760, 120, 151, 16))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setUnderline(True)
        self.plot_settings_label_portfolio.setFont(font)
        self.plot_settings_label_portfolio.setObjectName("plot_settings_label_portfolio")
        self.plot_settings_label_portfolio.setText("Plot Settings")

        font.setFamily("Castellar")

        self.stocks_scrollArea_portfolio = QtWidgets.QScrollArea(self.portfolio_tab)
        self.stocks_scrollArea_portfolio.setGeometry(QtCore.QRect(360, 230, 655, 341))
        self.stocks_scrollArea_portfolio.setWidgetResizable(True)
        self.stocks_scrollArea_portfolio.setObjectName("stocks_scrollArea_portfolio")

        self.stocks_portfolio_Contents = QtWidgets.QWidget()
        self.stocks_portfolio_Contents.setGeometry(QtCore.QRect(0, 0, 279, 79))
        self.stocks_portfolio_Contents.setObjectName("stocks_portfolio_Contents")

        self.stocks_portfolio_verticalLayout = QtWidgets.QVBoxLayout(self.stocks_portfolio_Contents)
        self.stocks_portfolio_verticalLayout.setObjectName("stocks_portfolio_verticalLayout")

        self.stock_widget = QtWidgets.QWidget(self.stocks_portfolio_Contents)
        self.stock_widget.setGeometry(QtCore.QRect(30, 110, 611, 80))
        self.stock_widget.setObjectName("widget")

        self.orders_scrollArea_portfolio = QtWidgets.QScrollArea(self.portfolio_tab)
        self.orders_scrollArea_portfolio.setGeometry(QtCore.QRect(5, 230, 350, 341))
        self.orders_scrollArea_portfolio.setWidgetResizable(True)
        self.orders_scrollArea_portfolio.setObjectName("orders_scroll_area_portfolio")

        self.orders_portfolio_Contents = QtWidgets.QWidget()
        self.orders_portfolio_Contents.setGeometry(QtCore.QRect(0, 0, 339, 339))
        self.orders_portfolio_Contents.setObjectName("orders_portfolio_Contents")

        self.orders_portfolio_verticalLayout = QtWidgets.QVBoxLayout( self.orders_portfolio_Contents)
        self.orders_portfolio_verticalLayout.setObjectName("orders_portfolio_verticalLayout")

        self.tabWidget.addTab(self.portfolio_tab, "     Portfolio     ")

        # tab 5 -------- stock market

        self.stock_market = QtWidgets.QWidget()
        self.stock_market.setObjectName("stock_market")
        self.background_tab_6 = QtWidgets.QLabel(self.stock_market)
        self.background_tab_6.setGeometry(QtCore.QRect(0, -20, 1031, 651))
        self.background_tab_6.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"stock_market_tab_background.png"))
        self.background_tab_6.setObjectName("background_tab_6")

        self.close_market_label_market = QtWidgets.QLabel(self.stock_market)
        self.close_market_label_market.setGeometry(QtCore.QRect(540, 30, 361, 91))
        self.close_market_label_market.setObjectName("close_market_label_market")
        self.close_market_label_market.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"the_market_is_close_label.png"))

        self.details_label_market = QtWidgets.QLabel(self.stock_market)
        self.details_label_market.setGeometry(QtCore.QRect(290, 205, 711, 20))
        font.setUnderline(False)
        font.setItalic(True)
        font.setPointSize(14)
        font.setWeight(50)
        self.details_label_market.setFont(font)
        self.details_label_market.setObjectName("details_label_market")
        self.details_label_market.setText("  Name                  price        change          plot          orders")

        font = QtGui.QFont()
        font.setFamily("Californian FB")
        font.setBold(True)
        font.setUnderline(False)
        font.setItalic(False)
        font.setWeight(75)

        self.High_checkBox_market = QtWidgets.QCheckBox(self.stock_market)
        self.High_checkBox_market.setGeometry(QtCore.QRect(715, 140, 70, 17))
        self.High_checkBox_market.setFont(font)
        self.High_checkBox_market.setObjectName("High_checkBox_market")
        self.High_checkBox_market.setText("High")

        self.Low_checkBox_market = QtWidgets.QCheckBox(self.stock_market)
        self.Low_checkBox_market.setGeometry(QtCore.QRect(715, 160, 70, 17))
        self.Low_checkBox_market.setFont(font)
        self.Low_checkBox_market.setObjectName("Low_checkBox_market")
        self.Low_checkBox_market.setText("Low")

        self.Open_checkBox_market = QtWidgets.QCheckBox(self.stock_market)
        self.Open_checkBox_market.setGeometry(QtCore.QRect(770, 140, 70, 17))
        self.Open_checkBox_market.setFont(font)
        self.Open_checkBox_market.setObjectName("Open_checkBox_market")
        self.Open_checkBox_market.setText("Open")

        self.Close_checkBox_market = QtWidgets.QCheckBox(self.stock_market)
        self.Close_checkBox_market.setGeometry(QtCore.QRect(770, 160, 70, 17))
        self.Close_checkBox_market.setFont(font)
        self.Close_checkBox_market.setObjectName("Close_checkBox_market")
        self.Close_checkBox_market.setText("Close")

        self.Volume_checkBox_market = QtWidgets.QCheckBox(self.stock_market)
        self.Volume_checkBox_market.setGeometry(QtCore.QRect(825, 140, 101, 17))
        self.Volume_checkBox_market.setFont(font)
        self.Volume_checkBox_market.setObjectName("Volume_checkBox_market")
        self.Volume_checkBox_market.setText("Volume")

        self.AdjClose_checkBox_market = QtWidgets.QCheckBox(self.stock_market)
        self.AdjClose_checkBox_market.setGeometry(QtCore.QRect(825, 160, 111, 17))
        self.AdjClose_checkBox_market.setFont(font)
        self.AdjClose_checkBox_market.setObjectName("AdjClose_checkBox_market")
        self.AdjClose_checkBox_market.setText("Adj Close")

        self.plot_settings_label_market = QtWidgets.QLabel(self.stock_market)
        self.plot_settings_label_market.setGeometry(QtCore.QRect(760, 120, 151, 16))
        font.setPointSize(11)
        font.setUnderline(True)
        self.plot_settings_label_market.setFont(font)
        self.plot_settings_label_market.setObjectName("plot_settings_label_market")
        self.plot_settings_label_market.setText("Plot Settings")

        font.setFamily("Castellar")

        self.stocks_market_scrollArea = QtWidgets.QScrollArea(self.stock_market)
        self.stocks_market_scrollArea.setGeometry(QtCore.QRect(290, 230, 721, 341))
        self.stocks_market_scrollArea.setWidgetResizable(True)
        self.stocks_market_scrollArea.setObjectName("stocks_market_scrollArea")

        self.stocks_market_Contents = QtWidgets.QWidget()
        self.stocks_market_Contents.setGeometry(QtCore.QRect(0, 0, 279, 79))
        self.stocks_market_Contents.setObjectName("stocks_market_Contents")
        self.stocks_market_verticalLayout = QtWidgets.QVBoxLayout(self.stocks_market_Contents)
        self.stocks_market_verticalLayout.setObjectName("verticalLayout")

        self.searching_tabwidget_market = QtWidgets.QTabWidget(self.stock_market)
        self.searching_tabwidget_market.setGeometry(QtCore.QRect(10, 230, 261, 341))

        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        font.setPointSize(1)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)

        self.searching_tabwidget_market.setFont(font)
        self.searching_tabwidget_market.setObjectName("searching_tabwidget_market")

        self.specific_search_tab_market = QtWidgets.QWidget()
        self.specific_search_tab_market.setFont(font)
        self.specific_search_tab_market.setObjectName("specific_search_tab_market")

        self.spec_background_market = QtWidgets.QLabel(self.specific_search_tab_market)
        self.spec_background_market.setGeometry(QtCore.QRect(0, 0, 261, 321))
        self.spec_background_market.setText("")
        self.spec_background_market.setPixmap(QtGui.QPixmap(PATH_SIMPLE + "search_market_tab_background.png"))
        self.spec_background_market.setObjectName("spec_background_market")

        self.price_slider_spectab_market = QtWidgets.QSlider(self.specific_search_tab_market)
        self.price_slider_spectab_market.setGeometry(QtCore.QRect(10, 260, 231, 20))
        font.setFamily("Candara")
        self.price_slider_spectab_market.setFont(font)
        self.price_slider_spectab_market.setMaximum(3500)
        self.price_slider_spectab_market.setSingleStep(10)
        self.price_slider_spectab_market.setPageStep(8)
        self.price_slider_spectab_market.setProperty("value", 1750)
        self.price_slider_spectab_market.setOrientation(QtCore.Qt.Horizontal)
        self.price_slider_spectab_market.setObjectName("price_slider_spectab_market")

        self.numbers_slider_label_spectab_market = QtWidgets.QLabel(self.specific_search_tab_market)
        self.numbers_slider_label_spectab_market.setGeometry(QtCore.QRect(10, 270, 241, 20))
        font.setFamily("Californian FB")
        font.setPointSize(8)
        font.setUnderline(False)
        self.numbers_slider_label_spectab_market.setFont(font)
        self.numbers_slider_label_spectab_market.setText("0           500        1000      1500"
                                                         "      2000     2500      3000      3500")
        self.numbers_slider_label_spectab_market.setObjectName("numbers_slider_label_spectab_market")

        self.industry_combobox_spec_market = QtWidgets.QComboBox(self.specific_search_tab_market)
        self.industry_combobox_spec_market.setGeometry(QtCore.QRect(100, 40, 151, 22))
        self.industry_combobox_spec_market.setObjectName("industry_combobox_spec_market")

        self.industry_checkBox_spec_market = QtWidgets.QCheckBox(self.specific_search_tab_market)
        self.industry_checkBox_spec_market.setGeometry(QtCore.QRect(10, 40, 111, 17))
        self.industry_checkBox_spec_market.setText("Industry")
        self.industry_checkBox_spec_market.setObjectName("industry_checkBox_spec_market")

        industry_types = ['Automobiles', 'Apparel', 'Aerospace', 'Beverages', 'Banking', 'Biotechnology', 'Computers',
                           'Communications', 'Containers', 'Chemicals', 'Drug', 'Electr', 'Entertainment','Food',
                           'Freight','Gas', 'Hotels', 'Healthcare', 'Homebuilding','Insurance', 'IT', 'Investment',
                           'Machinery', 'Media','Oil','Personal', 'Pharmaceuticals','Retail', 'Residential',
                           'Semiconductors', 'Software', 'Services','Tobacco', 'Textiles']

        self.industry_combobox_spec_market.addItems(industry_types)

        self.index_comboBox_spec_market = QtWidgets.QComboBox(self.specific_search_tab_market)
        self.index_comboBox_spec_market.setGeometry(QtCore.QRect(10, 10, 242, 22))
        self.index_comboBox_spec_market.setObjectName("index_comboBox_spec_market")

        self.index_comboBox_spec_market.addItems(["DowJones30","S&P500","Russell1000","Nasdaq100"])

        self.cap_checkBox_spec_market = QtWidgets.QCheckBox(self.specific_search_tab_market)
        self.cap_checkBox_spec_market.setGeometry(QtCore.QRect(10, 70, 141, 17))
        self.cap_checkBox_spec_market.setText("Market Cap ($)")
        self.cap_checkBox_spec_market.setObjectName("cap_checkBox_spec_market")

        self.small_cap_button_spec_market = QtWidgets.QRadioButton(self.specific_search_tab_market)
        self.small_cap_button_spec_market.setGeometry(QtCore.QRect(20, 90, 221, 17))
        self.small_cap_button_spec_market.setText("500 million - 20 billion")
        self.small_cap_button_spec_market.setObjectName("small_cap_button_spec_market")

        self.aveg_cap_button_spec_market = QtWidgets.QRadioButton(self.specific_search_tab_market)
        self.aveg_cap_button_spec_market.setGeometry(QtCore.QRect(20, 110, 221, 17))
        self.aveg_cap_button_spec_market.setText("20 billion - 100 billion")
        self.aveg_cap_button_spec_market.setObjectName("aveg_cap_button_spec_market")

        self.big_cap_button_spec_market = QtWidgets.QRadioButton(self.specific_search_tab_market)
        self.big_cap_button_spec_market.setGeometry(QtCore.QRect(20, 130, 231, 17))
        self.big_cap_button_spec_market.setText("100 billion - 2.5 trillion")
        self.big_cap_button_spec_market.setObjectName("big_cap_button_spec_market")

        self.price_checkBox_spec_market = QtWidgets.QCheckBox(self.specific_search_tab_market)
        self.price_checkBox_spec_market.setGeometry(QtCore.QRect(10, 240, 81, 17))
        self.price_checkBox_spec_market.setText("price($)")
        self.price_checkBox_spec_market.setObjectName("price_checkBox_spec_market")

        self.change_checkBox_spec_market = QtWidgets.QCheckBox(self.specific_search_tab_market)
        self.change_checkBox_spec_market.setGeometry(QtCore.QRect(10, 150, 191, 17))
        self.change_checkBox_spec_market.setText("Change Percentage(%)")
        self.change_checkBox_spec_market.setObjectName("change_checkBox_spec_market")

        self.change_dial_spec_market = QtWidgets.QDial(self.specific_search_tab_market)
        self.change_dial_spec_market.setGeometry(QtCore.QRect(60, 180, 111, 51))
        self.change_dial_spec_market.setMinimum(-15)
        self.change_dial_spec_market.setMaximum(15)
        self.change_dial_spec_market.setProperty("value", -15)
        self.change_dial_spec_market.setSliderPosition(-15)
        self.change_dial_spec_market.setObjectName("change_dial_spec_market")

        self.spec_search_Button_market = QtWidgets.QPushButton(self.specific_search_tab_market)
        self.spec_search_Button_market.setGeometry(QtCore.QRect(90, 290, 75, 21))
        self.spec_search_Button_market.setText("search")
        self.spec_search_Button_market.setFont(font)
        self.spec_search_Button_market.setObjectName("spec_search_Button_market")

        self.fifteen_label_market = QtWidgets.QLabel(self.specific_search_tab_market)
        self.fifteen_label_market.setGeometry(QtCore.QRect(120, 220, 21, 16))
        self.fifteen_label_market.setText("15")
        self.fifteen_label_market.setObjectName("fifteen_label_market")
        self.ten_label_market = QtWidgets.QLabel(self.specific_search_tab_market)
        self.ten_label_market.setGeometry(QtCore.QRect(140, 200, 16, 16))
        self.ten_label_market.setText("10")
        self.ten_label_market.setObjectName("ten_label_market")
        self.minus_five_label_market = QtWidgets.QLabel(self.specific_search_tab_market)
        self.minus_five_label_market.setGeometry(QtCore.QRect(80, 180, 21, 16))
        self.minus_five_label_market.setText("-5")
        self.minus_five_label_market.setObjectName("minus_five_label_market")
        self.zero_label_market = QtWidgets.QLabel(self.specific_search_tab_market)
        self.zero_label_market.setGeometry(QtCore.QRect(110, 170, 16, 16))
        self.zero_label_market.setText("0")
        self.zero_label_market.setObjectName("zero_label_market")
        self.five_label_market = QtWidgets.QLabel(self.specific_search_tab_market)
        self.five_label_market.setGeometry(QtCore.QRect(130, 180, 16, 16))
        self.five_label_market.setObjectName("five_label_market")
        self.five_label_market.setText("5")
        self.minus_ten_label_market = QtWidgets.QLabel(self.specific_search_tab_market)
        self.minus_ten_label_market.setGeometry(QtCore.QRect(70, 200, 31, 16))
        self.minus_ten_label_market.setObjectName("minus_ten_label_market")
        self.minus_ten_label_market.setText("-10")
        self.minus_fifteen_label_market = QtWidgets.QLabel(self.specific_search_tab_market)
        self.minus_fifteen_label_market.setGeometry(QtCore.QRect(80, 220, 31, 16))
        self.minus_fifteen_label_market.setText("-15")
        self.minus_fifteen_label_market.setObjectName("minus_fifteen_label_market")

        self.searching_tabwidget_market.addTab(self.specific_search_tab_market, "Specific Search")

        self.free_search_tab_market = QtWidgets.QWidget()
        self.free_search_tab_market.setObjectName("free_search_tab_market")

        self.free_background_market = QtWidgets.QLabel(self.free_search_tab_market)
        self.free_background_market.setGeometry(QtCore.QRect(0, -8, 261, 321))
        self.free_background_market.setText("")
        self.free_background_market.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"search_market_tab_background.png"))
        self.free_background_market.setObjectName("free_background_market")

        self.stocks_comboBox_free_market = QtWidgets.QComboBox(self.free_search_tab_market)
        self.stocks_comboBox_free_market.setGeometry(QtCore.QRect(10, 50, 241, 22))
        self.stocks_comboBox_free_market.setObjectName("stocks_comboBox_free_market")

        stocks_per_indexes = ["3M~DowJones30","APPLE~DowJones30","BOEING~DowJones30","CISCO~DowJones30",
                              "COCA-COLA~DowJones30","HOME DEPOT~DowJones30","INTEL~DowJones30",
                              "JOHNSON & JOHNSON~DowJones30","MCDONALD'S~DowJones30","MICROSOFT ~DowJones30",
                              "NIKE~DowJones30","VISA~DowJones30","WALMART~DowJones30",'ADOBE~Nasdaq100',
                              'ALIGN TECHNOLOGY~Nasdaq100', 'ALPHABET~Nasdaq100','AMAZON.COM~Nasdaq100',
                              'AUTODESK~Nasdaq100', 'Baidu~Nasdaq100','BOOKING HOLDINGS~Nasdaq100',
                              'CHECK POINT~Nasdaq100', 'EBAY~Nasdaq100', 'FACEBOOK~Nasdaq100','FOX CORPORATION~Nasdaq100',
                              'MODERNA~Nasdaq100', 'PAYPAL HOLDINGS~Nasdaq100','UNUM GROUP~S&P500', 'APA CORPORATION~S&P500',
                              'DXC TECHNOLOGY~S&P500', 'CABOT OIL & GAS~S&P500','ALASKA AIR GROUP~S&P500',
                              'JUNIPER NETWORKS~S&P500','MARATHON OIL~S&P500', 'RALPH LAUREN CORPORATION~S&P500',
                              'NRG ENERGY~S&P500', 'HENRY SCHEIN~S&P500', 'EVEREST RE GROUP~S&P500','GDI Services~Russell1000',
                              'KOSMOS ENERGY ~Russell1000', 'WHITING PETROLEUM~Russell1000', 'BGC PARTNERS~Russell1000',
                              'PBF ENERGY~Russell1000', 'DOMTAR CORPORATION~Russell1000','MFA FINANCIAL~Russell1000',
                              'EMPIRE STATE REALTY TRUST.~Russell1000','TWO HARBORS INVESTMENT CORP.~Russell1000',
                              'THE MACERICH COMPANY~Russell1000','SERVICE PROPERTIES TRUST~Russell1000','COLUMBIA PROPERTY TRUST, INC.~Russell1000',
                              'Ultimovacs ASA~Russell1000', 'SM ENERGY COMPANY~Russell1000','BLUEBIRD BIO, INC.~Russell1000',
                              'Transocean Ltd~Russell1000','AMC NETWORKS INC.~Russell1000', 'ECHOSTAR CORPORATION~Russell1000',
                              'BRANDYWINE REALTY TRUST~Russell1000', 'PARAMOUNT GROUP~Russell1000','WELBILT.~Russell1000',
                              'MEDNAX~Russell1000','O-I GLASS~Russell1000', 'UNITI GROUP~Russell1000']

        self.stocks_comboBox_free_market.addItems(stocks_per_indexes)

        self.free_search_Button_market = QtWidgets.QPushButton(self.free_search_tab_market)
        self.free_search_Button_market.setGeometry(QtCore.QRect(90, 290, 75, 21))
        self.free_search_Button_market.setFont(font)
        self.free_search_Button_market.setText("search")
        self.free_search_Button_market.setObjectName("free_search_Button_market")

        self.list_button_free_market = QtWidgets.QRadioButton(self.free_search_tab_market)
        self.list_button_free_market.setGeometry(QtCore.QRect(10, 20, 201, 17))
        self.list_button_free_market.setText("Searching From The List")
        self.list_button_free_market.setObjectName("list_button_free_market")

        self.typed_button_free_market = QtWidgets.QRadioButton(self.free_search_tab_market)
        self.typed_button_free_market.setGeometry(QtCore.QRect(10, 160, 141, 17))
        self.typed_button_free_market.setObjectName("typed_button_free_market")
        self.typed_button_free_market.setText("Free Searching")

        self.typed_lineEdit_free_market = QtWidgets.QLineEdit(self.free_search_tab_market)
        self.typed_lineEdit_free_market.setGeometry(QtCore.QRect(10, 180, 241, 20))
        self.typed_lineEdit_free_market.setObjectName("typed_lineEdit_free_market")
        self.typed_lineEdit_free_market.setText("Tesla")

        self.searching_tabwidget_market.addTab(self.free_search_tab_market, "Free Search")

        self.tabWidget.addTab(self.stock_market, "    Stock market    ")

        # tab 6 -------- stock indexes

        self.stock_index = QtWidgets.QWidget()
        self.background_tab_7 = QtWidgets.QLabel(self.stock_index)
        self.background_tab_7.setGeometry(QtCore.QRect(0, 0, 1031, 611))
        self.background_tab_7.setPixmap(QtGui.QPixmap(PATH_SIMPLE+"stock_index_tab_background.png"))

        font.setBold(True)
        font.setPointSize(10)
        font.setUnderline(False)
        font.setItalic(False)
        font.setWeight(75)

        self.Low_checkBox_in_index_widget = QtWidgets.QCheckBox(self.stock_index)                             # plot settings checkboxes
        self.Low_checkBox_in_index_widget.setGeometry(QtCore.QRect(665, 200, 70, 17))
        self.Low_checkBox_in_index_widget.setFont(font)
        self.Low_checkBox_in_index_widget.setObjectName("Low_checkBox_in_index_widget")
        self.Low_checkBox_in_index_widget.setText("Low")

        self.High_checkBox_in_index_widget = QtWidgets.QCheckBox(self.stock_index)
        self.High_checkBox_in_index_widget.setGeometry(QtCore.QRect(665, 170, 70, 17))
        self.High_checkBox_in_index_widget.setFont(font)
        self.High_checkBox_in_index_widget.setObjectName("High_checkBox_in_index_widget")
        self.High_checkBox_in_index_widget.setText("High")

        self.Close_checkBox_in_index_widget = QtWidgets.QCheckBox(self.stock_index)
        self.Close_checkBox_in_index_widget.setGeometry(QtCore.QRect(720, 200, 70, 17))
        self.Close_checkBox_in_index_widget.setFont(font)
        self.Close_checkBox_in_index_widget.setObjectName("Close_checkBox_in_index_widget")
        self.Close_checkBox_in_index_widget.setText("Close")

        self.Open_checkBox_in_index_widget = QtWidgets.QCheckBox(self.stock_index)
        self.Open_checkBox_in_index_widget.setGeometry(QtCore.QRect(720, 170, 70, 17))
        self.Open_checkBox_in_index_widget.setFont(font)
        self.Open_checkBox_in_index_widget.setObjectName("Open_checkBox_in_index_widget")
        self.Open_checkBox_in_index_widget.setText("Open")

        self.AdjClose_checkBox_in_index_widget = QtWidgets.QCheckBox(self.stock_index)
        self.AdjClose_checkBox_in_index_widget.setGeometry(QtCore.QRect(775, 200, 111, 17))
        self.AdjClose_checkBox_in_index_widget.setFont(font)
        self.AdjClose_checkBox_in_index_widget.setObjectName("AdjClose_checkBox_in_index_widget")
        self.AdjClose_checkBox_in_index_widget.setText("Adj Close")

        self.Volume_checkBox_in_index_widget = QtWidgets.QCheckBox(self.stock_index)
        self.Volume_checkBox_in_index_widget.setGeometry(QtCore.QRect(775, 170, 101, 17))
        self.Volume_checkBox_in_index_widget.setFont(font)
        self.Volume_checkBox_in_index_widget.setObjectName("Volume_checkBox_in_index_widget")
        self.Volume_checkBox_in_index_widget.setText("Volume")

        self.plot_settings_label_in_index_widget = QtWidgets.QLabel(self.stock_index)
        self.plot_settings_label_in_index_widget.setGeometry(QtCore.QRect(700, 140, 151, 16))
        font.setPointSize(11)
        font.setUnderline(True)
        self.plot_settings_label_in_index_widget.setFont(font)
        self.plot_settings_label_in_index_widget.setObjectName("plot_settings_label_in_index_widget")
        self.plot_settings_label_in_index_widget.setText("Plot Settings")

        self.scrollArea = QtWidgets.QScrollArea(self.stock_index)                                               # scroll Area for indexes
        self.scrollArea.setGeometry(QtCore.QRect(10, 230, 1001, 341))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 999, 339))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        font.setUnderline(False)
        font.setItalic(True)
        font.setWeight(70)
        font.setPointSize(10)

        max_date = datetime.date.today()
        min_date = max_date- datetime.timedelta(days=500)

        self.DJIA_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)                         # DJIA index widget
        self.DJIA_widget.setMinimumHeight(150)
        color = self.DJIA_widget.palette()
        color.setColor(self.DJIA_widget.backgroundRole(), Qt.gray)
        self.DJIA_widget.setPalette(color)
        self.DJIA_widget.setAutoFillBackground(Qt.gray)

        self.text_in_DJIA_widget = QtWidgets.QLabel(self.DJIA_widget)
        self.text_in_DJIA_widget.setGeometry(QtCore.QRect(10, 10, 591, 130))
        self.text_in_DJIA_widget.setFont(font)
        self.text_in_DJIA_widget.setText("Dow Jones\n\n"
                                         "The Dow Jones Industrial Average groups together the\n"
                                         "prices of 30 of the most traded stocks on the\n"
                                         "New York Stock Exchange ( NYSE ) and the Nasdaq.\n"
                                         "The DJIA contain shares from 3M, IBM, Microsoft, Apple,\n"
                                         "Visa, Boeing, Walmart, Coca-Cola and more . . . ")

        self.start_dateEdit_in_DJIA_widget = QtWidgets.QDateEdit(self.DJIA_widget)
        self.start_dateEdit_in_DJIA_widget.setGeometry(QtCore.QRect(610, 40, 110, 22))
        self.start_dateEdit_in_DJIA_widget.setFont(font)
        self.start_dateEdit_in_DJIA_widget.setMaximumDate(max_date)
        self.start_dateEdit_in_DJIA_widget.setMinimumDate(min_date)

        self.end_label_in_DJIA_widget = QtWidgets.QLabel(self.DJIA_widget)
        self.end_label_in_DJIA_widget.setGeometry(QtCore.QRect(740, 40, 110, 22))
        self.end_label_in_DJIA_widget.setFont(font)
        self.end_label_in_DJIA_widget.setText(str(max_date))

        self.plot_button_in_DJIA_widget = QtWidgets.QPushButton(self.DJIA_widget)
        self.plot_button_in_DJIA_widget.setGeometry(QtCore.QRect(870, 12, 91, 51))
        self.plot_button_in_DJIA_widget.setFont(font)
        self.plot_button_in_DJIA_widget.setText("PLOT")

        self.start_end_label_in_DJIA_widget = QtWidgets.QLabel(self.DJIA_widget)
        self.start_end_label_in_DJIA_widget.setGeometry(QtCore.QRect(610, 20, 241, 16))
        self.start_end_label_in_DJIA_widget.setFont(font)
        self.start_end_label_in_DJIA_widget.setText("start              end")

        self.verticalLayout.addWidget(self.DJIA_widget)



        self.NDAQ_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)                         # NDAQ index widget
        self.NDAQ_widget.setMinimumHeight(150)


        self.text_in_NDAQ_widget = QtWidgets.QLabel(self.NDAQ_widget)
        self.text_in_NDAQ_widget.setGeometry(QtCore.QRect(10, 10, 591, 130))
        self.text_in_NDAQ_widget.setFont(font)
        self.text_in_NDAQ_widget.setText("Nasdaq Index\n\n"
                                         "The Nasdaq Index groups together the\n"
                                         "prices of over 100 of the most traded stocks\n"
                                         "on the Nasdaq stock exchange.\n"
                                         "The NDAQ contain shares from Cisco, Intel,\n"
                                         "Facebook, Alphabet, Amazon, Apple, Microsoft and more . . .")

        self.start_dateEdit_in_NDAQ_widget = QtWidgets.QDateEdit(self.NDAQ_widget)
        self.start_dateEdit_in_NDAQ_widget.setGeometry(QtCore.QRect(610, 40, 110, 22))
        self.start_dateEdit_in_NDAQ_widget.setFont(font)
        self.start_dateEdit_in_NDAQ_widget.setMaximumDate(max_date)
        self.start_dateEdit_in_NDAQ_widget.setMinimumDate(min_date)

        self.end_label_in_NDAQ_widget = QtWidgets.QLabel(self.NDAQ_widget)
        self.end_label_in_NDAQ_widget.setGeometry(QtCore.QRect(740, 40, 110, 22))
        self.end_label_in_NDAQ_widget.setFont(font)
        self.end_label_in_NDAQ_widget.setText(str(max_date))

        self.plot_button_in_NDAQ_widget = QtWidgets.QPushButton(self.NDAQ_widget)
        self.plot_button_in_NDAQ_widget.setGeometry(QtCore.QRect(870, 12, 91, 51))
        self.plot_button_in_NDAQ_widget.setFont(font)
        self.plot_button_in_NDAQ_widget.setText("PLOT")

        self.start_end_label_in_NDAQ_widget = QtWidgets.QLabel(self.NDAQ_widget)
        self.start_end_label_in_NDAQ_widget.setGeometry(QtCore.QRect(610, 10, 241, 16))
        self.start_end_label_in_NDAQ_widget.setFont(font)
        self.start_end_label_in_NDAQ_widget.setText("start              end")

        self.verticalLayout.addWidget(self.NDAQ_widget)


        self.Russell_1000_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)         # Russell 1000 index widget
        self.Russell_1000_widget.setMinimumHeight(150)
        color = self.Russell_1000_widget.palette()
        color.setColor(self.Russell_1000_widget.backgroundRole(), Qt.gray)
        self.Russell_1000_widget.setPalette(color)
        self.Russell_1000_widget.setAutoFillBackground(Qt.gray)
        self.Russell_1000_widget.setAutoFillBackground(Qt.gray)

        self.text_in_Russell_1000_widget = QtWidgets.QLabel(self.Russell_1000_widget)
        self.text_in_Russell_1000_widget.setGeometry(QtCore.QRect(10, 10, 591, 130))
        self.text_in_Russell_1000_widget.setFont(font)
        self.text_in_Russell_1000_widget.setText("Russell 1000\n\n"
                                                "The Russell 1000 Index groups together the\n"
                                                "prices of 1000 that are available to private traders on USA.\n"
                                                "The Russell 1000 contain shares from Index Microsof, Apple\n"
                                                "Amazon, Facebook, Alphabet, Johnson & Johnson and more")


        self.start_dateEdit_in_Russell_1000_widget = QtWidgets.QDateEdit(self.Russell_1000_widget)
        self.start_dateEdit_in_Russell_1000_widget.setGeometry(QtCore.QRect(610, 40, 110, 22))
        self.start_dateEdit_in_Russell_1000_widget.setFont(font)
        self.start_dateEdit_in_Russell_1000_widget.setMaximumDate(max_date)
        self.start_dateEdit_in_Russell_1000_widget.setMinimumDate(min_date)

        self.end_label_in_Russell_1000_widget = QtWidgets.QLabel(self.Russell_1000_widget)
        self.end_label_in_Russell_1000_widget.setGeometry(QtCore.QRect(740, 40, 110, 22))
        self.end_label_in_Russell_1000_widget.setFont(font)
        self.end_label_in_Russell_1000_widget.setText(str(max_date))

        self.plot_button_in_Russell_1000_widget = QtWidgets.QPushButton(self.Russell_1000_widget)
        self.plot_button_in_Russell_1000_widget.setGeometry(QtCore.QRect(870, 12, 91, 51))
        self.plot_button_in_Russell_1000_widget.setFont(font)
        self.plot_button_in_Russell_1000_widget.setText("PLOT")

        self.start_end_label_in_Russell_1000_widget = QtWidgets.QLabel(self.Russell_1000_widget)
        self.start_end_label_in_Russell_1000_widget.setGeometry(QtCore.QRect(610, 10, 241, 16))
        self.start_end_label_in_Russell_1000_widget.setFont(font)
        self.start_end_label_in_Russell_1000_widget.setText("start              end")

        self.verticalLayout.addWidget(self.Russell_1000_widget)

        self.VIX_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)                          # VIX index widget
        self.VIX_widget.setMinimumHeight(150)

        self.text_in_VIX_widget = QtWidgets.QLabel(self.VIX_widget)
        self.text_in_VIX_widget.setGeometry(QtCore.QRect(10, 10, 591, 130))
        self.text_in_VIX_widget.setFont(font)
        self.text_in_VIX_widget.setText("VIX\n\n"
                                        "The Volatility Index is a market index\n"
                                        "representing the market's expectations for volatility\n"
                                        "in S&P index. ")

        self.start_dateEdit_in_VIX_widget = QtWidgets.QDateEdit(self.VIX_widget)
        self.start_dateEdit_in_VIX_widget.setGeometry(QtCore.QRect(610, 40, 110, 22))
        self.start_dateEdit_in_VIX_widget.setFont(font)
        self.start_dateEdit_in_VIX_widget.setMaximumDate(max_date)
        self.start_dateEdit_in_VIX_widget.setMinimumDate(min_date)

        self.end_label_in_VIX_widget = QtWidgets.QLabel(self.VIX_widget)
        self.end_label_in_VIX_widget.setGeometry(QtCore.QRect(740, 40, 110, 22))
        self.end_label_in_VIX_widget.setFont(font)
        self.end_label_in_VIX_widget.setText(str(max_date))

        self.plot_button_in_VIX_widget = QtWidgets.QPushButton(self.VIX_widget)
        self.plot_button_in_VIX_widget.setGeometry(QtCore.QRect(870, 12, 91, 51))
        self.plot_button_in_VIX_widget.setFont(font)
        self.plot_button_in_VIX_widget.setText("PLOT")

        self.start_end_label_in_VIX_widget = QtWidgets.QLabel(self.VIX_widget)
        self.start_end_label_in_VIX_widget.setGeometry(QtCore.QRect(610, 10, 241, 16))
        self.start_end_label_in_VIX_widget.setFont(font)
        self.start_end_label_in_VIX_widget.setText("start              end")

        self.verticalLayout.addWidget(self.VIX_widget)

        self.SP_500_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)                # S&P 500 index widget
        self.SP_500_widget.setMinimumHeight(150)
        color = self.SP_500_widget.palette()
        color.setColor(self.SP_500_widget.backgroundRole(), Qt.gray)
        self.SP_500_widget.setPalette(color)
        self.SP_500_widget.setAutoFillBackground(Qt.gray)
        self.SP_500_widget.setAutoFillBackground(Qt.gray)

        self.text_in_SP_500_widget = QtWidgets.QLabel(self.SP_500_widget)
        self.text_in_SP_500_widget.setGeometry(QtCore.QRect(10, 10, 591, 130))
        self.text_in_SP_500_widget.setFont(font)
        self.text_in_SP_500_widget.setText("S&P 500\n\n"
                                           "The S&P 500 Index groups together the\n"
                                           "prices of 500 large companies stocks in United States.\n"
                                           "The S&P 500 contain shares from Berkshire Hathaway,\n"
                                           "Facebook, Microsoft, Johnson & Johnson, Amazon and more . . .")

        self.start_dateEdit_in_SP_500_widget = QtWidgets.QDateEdit(self.SP_500_widget)
        self.start_dateEdit_in_SP_500_widget.setGeometry(QtCore.QRect(610, 40, 110, 22))
        self.start_dateEdit_in_SP_500_widget.setFont(font)
        self.start_dateEdit_in_SP_500_widget.setMaximumDate(max_date)
        self.start_dateEdit_in_SP_500_widget.setMinimumDate(min_date)

        self.end_label_in_SP_500_widget = QtWidgets.QLabel(self.SP_500_widget)
        self.end_label_in_SP_500_widget.setGeometry(QtCore.QRect(740, 40, 110, 22))
        self.end_label_in_SP_500_widget.setFont(font)
        self.end_label_in_SP_500_widget.setText(str(max_date))

        self.plot_button_in_SP_500_widget = QtWidgets.QPushButton(self.SP_500_widget)
        self.plot_button_in_SP_500_widget.setGeometry(QtCore.QRect(870, 12, 91, 51))
        self.plot_button_in_SP_500_widget.setFont(font)
        self.plot_button_in_SP_500_widget.setText("PLOT")

        self.start_end_label_in_SP_500_widget = QtWidgets.QLabel(self.SP_500_widget)
        self.start_end_label_in_SP_500_widget.setGeometry(QtCore.QRect(610, 10, 241, 16))
        self.start_end_label_in_SP_500_widget.setFont(font)
        self.start_end_label_in_SP_500_widget.setText("start              end")

        self.verticalLayout.addWidget(self.SP_500_widget)

        self.tabWidget.addTab(self.stock_index, "     indexes     ")

        # finish

        self.stackedWidget.addWidget(self.inside_page)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1042, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
