import requests
import json
from PIL import Image
import tkfilebrowser

from FixRawInput.helper_funcs import get_line_bounding_box


def get_data_from_image(filename, language='eng'):
    """
    OCR.space API requests with local file.

    :param filename: Your file path & name.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    api_key = "K85003833988957"

    payload = {'isOverlayRequired': True,
               'apikey': api_key,
               'language': language,
               'scale': True
               }

    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )

    # decode
    return_data = r.content.decode()
    # from json-str to python-array
    return_data = json.loads(return_data)
    return return_data


def clean_up_data(dirty_data):
    """
    converts the raw return data into a better format

    :param dirty_data: the raw json data
    :return: a cleaner version of the data
    """
    clean_data = []

    # data format
    # [
    #     {
    #         'text': 'the lines text',
    #
    #         'x': 'x position (int)',
    #         'y': 'y position (int)',
    #         'width': 'width (int)',
    #         'height': 'height (int)'
    #     },
    #
    #     ...
    # ]

    for line in dirty_data["ParsedResults"][0]["TextOverlay"]["Lines"]:
        line_pos = get_line_bounding_box(line)

        line_data = {
            'text': line['LineText'],

            'x': line_pos[0],
            'y': line_pos[1],
            'width': line_pos[2],
            'height': line_pos[3]
        }

        clean_data.append(line_data)

    return clean_data


def get_existence(item, lis):
    for word in lis:
        # full match
        if item['x'] == word['x'] and \
                item['y'] == word['y'] and \
                item['width'] == word['width'] and \
                item['height'] == word['height']:
            return None

    for word in lis:
        # start match
        if item['x'] == word['x'] and \
                item['y'] == word['y'] and \
                item['height'] == word['height']:
            # sets the word to the longest
            if item['width'] < word['width']:
                return word

            # if you can't set it now prevent it from appending it
            return None

        # end match
        elif item['x'] + item['width'] == word['x'] + word['width'] and \
                item['y'] == word['y'] and \
                item['height'] == word['height']:
            # sets the word to the longest
            if item['width'] < word['width']:
                return word

            # if you can't set it now prevent it from appending it
            return None

    return 'NaN'


def get_missing_words(lan1, lan2):
    for i, word in enumerate(lan1):
        ret = get_existence(word, lan2)
        if ret is not None:
            if ret == 'NaN':
                lan2.append(word)
            else:
                lan1[i] = ret

    for i, word in enumerate(lan2):
        ret = get_existence(word, lan1)
        if ret is not None:
            if ret == 'NaN':
                lan1.append(word)
            else:
                lan2[i] = ret

    return lan1, lan2


def new_image(select_image, lan):
    files = [r'..\tinker_convert\data\lan1_data.json', r'..\tinker_convert\data\lan2_data.json']

    # crops it due to the 1k x 1k limit from the api
    image = Image.open(select_image)
    image.thumbnail((1000, 1000))

    image.save(r'..\tinker_convert\data\selected_image.jpg')

    # gets the data and cleans up the data format
    clean_data = []
    for i in range(2):
        json_data = get_data_from_image(r'..\tinker_convert\data\selected_image.jpg', language=lan[i])
        clean_data.append(clean_up_data(json_data))

    # add some missing words
    fixed_data = get_missing_words(*clean_data)

    # saves the data
    for i in range(2):
        fixed_data[i].sort(key=lambda x: x['y'])

        # converts python-array to json-document with indent 4
        json_object = json.dumps(fixed_data[i], indent=4)
        with open(files[i], "w") as outfile:
            outfile.write(json_object)
            
    return fixed_data


def get():
    def _get_data(file):
        # gets the data
        with open(file) as jsonFile:
            json_object = json.load(jsonFile)
            jsonFile.close()

        return json_object

    data_1 = _get_data(r'..\tinker_convert\data\lan1_data.json')
    data_2 = _get_data(r'..\tinker_convert\data\lan2_data.json')

    return data_1, data_2


def debug(select_image):
    """
    format:
    lan_1_word  lan_2_word     lan_1_word  lan_2_word
    lan_1_word  lan_2_word     lan_1_word  lan_2_word
    lan_1_word  lan_2_word     lan_1_word  lan_2_word

    languishes = lan_1_word, lan_2_word
    """

    languishes = 'spa', 'swe'

    test_images = {
        "eng_text_page": r"C:\Users\videw\Downloads\book page.jpg",
        "spa_text_glossary_rotated": r"C:\Users\videw\Downloads\IMG_2439.jpg",
        "spa_text_glossary_perfect": r"C:\Users\videw\Downloads\IMG_2438.jpg",
        "spa_text_glossary_imperfect": r"C:\Users\videw\Downloads\IMG_2421.png"
    }

    select_image = test_images[select_image] if select_image in test_images else select_image

    new_image(select_image, languishes)


def save_data(data):
    selected_directories = tkfilebrowser.askopenfilename(initialdir=r"../load_words/words/", title='select')

    # converts python-array to json-document with indent 4
    json_object = json.dumps(data, indent=4)
    with open(selected_directories, "w") as outfile:
        outfile.write(json_object)
