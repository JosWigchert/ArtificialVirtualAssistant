import os
import importlib.util


def load_functions_from_folder(folder_path):
    folder_path = folder_path.replace("/", os.sep)
    function_dict = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            module_name = os.path.splitext(filename)[0]
            module_path = os.path.join(folder_path, filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Get all functions from the module
            functions = {}
            for f in dir(module):
                func = getattr(module, f)
                if callable(func):
                    functions[f] = func

            # Store the functions in a dictionary
            function_dict[module_name] = functions

    return function_dict
