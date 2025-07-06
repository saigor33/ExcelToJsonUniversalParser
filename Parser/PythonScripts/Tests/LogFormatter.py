from colorama import Fore, Style


def formatErrorColor(text: str) -> str:
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


def formatWarningColor(text: str) -> str:
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"


def formatWarning(text: str) -> str:
    return f"{formatWarningColor(f'Warning. {text}')}"


def formatError(text: str) -> str:
    return f"{formatErrorColor(f'Error. {text}')}"
