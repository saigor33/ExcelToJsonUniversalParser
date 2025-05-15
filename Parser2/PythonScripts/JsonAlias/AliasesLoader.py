import json
from pathlib import Path
from prettytable import PrettyTable
from JsonAlias import AliasFactory
from JsonAlias.Alias import Alias
from Tests import LogFormatter


def load(json_aliases_file_paths: list[str]) -> dict[str, Alias]:
    valid_json_aliases_file_paths = __FilterValidPaths(json_aliases_file_paths)

    return __Load(valid_json_aliases_file_paths)


def __FilterValidPaths(json_aliases_file_paths: list[str]) -> list[str]:
    result: list[str] = []

    absolute_json_aliases_file_paths = set()
    not_found_json_aliases_file_paths = []
    duplicate_json_aliases_file_paths: list[str] = []

    for json_aliases_file_path in json_aliases_file_paths:
        path = Path(json_aliases_file_path)
        absolute_path = str(path.absolute())

        is_path_valid = True
        if not path.exists():
            not_found_json_aliases_file_paths.append(json_aliases_file_path)
            is_path_valid = False

        if absolute_path in absolute_json_aliases_file_paths:
            duplicate_json_aliases_file_paths.append(absolute_path)
            is_path_valid = False
        else:
            absolute_json_aliases_file_paths.add(absolute_path)

        if is_path_valid:
            result.append(json_aliases_file_path)

    if bool(not_found_json_aliases_file_paths):
        __LogNotFoundJsonAliasesFilePath(not_found_json_aliases_file_paths)
    if bool(duplicate_json_aliases_file_paths):
        __LogDuplicateJsonAliasesFilePath(duplicate_json_aliases_file_paths)

    return result


def __Load(json_aliases_file_paths):
    json_aliases: dict[str, Alias] = {}
    json_aliases_file_paths_by_alias_func_name: dict[str, list[str]] = {}
    duplicate_json_keys_in_file_by_file_path: dict[str, list[str]] = {}
    for json_aliases_file_path in json_aliases_file_paths:
        json_file = open(json_aliases_file_path, "r")
        text = json_file.read()
        json_file.close()

        duplicate_json_keys_in_file: list[str] = []
        object_pairs_hook = lambda x: __ValidateDuplicateKeys(x, duplicate_json_keys_in_file)
        config_json = json.loads(text, object_pairs_hook=object_pairs_hook)

        if len(duplicate_json_keys_in_file) > 0:
            duplicate_json_keys_in_file_by_file_path[json_aliases_file_path] = duplicate_json_keys_in_file

        for json_alias_func_name in config_json.keys():
            if json_alias_func_name not in json_aliases_file_paths_by_alias_func_name:
                json_aliases_file_paths_by_alias_func_name[json_alias_func_name] = []

            json_aliases_file_paths_by_alias_func_name[json_alias_func_name].append(json_aliases_file_path)

            if json_alias_func_name not in json_aliases:
                json_alias_func_text: str = str(config_json[json_alias_func_name])
                json_aliases[json_alias_func_name] = AliasFactory.create(json_alias_func_name, json_alias_func_text)
    duplicate_json_aliases_file_paths_by_alias_func_name = {key: val for key, val in
                                                            json_aliases_file_paths_by_alias_func_name.items() if
                                                            len(val) > 1}
    if bool(duplicate_json_keys_in_file_by_file_path):
        __LogDuplicateJsonKeys(duplicate_json_keys_in_file_by_file_path)
    if bool(duplicate_json_aliases_file_paths_by_alias_func_name):
        __LogDuplicateJsonAliasFuncs(duplicate_json_aliases_file_paths_by_alias_func_name)

    return json_aliases


def __ValidateDuplicateKeys(ordered_pairs, duplicate_keys: list[str]):
    result = {}
    for key, value in ordered_pairs:
        if key in result:
            if key not in duplicate_keys:
                duplicate_keys.append(key)
        else:
            result[key] = value

    return result


def __LogNotFoundJsonAliasesFilePath(not_found_json_aliases_file_paths: list[str]):
    pretty_table = PrettyTable()
    pretty_table.field_names = ["File path"]
    pretty_table.align['File path'] = 'l'
    for not_found_json_aliases_file_path in not_found_json_aliases_file_paths:
        pretty_table.add_row([not_found_json_aliases_file_path], divider=True)
    print("".join([
        "\t"
        f"{LogFormatter.formatWarningColor('Warning. Not found aliases file path.')}",
        "\n"
        f"{str(pretty_table)}"
    ]))


def __LogDuplicateJsonAliasesFilePath(duplicate_json_aliases_file_paths: list[str]):
    pretty_table = PrettyTable()
    pretty_table.field_names = ["File path"]
    pretty_table.align['File path'] = 'l'
    for not_found_json_aliases_file_path in duplicate_json_aliases_file_paths:
        pretty_table.add_row([not_found_json_aliases_file_path], divider=True)
    print("".join([
        "\t"
        f"{LogFormatter.formatWarningColor('Warning. Duplicate aliases file path.')}",
        "\n"
        f"{str(pretty_table)}"
    ]))


def __LogDuplicateJsonAliasFuncs(duplicate_json_aliases_file_paths_by_alias_func_name):
    pretty_table = PrettyTable()
    pretty_table.field_names = ["Alias func name", "File path"]
    pretty_table.align['File path'] = 'l'
    for duplicate_alias_func_name, file_paths in duplicate_json_aliases_file_paths_by_alias_func_name.items():
        pretty_table.add_row([duplicate_alias_func_name, "\n".join(file_paths)], divider=True)
    print("".join([
        "\t"
        f"{LogFormatter.formatWarningColor('Warning. Duplicate json alias func name.')}",
        "\n"
        f"{str(pretty_table)}"
    ]))


def __LogDuplicateJsonKeys(duplicate_json_keys_in_file_by_file_path):
    pretty_table = PrettyTable()
    pretty_table.field_names = ["File path", "Json key"]
    pretty_table.align['File path'] = 'l'
    for file_path, duplicate_keys in duplicate_json_keys_in_file_by_file_path.items():
        pretty_table.add_row([file_path, "\n".join(duplicate_keys)], divider=True)
    print("".join([
        "\t"
        f"{LogFormatter.formatWarningColor('Warning. Duplicate json keys per layer.')}",
        "\n"
        f"{str(pretty_table)}"
    ]))
