run:
	python src/main.py

today:
	python src/init.py | xargs nvim

upload: resize
	python src/upload.py

resize:
	python src/resize.py

