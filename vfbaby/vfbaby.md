# write up vfbaby 
- khi mở chương trình lên, chương trình cho phép em có thể có được địa chỉ của libc

![image](https://github.com/antkss/training_task/assets/88892713/eff50485-56f2-4c56-b24d-039e03afdf76)

-  Bài tập trung vào lỗi của exit vì bài có arbitrary read, nhìn vào hàm dường như không thấy gì ngoài việc ta có thể ghi dữ liệu vào 1 địa chỉ nào đó thông qua read vì thế em có thể dùng read để ghi 1 cái gì đó vào vùng ghi được của libc


![image](https://github.com/antkss/training_task/assets/88892713/96320f1a-f511-4b11-a4cf-065d8a21afbc)

khi debug và đi sâu xuống hàm exit(), em bắt gặp nó call cái địa chỉ này, đây chính là nó đang call hàm __run_exit_handlers
![image](https://github.com/antkss/training_task/assets/88892713/25b25f3d-e1f1-4219-b9c1-dbb9fdb5bf52)


`
void
exit (int status)
{
  __run_exit_handlers (status, &__exit_funcs, true, true);
}
`
