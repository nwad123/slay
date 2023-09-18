# Things TODO for SLAY

1. Implement the makefile commands for GHDL. Currently SLAY does not correctly
build all of the design units in a file and so is unuseable across multiple
files. GHDL has the import command and some other commands it can use to
generate makefiles which should make this process easier.

2. Add a message to `slay check` that indicates if it was successful or not.

