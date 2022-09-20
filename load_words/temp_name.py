import get_data as data_fetcher
import clean_up_word as filter


def get_data(select):
    # example parameters
    filter.Split(';')
    filter.RemoveBetween('(', ')')
    filter.RemoveBetween('/', '/')
    filter.RemoveX('ung.')

    all_data = data_fetcher.get(select)
    for i, pair in enumerate(all_data):
        for j, word in enumerate(pair):
            all_data[i][j] = filter.clean(word)

    return filter.find_alternative_translations(all_data)


print(get_data('multiple'), 'ds')
