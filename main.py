import pathlib


def assign_new_place(path: pathlib.Path, paths_available: list[pathlib.Path], debug: bool = True) -> pathlib.Path:
    if debug:
        return path

    if len(paths_available) < 1:
        optional_targets = "[no targets available, suggest a new one]"
    else:
        optional_targets = f"{'  \n'.join(x.as_posix() for x in paths_available)}"

    answer = None
    while answer is None:
        question = (
            f"Folder to archive:\n"
            f"{path}\n"
            f"\n"
            f"Available paths:\n"
            f"{optional_targets}\n"
            f"\n"
            f"Where should the folder above be moved to (enter new path if none fits)?\n"
            f"Enter the new path: "
        )
        answer = input(question)

    return pathlib.Path(answer)


def traverse_file_system(folder_path: pathlib.Path, debug: bool = True) -> bool:
    if debug:
        return True

    # judging from the path name and its content, should its contents be re-ordered?
    answer = None
    while answer not in {"y", "n"}:
        question = (
            f"Folder name:\n"
            f"{folder_path}\n"
            f"\n"
            f"Folder contents:\n"
            f"{'\n'.join(x.as_posix() for x in folder_path.iterdir())}\n"
            f"\n"
            f"Judging from this information only, is it probable that re-ordering the contents of this folder breaks "
            f"relative path references to it, the files, or folders it contains? (Y/n) "
        )
        answer = input(question)

    return answer != "y"


def move_folder(folder_path: pathlib.Path, target_path: pathlib.Path) -> None:
    # move the folder to the target path
    print(f"Moving {folder_path} to {target_path}...")
    # folder_path.rename(target_path)


def reorder_file_system(start_path: pathlib.Path) -> None:
    visited_places = list[pathlib.Path]()

    def depth_first_traversal(current_dir: pathlib.Path) -> None:
        for item in current_dir.iterdir():
            is_folder = item.is_dir()
            if not (is_folder and traverse_file_system(item)):
                continue

            depth_first_traversal(item)

            assigned_place = assign_new_place(item, visited_places)
            if assigned_place not in visited_places:
                visited_places.append(assigned_place)

            move_folder(item, assigned_place)

    depth_first_traversal(start_path)
    print(visited_places)
    print(len(visited_places))


def main() -> None:
    start_path = pathlib.Path("/home/mark/nas/")
    reorder_file_system(start_path)


if __name__ == "__main__":
    main()
