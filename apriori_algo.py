import numpy as np


def load_transactions(path, order):
    ''' Creates transactions as a list of lists - each of the inner lists represents specific invoice'''
    transactions = []
    with open(path, 'r') as file:
        for line in file:
            str_line = line.strip().split(',')
            temp = list(np.unique(str_line))
            temp.sort(key=lambda x: order.index(x))
            transactions.append(temp)
    return transactions


# def load_transactions(arr, order):
#     transactions = []
#     for line in arr:
#             str_line = line.split(',')
#             temp = list(np.unique(str_line))
#             temp.sort(key=lambda x: order.index(x))
#             transactions.append(temp)
#     return transactions


def count_occurences(itemset, transactions):
    '''
    Function counts how many times the itemset occurs in transactions
    '''
    count = 0
    for i in range(len(transactions)):
        if set(itemset).issubset(set(transactions[i])):
            count +=1
    return count


def join_two_itemsets(it1,it2, order):
    '''
    Joining algorithm compares particular itemsets, when conditions met
    -> create +1 size itemset
    '''
    it1.sort(key=lambda x: order.index(x))
    it2.sort(key=lambda x: order.index(x))

    for i in range(len(it1)-1):
        if it1[i] != it2[i]:
            return []

    if order.index(it1[-1]) < order.index(it2[-1]):
        return it1 + [it2[-1]]

    return []


def join_set_itemsets(set_of_itemsets, order):
    '''
    Function outputs candidate set of itemsets; has function that determines if two itemsets can be joined
    '''
    C = []
    for i in range(len(set_of_itemsets)):
        for j in range(i+1, len(set_of_itemsets)):
            it_out = join_two_itemsets(set_of_itemsets[i], set_of_itemsets[j], order)
            if len(it_out) > 0:
                C.append(it_out)
    return C


def get_frequent(itemsets, transactions, min_support, prev_discarded):
    '''Function outputs list frequent itemsets having frequency above threshold;
    list of support counts of frequent itemsets (same ordering !!);
    list of discarded itemsets (not meeting minimal threshold)
    '''
    L = []
    supp_count = []
    new_discarded = []

    k = len(prev_discarded.keys())

    for s in range(len(itemsets)):
        discarded_before = False
        if k > 0:
            for it in prev_discarded[k]:
                if set(it).issubset(set(itemsets[s])):
                    discarded_before = True
                    break

        if not discarded_before:
            count = count_occurences(itemsets[s], transactions)
            if count/len(transactions) >= min_support:
                L.append(itemsets[s])
                supp_count.append(count)
            else:
                new_discarded.append(itemsets[s])

    return L, supp_count, new_discarded


def print_table(T, supp_count):
    print('Itemsets | Frequency')
    for k in range(len(T)):
        print(f'{T[k]} : {supp_count[k]}')
    print('\n\n')