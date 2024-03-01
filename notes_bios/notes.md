# write up Notes bi0s
- đầu tiên nhìn vào source code thì chương trình sẽ tạo ra 2 thread mới chạy 2 hàm khác nhau là hàm choices và hàm start_routine

![image](https://github.com/antkss/training_task/assets/88892713/cf94f786-da17-4ed7-a8fb-95e3efcc70d6)


- hàm start_routine sẽ chạy liên tục hàm process
![image](https://github.com/antkss/training_task/assets/88892713/75530958-c430-48d2-ad06-3e6c5ca59f3b)

- hàm process sẽ check size -> mã hóa content của note -> copy note đến stack 

![image](https://github.com/antkss/training_task/assets/88892713/41e25fae-220e-425b-95d1-371bb0da7be2)

- hàm choices sẽ có các chức năng này

![image](https://github.com/antkss/training_task/assets/88892713/e5c1cf30-f3dc-4b32-afe6-ebf137307e0a)


![image](https://github.com/antkss/training_task/assets/88892713/cb5068c7-beaa-478b-abaa-199797ce9a0d)

tại hàm storenote ta có thể thay đổi note_size và content của note

tại hàm process có sleep ở 1 số chỗ như này ta có thể dùng để khai thác race condition

![image](https://github.com/antkss/training_task/assets/88892713/da7fdea6-f1ed-4800-a0a6-e663c0c84bc8)

sleep trong hàm encrypt_note

![image](https://github.com/antkss/training_task/assets/88892713/4d00f721-1b41-4d8b-ba1c-e73d84815641)

hàm check sẽ check size có vượt quá 64 hay không, nếu có thì nó sẽ báo size vượt quá kích thước và không memcpy note tới stack 
vì vậy đầu tiên em cần tạo ra note có kích thước vừa đủ để vượt qua check
sau khi đến hàm encrypt_note thì hàm sẽ có sleep là 2 giây 

![image](https://github.com/antkss/training_task/assets/88892713/299d1fd3-a804-4eac-9dcc-a52b473fa52c)

trong vòng 2 giây em cần phải viết script để thực hiện đổi kích thước cũng như content, vậy là em có thể leak được địa chỉ khi phóng đại kích thước cũng như overwrite saved rip của hàm process khi thực hiện xong memcpy 

đầu tiên em cần leak địa chỉ vì nhận ra rằng cần địa chỉ stack của thread start_routine để có thể lấy địa chỉ chuỗi /bin/sh dùng cho sau này 





