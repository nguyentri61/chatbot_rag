-- Tạo bảng lưu hướng dẫn sử dụng UI
CREATE TABLE IF NOT EXISTS ui_instructions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(500) NOT NULL,
    instruction TEXT NOT NULL,
    category VARCHAR(100),
    keywords TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    FULLTEXT INDEX idx_keywords (keywords, question)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


INSERT INTO ui_instructions (question, instruction, category, keywords) VALUES
('Làm sao để tham gia một hoạt động?',
'**Cách tham gia hoạt động:**  

1. Vào **"Danh sách hoạt động"**  
2. Chọn hoạt động muốn tham gia  
3. Xem chi tiết:
   • Thời gian  
   • Địa điểm  
   • Số người tham gia  
4. Nhấn **"Tham gia hoạt động"**  
5. Trạng thái sẽ chuyển sang **"Đã đăng ký"**

**Lưu ý:**  
• Thành viên không tham gia mà không có lý do hợp lệ sẽ bị **trừ điểm uy tín**  
• Có thể gửi **lý do vắng mặt** sau khi hoạt động kết thúc.',
'Activity',
'tham gia hoạt động, đăng ký hoạt động, join activity');


INSERT INTO ui_instructions (question, instruction, category, keywords) VALUES
('Làm thế nào để gửi lý do vắng mặt cho hoạt động?',
'**Cách gửi lý do vắng mặt:**  

1. Đăng nhập vào hệ thống  
2. Vào **"Hoạt động của tôi"**  
3. Chọn hoạt động bạn đã đăng ký nhưng **không tham gia**  
4. Khi trạng thái là **"Vắng mặt"**, nhấn **"Gửi lý do vắng mặt"**  
5. Nhập nội dung lý do:
   • Lý do cá nhân / sức khỏe / công việc  
   • Có thể đính kèm minh chứng (nếu có)  
6. Nhấn **"Gửi lý do"** để hoàn tất  

**Lưu ý:**  
• Mỗi hoạt động chỉ được gửi lý do **1 lần**  
• Lý do sẽ được gửi đến **Chủ CLB** để xét duyệt  
• Trong thời gian chờ duyệt, điểm uy tín vẫn bị trừ tạm thời.',
'Activity Attendance',
'gửi lý do vắng mặt, vắng mặt hoạt động, xin phép vắng, absence reason');


INSERT INTO ui_instructions (question, instruction, category, keywords) VALUES
('Chủ CLB duyệt lý do vắng mặt như thế nào?',
'**Cách duyệt lý do vắng mặt (Chủ CLB):**  

1. Đăng nhập với tài khoản **Chủ CLB**  
2. Vào **"Quản lý CLB"** → **"Hoạt động"**  
3. Chọn hoạt động cần quản lý  
4. Mở tab **"Danh sách vắng mặt"**  
5. Chọn thành viên đã gửi lý do  
6. Xem chi tiết:
   • Nội dung lý do  
   • Thời gian gửi  
   • Minh chứng (nếu có)  
7. Thực hiện:
   • **Chấp nhận** → Hoàn lại điểm uy tín  
   • **Từ chối** → Giữ nguyên mức trừ điểm  

**Lưu ý:**  
• Mỗi lý do chỉ được duyệt một lần  
• Kết quả duyệt sẽ được gửi thông báo cho thành viên.',
'Club Management',
'duyệt lý do vắng mặt, xét duyệt vắng mặt, chủ CLB duyệt, attendance approval');

INSERT INTO ui_instructions (question, instruction, category, keywords) VALUES
('Làm thế nào để đăng ký tài khoản?',
'**Cách đăng ký tài khoản:**  

1. Truy cập trang **"Đăng ký"**  
2. Nhập thông tin:
   • Email  
   • Mật khẩu  
   • Xác nhận mật khẩu  
3. Nhấn **"Đăng ký"**  
4. Kiểm tra email và nhấn link **xác thực tài khoản**  
5. Sau khi xác thực, bạn có thể đăng nhập hệ thống  

**Lưu ý:**  
• Email phải hợp lệ và chưa được sử dụng  
• Mật khẩu tối thiểu 8 ký tự.',
'Account',
'đăng ký, tạo tài khoản, register, sign up');


INSERT INTO ui_instructions (question, instruction, category, keywords) VALUES
('Làm sao để đăng nhập?',
'**Cách đăng nhập:**  

1. Truy cập trang **"Đăng nhập"**  
2. Nhập:
   • Email  
   • Mật khẩu  
3. Nhấn **"Đăng nhập"**  
4. Hệ thống chuyển đến trang chính sau khi đăng nhập thành công  

**Lưu ý:**  
• Tài khoản cần được xác thực email trước khi đăng nhập.',
'Account',
'đăng nhập, login, sign in');


INSERT INTO ui_instructions (question, instruction, category, keywords) VALUES
('Quên mật khẩu thì phải làm sao?',
'**Cách lấy lại mật khẩu:**  

1. Tại màn hình **"Đăng nhập"**, chọn **"Quên mật khẩu"**  
2. Nhập email đã đăng ký  
3. Nhấn **"Gửi yêu cầu"**  
4. Kiểm tra email và nhấn link đặt lại mật khẩu  
5. Nhập mật khẩu mới và xác nhận  

**Lưu ý:**  
• Link đặt lại mật khẩu có thời hạn  
• Không chia sẻ link cho người khác.',
'Account',
'quên mật khẩu, reset password, lấy lại mật khẩu');


