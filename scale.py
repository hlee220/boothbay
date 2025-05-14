from collections import OrderedDict

class Weight:
    def __init__(self, weight):
        self.weight = weight

    def balance_scale(self, extra_weights):
        return self.weight

class Scale:
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right
        self.weight = 1

    def balance_scale(self, extra_weights):
        left_weight = self.left.balance_scale(extra_weights)
        right_weight = self.right.balance_scale(extra_weights)

        extra_weights[self.name] = (max(right_weight-left_weight, 0), max(left_weight-right_weight, 0))
        return max(left_weight, right_weight)*2 + self.weight
    
def read_input(filename):
    # Assume input data is a valid tree
    input_dict = OrderedDict()
    all_children = set()
    with open("System.in") as f:
        for line in f.readlines():
            if not line.startswith('#'):
                node, left, right = line.rstrip().split(',')
                input_dict[node] = (left, right)
                all_children.add(left)
                all_children.add(right)

    # head is the node that is not a child of any other node
    head = None
    for node in input_dict:
        if node not in all_children:
            head = node

    # build binary tree
    def create_scale(parent_name, input_dict):
        if parent_name[0].isalpha():
            left, right = input_dict[parent_name]
            return Scale(parent_name, create_scale(left, input_dict), create_scale(right, input_dict))
        else:
            return Weight(int(parent_name))

    return (input_dict, create_scale(head, input_dict))

if __name__ == "__main__":
    input_dict, head_scale = read_input("System.in")

    extra_weights = {}
    total = head_scale.balance_scale(extra_weights)

    with open("System.out", "w") as f:
        # Assume input order is already in alhpabetical order
        for name in input_dict:
            if name[0].isalpha():
                weight = extra_weights[name]
                print(f"{name},{weight[0]},{weight[1]}", file=f)
