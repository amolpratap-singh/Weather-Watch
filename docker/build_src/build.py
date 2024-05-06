import os
import yaml


api_spec_dir = os.getenv("API_SPEC_DIR", "weather-api-spec")
build_src_dir = os.getenv("API_SERVER_BUILD_DIR", "build_src")
api_ctrl_dir = os.getenv("API_SERVER_DIR", "weather-api-server-app")

#target_dir = os.path.join(build_src_dir, "weather-api-server")
target_dir = "weather-api-server-app"
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
#os.system(f"java -jar swagger-codegen-cli.jar generate -i {out_spec_file} -l python-flask -o {target_dir}")
        