# GDB dump

This script can be used to dump the address space of a process using gdb. The dump can be loaded into QEMU by using the 
`-device gdb_map_layout` command line option.

## How does it work?
The script will first execute the command `info proc mapping` for dumping the entire debugged process' mapped 
memory. The start and end addresses will be extracted from the output and used to generate a `dump binary memory` command
for each memory allocation.

The `layout_memory` is generated in the output directory, and it contains information obtained from 
`info proc mapping`, which can be later parsed from QEMU. Also, each entry contains the path to the dump file of its 
respective memory area.

If a memory area cannot be dumped, it will be automatically skipped, and it won't be present in the generated dump.

## How to use it
- [Mandatory] Initialize the `OUTDIR` variable, where the dump files will be stored. For example:

`OUTDIR = /tmp/dump`

- [Optional] Initialize the `PID` variable. The `info proc mapping` command might require the process ID when you attach
to a remote `gdbserver` instance.

`PID = "1327"`

- From your gdb session, execute the following command:

`(gdb) source gdb_dump.py`

- The file `layout_memory` will be generated in the directory specified in the `OUTDIR` variable, together with 
the dump files for all memory regions.