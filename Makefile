##########################
#	Makefile template.
##########################

# config your c++ compiler.
export CC=g++

# Using -Ofast instead of -O3 might result in faster code, 
# but is only supported by newer GCC versions
CFLAGS = -pthread -O3 -Wall -fPIC # -shared
#DEBUG_CFLAGS= -lm -pthread -O0 -Wall -g

# flag for linker.
LDFLAGS= -pthread -lm -fPIC

# libs 
LIBS= -lm

# includes.
INCLUDES=

# output obejcts.
OBJECTS=

TARGETS= 

# common function for make.
define notice_log
	@echo -e "\033[40;32;1m --> $(1) <-- \033[0m"
endef

# fake object.
.PHONY: all output clean

all: clean $(TARGETS) output
	$(call notice_log, 'MAKE ALL!')

output:
	rm -rf output
	mkdir output

clean:
	rm -rf $(OBJECTS) $(TARGETS) *~ .*.swp *.pyc 

# common object.
$(OBJECTS): %.o:%.cc
	$(call notice_log, '[[ $@ ]]'
	$(CC) -c $^ -o $@ $(CFLAGS) $(INCLUDES)

#
# Example of a bin.
#bin : a.cc b.cc
#	$(call notice_log, "make : [[ $@ ]]")
#	$(CC) $^ -o $@ $(CFLAGS) $(LIBS) $(INCLUDES)
#
# Example of a so.
#some.so: some.cc some.o
#	$(call notice_log, "make [[ $@ ]]")
#	$(CC) $(CFLAGS) $(LDFLAGS) $(INCLUDES) -o $@ $(filter %.cpp %.o %.c %.cc, $^)
#


