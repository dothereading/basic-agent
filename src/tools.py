from anthropic import beta_tool

@beta_tool
def read_file(path:str) -> str:
    """REads a file.
    Args:
        path (str): file path
    Returns:
        str: contents of file
    """

    return open(path).read()
