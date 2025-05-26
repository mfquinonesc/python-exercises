import click
import validator as vl
import scaffold as sc
import utils as ut


@click.command()
@click.argument('type')
@click.argument('name')
@click.option('--style', default='auto', help='')
@click.option('--style-ext', default='auto', help='')
@click.option('--react-ext', default='auto', help='')
@click.option('--barrel', '-b', is_flag=True, help='')
@click.option('--test', '-t', is_flag=True, help='')
def g(type: str, name: str, style: str, style_ext: str, react_ext: str, barrel: bool, test: bool):

    print(barrel, test)

    if not __is_valid_environment():
        return

    if not __are_valid_parameters(type, name, style, style_ext, react_ext):
        return

    __generate_template(type,name, style, style_ext, react_ext, barrel, test)

    click.secho(f"{','.join([type, name, style, style_ext, react_ext, str(barrel), str(test)])}", fg='green')


@click.command()
@click.argument('type')
@click.argument('name')
def generate():
    pass


def __is_valid_environment():

    if not vl.check_required_files(['package.json']):
        click.secho(
            'Error: This command must be run inside a React project folder.', fg='red')
        return False

    if not vl.is_react_project():
        click.secho(
            'Error: No React project was found in the current directory.', fg='red')
        return False

    return True


def __are_valid_parameters(type: str, name: str, style: str, style_ext: str, react_ext: str):

    types = ["component", "page", "router", "service", "store",
             "hook", "context", "class", "interface", "c", "s"]

    if not type in types:
        click.secho(f"Error: '{type}' is not a valid argument.", fg='red')
        return False

    if not vl.check_file_path(name):
        click.secho(
            f"Error: The name or path you entered is invalid.", fg='red')
        click.secho(f"Invalid argument: {name}")
        return False

    style_modes = ['auto', 'regular', 'none', 'module', '-r', '-n', '-m']

    if not style in style_modes:
        click.secho(f"Error: Invalid style option: '{style}'", fg='red')
        click.secho(f"Allowed values are: {', '.join(style_modes)}.", fg='red')
        return False

    style_exts = ["auto", "css", "scss"]

    if not style_ext in style_exts:
        click.secho(
            f"Error: Invalid value for --style-ext: '{style_ext}'", fg='red')
        click.secho(f"Allowed values are: {', '.join(style_exts)}.", fg='red')

    react_exts = ["auto", "js", "jsx", "ts", "tsx"]

    if not react_ext in react_exts:
        click.secho(
            f"Error: Invalid value for --react-ext: '{react_ext}'", fg='red')
        click.secho(f"Allowed values are: {', '.join(react_exts)}.", fg='red')

    return True


def __create_component(name: str, react_ext: str, style_mode: str, style_ext: str, barrel: bool, test: bool):

    folders = name.split('/')
    component = folders.pop()
    folders.append(sc.__uppercase_first(component))
    path = '/'.join(folders)
    path = ut.format_path(path, True)
    path = sc.get_encapsulated_path(path)

    extension = vl.get_component_extension() if react_ext == 'auto' else react_ext
    include_stylesheet = style_mode != 'none' and style_mode != '-n'
    use_module = style_mode == 'module' or style_mode == '-m'
    use_scss = vl.get_styles_extension() == 'scss' if style_ext == 'auto' else style_ext == 'scss'

    sc.generate_component(path, extension, include_stylesheet, use_module, use_scss)
    
    if include_stylesheet:
        sc.generate_stylesheet(path, use_module, use_scss)
    
    if test:
        sc.generate_test(path, extension)

    if barrel:
        use_typescript = extension in ['tsx', 'ts']
        sc.generate_barrel_file(path, use_typescript)        


def __generate_template(type: str, name: str, style_mode: str, style_ext: str, react_ext: str, barrel: bool, test: bool):

    # here has to be the typescript validation and asignament
    use_typescript = vl.detect_typescript()
    print('Is a typescript project ', use_typescript)
    # end

    if type == "component" or type == "c":
        __create_component(name, react_ext, style_mode, style_ext, barrel, test)

    if type == "service" or type == "s":
        pass

    if type == "page":
        pass

    if type == "interface":
        pass

    click.secho('DONE', fg='green')