INSERT INTO ui_instructions (question, instruction, category, keywords) VALUES
('Tôi có thể tạo CLB cầu lông như thế nào?',
'**Cách tạo CLB:**  

1. Đăng nhập hệ thống  
2. Vào **"Menu"** → **"CLB"**  
3. Nhấn **"Tạo CLB mới"**  
4. Nhập thông tin:
   • Tên CLB  
   • Mô tả  
   • Môn thể thao (Cầu lông)  
   • Khu vực hoạt động  
   • Ảnh đại diện CLB  
   • Số lượng thành viên tối đa 
5. Nhấn **"Tạo CLB"**

**Lưu ý:**  
• Người tạo sẽ trở thành **Chủ CLB**  
• Chủ CLB có quyền quản lý thành viên và hoạt động.',
'CLB Management',
'tạo CLB, tạo club cầu lông, lập CLB');


INSERT INTO ui_instructions (question, instruction, category, keywords) VALUES
('Tôi có thể tham gia CLB như thế nào?',
'**Cách tham gia CLB:**  

1. Vào **"Danh sách CLB"**  
2. Tìm CLB bạn quan tâm  
3. Nhấn vào CLB để xem chi tiết  
4. Chọn **"Tham gia CLB"** hoặc **"Gửi yêu cầu tham gia"**  
5. Chờ **Chủ CLB** phê duyệt  
6. Sau khi được duyệt, bạn trở thành **thành viên CLB**

**Lưu ý:**  
• Một số CLB cho phép tham gia tự do  
• Một số CLB yêu cầu xét duyệt.',
'CLB Management',
'tham gia CLB, join club, đăng ký CLB');


INSERT INTO ui_instructions (question, instruction, category, keywords) VALUES
('Làm sao để đăng ký tham gia giải đấu cầu lông?',
'**Cách đăng ký giải đấu:**  

1. Vào **"Giải đấu"**  
2. Chọn giải đấu cầu lông và hạng mục muốn tham gia  
3. Xem thông tin chi tiết và điều kiện  
4. Nhấn **"Đăng ký tham gia"**  
5. Xác nhận thông tin cá nhân  
6. Chờ Ban tổ chức xét duyệt  

**Lưu ý:**  
• Một số giải yêu cầu trình độ hoặc hạng đấu  
• Kiểm tra thời hạn đăng ký.',
'Tournament',
'đăng ký giải đấu, tham gia giải cầu lông');

INSERT INTO ui_instructions (question, instruction, category, keywords) VALUES
('Các loại sự kiện cầu lông trong hệ thống gồm những gì?',
'**Các loại sự kiện cầu lông:**  

• **Hoạt động:** Sinh hoạt định kỳ, giao lưu các thành viên của CLB  
• **Giải đấu:** Thi đấu chính thức, có bảng đấu và xếp hạng  

**Lưu ý:**  
• Mỗi sự kiện có điều kiện tham gia khác nhau  
• Thành viên cần đăng ký trước khi tham gia.',
'Activity',
'sự kiện cầu lông, hoạt động cầu lông, badminton event');

INSERT INTO ui_instructions (question, instruction, category, keywords) VALUES
('Làm thế nào để cập nhật hồ sơ cá nhân?',
'**Cách cập nhật hồ sơ cá nhân:**  

1. Đăng nhập vào hệ thống  
2. Nhấn vào **avatar / tên người dùng** ở góc trên  
3. Chọn **"Hồ sơ cá nhân"** hoặc **"Thông tin cá nhân"**  
4. Cập nhật các thông tin:
   • Họ và tên  
   • Ngày sinh  
   • Giới tính  
   • Số điện thoại  
   • Địa chỉ  
   • Ảnh đại diện  
   • Trình độ chơi cầu lông  
5. Nhấn **"Lưu thay đổi"**

**Lưu ý:**  
• Một số thông tin quan trọng (email) có thể cần xác thực  
• Thông tin trình độ giúp hệ thống gợi ý hoạt động phù hợp.',
'Account',
'cập nhật profile, chỉnh sửa hồ sơ, sửa thông tin cá nhân, update profile');


INSERT INTO ui_instructions (question, instruction, category, keywords) VALUES
('Làm sao để xem lịch hoạt động?',
'**Cách xem lịch hoạt động:**  

1. Vào menu **"Lịch hoạt động"**  
2. Các hoạt động hiển thị dưới dạng Danh sách (List view)  
3. Nhấn vào từng hoạt động để xem chi tiết:
   • Thời gian  
   • Địa điểm  
   • Trạng thái tham gia  

**Lưu ý:**  
• Chỉ hiển thị các hoạt động bạn có quyền xem  
• Có thể theo dõi lịch hoạt động của CLB đã tham gia.',
'Schedule',
'xem lịch hoạt động, lịch CLB, lịch sự kiện, activity calendar');







