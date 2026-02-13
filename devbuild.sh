rm -rf ~/.tutils/config.yaml

cp -r ./examples/Scripts ~/.tutils/

pip uninstall TUtils -y

rm -rf build/ dist/ tutils.egg-info __pycache__ .pytest_cache

pip install -e .