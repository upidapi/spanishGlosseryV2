import tkfilebrowser


# temporary implementation
# todo implement a custom file selector
def ask_select(initial_dir, amount='multiple'):
    print('asd')
    selected_directories = []

    if amount == 'multiple':
        selected_directories = tkfilebrowser.askopenfilenames(initialdir=initial_dir, title='select')
    elif amount == 'singular':
        selected_directories = tkfilebrowser.askopenfilename(initialdir=initial_dir, title='select')

    return selected_directories
