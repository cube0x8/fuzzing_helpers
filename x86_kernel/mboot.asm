; build with nasm -felf32 mboot.asm -o mboot.o

bits 32
global _start

MB1_MAGIC    equ 0x1badb002
MB1_FLAGS    equ 0x00000000
MB1_CHECKSUM equ -(MB1_MAGIC+MB1_FLAGS)

section .data
align 4
    dd MB1_MAGIC
    dd MB1_FLAGS
    dd MB1_CHECKSUM

section .text
_start:
    incbin "kernel32_x86.bin"
