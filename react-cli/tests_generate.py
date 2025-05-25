from src.scaffold import *
import shutil


# Delete folders
try:
    shutil.rmtree('tests')       
except Exception as e:
    pass


try:  
    shutil.rmtree('node_modules')    
except Exception as e:
    pass


# Testing scaffold

# Testing components

file_path = 'tests/components/button'

generate_component(file_path, '.js', True, True, True)

generate_component(file_path, '.jsx', True)

generate_component(file_path, '.tsx')

# Testing pages

file_path = 'tests/pages/home'

generate_page(file_path, '.js', True, True, True)

generate_page(file_path, '.jsx', True)

generate_page(file_path, '.tsx')

# Testing stores

file_path = 'tests/stores/appStore'

generate_store(file_path, '.js')

generate_store(file_path, '.jsx')

generate_store(file_path, '.tsx')

# Testing routes 

file_path = 'tests/routers/appRouter'

generate_router(file_path, '.js')

generate_router(file_path, '.jsx')

generate_router(file_path, '.tsx')

# Testing classes

file_path = 'tests/classes/user'

generate_class(file_path, True)

generate_class(file_path)

# Testing interfaces

file_path = 'tests/interfaces/login'

generate_interface(file_path)

# Testing services

file_path = 'tests/services/auth'

generate_service(file_path, False, True)

generate_service(file_path, True)

# Testing hooks

file_path = 'tests/hooks/width'

generate_hook(file_path)

generate_hook(file_path, True)

# Testing full component creation

file_path = get_encapsulated_path('tests/app/Button')

generate_component(file_path,'jsx',True)
generate_stylesheet(file_path)

file_path = get_encapsulated_path('tests/app/Selector')

generate_component(file_path,'jsx',True,True)
generate_stylesheet(file_path,True)

# Testing styles 

file_path = 'tests/styles/index'

generate_stylesheet(file_path, True)
generate_stylesheet(file_path, True,True)

# Testing folders 

file_path =  'tests/modules/'

generate_folders(file_path)

# Testing get encapsulated path

path = get_encapsulated_path('tests/react/components/modal')
print('path = ', path)

# Testing Context 

file_path = 'tests/context/login'

generate_context(file_path)

generate_context(file_path, True)

# Testing component test file 

file_path = get_encapsulated_path('tests/app/Button')

generate_test(file_path,'jsx')

file_path = get_encapsulated_path('tests/app/Selector')

generate_test(file_path,'tsx')

generate_test(file_path,'js')

# Testing barrel file 

file_path = get_encapsulated_path('tests/app/Selector')

generate_barrel_file(file_path)

generate_barrel_file(file_path, True)