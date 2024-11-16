import requests
import networkx as nx
import matplotlib.pyplot as plt
import itertools

def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ripple,cardano,bitcoin-cash,eos,litecoin,ethereum,bitcoin&vs_currencies=xrp,ada,bch,eos,ltc,eth,btc"
    response = requests.get(url)
    data = response.json()

    # Print the data for debugging purposes
    print(data)

    # Return the fetched data
    return data

def build_graph(data):
    g = nx.DiGraph()

    # Fetch the relevant exchange rates between cryptocurrencies
    cryptos = ['ripple', 'cardano', 'bitcoin-cash', 'eos', 'litecoin', 'ethereum', 'bitcoin']
    currencies = ['xrp', 'ada', 'bch', 'eos', 'ltc', 'eth', 'btc']

    # Add edges for each pair of cryptocurrencies with their exchange rate
    for crypto1, currency1 in zip(cryptos, currencies):
        for crypto2, currency2 in zip(cryptos, currencies):
            if crypto1 != crypto2:
                rate1_to_2 = 1 / data[crypto2][currency1] if currency1 in data[crypto2] else None
                rate2_to_1 = 1 / data[crypto1][currency2] if currency2 in data[crypto1] else None
                
                if rate1_to_2:
                    g.add_weighted_edges_from([(currency1, currency2, rate1_to_2)])

                if rate2_to_1:
                    g.add_weighted_edges_from([(currency2, currency1, rate2_to_1)])

    return g

def find_paths(graph, start, end):
    # Find all paths between start and end nodes
    paths = list(nx.all_simple_paths(graph, source=start, target=end))
    
    # Calculate the weight of each path
    weighted_paths = []
    for path in paths:
        weight = 1
        for i in range(len(path) - 1):
            weight *= graph[path[i]][path[i + 1]]['weight']
        weighted_paths.append((path, weight))
    
    return weighted_paths

def main():
    # Fetch the data from the API
    data = fetch_crypto_prices()

    # Build the graph based on the data
    g = build_graph(data)

    # Define start and end nodes for path search
    start_node = 'ltc'
    end_node = 'eth'

    # Find all paths and their weights
    weighted_paths = find_paths(g, start_node, end_node)

    # Output in the requested format
    print(f"paths from {start_node} to {end_node} ----------------------------------")
    for path, weight in weighted_paths:
        print(f"{path} {weight}")

    # Find the smallest and largest path weights
    if weighted_paths:
        smallest_weight = min(weighted_paths, key=lambda x: x[1])
        largest_weight = max(weighted_paths, key=lambda x: x[1])

        # Output in the requested format
        print("\nSmallest Paths weight factor:", smallest_weight[1])
        print("Paths:", smallest_weight[0], smallest_weight[0][::-1])  # Reverse the path for the reverse route

        print("\nGreatest Paths weight factor:", largest_weight[1])
        print("Paths:", largest_weight[0], largest_weight[0][::-1])  # Reverse the path for the reverse route

        # Additional formatting to match the example output
        print("\n")
        print(f"paths from {start_node} to {end_node} ----------------------------------")
        for path, weight in weighted_paths:
            print(f"{path} {weight}")

    # Plotting the graph with a circular layout and weights as edge labels
    pos = nx.circular_layout(g)  # Using circular layout to make nodes equidistant
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw(g, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
    plt.title("Cryptocurrency Network with Exchange Rates (Equidistant Layout)")
    plt.show()

if __name__ == "__main__":
    main()
