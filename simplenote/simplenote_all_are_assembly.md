# writeup simplenote 

- đầu tiên để làm được bài này em cần phải tìm ra trong code assembly của chương trình có 1 lỗi tại option 1

  ![image](https://github.com/antkss/training_task/assets/88892713/82e2a57f-40e2-4f5c-b96b-f0bbc6d20554)


![image](https://github.com/antkss/training_task/assets/88892713/73b59320-f6b6-45b5-b763-d6254294e764)

- mỗi lần vào option 1 nó sẽ subtract 0x40 tính từ lúc rsp trỏ đầu stack, vì vậy nó cứ lùi dần về sau, nhưng quan trọng hơn ở option 4 mỗi lần thực thi nó lại cộng thêm 0x40 bytes tính từ rsp vì vậy ta có thể ghi dữ liệu qua lại trên stack theo từng chunk có kích thước 0x40 bytes

  ![image](https://github.com/antkss/training_task/assets/88892713/92c93884-93b7-47b2-b061-02517a01784c)

khi đó ta có thể ghi đè return của hàm main để điều hướng chương trình 

- ban đầu khi chọn option 1 và nhập em thấy rằng có 1 địa chỉ chắn ngang ở đây, địa chỉ này chính là địa chỉ nhập rsi của hàm read ở option 1

  ![image](https://github.com/antkss/training_task/assets/88892713/1df8136e-1306-476b-8bb3-0680f7086c7f)
  chính vì vậy khi nhập full bytes sẽ tạo thành 1 chuỗi để chuyển sang option 2, có thể in ra từng byte một ở đây, và từ đó in cả địa chỉ

![image](https://github.com/antkss/training_task/assets/88892713/578525c8-2a21-4766-b37d-c2c5f165ce99)

sau mỗi lần write ra 1 byte thì nó sẽ tăng giá trị tại rbp-0x8 lên 1 bytes và nó quay trở về để thêm cộng giá trị đó với địa chỉ nhập rsp và lưu tại rdi, cứ như vậy địa chỉ tại rdi sẽ tăng dần cho đến khi giá trị tại địa chỉ trên rdi = NULL và từ đó in hết tất cả những gì trên stack bao gồm cả địa chỉ, sau khi lấy được địa chỉ thì em để đó để dùng cho lần sau 

![image](https://github.com/antkss/training_task/assets/88892713/f5fb830a-dd6f-44dd-9ad4-4823fac42eb2)



- sau khi có địa chỉ em cần ghi chuổi /bin/sh ở đâu đó trên stack và tính địa chỉ của nó
em sẽ lùi về 6 lần 0x40 theo hướng địa chỉ tăng và ghi /bin/sh ở đó 

![image](https://github.com/antkss/training_task/assets/88892713/ab163d63-a092-46cd-8a8c-036640e545ed)

- sau khi hoàn thành em cần ghi dữ liệu theo thứ tự của sigreturn trong bảng, chuck cuối sẽ đc nhập đầu tiên

![image](https://github.com/antkss/training_task/assets/88892713/2b52d510-94a2-4419-9a8b-839bf7ee78a0)

dựa vào bảng này thì em có thể xác định được dữ liệu cuối cùng em phải nhập sẽ là cs register có giá trị là 0x33 và fs là 0 vì đó là điều kiện khi chạy ở 64bit mode, nếu không thì code sẽ không chạy sau khi sigreturn , vì vậy em cần phải dùng offset ở cột bên trái để tính được địa chỉ của nó nằm ở chunk nào, tính từ syscall sigreturn, qua tính toán thì em thấy nó ở chunk thứ 3 nên em phải nhập dữ liệu cho thanh ghi bắt đầu từ đó,

em sẽ nhập chunk 6 là chuỗi /bin/sh rồi lấy địa chỉ 

tiếp theo đến chunk 3 sẽ là dữ liệu của rsp, rip và cs 

![image](https://github.com/antkss/training_task/assets/88892713/c9f122dc-7e09-4563-ba23-60439a62c534)

và chunk 2 là địa chỉ chuỗi /bin/sh và opcode 0x3b, chunk 1, 4 sẽ để trống vì không có thanh ghi nào cần dùng cả



- kết quả khi syscall

![image](https://github.com/antkss/training_task/assets/88892713/757fb2be-eb98-43bc-a790-298c2038fa8e)

![image](https://github.com/antkss/training_task/assets/88892713/01ceaaa7-5241-4802-8662-1559a14ce27a)



-kết quả khi cs=rác, chương trình sẽ không hoạt động 

![image](https://github.com/antkss/training_task/assets/88892713/14c36e8b-d8b3-428b-ac8d-3ac51a865857)

