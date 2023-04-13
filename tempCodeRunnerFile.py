
   # for i in range(len(dict_price)):
        # write the price on the bar without decimal places
        #plt.text(list(dict_price.keys())[i], list(dict_price.values())[i], str(int(list(dict_price.values())[i])), ha='center', va='bottom')
    plt.show()

def make_graph_price_area():
    global col_data_area
    # approximate area to 10m^2
    col_data_area = [round(i/10)*10 for i in col_data_area]
    make_graph(col_data_area, col_data_price)

def make_graph_price_distance():
    global col_data_distance
    # approximate area to 10m^2
    col_data_distance = [round(i/100)*100 for i in col_data_distance]
    #make_graph(col_data_distance, col_data_price)
    make_graph_scatter(col_data_distance, col_data_price)

make_graph_price_distance()