%.json: %.yml
	yq . $< > $@ || rm -f $@

all: hooks.json
