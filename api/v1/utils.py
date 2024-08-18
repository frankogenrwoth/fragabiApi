import random


def get_n_random_elements_from_list(n, upper):
    selected = []

    print(n, upper)

    if n > upper:
        return selected


    while len(selected) <= n:
        selected_random_number = random.randint(1, upper)
        if selected_random_number not in selected:
            selected.append(selected_random_number)

    return selected