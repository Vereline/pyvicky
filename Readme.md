# PyVicky

PyVicky is a visual development environment for Python written in PyQt.
Here you can:

+ write your python code, using highlight and autocomplete

+ edit as many files as you can at the moment

+ configure and open not only files, but whole projects

+ interpret your code

+ find and replace text by regex in your code

+ configure view, font, highlight and themes of **PyVicky** editor


## Installation

### Requirements
* Linux, Windows or any system, where PyQt can be installed
* Python 3.3 and up
* PyQt 5.10.* and up

###  Installation process
1. download official package from this repository
2. unpack it
3. `$ pip install -r requirements-freeze.txt`
4. `$ python setup.py install`

## Usage

```python
pyvicky [filename]... [key]...
keys:
-s  # silent mode(disable logging)
```
### Possible shortcuts

   * `Ctrl+C` - copy
   * `Ctrl+V` - paste
   * `Ctrl+O` - open file
   * `Ctrl+Shift+O` - open directory
   * `Ctrl+A` - select all text in a tab
   * `Ctrl+Y` - clear tab
   * `Ctrl+F` - search dialog
   * `Ctrl+Q` - quit
   * `Ctrl+P` - preferences dialog
   * `Ctrl+S` - save file
   * `Ctrl+N` - new Tab
   * `Ctrl+H` - local help
   * `Ctrl+E` - trigger autocomplete (if written less than 2 symbols)
   * `Tab` - tab(size equals 4 spaces(default))
   * `Ctrl+I` - interpreter dialog
   * `F11` - run defined script

## Development
```
$ pyvenv venv
$ venv/bin/activate
$ pip install -r requirements.txt
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Contacts
*vstanko1998@gmail.com* - feel free to communicate
