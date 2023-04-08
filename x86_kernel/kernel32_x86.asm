; build with nasm -g -f bin kernel32_x86.asm -o kernel32_x86.bin
        BITS 32
        section .data

        section .text
        global main

main:
        ; this routine will jump to the code you want to fuzz. replace the memory address below.
        mov eax, 0x565561c0
        jmp eax