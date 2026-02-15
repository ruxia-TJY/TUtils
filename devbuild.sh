rm -rf ~/.tutils

cp -r ./examples ~/.tutils/

pip uninstall TUtils -y

rm -rf build/ dist/ tutils.egg-info __pycache__ .pytest_cache

pip install -e .