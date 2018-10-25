    #example make file    
clean-build: 
	rm -rf build/
	
clean-dist: 
	rm -rf dist/

clean: clean-build clean-dist 
	rm -rf .eggs/
	rm -f Pipfile.*
	rm -f VERSION
	find . -name "*.egg-info" -exec rm -rf {} +
	find . -name "*.dist-info" -exec rm -rf {} +
	find . -name "*.egg" -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

init: clean
	pipenv --python $(PYTHON_VERSION)
	pipenv run pip install pylint

bdist_wheel-depen: init
	mkdir -p build && cd build && pipenv run pip wheel -r ../requirements.txt --only-binary all

wheel: bdist_wheel-depen
	mkdir -p dist && mv build/*.whl dist && pipenv run python setup.py bdist_wheel
