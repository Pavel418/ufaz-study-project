import matplotlib
import matplotlib.pyplot as plt

data = []
with open('cleared.csv', 'r') as f:
    data = f.read().splitlines()

# first row is the header
header = data[0].split(',')
# remove the header from the data
data = data[1:]
# split the data into rows
data = [row.split(',') for row in data]
secret_variable_count3 = len(data)
# select where city starts with 'Bak'
col_city = header.index('city')
data = [row for row in data if row[col_city].startswith('Bak')]
secret_variable_count1 = len(data)
# select where price is less than 500000
col_price = header.index('price')
data = [row for row in data if (float(row[col_price]) < 500000 and float(row[col_price]) > 20000)]
secret_variable_count2 = len(data)
print(secret_variable_count2, "/", secret_variable_count1, '/', secret_variable_count3)
print("This covers", round(secret_variable_count2/secret_variable_count1*100, 3), "% of the data in Baku")
print("Tihs covers", round(secret_variable_count2/secret_variable_count3*100, 3), "% of the data in Azerbaijan")
print("There are", round(secret_variable_count1/secret_variable_count3*100, 3), "% of the data in Baku across Azerbaijan")
col_room_count = header.index('Otaq sayД±')
col_cur_floor = header.index('current_floor')
col_total_floor = header.index('max_floor')
col_area = header.index('SahЙ™')
# select where area is less than 10000
data = [row for row in data if float(row[col_area]) < 10000]
# get the index of the column we want to graph
col_lat = header.index('latitude')
col_long = header.index('longitude')

# get the data for the column we want to graph
col_data_price = [float(row[col_price]) for row in data]
col_data_lat = [float(row[col_lat]) for row in data]
col_data_long = [float(row[col_long]) for row in data]
col_data_room_count = [float(row[col_room_count]) for row in data]
col_data_cur_floor = [float(row[col_cur_floor]) for row in data]
col_data_total_floor = [float(row[col_total_floor]) for row in data]
col_data_area = [float(row[col_area]) for row in data]

def make_map():
    # create map like graph, where x is longtitude and y is latitude and color is price
    plt.scatter(col_data_long, col_data_lat, c=col_data_price, cmap='RdYlGn', alpha=0.2, s=40, norm=matplotlib.colors.LogNorm())
    plt.colorbar()
    plt.show()

def make_graph_price_long():
    global col_data_long
    # create graph where x is longtitude and y is price
    # price is mean of all prices in the area (+- 0.1)
    col_data_long = [round(i, 2) for i in col_data_long]
    make_graph(col_data_long, col_data_price)

def make_graph_price_lat():
    global col_data_lat
    # create graph where x is latitude and y is price
    # price is mean of all prices in the area (+- 0.1)
    col_data_lat = [round(i, 2) for i in col_data_lat]
    make_graph(col_data_lat, col_data_price)

def make_3d_graph_price_long_lat():
    # create 3d graph where x is longtitude, y is latitude and z is price
    # price is mean of all prices in the area (+- 0.1)
    dict_price = {}
    dict_quantity = {}
    for i in range(len(col_data_long)):
        col_data_long[i] = round(col_data_long[i], 2)
        col_data_lat[i] = round(col_data_lat[i], 2)
        if (col_data_long[i], col_data_lat[i]) in dict_price:
            dict_price[(col_data_long[i], col_data_lat[i])] += col_data_price[i]
            dict_quantity[(col_data_long[i], col_data_lat[i])] += 1
        else:
            dict_price[(col_data_long[i], col_data_lat[i])] = col_data_price[i]
            dict_quantity[(col_data_long[i], col_data_lat[i])] = 1
    for key in dict_price:
        dict_price[key] /= dict_quantity[key]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # make list of 1st and 2nd element of dict_price keys
    # 1st element is longtitude, 2nd element is latitude
    list_long = [list(dict_price.keys())[i][0] for i in range(len(dict_price))]
    list_lat = [list(dict_price.keys())[i][1] for i in range(len(dict_price))]
    ax.bar3d(list_long, list_lat, 0, 0.005, 0.005, list(dict_price.values()), alpha=0.4)
    plt.show()

def make_graph_price_room_count():
    # create graph where x is room count and y is price
    make_graph(col_data_room_count, col_data_price)

def make_graph_price_current_floor():
    make_graph(col_data_cur_floor, col_data_price)

def make_graph_price_total_floor():
    make_graph(col_data_total_floor, col_data_price)

def make_graph(list1: list, list2: list):
    dict_price = {}
    dict_quantity = {}
    for i in range(len(list1)):
        if list1[i] in dict_price:
            dict_price[list1[i]] += list2[i]
            dict_quantity[list1[i]] += 1
        else:
            dict_price[list1[i]] = list2[i]
            dict_quantity[list1[i]] = 1
    for key in dict_price:
        dict_price[key] /= dict_quantity[key]
    plt.bar(dict_price.keys(), dict_price.values(), align='edge', width=0.5)
    for i in range(len(dict_price)):
        # write the price on the bar without decimal places
        plt.text(list(dict_price.keys())[i], list(dict_price.values())[i], str(int(list(dict_price.values())[i])), ha='center', va='bottom')
    plt.show()

def make_graph_price_area():
    global col_data_area
    # approximate area to 10m^2
    col_data_area = [round(i/10)*10 for i in col_data_area]
    make_graph(col_data_area, col_data_price)

make_graph_price_area()
