from autocorrect import Speller
import json

text_dict = {}
with open('raw_sw_lan_data', 'r') as f:
    for line in f:
        text, num = line.split(' ')
        if int(num) > 200:
            text_dict[text] = int(num)


json_object = json.dumps(text_dict, indent=4)
with open("word_count.json", "w") as outfile:
    outfile.write(json_object)

with open("word_count.json", "r") as jsonFile:
    json_object = json.load(jsonFile)
    jsonFile.close()

spell = Speller(lang='sw', nlp_data=json_object, only_replacements=True)
# spell = Speller(lang='sw')
print(spell("den blo ankann äv gil"))

