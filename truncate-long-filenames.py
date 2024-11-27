import os


ROOT = "E:\\"
LIMIT = 200  # number of bytes in UTF-8 encoding


def main() -> None:
    count = 0
    skipped = []

    for root, dirs, files in os.walk(ROOT):
        all_files = files + dirs  # order is important here, dirs after files
        for path in all_files:
            full_path = os.path.join(root, path)
            if len(path.encode()) > LIMIT:
                truncated_path = truncate(path)
                truncated_full_path = os.path.join(root, truncated_path)
                if os.path.exists(truncated_full_path):
                    skipped += full_path
                    continue
                try:
                    os.rename(full_path, truncated_full_path)
                    print(f"renamed {full_path}\n   into {truncated_full_path}\n")
                    count += 1
                except OSError:
                    print(f"failed to rename {full_path}")
                    skipped.append(full_path)

    print(f"renamed {count} files")
    print(f"skipped {len(skipped)} files:\n{'\n'.join(skipped)}")


def truncate(path: str) -> str:
    base, ext = os.path.splitext(path)
    max_bytes = LIMIT - len(ext.encode())
    if max_bytes < 0:
        raise ValueError("extension too long")
    # chop off characters until it's small enough
    new_base = base
    while len(new_base.encode()) > max_bytes:
        new_base = new_base[:-1]
    if base and not new_base:
        # we had to truncate away the whole name
        raise ValueError("extension too long")
    return new_base + ext

if __name__ == "__main__":
    main()
