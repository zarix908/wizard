from wizard.errors import Error, ErrorType


def check(args, compulsory_names=None, format_checkers=None):
    if not format_checkers:
        format_checkers = dict()
    if not compulsory_names:
        compulsory_names = list()

    error = None

    for name in compulsory_names:
        if args.get(name) is None:
            error = Error(ErrorType.ARGUMENT_NOT_PASS, f'{name} argument missed')

    for name, format_checker in format_checkers.items():
        arg = args.get(name)
        if arg and not format_checker(arg):
            error = Error(ErrorType.ARGUMENT_INVALID_FORMAT, f'{name} argument has invalid format')

    return error
