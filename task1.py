import sys
import os
from pathlib import Path
import shutil
import argparse

def has_write_permission(path) -> bool:
    return os.access(path, os.W_OK)

def has_read_permission(path) -> bool:
    return os.access(path, os.R_OK)

def throwIfNotDirectory(dir: Path):
    if not dir.is_dir():
        raise NotADirectoryError(f"'{dir}' is not a directory")

def throwIfNoWritePermission(dir: Path):
    if not has_write_permission(dir):
        raise ValueError(f"No write permission for '{dir}'")

def throwIfNoReadPermission(dir: Path):
    if not has_read_permission(dir):
        raise ValueError(f"No read permission for '{dir}'")

def throwIfDirIsFile(dir: Path):
    if dir.is_file():
        raise ValueError(f"Directory '{dir}' is a file")

def throwIfDirNotExists(dir: Path):
    if not dir.exists():
        raise FileNotFoundError(f"'{dir}' not found")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str, help="Source dir to copy")
    parser.add_argument("-d", "--dest", type=str, default="dist", help="Destination dir")
    
    return parser.parse_args()

def get_all_files_in_directory(source: Path, memo: list[Path] | None = None) -> list[Path]:
    throwIfDirNotExists(source)    
    throwIfNotDirectory(source)
    throwIfNoReadPermission(source)

    if memo is None:
        memo = list[Path]()

    for item in source.iterdir():
        if item.is_file():
            memo.append(item)
        else:
            get_all_files_in_directory(item, memo)

    return memo

def group_files_by_ext(files: list[Path]) -> dict[str, list[Path]]:
    result = dict[str, list[Path]]()
    for file in files:
        extension = file.suffix[1:] if file.suffix else "no_extension"
        if extension not in result:
            result[extension] = list[Path]()
        result[extension].append(file)
    return result

def copy_grouped_files(grouped_files: dict[str, list[Path]], destination: Path):
    throwIfNoWritePermission(destination.parent)
    destination.mkdir(parents=True, exist_ok=True)

    for extension, files in grouped_files.items():
        new_dir = Path(destination / extension)
        new_dir.mkdir(parents=True, exist_ok=True)

        for file in files:
            new_file = Path(new_dir / file.name)
            
            # find free file name
            copy_num = 0
            while new_file.exists():
                copy_num += 1
                new_file = new_dir / f"{file.stem} Copy {copy_num}{file.suffix}"
            
            shutil.copy2(file, new_file)

def main():
    args = parse_args()
    source = Path(args.src)
    destination = Path(args.dest)

    try:
        throwIfDirIsFile(destination)
        throwIfNoWritePermission(destination.parent)
        throwIfNotDirectory(source)
        files = get_all_files_in_directory(source)
        grouped_files = group_files_by_ext(files)
        copy_grouped_files(grouped_files, destination)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
