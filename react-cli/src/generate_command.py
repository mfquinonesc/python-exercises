import click
import validator as vl
import scaffold as sc
import utils as ut


def __is_valid_environment():

    if not vl.check_required_files(['package.json']):
        click.secho('Error: This command must be run inside a React project folder.', fg='red')
        return False

    if not vl.is_react_project():
        click.secho('Error: No React project was found in the current directory.', fg='red')
        return False

    return True


def __are_valid_parameters(type: str, name: str, style: str, style_ext: str, react_ext: str):

    types = ["component", "page", "router", "service", "store",
             "hook", "context", "class", "interface", "c", "p", "s"]

    if not type in types:
        click.secho(f"Error: '{type}' is not a valid argument.", fg='red')
        return False

    if not vl.check_file_path(name):
        click.secho(f"Error: The name or path you entered is invalid.", fg='red')
        click.secho(f"Invalid argument: {name}")
        return False

    style_modes = ['auto', 'regular', 'none', 'module', '-r', '-n', '-m']

    if not style in style_modes:
        click.secho(f"Error: Invalid style option: '{style}'", fg='red')
        click.secho(f"Allowed values are: {', '.join(style_modes)}.", fg='red')
        return False

    style_exts = ["auto", "css", "scss"]

    if not style_ext in style_exts:
        click.secho(f"Error: Invalid value for --style-ext: '{style_ext}'", fg='red')
        click.secho(f"Allowed values are: {', '.join(style_exts)}.", fg='red')

    react_exts = ["auto", "js", "jsx", "ts", "tsx"]

    if not react_ext in react_exts:
        click.secho(f"Error: Invalid value for --react-ext: '{react_ext}'", fg='red')
        click.secho(f"Allowed values are: {', '.join(react_exts)}.", fg='red')

    return True


def __create_component(name: str, react_ext: str, style_mode: str, style_ext: str, barrel: bool, test: bool, is_page:bool = False):

    dirs = name.split('/')
    component = dirs.pop()
    dirs.append(sc.__uppercase_first(component))
    path = '/'.join(dirs)
    dir_path = ut.format_path(path, True)
    path = sc.get_encapsulated_path(dir_path)

    extension = vl.get_component_extension() if react_ext == 'auto' else react_ext
    include_stylesheet = style_mode != 'none' and style_mode != '-n'
    # detect the module in the style files
    use_module = style_mode == 'module' or style_mode == '-m'
    use_scss = vl.get_styles_extension() == 'scss' if style_ext == 'auto' else style_ext == 'scss'

    generator = sc.generate_page if is_page else sc.generate_component
    generator(path, extension, include_stylesheet, use_module, use_scss)   
    
    click.secho(f"Created: {path}.{extension}", fg='green')
       
    if include_stylesheet:
        sc.generate_stylesheet(path, use_module, use_scss)
        click.secho(f"Created: {path}.{'module.'if use_module else ''}{ 'scss' if use_scss else 'css'}", fg='green')
    
    if test:
        sc.generate_test(path, extension)
        click.secho(f"Created: {path}.test.{extension}", fg='green')

    if barrel:
        use_typescript = extension in ['tsx', 'ts']
        sc.generate_barrel_file(path, use_typescript)
        click.secho(f"Created: {dir_path}/index.{'ts' if use_typescript else 'js'}", fg='green')


def __create_service(name: str, react_ext: str, include_axios: bool ):   
 
    use_typescript =  vl.detect_typescript() if  react_ext == 'auto' else (react_ext in ['tsx', 'ts'])
    sc.generate_service(name, use_typescript, include_axios)
    dirs = name.split('/')
    service = dirs.pop()
    click.secho(f"Created: {'/'.join(dirs)}/{service}Service.{'ts' if use_typescript else 'js'}", fg='green')


def __create_interface(name:str):
    sc.generate_interface(name)
    click.secho(f"Created: {name}.ts", fg='green')


def __create_class(name:str, react_ext:str):
    extension = ('ts' if vl.detect_typescript() else 'js') if react_ext == 'auto' else react_ext.replace('x','')
    sc.generate_class(name)
    click.secho(f"Created: {name}.{extension}", fg='green')




def __generate_template(type: str, name: str, style_mode: str, style_ext: str, react_ext: str, barrel: bool, test: bool, axios: bool):

    if type == "component" or type == "c":
        __create_component(name, react_ext, style_mode, style_ext, barrel, test)

    if type == "page" or type == "p":
       __create_component(name, react_ext, style_mode, style_ext, barrel, test, True)

    if type == "service" or type == "s":
       __create_service(name, react_ext, axios)

    if type == "interface":
        __create_interface(name)

    if type == 'class':
        __create_class(name, react_ext)

   


def __common_generate_options(func):
    func = click.argument('name')(func)
    func = click.argument('type')(func)
    func = click.option('--style', default='auto', help='')(func)
    func = click.option('--style-ext', default='auto', help='')(func)
    func = click.option('--react-ext', default='auto', help='')(func)
    func = click.option('--barrel', '-b', is_flag=True, help='')(func)
    func = click.option('--test', '-t', is_flag=True, help='')(func)
    func = click.option('--axios','-a', is_flag=True, help='')(func)
    return func


def genarate_handler(type: str, name: str, style: str, style_ext: str, react_ext: str, barrel: bool, test: bool, axios: bool):

    if not __is_valid_environment():
        return

    if not __are_valid_parameters(type, name, style, style_ext, react_ext):
        return

    __generate_template(type,name, style, style_ext, react_ext, barrel, test, axios)  



@click.command()
@__common_generate_options
def g(type: str, name: str, style: str, style_ext: str, react_ext: str, barrel: bool, test: bool, axios: bool):

    genarate_handler(type, name, style, style_ext, react_ext, barrel, test, axios)


@click.command()
@__common_generate_options
def generate(type: str, name: str, style: str, style_ext: str, react_ext: str, barrel: bool, test: bool, axios: bool):

    genarate_handler(type, name, style, style_ext, react_ext, barrel, test, axios)
