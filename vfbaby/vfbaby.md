# write up vfbaby 
- khi mở chương trình lên, chương trình cho phép em có thể có được địa chỉ của libc

![image](https://github.com/antkss/training_task/assets/88892713/eff50485-56f2-4c56-b24d-039e03afdf76)

-  Bài tập trung vào lỗi của exit vì bài có arbitrary read, nhìn vào hàm dường như không thấy gì ngoài việc ta có thể ghi dữ liệu vào 1 địa chỉ nào đó thông qua read vì thế em có thể dùng read để ghi 1 cái gì đó vào vùng ghi được của libc

```assembly
  0x7c0c1f3c0000     0x7c0c1f3c4000 r--p     4000 1c0000 /home/as/pwnable/vfbaby/libc-2.23.so
    0x7c0c1f3c4000     0x7c0c1f3c6000 rw-p     2000 1c4000 /home/as/pwnable/vfbaby/libc-2.23.so
    ```
khi debug và đi sâu xuống hàm exit(), em bắt gặp nó call cái địa chỉ này, đây chính là nó đang call hàm __run_exit_handlers
```assembly
 ► 0x5d00caa00780 <exit@plt>     jmp    qword ptr [rip + 0x20085a]    <exit>
    ↓
   0x7c0c1f03a030 <exit>         lea    rsi, [rip + 0x38a5c1]
   0x7c0c1f03a037 <exit+7>       sub    rsp, 8
   0x7c0c1f03a03b <exit+11>      mov    edx, 1
   0x7c0c1f03a040 <exit+16>      call   0x7c0c1f039f10                <0x7c0c1f039f10>
 
   0x7c0c1f03a045                nop    word ptr cs:[rax + rax]
   0x7c0c1f03a04f                nop    
   0x7c0c1f03a050 <on_exit>      push   rbp
   0x7c0c1f03a051 <on_exit+1>    push   rbx
   0x7c0c1f03a052 <on_exit+2>    mov    rbx, rdi
   0x7c0c1f03a055 <on_exit+5>    lea    rdi, [rip + 0x38a59c]
   ```


```C
void
exit (int status)
{
  __run_exit_handlers (status, &__exit_funcs, true, true);
}
```

- tiếp tục đi sâu vào hàm đó thì em 
