def create_rules(lhs, rhs):
    rhs = rhs.split(' | ')
    rules = dict()
    for product in rhs:
        rules[product.strip()] = lhs
    return rules


def load_grammar(file_path):
    with open(file_path, 'r') as file:
        data = file.read().split('\n')
    result = dict()
    for line in data:
        rule = line.split('->')
        lhs = rule[0].strip()
        rhs = rule[1]

        rules = create_rules(lhs, rhs)
        result.update(rules)
    return result
