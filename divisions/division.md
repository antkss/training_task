![image](https://github.com/antkss/training_task/assets/88892713/bec0bda0-4f31-4154-ace9-16a50abca5a4)# write up divisions
- đầu tiên khi decompile ra ta thấy bài có ptrace nhằm mục đích antidebug, khi chạy bình thường thì hàm vẫn chạy như bình thường, chính vì vậy muốn debug thì phải sửa assembly code cùa chương trình để loại bỏ ptrace, chỉ cần dùng tính năng có sẵn của ida là có thể sửa được thành nop

![image](https://github.com/antkss/training_task/assets/88892713/1c1f96f4-2317-4421-80d9-8690280a5af5)

nhìn vào code thấy rằng bài đọc bằng read không chèn null byte

![image](https://github.com/antkss/training_task/assets/88892713/337af3a1-d8fe-4916-b80d-5eedf3220d32)

cộng thêm việc in ra màn hình bằng puts, mà puts và prinf đều đọc đến \0 nên 
có thể nhập dữ liệu vào để leak canary và địa chỉ 
trước tiên phải tách được phép tính ra để thực hiện tính toán để lấy kết quả nhập lại, như thế thì có thể thực hiện nhập đc lần thứ 2 


![image](https://github.com/antkss/training_task/assets/88892713/fb49f1a8-4343-4ef2-946d-aa992f3646a3)


sau khi tách xong thì cho vào payload + dữ liệu overwrite đến khi chạm canary
để nối thành chuỗi, em sử dụng 3 ký tự cuối khác các ký tự trước để thực hiện lấy canary dễ dàng hơn 

![image](https://github.com/antkss/training_task/assets/88892713/5d10fc4f-c66a-43ae-9e97-a304acd9be67)


sau khi lấy đc canary xong thì leak địa chỉ libc theo cách tương tự

![image](https://github.com/antkss/training_task/assets/88892713/847a9ad6-4535-49af-81fe-bb360385dac7)


sau khi leak xong thì tính toán các gadgets cần thiết để overwrite saved rip
vì read cho phép nhập 0x140 bytes nên quá đủ để overwrite saved rip của hàm loop 

![image](https://github.com/antkss/training_task/assets/88892713/9a2fde16-491f-4579-b8bf-9246a5afc388)

sau khi overwrite xong thì phép tính cuối cùng sẽ nhập 1 con số bất kì để hàm return false là while loop sẽ bị thoát và vào return 

![image](https://github.com/antkss/training_task/assets/88892713/9d39c56f-a963-474d-8d99-166275fd8e2e)



![image](https://github.com/antkss/training_task/assets/88892713/2f5184af-b249-47be-9b69-0e0377541f59)

