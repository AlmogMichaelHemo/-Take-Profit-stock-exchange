import pandas as pd
import matplotlib.pyplot as plt
import pickle, struct, os

PATH_EXCEL = "C:\\Users\\User\\Desktop\\TPclient_folder\\"


def delete_a_file(file_name):
    """
    Try to delete a csv file after it was used for create matplotlib window
    """
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
        except Exception as ex:
            print(ex)


def ask_for_stock_excel(client, ticker_name, start_date, end_date, plot_check_boxes):
    """
    Ask for excel file with the stock history
    """
    try:
        list_to_server = (ticker_name, start_date.toPyDate(), end_date)
    except:
        list_to_server = (ticker_name, start_date, end_date)
    client.send("stock_excel".encode())
    client.send(pickle.dumps(list_to_server))

    data = b""
    size = struct.calcsize('>Q')
    while len(data) < size:
        data += client.recv(1024)
    packed_size = data[:size]
    data = data[size:]
    actual_size = struct.unpack('>Q', packed_size)[0]
    while len(data) < actual_size:
        data += client.recv(1024)
    data = data[:actual_size]
    with open(PATH_EXCEL + ticker_name + '.csv', 'wb') as f:
        f.write(data)
    plot_parameters_list = get_plot_parameters_list(plot_check_boxes)

    open_a_plot_func(PATH_EXCEL + ticker_name + '.csv', ticker_name, plot_parameters_list)


def get_plot_parameters_list(bool_list):
    """
    Get the client boolean list from the checkboxes and return the plot parameters list
    """
    plot_possible_parameters_list = ['High','Low','Open','Close','Adj Close','Volume']
    parameters_list = []

    for i in range(len(plot_possible_parameters_list)):
        if bool_list[i]:
            parameters_list.append(plot_possible_parameters_list[i])

    if not parameters_list:
        parameters_list.append('Adj Close')

    return parameters_list


def open_a_plot_func(path, title, plot_parameters):
    """
    Get a path for excel file, title and the plot parameters and open it with matplotlib graph.
    After opening the matplotlib graph the function delete the excel file.
    """
    data_frame = pd.read_csv(path, parse_dates= True, index_col =0)
    data_frame[plot_parameters].plot()
    plt.xlabel("Date")
    plt.ylabel("USD")
    plt.title(title)
    plt.show()

    delete_a_file(path)