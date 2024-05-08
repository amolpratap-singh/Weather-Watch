import os
import re
import yaml
import shutil

api_spec_dir = os.getenv("API_SPEC_DIR", "weather-api-spec")
build_src_dir = os.getenv("API_SERVER_BUILD_DIR", "build_src")
api_ctrl_dir = os.getenv("API_SERVER_DIR", "weather-api-server-app/src")

target_dir = os.path.join(build_src_dir, "src")
base_config_file = os.path.join(build_src_dir, "base_configuration.yaml")

final_spec = dict()
final_spec['paths'] = dict()
final_spec['components'] = dict()
final_spec['components']['schemas'] = dict()

def merge_dict(src, dst):
    for key, val in src['paths'].items():
        if key not in dst['paths']:
            dst['paths'][key] = val
    
    if 'components' in src.keys():
        for key, val in src['components']['schemas'].items():
            if key not in dst['components']['schemas']:
                dst['components']['schemas'][key] = val

for file in os.listdir(api_spec_dir):
    if file.endswith('.yaml'):
        if file == "static_page.yaml":
            print(f"Skipping the file: {file}")
            continue
        with open(os.path.join(api_spec_dir, file)) as f:
            new_spec = yaml.safe_load(f)
            merge_dict(new_spec, final_spec)
            
# Addition of base configuration file to final spec
with open(base_config_file) as f:
    new_spec = yaml.safe_load(f)
    final_spec.update(new_spec)

print(final_spec)

# Creation of Final spec
out_spec_file = os.path.join(build_src_dir, "weather_watch_api.yaml")
with open(out_spec_file, mode="w") as f:
    yaml.safe_dump(final_spec, f)
    
# Generate models using swagger-codegen-cli
os.system(f"java -jar swagger-codegen-cli.jar generate -i {out_spec_file} -l python-flask -o {target_dir}")

# Copy the Controllers
dst_controllers_dir = os.path.join(target_dir, 'swagger_server', 'controllers')
print(f"dst_controllers_dir: {dst_controllers_dir} ")

src_controllers_dir = os.path.join(api_ctrl_dir, 'controllers')
print(f"src_controller_dir: {src_controllers_dir}")

for file in os.listdir(src_controllers_dir):
    shutil.copy(os.path.join(src_controllers_dir, file), dst_controllers_dir)
    
# TODO just check is it required or not
# Update of Generated controllers
for file in os.listdir(dst_controllers_dir):
    if re.match('v[0-9]*(_[a-z0-9]*)+_controller.py', file):
        file_path = os.path.join(dst_controllers_dir, file)
        
        with open(file_path) as f:
            content = f.readlines()
        import_file = f"{file.split('.')[0]}_defined"
        content.insert(0, f"""import inspect
from utils import gen_utils
from swagger_server.controllers import {import_file}
""")
        func_name = ''
        for func in content:
            if func.startswith('def '):
                func_name = func.split('(')[0].split()[1]
            if func.__contains__('.is_josn:'):
                index = content.index(func)
                content[index] = func.replace('.is_json:', '.mimetype == "application/json":')
            if func.__contains__('.get_json()'):
                index = content.index(func)
                content[index] = func.replace('body = ', 'pass # body = ')
            if func.__contains__("return 'do some magic!'"):
                return_func = func.replace("return 'do some magic!'",
                                           f"return gen_utils.call_function({import_file}.{func_name}, inspect.currentframe().f_locals)")
                index = content.index(func)
                content[index] = return_func
        with open(file_path, mode='w') as w:
            w.writelines(content)


