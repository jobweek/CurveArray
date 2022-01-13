import importlib
import sys

path = 'W:\Users\79253\AppData\Roaming\Python\Python39\site-packages\memory_profiler.py'
name = 'memory_profiler'

spec = importlib.util.spec_from_file_location(name, path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module 
spec.loader.exec_module(module)