# Compensair Automatic Translator (CAT)

- Adds new keys into existing translations
- Adds new languages based on existing (currently uses `en` as archetypical) (NOTE: this feature is experimental)

## Installation

### Requirements

- Python >= 3.6
- tqdm
- Jinja2
- fire
- googletrans

```
(OPTIONAL) conda create -n cat python=3.6
git clone https://github.com/ruslanmustafin/cat
cd cat
pip install .
```

## Example

Insert a new key `404_new_text` into file `404.php` with value `This is a sample text`:
```
python -m cat insert --root=~/work/site/public/views/messages --file=404.php --key=404_new_text --value="This is a sample text"
```

Add a japanese translation:
```
python -m cat newlang --root=~/work/site/public/views/messages --code ja
```


## Usage

### Adding a new key into existing translations

```
python -m cat insert --root=path_to_messages_folder --file=file_with_ext --key=sample_key --value="sample value"
```

Mandatory params:

`root` - path to the folder with messages

`file` - what file to modify (example: `404.php`)

`key` - this key will be inserted into the list of existing translations

`value` - this value will be inserted into the list of existing translations

Optional flags:

`overwrite` - set to true in order to overwrite an existing key (throws `ValueError` if the key does not exist) 

Example:
```
python -m cat insert --root=path_to_messages_folder --file=file_with_ext --key=existing_key --value="new value" --overwrite
```
The above command will try to replace a `existing_key` with `new value`

### Adding a new translation

```
python -m cat newlang --root=path_to_messages_folder --code lang_code
```

`root` - path to the folder with messages

`code` - iso639-1 language code
