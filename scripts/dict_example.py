from pprint import pprint

example_node_list = [
    [1,5],
    [1,4], [5,4],
    [1,3], [3,3], [5,3], [8,3],
    [1,2], [2,2], [3,2], [4,2], [5,2], [6,2], [7,2], [8,2], [9,2],
    [1,1], [2,1], [3,1], [4,1], [5,1], [6,1], [7,1], [8,1], [9,1], [10,1],
]

# print('Example Node List')
# print(example_node_list)

node_dict = {}

for node in example_node_list:

    measure_number, level = node[0], node[1]

    if level in node_dict:
        node_dict[level].append(measure_number)
    else:
        node_dict[level] = [measure_number]


print('\nDict with Measures by Level')
pprint(node_dict)