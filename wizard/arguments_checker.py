import wizard.arguments_checker.errors as errors


class ArgumentNotPassError(TypeError):
    pass


def check(args, compulsory_arg_names, optional_arg_names, args_formats):
    for name in compulsory_arg_names:
        if args.get(name) is None:
            return errors.NotPass(name)
