import sys
import os
from pathlib import Path
import shutil

def has_write_permission(path) -> bool:
    return os.access(path, os.W_OK)

def has_read_permission(path) -> bool:
    return os.access(path, os.R_OK)

def copy(source: Path, dest: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"File not found: {source}")
    
    if not has_read_permission(source):
        raise ValueError(f"No read permission for '{source}'")

    if not has_write_permission(dest.parent):
        raise ValueError(f"No write permission for '{dest}'")

    if source.is_file():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        print(f"{source} -> {dest}")
        return
    
    if source.is_dir():
        dest.mkdir(parents=True, exist_ok=True)
        print(f"{source} -> {dest}")
        for item in source.iterdir():
            dest_item = dest / item.name
            copy(item, dest_item)

def main():
    if len(sys.argv) != 2:
        print(
            "Usage: tast1.py <source> [dest_dir]\n"
            "Default: dest_dir=dist"
            )
        sys.exit(1)

    source_arg = sys.argv[1] if len(sys.argv) > 1 else None
    dist_arg = sys.argv[2] if len(sys.argv) > 2 else 'dist'
    source = Path(source_arg)
    dist = Path(dist_arg)
    
    if not source.exists():
        print(f"Error: '{source}' not found")
        sys.exit(1)
    
    if not source.is_dir(): 
        print(f"Error: '{source}' is not a directory")
        sys.exit(1)
    
    if dist.exists() and dist.is_file():
        print(f"Error: Can't copy. '{dist}' is a file")
        sys.exit(1)
    
    try:
        copy(source, dist)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
