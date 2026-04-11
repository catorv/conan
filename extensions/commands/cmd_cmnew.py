import os
from argparse import ArgumentParser
import sys

from conan.api.conan_api import ConanAPI
from conan.cli.command import conan_command


@conan_command(group="CMake")
def cmnew(conan_api: ConanAPI, parser: ArgumentParser, *args):
    """
    Create a new example recipe and source files from a template.
    """
    parser.add_argument(
        "template",
        nargs="?",
        help="Template name, "
        "either a predefined built-in or a user-provided one. "
        "Available built-in templates: "
        "basic, cmake_lib, cmake_exe, vee_cmake_lib, vee_cmake_exe, header_lib, "
        "meson_lib, meson_exe, msbuild_lib, msbuild_exe, bazel_lib, bazel_exe, "
        "autotools_lib, autotools_exe, premake_lib, premake_exe, local_recipes_index, workspace. "
        "E.g. 'conan new cmake_lib -d name=hello -d version=0.1'. "
        "You can define your own templates too by inputting an absolute path "
        "as your template, or a path relative to your conan home folder."
        "(default: vee_cmake_exe)",
    )
    parser.add_argument(
        "-d",
        "--define",
        action="append",
        help="Define a template argument as key=value, e.g., -d name=mypkg",
    )
    parser.add_argument(
        "-n",
        "--name",
        help='Equivalent to "-d name=NAME", but takes precedence.',
        nargs="?",
    )
    parser.add_argument(
        "--lib",
        action="store_true",
        help="Change the default template to vee_cmake_lib.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite file if it already exists",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output folder for the generated files",
    )

    args = parser.parse_args(*args)

    if args.name is None and args.define is not None:
        for define in args.define[:]:
            if define.startswith("name="):
                args.name = define[5:]
                args.define.remove(define)

    cwd = os.getcwd()
    if args.name is None:
        name = os.path.basename(cwd)
        args.name = name
        args.output = cwd
    else:
        args.output = os.path.join(cwd, args.name)

    if not args.force and not is_dir_empty(args.output):
        print(
            f"\033[31mERROR: Directory '{args.output}' is not empty,"
            " and --force not defined, aborting\033[0m"
        )
        sys.exit(0)

    if args.template is None:
        args.template = "vee_cmake_lib" if args.lib else "vee_cmake_exe"

    if args.define is None:
        args.define = [f"name={args.name}"]
    else:
        for define in args.define[:]:
            if define.startswith("name="):
                args.define.remove(define)
        args.define.append(f"name={args.name}")

    conan_api.new.save_template(args.template, args.define, args.output, args.force)


def is_dir_empty(path):
    return not os.path.exists(path) or len(os.listdir(path)) == 0
