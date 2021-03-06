# list of module
DIRECTORIES = Decoders ProblemUtils Solvers Utils

# makes the code cleaner by handling verbosity within these variables
VERBOSE_1 = ;
VERBOSE_0 = > /dev/null ;
V = 0
VERBOSE = $(VERBOSE_$(V))

# help getting printed out when no command is specified
help:
	$(info make doc [V=1]: grenerate the documentation of the project (html), set V to 1 for a verbose output)
	$(info make clean: cleans the generated documentation)
	$(info )

# generates the documentation of the whole project, stored in doc/
doc:
	@cd docs/ && \
	for dir in $(DIRECTORIES); do \
		sphinx-apidoc -f -o source ../src/$$dir/ $(VERBOSE) \
	done && \
	make html $(VERBOSE)

# removes all the junk generated by sphinx (you can comment it if you want
# it should make generating the doc faster if you generate it multiple times)
	@rm -rf **/*.pyc
	@rm -rf **/**/*.pyc
	@rm -rf **/__pycache__/
	@rm -rf **/**/__pycache__
	$(info Documentation will be generated in docs/build/html/)

# removes the doc folder
clean:
	@rm -rf docs/build/
	@rm -rf docs/source/modules.rst

	@for dir in $(DIRECTORIES); do \
		rm -rf docs/source/$$dir.rst $(VERBOSE) \
	done

# so each command can be called all the time (otherwise Makefile waits for 
# a change in the args, which will never happen since no args are given)
.PHONY: all doc clean