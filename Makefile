.PHONY: all build unittest buildtest

all: clean build unittest

build:
	pip install .

test:
	python -m unittest discover ./unittests

buildtest: build test

clean:
	rm -rf build/*
	rm -rf src/cython/build/*
	rm -f src/artery/*.pyd
	rm -f src/artery/*/*.pyd
	rm -f src/artery/*/*/*.pyd
	rm -f src/artery/*.so
	rm -f src/artery/*/*.so
	rm -f src/artery/*/*/*.so