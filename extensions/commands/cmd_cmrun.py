import os
import re
import subprocess
import sys
from argparse import ArgumentParser

from conan.api.conan_api import ConanAPI
from conan.cli.command import conan_command


@conan_command(group="CMake")
def cmrun(conan_api: ConanAPI, parser: ArgumentParser, *args):
    """
    Build and run the specified executable using CMake.
    """
    parser.add_argument(
        "build_target",
        help="The executable to run, if not specified, the first one will be chosen",
        nargs="?",
    )
    parser.add_argument(
        "--debug",
        action="store_const",
        help="Build in Debug mode (Default)",
        const="debug",
        dest="build_type",
        default="debug",
    )
    parser.add_argument(
        "--release",
        action="store_const",
        help="Build in Release mode",
        const="release",
        dest="build_type",
    )

    build_args, other_args, run_args = split_args(args[0])

    # print(args, build_args, other_args, run_args)
    opts = parser.parse_args(build_args, *args[1:])
    opts = vars(opts)
    if not opts["v"]:
        opts["v"] = "quiet"
    if opts["build_target"]:
        opts["build_target"] = find_executable_from_cmake(opts["build_target"])
    else:
        opts["build_target"] = get_first_executable_from_cmake()

    cmd_args = ["build"] + other_args
    for key, value in opts.items():
        if value is None:
            continue
        # print(f"{key}: {value}")
        if key == "v":
            cmd_args.append(f"-v{value}")
        elif key == "build_type":
            cmd_args.append("-s")
            cmd_args.append(f"build_type={value.capitalize()}")
        elif key == "build_target":
            cmd_args.append("-o")
            cmd_args.append(f"build_target={value}")
        else:
            cmd_args.append(value)

    conan_api.command.run(cmd_args)
    subprocess.run(
        [f"build/{opts['build_type'].capitalize()}/{opts['build_target']}"] + run_args
    )


def split_args(args: list[str]) -> tuple[list[str], list[str], list[str]]:
    build_args = []
    other_args = []
    run_args = []

    has_v_arg = False
    is_run_args = False
    i = 0
    while i < len(args):
        arg = args[i]
        if is_run_args:
            run_args.append(arg)
            i += 1
            continue

        if arg.startswith("-"):
            if arg.startswith("-v"):
                has_v_arg = True
                build_args.append(arg)
                if arg == "-v" and i < len(args) - 1:
                    if args[i + 1].startswith("-"):
                        build_args.append("verbose")
                    else:
                        build_args.append(args[i + 1])
                        i += 1
            elif arg in ["-h", "--help", "--debug", "--release"]:
                build_args.append(arg)
            else:  # for other_args
                other_args.append(arg)
                if (
                    arg
                    not in [
                        "--build-require",
                        "-nr",
                        "--no-remote",
                        "--lockfile-partial",
                        "--lockfile-clean",
                    ]
                    and i < len(args) - 1
                ):
                    other_args.append(args[i + 1])
                    i += 1
        else:
            build_args.append(arg)
            is_run_args = True
        i += 1

    if not has_v_arg:
        build_args.append("-vquiet")

    return (build_args, other_args, run_args)


def get_first_executable_from_cmake():
    if not os.path.exists("CMakeLists.txt"):
        print("cannot access: 'CMakeLists.txt': No such file or directory")
        sys.exit(1)
    with open("CMakeLists.txt", "r") as f:
        for line in f:
            line = line.strip()
            m = re.match(r"add_executable\(\s*(\w+)", line)
            if m:
                return m.group(1)
    print("No executable found in CMakeLists.txt")
    sys.exit(1)


def find_executable_from_cmake(name):
    if not os.path.exists("CMakeLists.txt"):
        print("cannot access: 'CMakeLists.txt': No such file or directory")
        sys.exit(1)
    with open("CMakeLists.txt", "r") as f:
        # prefer executables with names that match exactly
        for line in f:
            line = line.strip()
            if name not in line:
                continue
            m = re.match(r"^add_executable\(\s*(\w+)", line)
            if m and m.group(1) == name:
                return m.group(1)

        f.seek(0)

        # failback to partial text match
        for line in f:
            line = line.strip()
            if name not in line:
                continue
            m = re.match(r"^add_executable\(\s*(\w+)", line)
            if m:
                return m.group(1)
    print(f"No executable matching '{name}' was found in CMakeLists.txt")
    sys.exit(1)
