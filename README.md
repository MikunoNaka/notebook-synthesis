# Notebook Synthesis

Fork of <https://github.com/otuva/handwriting-synthesis>. Specially meant for writing
the output to a PDF simulating a regular notebook.

## Installation

``` shell
git clone https://github.com/MikunoNaka/notebook-synthesis
cd notebook-synthesis
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You should have ImageMagick installed and `magick` and `convert` commands should be accessible from $PATH

## Usage

### Validating Input

``` shell
python validate.py --help
```

If the input file containing any invalid characters, 
this command will point them out:

``` shell
python validate.py input.txt --show-errors
```

To automatically remove invalid characters:

``` shell
python validate.py input.txt --autofix
```

Use the `--autofix-use-whitespaces` flag to replace 
invalid characters with whitespaces.

### Formatting Input

``` shell
python format.py --help
```

The max character limit is 75 characters.
Following command will word-wrap your input file.

``` shell
python format.py input.txt
```

You can also set a lower character limit 
with the `--max-width` flag.

### Rendering a Notebook 

``` shell
python notebook-synthesis.py --help
```

``` shell
python notebook-synthesis.py input.txt output.pdf
```
