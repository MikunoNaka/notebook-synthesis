import click

LEGAL_CHARS = ['I', 'O', '-', 'p', 'r', '7', 'h', '2', 'j', 'W', 'H', 'w', "'", ',', 'z', 'c', '4', '#', 'B', 'F', 'M', 'T', 'U', '3', ')', 'D', 'd', 'y', '?', '0', ' ', 'E', 'J', 'V', 'u', 's', 'v', 'A', 'C', '.', '6', '1', '!', 'e', 'L', 'm', 'o', '(', 'P', '\x00', 'q', '"', '5', 'g', 'N', 'R', 'Y', 'S', 'a', ':', 'b', 'f', 'l', 'n', '9', 't', 'x', 'k', 'G', 'K', 'i', ';', '8']

# looks for illegal characters and returns their line and index
def check_illegal_chars(lines):
    errors = {}
    for line_index in range(len(lines)):
        for char_index in range(len(lines[line_index])):
            if lines[line_index][char_index] not in LEGAL_CHARS:
                if line_index in errors:
                    errors[line_index].append(char_index)
                else:
                    errors[line_index] = [char_index]

    return errors


# pretty prints the positions of the illegal characters
def show_illegal_chars(lines, errors):
    print("Invalid characters:\n")

    for i in errors.keys():
        line = lines[i]

        s = " " * len(line)
        for j in errors[i]:
            s = s[:j] + "^" + s[j+1:]

        print(f"Line {i+1}: Position(s) {[x + 1 for x in errors[i]]}")
        print(line)
        print(s)


# automatically remove the illegal characters
def del_illegal_chars(lines, errors, add_whitespace=False):
    print("Attempting to fix errors by deleting invalid characters...")

    for i in errors.keys():
        line = lines[i]

        x = 0 # to keep track of index ofset after deletion of characters
        for j in errors[i]:
            j = j - x

            if add_whitespace:
                line = line[:j] + " " + line[j+1:]
            else:
                line = line[:j] + line[j+1:]
                x += 1

        lines[i] = line
    
    return lines


@click.command()
@click.argument('input_file')
@click.option('--show-errors', is_flag=True, help="Print errors (if any)")
@click.option('--autofix', is_flag=True, help="Remove invalid characters from file without replacement")
@click.option('--autofix-use-whitespaces', is_flag=True, help="Replace invalid characters with whitespaces (use with --autofix)")
@click.option('--stdout', is_flag=True, help="Print output to STDOUT instead of output file (use with --autofix)")
@click.argument('output_file', default=f"./fixed.txt")

def main(input_file, show_errors, autofix, autofix_use_whitespaces, stdout, output_file):
    _input = open(input_file, "r")
    lines = _input.read().splitlines()

    errors = check_illegal_chars(lines)

    if errors:
        print(f"{input_file} contains errors.")

        if show_errors:
            show_illegal_chars(lines, errors)
        else:
            print("Use --show-errors to display errors.")

        if autofix:
            fixed = del_illegal_chars(lines, errors, autofix_use_whitespaces)
            if stdout: # print to STDOUT instead of writing to file
                for i in fixed:
                    print(i)
            else: # write to output_file
                print(f"Writing to file {output_file}")
                _output = open(output_file, "w")
                _output.writelines(l + "\n" for l in lines)
                _output.close()
        else:
            print("Use --autofix to attempt to fix automatically.")
    else:
        print(f"Awesome! {input_file} is completely error free.")

    _input.close()


if __name__ == "__main__":
    main()
