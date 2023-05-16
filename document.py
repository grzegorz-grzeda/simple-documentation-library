#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2023 Grzegorz Grzęda
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import shutil
import argparse
import subprocess

DOXYFILE_TEMPLATE = 'Doxyfile.template'
DOXYFILE = 'Doxyfile'


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('version')
    parser.add_argument('brief')
    parser.add_argument('input')
    parser.add_argument('output')
    return parser.parse_args()


def get_current_script_path():
    return os.path.dirname(os.path.realpath(__file__))


def generate_doxyfile(name, version, brief, input, output, destination_path):
    template_path = os.path.join(get_current_script_path(), DOXYFILE_TEMPLATE)
    if not os.path.isabs(input):
        input = os.path.join(os.getcwd(), input)

    with open(template_path) as template:
        content = template.read()
        content = content.replace('__PROJECT_NAME__', f'"{name}"')
        content = content.replace('__PROJECT_NUMBER__', f'"{version}"')
        content = content.replace('__PROJECT_BRIEF__', f'"{brief}"')
        content = content.replace('__INPUT__', f'"{input}"')
        content = content.replace('__OUTPUT_DIRECTORY__', f'{output}')
        output_file_path = os.path.join(destination_path, DOXYFILE)
        with open(output_file_path, 'w') as output_file:
            output_file.write(content)


def prepare_destination_directory(destination_path):
    cwd = os.getcwd()
    destination = os.path.join(cwd, destination_path)
    shutil.rmtree(destination, ignore_errors=True)
    os.makedirs(destination)
    source_style_path = os.path.join(get_current_script_path(), 'style')
    destination_style_path = os.path.join(destination, 'style')
    shutil.copytree(source_style_path, destination_style_path)


def run_doxygen(output_path):
    subprocess.call(f'doxygen {output_path}/Doxyfile', shell=True)


def main():
    args = parse_arguments()
    output_path = args.output
    prepare_destination_directory(output_path)
    generate_doxyfile(args.name, args.version,
                      args.brief, args.input, args.output, output_path)
    run_doxygen(output_path)


if __name__ == "__main__":
    main()
