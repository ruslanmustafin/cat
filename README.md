# Compensair Automatic Translator (CAT)

## Installation

### Requirements

- Python >= 3.6
- tqdm
- Jinja2
- fire

```
(OPTIONAL) conda create -n cat python=3.6
git clone https://github.com/ruslanmustafin/cat
cd cat
pip install .
```

## Example

Insert a new key `404_new_text` into file `404.php` with value `This is a sample text`:
```
python -m cat --root=~/work/site/public/views/messages --file=404.php --key=404_new_text --value="This is a sample text"
```


## Usage

```
python -m cat --root=path_to_messages_folder --file=file_with_ext --key=sample_key --value="sample value"
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
python -m cat --root=path_to_messages_folder --file=file_with_ext --key=existing_key --value="new value" --overwrite
```
The above command will try to replace a `existing_key` with `new value`
