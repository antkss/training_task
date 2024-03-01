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


![image](https://github.com/antkss/training_task/assets/88892713/765210d0-b099-451c-a06e-acb41434fb1b)


ở đây ta thấy vùng địa chỉ khi nhập notes và vùng địa chỉ của ld-linux gần nhau nên có thể phóng đại kích thước để leak địa chỉ từ ld-linux 

![image](https://github.com/antkss/training_task/assets/88892713/c6b4b3a1-44cf-4946-be51-2427a2369f4b)

tại đây em phát hiện địa chỉ của thread nên em leak luôn


![image](https://github.com/antkss/training_task/assets/88892713/4480a95d-4dc2-4fe4-a8c7-52baa0703477)

đầu tiên em nhập đúng kích thước, sau đó đợi khoảng 2 giây để vượt qua check, sau đó em đổi kích thước sang 5706 để leak địa chỉ, sau khi đổi kích thước và chọn option 3 là print_note thì em leak đc địa chỉ cần leak, lọc đống rác trên màn hình và lấy địa chỉ rồi tính chỗ mình cần nhập chuỗi /bin/sh

sau khi lấy được địa chỉ nhân lúc hàm chưa kết thúc thì em sẽ đổi content của note thành gadget để overwrite saved rip của process, cùng với đó là ghi chuỗi /bin/sh vào chỗ mình cần ghi 


![image](https://github.com/antkss/training_task/assets/88892713/a7bcb351-a8d3-4ae3-91f6-8ad78ac9d80b)

gadget sẽ là gadget có sẵn của rdi, gắn gadget vào để nó chạy được syscall sigreturn và setup frame cho sigreturn rồi gửi đi 

![image](https://github.com/antkss/training_task/assets/88892713/c4248108-d7c4-42c0-9048-bdd77506956d)

vậy là xong xuôi, shellcode sẽ được thực thi khi chữ Sent! xuất hiện 


![image](https://github.com/antkss/training_task/assets/88892713/95c8bfc6-718a-44fa-86f0-e154db436d59)



# lưu ý

- bài chỉ run khi alsr được bật full tính năng 



