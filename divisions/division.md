# write up divisions
- đầu tiên khi decompile ra ta thấy bài có ptrace nhằm mục đích antidebug, khi chạy bình thường thì hàm vẫn chạy như bình thường, chính vì vậy muốn debug thì phải sửa assembly code cùa chương trình để loại bỏ ptrace, chỉ cần dùng tính năng có sẵn của ida là có thể sửa được thành nop

![image](https://github.com/antkss/training_task/assets/88892713/1c1f96f4-2317-4421-80d9-8690280a5af5)

nhìn vào code thấy rằng bài đọc bằng read không chèn null byte

![image](https://github.com/antkss/training_task/assets/88892713/337af3a1-d8fe-4916-b80d-5eedf3220d32)

cộng thêm việc in ra màn hình bằng puts, mà puts và prinf đều đọc đến \0 nên 
có thể nhập dữ liệu vào để leak địa chỉ 
trước tiên phải tách được phép tính ra để thực hiện tính toán để lấy kết quả nhập lại, như thế thì có thể thực hiện nhập đc lần thứ 2 


![image](https://github.com/antkss/training_task/assets/88892713/fb49f1a8-4343-4ef2-946d-aa992f3646a3)


sau khi tách xong thì cho vào payload + dữ liệu overwrite đến khi chạm địa chỉ
để nối thành chuỗi, em sử dụng 3 ký tự cuối khác các ký tự trước để thực hiện lấy địa chỉ dễ dàng hơn 


