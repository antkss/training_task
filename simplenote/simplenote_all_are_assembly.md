# writeup simplenote 

- đầu tiên để làm được bài này em cần phải tìm ra trong code assembly của chương trình có 1 lỗi tại option 1

  ![image](https://github.com/antkss/training_task/assets/88892713/82e2a57f-40e2-4f5c-b96b-f0bbc6d20554)


![image](https://github.com/antkss/training_task/assets/88892713/73b59320-f6b6-45b5-b763-d6254294e764)

- mỗi lần vào option 1 nó sẽ subtract 0x40 tính từ lúc rsp trỏ đầu stack, vì vậy nó cứ lùi dần về sau, nhưng quan trọng hơn ở option 4 mỗi lần thực thi nó lại cộng thêm 0x40 bytes tính từ rsp vì vậy ta có thể ghi dữ liệu qua lại trên stack theo từng block có kích thước 0x40 bytes

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

sau khi hoàn thành em cần ghi dữ liệu theo thứ tự của sigreturn 


