from colorama import Fore, Style


def formatErrorColor(text: str) -> str:
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

def formatWarningColor(text: str) -> str:
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"
