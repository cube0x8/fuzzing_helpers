#!/bin/sh
rm -f kernel32_x86.bin mboot.o kernel32_x86.elf
nasm -g -f bin kernel32_x86.asm -o kernel32_x86.bin
nasm -g -F dwarf -f elf32 mboot.asm -o mboot.o
ld -Ttext=0x101000 -Tdata=0x100000 -melf_i386 mboot.o -o kernel32_x86.elf
