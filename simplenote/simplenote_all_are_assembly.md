# writeup simplenote 

- đầu tiên để làm được bài này em cần phải tìm ra trong code assembly của chương trình có 1 lỗi tại option 1

  ![image](https://github.com/antkss/training_task/assets/88892713/82e2a57f-40e2-4f5c-b96b-f0bbc6d20554)


![image](https://github.com/antkss/training_task/assets/88892713/73b59320-f6b6-45b5-b763-d6254294e764)

- mỗi lần vào option 1 nó sẽ subtract 0x40 tính từ lúc rsp trỏ đầu stack, vì vậy nó cứ lùi dần về sau, nhưng quan trọng hơn ở option 4 mỗi lần thực thi nó lại cộng thêm 0x40 bytes tính từ rsp vì vậy ta có thể ghi dữ liệu qua lại trên stack theo từng block có kích thước 0x40 bytes

  ![image](https://github.com/antkss/training_task/assets/88892713/92c93884-93b7-47b2-b061-02517a01784c)

khi đó ta có thể ghi đè return của hàm main để điều hướng chương trình 


