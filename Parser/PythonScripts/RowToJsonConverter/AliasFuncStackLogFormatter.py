def stackFormat(alias_func_stack: list[str], alias_func_name: str) -> str:
    log = [f"->{alias_func_name}"]

    if len(alias_func_stack) > 0:
        log.append("\n".join(reversed(alias_func_stack)))

    log.append("<start>")

    return "\n".join(log)
