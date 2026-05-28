# bill=int(input("Nhập đơn giá:"));
# amount=int(input("Nhập số lượng:"));
# total_payment=bill*amount;
# if(total_payment>=1000000):
#     total_payment=total_payment*0.9;
# print(f"Tổng tiền thanh toán:{total_payment}");

# count=0;
# correct_password=123456;
# for i in range(4):
#     input_password=int(input("Nhập mật khẩu:"));
#     if(count==3):
#         print("Tài khoản bị khóa!");
#         break;
#     elif(input_password==correct_password):
#         print("Đăng nhập thành công");
#         break;
#     else:
#         print("Mật khẩu sai, vui lòng nhập lại!");
#         count+=1;


correct_box=0;
count=0;
total_product=0
while True:
    product=int(input("Nhập vào số lượng sản phẩm:"));
    if(product<0):
        print("Số lượng không hợp lệ!");
    elif(product==0):
        break;
    else:
        total_product+=product;
        correct_box+=1;
print("Tổng số thùng hàng hợp lệ đã đếm:",correct_box);
print("Tổng số lượng sản phẩm thu được:",total_product);

