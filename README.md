# Compensair Automatic Translator (CAT)

## Installation

```
pip install git+git://github.com/ruslanmustafin/cat
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
