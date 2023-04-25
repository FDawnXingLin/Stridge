import argparse
import os
import random
import string

# Defines meta information for the program.
STRIDGE = {
    'name': 'Stridge',
    'version': '0.1.0',
    'author': 'FDawnXL',
    'homepage': 'https://github.com/FDawnXingLin/stridge'
}


# The following functions are used to parse simple YAML key-value pair structures.
def parse_yaml(yaml_string):
    # initialize an empty dictionary to store the key-value pairs
    result = {}
    # split the string by newline characters
    lines = yaml_string.split("\n")
    # loop through each line
    for line in lines:
        # strip any leading or trailing whitespace
        line = line.strip()
        # skip empty lines or comments
        if not line or line.startswith("#"):
            continue
        # split the line by the first colon character
        key, value = line.split(":", 1)
        # strip any leading or trailing whitespace from the key and value
        key = key.strip()
        value = value.strip()
        # store the key-value pair in the result dictionary
        result[key] = value
    # return the result dictionary
    return result


# The following code will be executed when the program is run with the "add" command.
# The "add" command must accept only one parameter <url>, which will form a key-value pair with a randomly generated key. This key-value pair will be appended to the data file.
def command_add(args):
    # If a symbol value is specified, use it as the key, otherwise randomly generate a string of length 5 as the key.
    print(args.symbol)
    if args.symbol is None:
        key = "".join(random.choices(string.ascii_letters, k=5))
    else:
        key = args.symbol
    # Append data to the data file.
    with open(data_file, "a") as f:
        f.write(f"{key}: {args.url}\n")
    # Output operation information.
    print(f"Added {key}: {args.url} to {data_file},the url is {domain}/{key}")


# The following code will be executed when the program is run with the "remove" command.
# The "remove" command must accept only one parameter <symbol>, which is a randomly generated identifier corresponding to the added URL.
def command_remove(args):
    # The following code will iterate through the data file and eliminate items that meet the criteria (that is, the same as the passed in Symbol).
    with open(data_file, "r+") as f:
        lines = f.readlines()
        new_lines = []
        for line in lines:
            parts = line.split(":")
            if parts[0] != args.symbol:
                new_lines.append(line)
            else:
                print(f"{args.symbol} has been found and deleted.")
        f.seek(0)
        f.writelines(new_lines)
        f.truncate()
        print(
            "The operation \"Remove\" has been completed. If there is no other prompt besides this prompt, it means that this identifier does not exist in the data file.")


# The following code will be executed when the program is run with the "generate" command.
# The "generate" command is responsible for generating static files based on the data in the data files. Before generating the file, the program will automatically clean up the last output.
def command_generate(args):
    # Read template files and data files.
    with open(template_file, "r") as f:
        template = f.read()
    with open(data_file, "r") as f:
        data = f.read()
    # Check if the output directory exists, empty it if it exists, otherwise create the output directory.
    if os.path.exists(dist_dir):
        print(f"{dist_dir} exists. Deleting all files in it.")
        for file in os.listdir(dist_dir):
            os.remove(os.path.join(dist_dir, file))
    else:
        print(f"{dist_dir} does not exist. Creating it.")
        os.mkdir(dist_dir)

    # Convert data from yaml format to dictionary type.
    data_dict = parse_yaml(data)

    # Render all key-value pairs in the data dictionary to static files and output to the output directory.
    for key, value in data_dict.items():
        # Replace the field {url} in the template with the data.
        content = template.replace("{url}", value)
        # Generate a html file according to the key name and write it.
        with open(os.path.join(dist_dir, key + ".html"), "w") as f:
            f.write(content)
        # Output operation information.
        print(f"Generated {key}.html in {dist_dir}")


# The following code will be executed when the program is run with the "clean" command.
# The "generate" command is designed to clean up generated static files.
def command_clean(args):
    # Delete the output folder, if it exists, and the files in it.
    if os.path.exists(dist_dir):
        print(f"{dist_dir} exists. Deleting it.")
        for file in os.listdir(dist_dir):
            os.remove(os.path.join(dist_dir, file))
        os.rmdir(dist_dir)

# The following code will be executed when the program is run with the "version" command.
# The "version" command is designed to output program meta information.
def command_version(args):
    print("{}\nVersion:{}\nAuthor:{}\nFor more information,please visit {}".format(STRIDGE['name'], STRIDGE['version'],
                                                                                   STRIDGE['author'],
                                                                                   STRIDGE['homepage']))


# The following functions are used to check program operating conditions and perform initialization operations.
def initialize():
    # The following code is used to check whether there are template files and data files in the running directory, and create them with default values ​​if they do not exist.
    if not os.path.exists(template_file):
        print(f"{template_file} does not exist. Creating it with default value.")
        with open(template_file, "w") as f:
            f.write(default_template)

    if not os.path.exists(data_file):
        print(f"{data_file} does not exist. Creating it with default value.")
        with open(data_file, "w") as f:
            f.write(default_data)


# Define some basic information, you can customize it according to your own needs.
# Define the template filename and data filename.
template_file = "template.html"
data_file = "data.yaml"
# Defines the output directory name.
dist_dir = "dist"
# Define defaults for template files and data files. These two files will be created with default values if they do not exist.
default_template = "<!DOCTYPE html><html><head><title>Jump</title><style>a {display: inline-block;padding: 10px 20px;background-color: #4CAF50;color: white;text-decoration: none;border-radius: 5px;}a.center {position: absolute;top: 50%;left: 50%;transform: translate(-50%, -50%);}</style></head><body><a href=\"{url}\" target=\"_blank\" rel=\"noopener noreferrer\" class=\"center\">Click here to jump to {url}</a></body></html>"

default_data = ""
# Define a domain name, which is spliced together with randomly generated strings to form a short URL. For example: example.com/*****.html
domain = "example.com"

# Execute the initialization function.
initialize()

# Defines the commands and arguments accepted by argparse.At the same time, add the processing function corresponding to the command.
parser = argparse.ArgumentParser(description='Shrink is a short link generator based on static file hosting services.')
subparsers = parser.add_subparsers()

parser_add = subparsers.add_parser('add', help='Add a link.')
parser_add.add_argument('url', type=str, help='The target URL to which the generated short link points.')
parser_add.add_argument("--symbol",
                        help="optional. When this value is specified, the application will use this value as the suffix (symbol) of the short link instead of randomly generating one.")
parser_add.set_defaults(func=command_add)

parser_remove = subparsers.add_parser('remove', help='Delete a link by symbol.')
parser_remove.add_argument('symbol', type=str, help='Specify the symbol to delete.')
parser_remove.set_defaults(func=command_remove)

parser_generate = subparsers.add_parser('generate', help='Clean up all previous output files and build again.')
parser_generate.set_defaults(func=command_generate)

parser_clean = subparsers.add_parser('clean', help='Clean up all previous output files.')
parser_clean.set_defaults(func=command_clean)

parser_version = subparsers.add_parser('version', help='Output program meta information.')
parser_version.set_defaults(func=command_version)

args = parser.parse_args()
args.func(args)
