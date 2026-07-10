.PHONY: resume build check serve

resume:
	cd resume-src && xelatex -interaction=nonstopmode -halt-on-error bowei-xia-resume.tex

build: resume
	python3 scripts/build_site.py

check:
	python3 scripts/build_site.py --check

serve: build
	python3 -m http.server 4173 --directory site
