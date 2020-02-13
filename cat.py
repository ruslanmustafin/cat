import glob
import os
import re

import tqdm
import fire

from jinja2 import Environment, BaseLoader
from googletrans import Translator

DOC_TEMPLATE = \
"""<?php

return [
    {{lines|join(',\n    ')}}
];

"""

LANG_MAP = {
    'cz':'cs',
    'dk':'da',
    'se':'sv'
}

def is_translation(l):
    return re.match(r'.* => .*', l) is not None


def clean(l):
    l = l.strip()
    if l.endswith(','):
        l = l[:-1]
        
    return l

def extract_key(l):
    key = l.split('=>')[0].strip()
    
    if key.startswith("'"):
        key = key[1:]
        
    if key.endswith("'"):
        key = key[:-1]
        
    return key
        

def key_exists(translations, key):
    for t in translations:
        t_key = extract_key(t)
        
        if key==t_key:
            return True
        
    return False


def translate(root, file, key, value, force=False, src_lang='en'):
    
    translator = Translator()
    template = Environment(loader=BaseLoader).from_string(DOC_TEMPLATE)
    
    all_langs = glob.glob(os.path.join(root, '*'))
    
    print(key, value)
    
    for l in tqdm.tqdm(sorted(all_langs)):
        path = os.path.join(l, file)
        dst_lang = os.path.basename(l)

        with open(path, 'r') as f:
            translations = [clean(l) for l in f.readlines() if is_translation(l)]

        if force or not key_exists(translations, key):
            dst_lang = LANG_MAP.get(dst_lang, dst_lang)

            if dst_lang != 'en':
                translated_value = translator.translate(value, src=src_lang, dest=dst_lang).text
            else:
                translated_value = value


            translations.append(f"'{key}' => '{translated_value}'")

            with open(path, 'w') as f:
                f.write(template.render(lines=sorted(translations)))
        else:
            print(f'language: {dst_lang}; file {file} - key {key} already exists. Set force to True to overwrite')
    
    
if __name__ == '__main__':
    fire.Fire(translate)
    