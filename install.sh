#!/bin/bash

root_path=$(dirname $0)

conan_home=$(conan config home 2>/dev/null)

if [[ ! -d $conan_home ]]; then
  echo -e "\033[31mCannot find Conan's configuration home directory\033[0m" >&2
  exit 1
fi

# Commands

commands_path=$conan_home/extensions/commands
if [[ ! -d "$commands_path" ]]; then
  mkdir -p "$commands_path" || exit 1
fi
echo -e "\033[3;35mLink commands to $commands_path ...\033[0m"
for file in "$commands_path"/cmd_*.py; do
  test -L "$file" || continue
  if [[ ! -e "$file" ]]; then
    rm -f "$file"
    name=$(basename "$file" | sed -r 's/cmd_(.*)\.py/\1/')
    echo -e "⚠️ command \033[1;36m$name\033[0m is not linked. [\033[1;33mDELETED\033[0m]" >&2
  fi
done

function link_commands() {
  for file in "$1"/cmd_*.py; do
    test -f "$file" || continue

    source_file=$(realpath "$file")
    target_file=$commands_path/$(basename "$file")
    name=$(basename "$target_file" | sed -r 's/cmd_(.*)\.py/\1/')

    if [[ ! -L "$target_file" ]]; then
      ln -s "$source_file" "$target_file"
      echo -e "✅ command \033[1;36m$name\033[0m is linked"
    else
      echo -e "⚠️ command \033[1;36m$name\033[0m already exists. [\033[1;33mSKIPPED\033[0m]" >&2
    fi
  done
}

link_commands "$root_path/extensions/commands"

# Templates

templates_path=$conan_home/templates/command/new
if [ ! -d "$templates_path" ]; then
  mkdir -p "$templates_path" || exit 1
fi
echo -e "\033[3;35mLink templates to $templates_path ...\033[0m"
for dir in "$templates_path"/vee_*; do
  test -L "$dir" || continue
  if [[ ! -e "$dir" ]]; then
    rm -f "$dir"
    name=$(basename "$dir")
    echo -e "⚠️ template \033[1;36m$name\033[0m is not linked. [\033[1;33mDELETED\033[0m]" >&2
  fi
done

function link_templates() {
  for dir in "$1"/*; do
    test -d "$dir" || continue

    name=$(basename "$dir")
    source_dir=$(realpath "$dir")
    target_dir=$templates_path/$name

    if [[ ! -L "$target_dir" ]]; then
      ln -s "$source_dir" "$target_dir"
      echo -e "✅ template \033[1;36m$name\033[0m is linked"
    else
      echo -e "⚠️ template \033[1;36m$name\033[0m already exists. [\033[1;33mSKIPPED\033[0m]" >&2
    fi
  done
}

link_templates "$root_path/templates/command/new"
