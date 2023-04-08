# Fuzzing misc
This repository contains random scripts, tools and material for fuzzing things.

* gdb_dump: this tool can be used to dump the memory of a process from a live gdb instance. 
The dump can be later loaded in `qemu-system` and fuzzed.
* x86_kernel: a dummy 32bit ELF binary that can be used as `-kernel` in QEMU 
* x86_fuzzing_target: a simple 32 bit fuzzing target taken from https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/qemu_systemmode