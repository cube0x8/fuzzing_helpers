# x86 (32 bit) basic kernel

A basic kernel with multiboot header that can be loaded and booted from QEMU. After initialization, the kernel will jump 
to the user-specified address.

The address where to jump to it's hardcoded in the file `kernel32_x86.asm` and can be replaced with one of your choice.

To build the kernel, run:

`./build.sh`

Then, pass the generated `kernel32_x86.elf` file to the QEMU's `-kernel` command line switch.

The `gdbinit` file can be used to debug the BIOS and the kernel (when using QEMU `-s -S` command line options):

`gdb -x gdbinit`

This will display real-mode instructions during debugging. If you want to display protected mode instructions as well,
run:

`(gdb) display /5i $pc`