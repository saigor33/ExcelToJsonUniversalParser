from Tests import LogFormatter


def handle(exception: Exception, need_print_stacktrace: bool):
    if need_print_stacktrace:
        raise exception
    else:
        print(LogFormatter.formatErrorColor(f"Error: {exception}"))
