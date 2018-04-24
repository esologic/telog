
import yaml

path = "filter_in.yaml"

with open(path, 'rt') as f:
    cfg = yaml.safe_load(f.read())

print(cfg)