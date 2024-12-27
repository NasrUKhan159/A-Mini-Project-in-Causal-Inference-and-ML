from causallearn.search.ConstraintBased.PC import pc
from data_processing import process_data

if __name__ == "__main__":
    data_filtered_nodate = process_data()
    # extract the numeric columns
    data_filtered_nodate_numeric = data_filtered_nodate[
        ['Adj_Close_VYM', 'Volume_VYM', 'Adj_Close_XGIU_L', 'Volume_XGIU_L']]

    labels = [f'{col}' for i, col in enumerate(data_filtered_nodate_numeric.columns)]
    data = data_filtered_nodate_numeric.to_numpy()

    cg = pc(data)

    # indices 0-3 are: 'Adj_Close_VYM', 'Volume_VYM', 'Adj_Close_XGIU_L', 'Volume_XGIU_L'
    # cg.G.graph[j,i]=1 and cg.G.graph[i,j]=-1 indicate i –> j;
    # cg.G.graph[i,j] = cg.G.graph[j,i] = -1 indicate i — j;
    # cg.G.graph[i,j] = cg.G.graph[j,i] = 1 indicates i <-> j.
    # ref: https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html
    connections = {}
    for i in range(cg.G.graph.shape[0]):
        for j in range(cg.G.graph.shape[1]):
            if cg.G.graph[j, i] == 1 and cg.G.graph[i, j] == -1:
                connections[i, j] = 'i_to_j'
            elif cg.G.graph[i, j] == cg.G.graph[j, i] == -1:
                connections[i, j] = 'no_dir_conn_betw_i_j'
            elif cg.G.graph[i, j] == cg.G.graph[j, i] == 1:
                connections[i, j] = 'i_to_j_and_j_to_i'
    print(connections)