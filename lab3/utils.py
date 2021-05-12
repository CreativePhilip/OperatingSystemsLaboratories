def get_min_from_arr(arr):
    smallest = arr[0]

    for i in arr:
        if i < smallest:
            smallest = i

    return smallest


def least_used_in_the_future(idx, arr, cache):
    use_stat = {}
    for item in arr[idx:]:
        if item in use_stat:
            use_stat[item] += 1
        else:
            use_stat[item] = 1

    min_use = use_stat.get(cache[0], 0)
    min_item = cache[0]
    for item in cache:
        use_amount = use_stat.get(item, 0)
        if use_amount < min_use:
            min_use = use_amount
            min_item = item

    return min_item
