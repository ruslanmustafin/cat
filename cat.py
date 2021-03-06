import glob
import os
import re

import tqdm
import fire
import html

import shutil

from json import JSONDecodeError

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

def extract_value(l):
    key = l.split('=>')[1].strip()
    
    if key.startswith("'") or key.startswith('"'):
        key = key[1:]
        
    if key.endswith("'") or key.endswith('"'):
        key = key[:-1]
        
    return key


def extract_key(l):
    key = l.split('=>')[0].strip()
    
    if key.startswith("'") or key.startswith('"'):
        key = key[1:]
        
    if key.endswith("'") or key.endswith('"'):
        key = key[:-1]
        
    return key
        

def key_exists(translations, key):
    for t in translations:
        t_key = extract_key(t)
        
        if key==t_key:
            return True
        
    return False

def replace_key(translations, key, translated_value):
    for idx, t in enumerate(translations):
        t_key = extract_key(t)
        
        if t_key == key:
            break
    else:
        raise ValueError(f'Key {key} not found in translations!')
            
    translations[idx] = f"'{key}' => '{translated_value}'"
    
    return translations


def build_string(key, value):
    return f'"{key}" => "{value}"'


def newlang(root, code, template_lang='en'):
    
    translator = Translator(timeout=1.0)
    template = Environment(loader=BaseLoader).from_string(DOC_TEMPLATE)
    
    template_dir = os.path.join(root, template_lang)
    dest_dir = os.path.join(root, code)
    
    files = glob.glob(os.path.join(template_dir, '*'))
    
    os.makedirs(os.path.join(root, code), exist_ok=True)
    
    for f in tqdm.tqdm(files):
        fname = os.path.basename(f)
        out_fname = os.path.join(root, code, fname)
        
        if os.path.exists(out_fname):
            print(f'{code}-{fname} already exists, skipping...')
            continue
        
        with open(f, 'r') as f_in:
            translations = [clean(l) for l in f_in.readlines() if is_translation(l)]
            
        keys = [extract_key(t) for t in translations]
        values = [html.unescape(extract_value(t)) for t in translations]
        
        try:
            translations = translator.translate(values, src=template_lang, dest=code)
            
            new_translations = []
            
            for key, value in zip(keys, translations):        
                new_translations.append(build_string(key, value.text))
            
            with open(os.path.join(root, code, fname), 'w+') as f_out:
                f_out.write(template.render(lines=sorted(new_translations)))
                
        except JSONDecodeError as e:
            print(f'Could not translate {fname}, the text contains illegal characters (&,#,;) or you may have exceeded the request limit')
            
    

def insert(root, file, key, value, overwrite=False, src_lang='en'):
    
    translator = Translator(timeout=1.0)
    template = Environment(loader=BaseLoader).from_string(DOC_TEMPLATE)
    
    all_langs = glob.glob(os.path.join(root, '*'))
    
    print(key, value)
    
    for l in tqdm.tqdm(sorted(all_langs)):
        path = os.path.join(l, file)
        dst_lang = os.path.basename(l)

        with open(path, 'r') as f:
            translations = [clean(l) for l in f.readlines() if is_translation(l)]

        # print(key_exists(translations, key), translations, key)

        if overwrite or not key_exists(translations, key):
            dst_lang = LANG_MAP.get(dst_lang, dst_lang)

            if dst_lang != 'en':
                translated_value = translator.translate(value, src=src_lang, dest=dst_lang).text
            else:
                translated_value = value

            if overwrite:
                translations = replace_key(translations, key, translated_value)
            else:
                translations.append(build_string(key, translated_value))

            with open(path, 'w') as f:
                f.write(template.render(lines=sorted(translations)))
        else:
            print(f'language: {dst_lang}; file {file} - key {key} already exists. Set overwrite to True to overwrite')
    
    
if __name__ == '__main__':
    fire.Fire()
    