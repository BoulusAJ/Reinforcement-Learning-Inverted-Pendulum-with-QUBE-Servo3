from pathlib import Path

def export_tree(
    root: Path,
    output_file: Path,
    ignore_dirs=None,
    omit_contents_dirs=None
):
    """
    Export folder structure as a tree.

    - ignore_dirs: folders completely skipped (not shown at all)
    - omit_contents_dirs: folders shown, but whose contents are omitted
    """

    if ignore_dirs is None:
        ignore_dirs = {".git", "__pycache__", ".venv", "env", ".conda"}

    if omit_contents_dirs is None:
        omit_contents_dirs = set()

    lines = []

    def walk(dir_path: Path, prefix=""):
        entries = sorted(
            [e for e in dir_path.iterdir() if e.name not in ignore_dirs],
            key=lambda x: (x.is_file(), x.name.lower())
        )

        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            lines.append(prefix + connector + entry.name)

            if entry.is_dir():
                extension = "    " if is_last else "│   "

                if entry.name in omit_contents_dirs:
                    lines.append(
                        prefix + extension + "└── [contents omitted intentionally]"
                    )
                else:
                    walk(entry, prefix + extension)

    lines.append(root.name + "/")
    walk(root)

    output_file.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    root_dir = Path(".").resolve()
    output_path = Path("folder_structure.txt")

    export_tree(
        root=root_dir,
        output_file=output_path,
        ignore_dirs={
            ".git",
            "__pycache__",
            ".venv",
        },
        omit_contents_dirs={
            "MATLAB",        # shown, but not expanded
            #"third_party",   # example
        },
    )

    print(f"Folder structure exported to: {output_path.resolve()}")
