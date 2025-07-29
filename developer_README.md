## Overview

### Adding new Perturbations
In `examples\make_a_new_perturbations_example.ipynb` we show how to add a simple Perturbation for your own use. 
If you want to add a Perturbation to this package, you should do a bit more
- Make your new Perturbation, with at least the three required abstract methods: (1) `__init__`, (2) `_infer_transformation`, (3) `_apply_perturbation`
- Make a script for in the `examples/perturbation_demos/` folder, which shows the purpose and result of your perturbation.
- In `noisy_load_profiles/perturbations/__init__.py`, import the new perturbation, and add it to `__all__`

### Uploading new version

Overview to upload new versions:
- Change the version number in the .toml
- remove the dist folder
- run `python -m build`
- run `twine upload dist/*` (you need to done `pip install twine` in this environment)
- When twine asks for the API key, ctrl+c and than rightclick to add the API key that starts with pypi-...
