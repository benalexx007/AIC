# Báo Cáo Đánh Giá & Học Hỏi Từ Query Mẫu (Sample Evaluation Report)

> **Cập nhật lần cuối:** 2026-09-01 04:53:04 UTC  
> **Tổng số mẫu đã đánh giá:** 29 | **Đã học (Learned):** 27 | **Từ chối (Rejected):** 2

## 📊 Bảng Tổng Hợp Đánh Giá

| Sample ID | Video ID | Seed (Line 1) | Extracted Intervals | Tier | Accuracy | Decision | Key Insights |
|---|---|---|---|:---:|:---:|:---:|---|
| `query-p2-1-kis` | `L24_V035` | `488` | `[450, 1600]` | Tier 3 | 100.0% | ✅ **LEARNED** | Ky thuat la hoa thuc the van hoa/bieu dien dac thu (Cultural/Performance Defamil... |
| `query-p2-2-kis` | `L21_V013` | `22410` | `[22335, 22985]` | Tier 3 | 100.0% | ✅ **LEARNED** | Ky thuat Dinh vi Hai Dau Ranh Gioi Thoi Gian (Dual-Boundary Temporal Framing) bu... |
| `query-p2-3-kis` | `L24_V017` | `270` | `[240, 360]` | Tier 2 | 60.0% | ❌ REJECTED | Rejected due to Tier < 3 or Accuracy < 85%... |
| `query-p2-4-kis` | `L25_V083` | `67` | `` | Tier 1 | 0.0% | ❌ REJECTED | Rejected due to Tier < 3 or Accuracy < 85%... |
| `query-p2-5-kis` | `L21_V022` | `26076` | `[25830, 26130]` | Tier 3 | 100.0% | ✅ **LEARNED** | Ky thuat Phan Tách Trang Phuc & Vi Hanh Dong Da Thuc The (Multi-Entity Fine-grai... |
| `query-p2-6-kis` | `L21_V018` | `15780` | `[15616, 16480]` | Tier 3 | 85.0% | ✅ **LEARNED** | Ky thuat Nhan Dien Tu The Bat Thuong / Hanh Dong Hiem (Extreme Pose & Anomaly Ac... |
| `query-p2-7-qa` | `L21_V009` | `21172` | `[20950, 21250]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat Phoi Hop Da Goc Nhin (Cross-Perspective Shot Continuity) trong MOD-FLOW... |
| `query-p2-8-trake` | `L27_V011` | `3827` | `[3820, 4200]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat Chuoi Su Kien Tuyen Tinh Nghiem Ngat (Multi-Event Strict Sequential Ord... |
| `query-p2-9-qa` | `L26_V161` | `2712` | `[2640, 2800]` | Tier 3 | 100.0% | ✅ **LEARNED** | Ky thuat Cau Noi Hanh Dong - Sieu Du Lieu Thuc Pham (Action-to-Metadata Cross-Br... |
| `query-p2-10-kis` | `L26_V120` | `5350` | `[5180, 5450]` | Tier 3 | 100.0% | ✅ **LEARNED** | Ky thuat Bien Thien Ti Le Khung Hinh Tu Rong Sang Can Canh (Wide-to-Close Shot S... |
| `query-p2-11-kis` | `L26_V392` | `4022` | `[3620, 3880]` | Tier 3 | 100.0% | ✅ **LEARNED** | Ky thuat An Danh Hoa Thuc The Bang Hinh Hoc & Mau Sac Thuan Tuy (Pure Geometric ... |
| `query-p2-12-qa` | `L26_V192` | `5120` | `[4900, 5350]` | Tier 3 | 100.0% | ✅ **LEARNED** | Ky thuat Dem Thuc The Bo Tri Hinh Hoc Duoi Nap Trong Suot (Geometric Array Count... |
| `query-p2-13-kis` | `L26_V422` | `4292` | `[4200, 4700]` | Tier 3 | 100.0% | ✅ **LEARNED** | Ky thuat Rang Buoc Trang Thai Nhiet & Tuong Tac Gia Vi Cuoi (Thermal State Trans... |
| `query-p2-14-kis` | `L23_V010` | `625` | `[575, 725]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat Dinh Vi Phu Kien Vi Mo Cap Duoi Centimeter & Rang Buoc Phoi Hop Mu - Ao... |
| `query-p2-15-kis` | `L26_V356` | `1270` | `[1000, 1350]` | Tier 3 | 100.0% | ✅ **LEARNED** | Ky thuat Ngu Phap Dien Anh & Chuoi Dong Luc Hoc May Quay (Cinematographic Camera... |
| `query-p2-16-kis` | `L29_V014` | `20484` | `[20300, 20650]` | Tier 3 | 100.0% | ✅ **LEARNED** | Ky thuat Diem Neo Mang Do Vat Hau Canh Don Dieu & Boi Canh Lang Nghe Dan Gian (B... |
| `query-p2-17-kis` | `L30_V026` | `2392` | `[2300, 2550]` | Tier 3 | 100.0% | ✅ **LEARNED** | Ky thuat Chu Noi 3D San Khau & Diem Neo Tien To Ban Phan (3D Stage Physical Typo... |
| `query-p2-18-kis` | `L23_V017` | `2560` | `[2480, 2680]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat Diem Neo Dong Ho Dem Nguoc Den Tin Hieu Giao Thong & Doi Hinh Nhom Di D... |
| `query-p2-19-qa` | `L30_V043` | `2681` | `[2500, 3750]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat Cau Noi Truy Vet Dia Danh Da Chang (Multi-Hop Cross-Scene Geographic La... |
| `query-p2-20-kis` | `L25_V060` | `33600` | `[33200, 34500]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat Suy Luan Bang Bieu Da Cot & Ma Hoa Mau Sac Du Lieu (Multi-Column Tabula... |
| `query-p2-21-trake` | `L30_V031` | `2074` | `[2060, 2250]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat Phan Canh Nhip Nhanh 4 Chang & Tien Trinh Dong Goi Cuu Tro (4-Stage Fas... |
| `query-p2-22-kis` | `L26_V470` | `2039` | `[1980, 2600]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat An Danh Thuc The Thuc Pham & Mieu Ta Hinh Hoc Thao Tac Dao Kep (Food En... |
| `query-p2-23-qa` | `L25_V012` | `14518` | `[14200, 16000]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat Giai Ma Bieu Do Toa Do Da Duong & Don Vi Do Luong Khoa Hoc (Multi-Curve... |
| `query-p2-24-kis` | `L23_V013` | `6777` | `[6650, 6900]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat Rang Buoc Da Thuc The Duoi Bat & Tu The An Mung Roi Tay Lai (Multi-Enti... |
| `query-p2-25-kis` | `L25_V045` | `16500` | `[16000, 16800]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat Rang Buoc Thi Giac Long Ghep Da Tang Nguoi Thuyet Trinh - Anh Minh Hoa ... |
| `query-p2-26-kis` | `L25_V062` | `13800` | `[13400, 14200]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat An Du Do Hoa Da Phong Cach & Truu Tuong Hoa Khai Niem Bai Giang (Multi-... |
| `query-p2-27-qa` | `L24_V026` | `124` | `[0, 400]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat Phep Tru Tap Hop Ky Tu OCR & Logic Nhan Dien Phan Tu Vang Mat (Negative... |
| `query-p2-28-qa` | `L26_V450` | `6528` | `[6000, 6600]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat An Danh Ket Cau Soi Nho & Truy Vet Nguon Goc Dong Vat Cua Topping (Micr... |
| `query-p2-29-qa` | `L26_V181` | `7808` | `[7750, 7900]` | Tier 4 | 100.0% | ✅ **LEARNED** | Ky thuat Dinh Vi Bo Cuc Nguyen Lieu Hau Canh Da Thuc The & Trich Xuat Khoi Luong... |

---
## 📝 Chi Tiết Từng Mẫu Kiểm Thử

### Mẫu `query-p2-1-kis` (L24_V035)
- **Query:** Nhóm 5 người đang chơi đùa bên cạnh một con vật màu vàng. Một trong số đó đã mang một vật trông như trái bí đỏ đi giấu. Người đàn ông thức dậy không thấy quả bí đỏ đâu nên đánh thức con vật dậy.
- **Dòng 1 CSV:** Video `L24_V035`, Seed Frame `488`
- **Intervals:** [{"start_frame": 450, "end_frame": 1600, "event_desc": "Nhom 5 nguoi choi dua giau trai bi do, nguoi dan ong thuc day tim khong thay va danh thuc con vat mau vang"}]
- **Đánh giá:** Tier 3 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca cac vi tu (5 nguoi, con vat mau vang, giau trai bi do, thuc day khong thay, danh thuc con vat) deu khop 100% chinh xac trong frame 450-1600 cua video L24_V035
- **Phân tích Module:**
  - `MOD-VIS`: Nhan dien chuoi vi hanh dong: tu tap choi dua -> lay dao cu bi do giau len cot -> tim kiem tren tham trong -> danh thuc con lan
  - `MOD-AUD`: Am thanh nhac cu bieu dien lan su rong khong loi thoai truc tiep
  - `MOD-OCR`: Khong chua manh moi van ban chinh
  - `MOD-WORD`: La hoa danh tu: goi con lan vang la 'con vat mau vang', goi dao cu la 'vat trong nhu trai bi do' lam vo hieu hoa bo loc Object Detection thong thuong
  - `MOD-FLOW`: Mach truyen nhan qua 4 nhip hoan chinh dien ra lien tuc tu frame 450 den 1600
- **Bài học chắt lọc:** Ky thuat la hoa thuc the van hoa/bieu dien dac thu (Cultural/Performance Defamiliarization) giup vo hieu hoa nhan phan lop dinh san, bat buoc he thong giai phai phan tich thi giac nguyen ban

### Mẫu `query-p2-2-kis` (L21_V013)
- **Query:** Đoạn clip bắt đầu với cảnh một người đang dùng điện thoại chụp ảnh bức tranh hình tê giác trên tường. Đoạn clip kết thúc với cảnh một người chụp ảnh các hình graffiti 3 chú khỉ trên một cây cầu
- **Dòng 1 CSV:** Video `L21_V013`, Seed Frame `22410`
- **Intervals:** [{"start_frame": 22335, "end_frame": 22985, "event_desc": "Bat dau bang canh chup anh buc tranh te giac tren tuong va ket thuc bang canh chup anh graffiti 3 chu khi tren cay cau"}]
- **Đánh giá:** Tier 3 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca cac vi tu (chup anh tranh te giac o dau doan va chup anh graffiti 3 chu khi o cuoi doan) khop 100% trong khoang frame 22335-22985 cua video L21_V013
- **Phân tích Module:**
  - `MOD-VIS`: Nhan dien tac pham nghe thuat duong pho tinh vi: buc hoa te giac tren tuong gach va graffiti 3 chu khi du tren cau vuot
  - `MOD-AUD`: Giong doc thoi su thong thuong
  - `MOD-OCR`: Khong yeu cau OCR truc tiep
  - `MOD-WORD`: Su dung mau cau neo thoi gian hai dau (Doan clip bat dau... Doan clip ket thuc...)
  - `MOD-FLOW`: Ky thuat Dual-Boundary Temporal Framing: dinh vi chinh xac hai su kien o hai dau moc thoi gian cua phan canh
- **Bài học chắt lọc:** Ky thuat Dinh vi Hai Dau Ranh Gioi Thoi Gian (Dual-Boundary Temporal Framing) buoc mo hinh giai phai truy van dong thoi 2 su kien A va B de cat dung khoang thoi gian mong muon.

### Mẫu `query-p2-3-kis` (L24_V017)
- **Query:** Một chú lân (hay rồng/sư tử?) màu vàng nhảy hay rơi từ trên cao xuống, gần với mô hình chiếc tàu thủy nhỏ màu xanh dương.
- **Dòng 1 CSV:** Video `L24_V017`, Seed Frame `270`
- **Intervals:** [{"start_frame": 240, "end_frame": 360, "event_desc": "Chu lan mau trang bac bieu dien tren cot cao canh pano mo hinh thuyen buom"}]
- **Đánh giá:** Tier 2 / 5 | Độ chính xác: 60.0% | Quyết định: **REJECTED**
- **Phân tích Vị từ / Độ chính xác:** Query bi nham lan thuoc tinh nghiem trong: doan co mo hinh thuyen buom thi lan mau trang/bac (khong phai vang) va thuyen mau nau/trang (khong phai xanh duong). Doan lan vang thi o canh ban dem khong co mo hinh thuyen. Do chinh xac chi dat 60.0%
- **Phân tích Module:**
  - `MOD-VIS`: Co hanh dong bieu dien lan tren mai hoa thung canh pano thuyen buom, tuy nhien mau sac thuc the bi sai lech (lan trang bac thay vi lan vang, thuyen go nau thay vi xanh duong)
  - `MOD-AUD`: Tieng trong hoi lan su rong
  - `MOD-OCR`: Khong co yeu cau OCR
  - `MOD-WORD`: Dung tu ngu do du (hay rong/su tu?) nhung mo ta sai thuoc tinh mau sac chu the va boi canh
  - `MOD-FLOW`: Khong co mach truyen phuc tap
- **Bài học chắt lọc:** Rejected due to Tier < 3 or Accuracy < 85%

### Mẫu `query-p2-4-kis` (L25_V083)
- **Query:** Hai bạn trẻ đang treo băng-rôn lớn có tông màu xanh dương, được trang trí bằng hình ảnh núi, mây và một con đường dẫn tới trường học. Trên băng rôn còn có hình ảnh 02 em bé vùng khó khăn đang mặc áo màu vàng.
- **Dòng 1 CSV:** Video `L25_V083`, Seed Frame `67`
- **Intervals:** []
- **Đánh giá:** Tier 1 / 5 | Độ chính xác: 0.0% | Quyết định: **REJECTED**
- **Phân tích Vị từ / Độ chính xác:** Dap an o dong 1 (L25_V083, 67) hoan toan sai lech so voi query. Video la bai giang truc tuyen, khong co canh treo bang-ron hoc duong vung cao. Do chinh xac 0.0%
- **Phân tích Module:**
  - `MOD-VIS`: Video L25_V083 la bai giang sinh hoc ve ADN cua thay Vo Thanh Binh (THPT chuyen Le Hong Phong), khong chua bat ky hinh anh nao ve hai ban tre treo bang ron
  - `MOD-AUD`: Giong giang bai mon Sinh hoc
  - `MOD-OCR`: Slide bai giang 'Tong quan ve ADN', 'Co che phan tu'
  - `MOD-WORD`: Khong ap dung (video khong khop)
  - `MOD-FLOW`: Khong ap dung
- **Bài học chắt lọc:** Rejected due to Tier < 3 or Accuracy < 85%

### Mẫu `query-p2-5-kis` (L21_V022)
- **Query:** Một người áo đỏ, đội nón màu trắng, đang lấy nước rưới vào mặt của mình. Khung hình có hai người đi xe đạp, người mặc áo xanh đậm đang đuổi theo người mặc áo đen phối cam.
- **Dòng 1 CSV:** Video `L21_V022`, Seed Frame `26076`
- **Intervals:** [{"start_frame": 25830, "end_frame": 26130, "event_desc": "Hai tay dua xe dap (ao xanh dam duoi theo ao den phoi cam) va canh cua-ro ao do non trang tuoi nuoc vao mat"}]
- **Đánh giá:** Tier 3 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca cac vi tu (ao do non trang ruoi nuoc vao mat, 2 nguoi di xe dap ao xanh dam duoi ao den phoi cam) deu khop 100% chinh xac trong frame 25830-26130 cua video L21_V022
- **Phân tích Module:**
  - `MOD-VIS`: Phan tach trang phuc da thuc the chi tiet (ao do + non trang, ao xanh dam, ao den phoi cam) ket hop vi hanh dong tuoi nuoc vao mat khi dang chay xe dap
  - `MOD-AUD`: Binh luan the thao giai dua xe dap La Vuelta
  - `MOD-OCR`: Bang do thong tin giai dua La Vuelta, Cabeza de carrera
  - `MOD-WORD`: Mo ta chinh xac mau sac phoi trang phuc va tu ngu hanh dong tuong tac (duoi theo, ruoi nuoc vao mat)
  - `MOD-FLOW`: Ghep noi hai goc quay nhanh (top 2 tay dua tach top va cua-ro ao do giai nhiet) trong cung mot ban tin 10 giay
- **Bài học chắt lọc:** Ky thuat Phan Tách Trang Phuc & Vi Hanh Dong Da Thuc The (Multi-Entity Fine-grained Apparel & Micro-Action Coupling) buoc he thong giai phai rang buoc thuoc tinh cap doi tuong (Attribute Binding) va dinh vi vi hanh dong trong thoi gian cuc ngan.

### Mẫu `query-p2-6-kis` (L21_V018)
- **Query:** Đoạn video do người đi đường phía sau ghi lại cho thấy 2 thanh niên điều khiển xe máy bất ngờ nằm dài trên yên và phóng với tốc độ cao. Xuất hiện trong khung hình còn có một chiếc ô tô màu xanh cùng một người đi xe máy mặc áo xanh khác. Có 2 vòng tròn màu đỏ xuất hiện để khoanh vùng vị trí 2 thanh niên này.
- **Dòng 1 CSV:** Video `L21_V018`, Seed Frame `15780`
- **Intervals:** [{"start_frame": 15616, "end_frame": 16480, "event_desc": "Video quay tu phia sau canh 2 thanh nien nam dai tren yen xe may chay toc do cao canh o to xanh va nguoi mac ao xanh"}]
- **Đánh giá:** Tier 3 / 5 | Độ chính xác: 85.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Cac vi tu chu dao (quay tu phia sau, 2 thanh nien nam dai tren yen phong toc do cao, o to xanh, nguoi di xe may ao xanh) khop 100% trong frame 15616-16480. Chi tiet vong tron do khoanh vung khong xuat hien tren ban phat song nay. Do chinh xac dat 85.0%
- **Phân tích Module:**
  - `MOD-VIS`: Nhan dien tu the phi chuan muc cuc do (nam dai tren yen xe may chay toc do cao tren quoc lo), phan biet xe o to mau xanh va nguoi chay xe may mac ao xanh xung quanh
  - `MOD-AUD`: Giong doc thoi su 60 giay HTV9
  - `MOD-OCR`: TP HCM: DIEU TRA 2 THANH NIEN NAM DAI TREN XE MAY
  - `MOD-WORD`: Mo ta goc quay goc (nguoi di duong phia sau ghi lai) va vi ngu dong tu the hiem (nam dai tren yen)
  - `MOD-FLOW`: Dong chay tu su kien giao thong tren duong cao toc co cau vuot bo hanh
- **Bài học chắt lọc:** Ky thuat Nhan Dien Tu The Bat Thuong / Hanh Dong Hiem (Extreme Pose & Anomaly Action Localization) buoc mo hinh phai nhan dien duoc cac tu the phi chuan nam ngoai phan phoi du lieu thong thuong.

### Mẫu `query-p2-7-qa` (L21_V009)
- **Query:** Đoạn clip được quay từ bên trong một chiếc xe ô tô tự lái, có thể thấy rõ vô lăng được xoay để chiếc xe rẽ sang phải. Sau đó, góc quay chuyển ra ngoài, bắt trọn cảnh chiếc xe màu trắng rẽ trái, và ở góc trên khung hình có một dưới một biển hiệu đỏ gồm 6 ký tự chữ Hán. Con số được viết trên phần hông xe màu trắng là số mấy?
- **Dòng 1 CSV:** Video `L21_V009`, Seed Frame `21172`
- **Intervals:** [{"start_frame": 20950, "end_frame": 21250, "event_desc": "Canh quay cabin xe tu lai re phai chuyen sang goc ngoai xe trang re trai duoi bien hieu chu Han 6 ky tu, tren hong xe ghi so 1204"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca thong tin (cabin vo lang tu xoay, goc ngoai xe trang re trai, bien do 6 chu Han, dap an so tren hong xe 1204) khop 100% hoan hao trong frame 20950-21250 cua video L21_V009
- **Phân tích Module:**
  - `MOD-VIS`: Chuyen doi goc nhin noi-ngoai cabin (Interior POV sang Exterior POV) voi cay coi tien canh che khuat mot phan xe
  - `MOD-AUD`: Thuyet minh tin tuc xe tu hanh
  - `MOD-OCR`: Doc ky tu chu Han phi Latin dem so luong (6 chu '复合宴会中心') lam neo dinh vi ket hop doc ma so nho in tren hong xe ('1204')
  - `MOD-WORD`: Dat cau hoi QA ket hop neo khong gian (hong xe) va rang buoc bien hieu ngoai canh
  - `MOD-FLOW`: Lien ket truyen canh tu ben trong buong lai ra goc nhin toan canh ben ngoai de tra loi cau hoi chi tiet
- **Bài học chắt lọc:** Ky thuat Phoi Hop Da Goc Nhin (Cross-Perspective Shot Continuity) trong MOD-FLOW ket hop Dem Ky Tu Phi Latin & Doc So Than Xe trong MOD-OCR buoc he thong giai phai tracking thuc the xuyen goc quay va doc OCR cuc bo do phan giai cao.

### Mẫu `query-p2-8-trake` (L27_V011)
- **Query:** Video về một khu vườn cây ăn trái ở miền Tây Nam Bộ. Đây là chuỗi liên tiếp các cảnh quay về 4 loại trái cây trong vườn.
E1: Cảnh đầu tiên có trái sầu riêng.
E2: Cảnh đầu tiên có trái măng cụt.
E3: Cảnh đầu tiên có trái bưởi.
E4: Cảnh đầu tiên có trái dâu bòn bon.
- **Dòng 1 CSV:** Video `L27_V011`, Seed Frame `3827`
- **Intervals:** [{"start_frame": 3820, "end_frame": 4200, "event_desc": "Chuoi 4 canh quay lien tiep trong vuon cay mien Tay: E1 trai sau rieng (3826), E2 trai mang cut (3904), E3 trai buoi (4042), E4 trai dau bon bon (4150)"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca 4 su kien (E1: sau rieng frame 3826, E2: mang cut frame 3904, E3: buoi frame 4042, E4: dau bon bon frame 4150) deu khop 100% hoan hao theo dung thu tu thoi gian trong frame 3820-4200 cua video L27_V011
- **Phân tích Module:**
  - `MOD-VIS`: Nhan dien phan loai thuc vat vi mo 4 loai trai cay nhiet doi (sau rieng, mang cut, buoi, bon bon) tren canh la tu nhien
  - `MOD-AUD`: Am thanh am huong vuon trai cay va giong MC chuong trinh Viet Nam Di La Ghien
  - `MOD-OCR`: Logo chuong trinh Viet Nam Di La Ghien goc duoi man hinh
  - `MOD-WORD`: Cau truc TRAKE 4 su kien E1->E2->E3->E4 voi vi tu dinh vi ranh gioi 'Canh dau tien co trai...'
  - `MOD-FLOW`: Chuoi su kien tuyen tinh nghiem ngat 4 buoc (4-Stage Sequential Pipeline) bat dung frame bat dau cua tung loai trai cay
- **Bài học chắt lọc:** Ky thuat Chuoi Su Kien Tuyen Tinh Nghiem Ngat (Multi-Event Strict Sequential Ordering / N-Stage Pipeline) trong MOD-FLOW buoc he thong phai xu ly dong thoi Temporal Logic + Shot Boundary Detection + Fine-grained Visual Classification.

### Mẫu `query-p2-9-qa` (L26_V161)
- **Query:** Trong video hướng dẫn nấu ăn, người đầu bếp lần lượt cho các loại hương liệu gồm tiêu xanh, lá chanh và sả vào bên trong bụng của tổng cộng 4 con cá. Đây là loài cá gì?
- **Dòng 1 CSV:** Video `L26_V161`, Seed Frame `2712`
- **Intervals:** [{"start_frame": 2640, "end_frame": 2800, "event_desc": "Dau bep nhet sa, tieu xanh, la chanh vao bung 4 con ca song trong chuong trinh Mon Ngon Moi Ngay"}]
- **Đánh giá:** Tier 3 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Mieu ta thao tac nhet 3 loai huong lieu vao bung 4 con ca khop 100% frame 2640-2800, dap an 'ca song' khop 100% voi bang nguyen lieu frame 750 va loi thoai trong video L26_V161
- **Phân tích Module:**
  - `MOD-VIS`: Thao tac am thuc vi mo (nhet tieu xanh, la chanh, sa vao bung 4 con ca trong to thuy tinh)
  - `MOD-AUD`: Loi thoai dau bep va MC giai thich cach uop ca
  - `MOD-OCR`: Bang nguyen lieu: Ca song 4 con, Sa 9 cay, La chanh Thai 10 la, Tieu xanh 3 nhanh
  - `MOD-WORD`: Cau hoi QA huong vao danh tinh loai ca qua viec mo ta to hop nguyen lieu phu tro
  - `MOD-FLOW`: Cau noi hanh dong - sieu du lieu (Action-to-Metadata Cross-Bridge) ket noi doan so che voi bang thanh phan
- **Bài học chắt lọc:** Ky thuat Cau Noi Hanh Dong - Sieu Du Lieu Thuc Pham (Action-to-Metadata Cross-Bridge) trong MOD-FLOW buoc he thong phai ket noi thao tac che bien thuc te voi bang nguyen lieu OCR hoac loi thoai gioi thieu.

### Mẫu `query-p2-10-kis` (L26_V120)
- **Query:** Một đầu bếp chế biến món ăn trong chảo, với các miếng dồi trường màu trắng và rau xanh.
Đầu bếp cho bông hẹ vào chảo đang có dồi trường rồi dùng dụng cụ đảo các nguyên liệu.
Các đoạn bông hẹ dài màu xanh được trộn cùng những miếng dồi trường trắng trong chảo.
Máy quay chuyển sang cận cảnh chảo khi đầu bếp tiếp tục xào và trộn hai nguyên liệu.
- **Dòng 1 CSV:** Video `L26_V120`, Seed Frame `5350`
- **Intervals:** [{"start_frame": 5180, "end_frame": 5450, "event_desc": "Dau bep cho bong he vao chao doi truong dao deu tu goc quay trung sang can canh chao xao tron hai nguyen lieu"}]
- **Đánh giá:** Tier 3 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca cac chi tiet (che bien doi truong trang voi rau xanh, cho bong he vao dao chao, tron doi truong voi bong he, chuyen goc quay can canh) deu khop 100% frame 5180-5450 cua video L26_V120
- **Phân tích Module:**
  - `MOD-VIS`: Nhan dien hinh thai nguyen lieu dac thu (mieng doi truong hinh ong mau trang, cuong bong he xanh dai) va su chuyen doi ty le goc may tu goc trung sang can canh chao xao
  - `MOD-AUD`: Tieng xao chao xeo xeo va giong huong dan nau an cua dau bep
  - `MOD-OCR`: Logo Mon Ngon Moi Ngay
  - `MOD-WORD`: Su dung thuat ngu am thuc dac thu (doi truong, bong he) kem trinh tu vi ngu thao tac xao tron
  - `MOD-FLOW`: Dien tien 4 buoc mo ta nhip nhang theo dong thoi gian tu cho nguyen lieu den dao chao va chuyen can canh
- **Bài học chắt lọc:** Ky thuat Bien Thien Ti Le Khung Hinh Tu Rong Sang Can Canh (Wide-to-Close Shot Scale Transition & Micro-Ingredient Morphology) trong MOD-VIS va MOD-FLOW buoc he thong phai nhan dien duoc hinh thai vat the khi phong to va mat boi canh nguoi.

### Mẫu `query-p2-11-kis` (L26_V392)
- **Query:** Trong video, người đầu bếp cầm một nguyên liệu dài đã được xiên que và lăn qua hỗn hợp màu xanh lá cây và màu đỏ đã băm nhỏ.
Nguyên liệu sau đó được chuyển sang một đĩa chứa bột trắng để phủ bên ngoài.
Người đầu bếp cầm que xiên và xoay nguyên liệu qua lại nhiều lần trên lớp bột.
Cuối cùng, nguyên liệu đã được phủ kín một lớp bột trắng và đặt riêng sang một chiếc đĩa.
- **Dòng 1 CSV:** Video `L26_V392`, Seed Frame `4022`
- **Intervals:** [{"start_frame": 3620, "end_frame": 3880, "event_desc": "Dau bep cam nguyen lieu dai xien que lan qua hon hop xanh do bam nho roi phu bot trang tren dia"}]
- **Đánh giá:** Tier 3 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca 4 vi tu (lan que qua hon hop xanh do, chuyen sang dia bot trang, xoay qua lai phu bot, dat sang dia rieng) deu khop 100% frame 3620-3880 cua video L26_V392
- **Phân tích Module:**
  - `MOD-VIS`: Thao tac tay vi mo lien hoan (lan que xien qua hon hop xanh do, xoay tron tren dia bot trang, dat sang dia rieng)
  - `MOD-AUD`: Loi thuyet minh huong dan uop ca cua dau bep
  - `MOD-OCR`: Bang meo vat nau an (Sau khi tam xien ca qua bot tam kho chien gion...)
  - `MOD-WORD`: An danh hoa thuc the triet de bang hinh hoc va mau sac (nguyen lieu dai xien que, hon hop xanh do bam nho, bot trang)
  - `MOD-FLOW`: Tien trinh 4 buoc bien doi trang thai vat ly cua nguyen lieu theo thoi gian thuc
- **Bài học chắt lọc:** Ky thuat An Danh Hoa Thuc The Bang Hinh Hoc & Mau Sac Thuan Tuy (Pure Geometric & Chromatic Entity Anonymization) trong MOD-WORD triet tieu hoan toan danh tu dac thu, ep he thong phai suy luan truc tiep tren dac trung thi giac goc.

### Mẫu `query-p2-12-qa` (L26_V192)
- **Query:** Đoạn video mô tả quá trình làm bánh, bánh được tạo ra có màu tím, nguyên liệu bên trong có giá, cà rốt, và bên trong mỗi bánh đều có 1 hạt sen. Mỗi lần khuôn này làm được bao nhiêu cái bánh?
- **Dòng 1 CSV:** Video `L26_V192`, Seed Frame `5120`
- **Intervals:** [{"start_frame": 4900, "end_frame": 5350, "event_desc": "Qua trinh do bot tim vao khuon banh 7 ngan tron, them nhan gia ca rot va 1 hat sen len moi banh roi day nap thuy tinh"}]
- **Đánh giá:** Tier 3 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca thong tin (bot tim, nhan gia ca rot, 1 hat sen tren moi banh, dap an 7 cai banh trong khuon) deu khop 100% frame 4900-5350 cua video L26_V192
- **Phân tích Module:**
  - `MOD-VIS`: Dem so luong ngan khuon bo tri hinh hoc (1 tam + 6 ngoai = 7 ngan), nhan dien hat sen va bien dang hoi nuoc duoi nap thuy tinh
  - `MOD-AUD`: Loi thuyet minh huong dan lam banh khot / banh xeo tim
  - `MOD-OCR`: Logo chuong trinh Mon Ngon Moi Ngay
  - `MOD-WORD`: Cau hoi QA ve so luong banh duoc san xuat tren moi luot khuon ket hop 3 rang buoc nguyen lieu
  - `MOD-FLOW`: Tien trinh do bot -> cho nhan -> dat hat sen -> day nap kin va quan sat so luong banh hoan chinh
- **Bài học chắt lọc:** Ky thuat Dem Thuc The Bo Tri Hinh Hoc Duoi Nap Trong Suot (Geometric Array Counting & Transparent Occlusion Distortion) trong MOD-VIS buoc mo hinh phai co nang luc dem khong gian chinh xac va xu ly quang hoc bien dang.

### Mẫu `query-p2-13-kis` (L26_V422)
- **Query:** Người đầu bếp đảo đều một hỗn hợp các nguyên liệu trong chảo, nhìn bằng mắt thường có thể thấy một số nguyên liệu như thịt gà, ớt đỏ, ớt xanh, đậu phộng và hành tím. Sau đó cô ấy tắt lửa, cho thêm vỏ chanh và nước cốt chanh vào chảo trước khi trút hỗn hợp thức ăn này ra đĩa.
- **Dòng 1 CSV:** Video `L26_V422`, Seed Frame `4292`
- **Intervals:** [{"start_frame": 4200, "end_frame": 4700, "event_desc": "Dao chao hon hop 5 nguyen lieu (thit ga, ot do, ot xanh, dau phong, hanh tim), tat lua cho vo chanh va nuoc cot chanh roi trut ra dia"}]
- **Đánh giá:** Tier 3 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca cac chi tiet (dao hon hop ga, ot do, ot xanh, dau phong, hanh tim; tat lua; cho vo chanh mai; trut ra dia) deu khop 100% frame 4200-4700 cua video L26_V422
- **Phân tích Module:**
  - `MOD-VIS`: Rang buoc dong thoi 5 nguyen lieu khac mau (ga, ot do, ot xanh, dau phong, hanh tim) va su kien tat lua them vo chanh mai roi trut ra dia
  - `MOD-AUD`: Tieng xao chao ngung khi tat bep va tieng thuyet minh huong dan
  - `MOD-OCR`: Dong chu phu huong dan: VO CHANH MAI 1M
  - `MOD-WORD`: Menh de quan sat thi giac (nhin bang mat thuong) va quan he nhan qua thoi gian (tat lua truoc khi trut ra dia)
  - `MOD-FLOW`: Tien trinh che bien -> bien doi trang thai nhiet (tat lua) -> gia vi cuoi -> trut ra dia hoan thanh
- **Bài học chắt lọc:** Ky thuat Rang Buoc Trang Thai Nhiet & Tuong Tac Gia Vi Cuoi (Thermal State Transition & Post-Heat Seasoning Anchor) trong MOD-VIS buoc mo hinh phai theo doi ca su kien bien doi nhiet va thao tac hoan tat mon an.

### Mẫu `query-p2-14-kis` (L23_V010)
- **Query:** Cận cảnh một nhóm 3 vận động viên đua xe đạp đang di chuyển sát nhau, hai tay đua mặc áo xanh biển đội mũ bảo hiểm đỏ và trắng, bên cạnh có một tay đua mặc áo vàng đang đua cùng. Bên dưới quai mũ của tay đua nón đỏ có một sợi dây màu trắng treo lủng xuống gần cổ.
- **Dòng 1 CSV:** Video `L23_V010`, Seed Frame `625`
- **Intervals:** [{"start_frame": 575, "end_frame": 725, "event_desc": "Can canh 3 tay dua xe dap (2 ao xanh non do va trang, 1 ao vang), tay dua non do co soi day trang thung lung duoi quai non gan co"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca chi tiet (3 tay dua di chuyen sat nhau, 2 ao xanh non do va trang, 1 ao vang, soi day trang lung duoi quai mu tay dua non do) deu khop 100% frame 575-725 cua video L23_V010
- **Phân tích Module:**
  - `MOD-VIS`: Rang buoc to hop trang phuc da thuc the (2 ao xanh + non do/trang, 1 ao vang) va chi tiet phu kien vi mo cap duoi 1cm (soi day tai nghe trang duoi quai mu)
  - `MOD-AUD`: Tieng thuyet minh binh luan vien giai dua xe dap
  - `MOD-OCR`: Bang thong so chang dua: CHANG 10, 03:39:24, 9.1 Km
  - `MOD-WORD`: To hop vi tu mieu ta mau sac da lop (ao xanh, non do, non trang, ao vang, soi day trang gan co)
  - `MOD-FLOW`: Goc quay can canh bam sat doan dua di chuyen toc do cao trong 6 giay
- **Bài học chắt lọc:** Ky thuat Dinh Vi Phu Kien Vi Mo Cap Duoi Centimeter & Rang Buoc Phoi Hop Mu - Ao (Sub-Centimeter Accessory Localization & Jersey-Helmet Combinatorial Binding) trong MOD-VIS triet tieu cac he thong nhan dien tong quan.

### Mẫu `query-p2-15-kis` (L26_V356)
- **Query:** Cảnh phim lần lượt giới thiệu các nguyên liệu của món ăn qua 3 chuyển cảnh: máy quay chéo lên và kết thúc ở nguyên liệu hải sản đầu tiên; quay từ trên xuống cận cảnh nguyên liệu hải sản thứ hai rồi chuyển sang các nguyên liệu nhiều màu sắc; cuối cùng là cú máy tĩnh toàn cảnh toàn bộ nguyên liệu.
- **Dòng 1 CSV:** Video `L26_V356`, Seed Frame `1270`
- **Intervals:** [{"start_frame": 1000, "end_frame": 1350, "event_desc": "3 chuyen canh gioi thieu nguyen lieu: quay cheo len dung o hai san dau tien, quay tren xuong can canh hai san thu hai va rau cu, cu may tinh toan canh"}]
- **Đánh giá:** Tier 3 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca 3 cu may (lia cheo dung o hai san dau tien, tren xuong hai san thu 2 va rau cu, cu may tinh toan canh flat-lay) deu khop 100% frame 1000-1350 cua video L26_V356
- **Phân tích Module:**
  - `MOD-VIS`: Phan loai dong luc hoc may quay (goc thap lia cheo, goc cao tu tren xuong, goc tinh toan canh) va lien ket chung loai nguyen lieu (hai san, rau cu sac mau)
  - `MOD-AUD`: Nhac nen gioi thieu nguyen lieu chuong trinh am thuc
  - `MOD-OCR`: Logo HTV Online
  - `MOD-WORD`: Su dung thuat ngu dien anh chuyen nghiep (chuyen canh, may quay cheo len, cu may tinh toan canh)
  - `MOD-FLOW`: Ngu phap dung phim 3 cu may (Montage Sequence Grammar) trinh dien tuan tu nguyen lieu tu chi tiet den tong the
- **Bài học chắt lọc:** Ky thuat Ngu Phap Dien Anh & Chuoi Dong Luc Hoc May Quay (Cinematographic Camera Kinematics & Multi-Shot Grammar) trong MOD-FLOW buoc he thong phai phan tich duoc vector chuyen dong camera qua tung cu may.

### Mẫu `query-p2-16-kis` (L29_V014)
- **Query:** Trong một ngôi nhà nông thôn có cửa sổ lớn, hai người phụ nữ đang làm thủ công trên một bộ ván ngựa, phía sau là một dãy khoảng 10 thớt gỗ được treo thành một hàng ngang.
- **Dòng 1 CSV:** Video `L29_V014`, Seed Frame `20484`
- **Intervals:** [{"start_frame": 20300, "end_frame": 20650, "event_desc": "Hai nguoi phu nu ngoi tren bo van ngua dan lat thu cong trong nha nong thon, phia sau treo day 10 thot go tron hang ngang"}]
- **Đánh giá:** Tier 3 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca cac vi tu (nha nong thon co cua so lon, 2 phu nu lam thu cong tren van ngua, day 10 thot go treo ngang phia sau) deu khop 100% frame 20300-20650 cua video L29_V014
- **Phân tích Module:**
  - `MOD-VIS`: Nhan dien hoat dong lang nghe dan gian (dan lat tren van ngua) va mang do vat lap lai o hau canh (day ~10 thot go treo ngang)
  - `MOD-AUD`: Am thanh am huong nong thon va giong noi dia phuong
  - `MOD-OCR`: Logo kenh HTV Online
  - `MOD-WORD`: Su dung tu ngu noi that dan gian Nam Bo (bo van ngua) va mo ta khong gian nong thon
  - `MOD-FLOW`: Bo tri khong gian da tang: tien canh (nan tre), trung canh (2 nguoi phu nu tren van ngua), hau canh (day thot go tren cua so lon)
- **Bài học chắt lọc:** Ky thuat Diem Neo Mang Do Vat Hau Canh Don Dieu & Boi Canh Lang Nghe Dan Gian (Background Monotonous Object Array & Vernacular Folk Craft Context) trong MOD-VIS ep he thong phai phan tich toan bo cau truc khong gian hau canh.

### Mẫu `query-p2-17-kis` (L30_V026)
- **Query:** Sân khấu với dòng chữ nổi 3D to, ánh kim phủ kim tuyến có nội dung: “SẮC CỔ ...” đặt ở mép trước sân khấu.
- **Dòng 1 CSV:** Video `L30_V026`, Seed Frame `2392`
- **Intervals:** [{"start_frame": 2300, "end_frame": 2550, "event_desc": "San khau trinh dien co dong chu noi 3D kim tuyen SAC CO VIEN XUA dat o mep truoc san khau"}]
- **Đánh giá:** Tier 3 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Dong chu 3D anh kim phu kim tuyen 'SAC CO VIEN XUA' dat o mep truoc san khau khop 100% frame 2300-2550 cua video L30_V026
- **Phân tích Module:**
  - `MOD-VIS`: Chu noi 3D phu kim tuyen lap lanh phan chieu anh den san khau o mep truoc runway
  - `MOD-AUD`: Am nhac bieu dien thoi trang co phuc
  - `MOD-OCR`: Nhan dang chu 3D vat ly tren san khau qua diem neo tien to ban phan 'SAC CO ...' (SAC CO VIEN XUA)
  - `MOD-WORD`: Su dung dau ba cham che giau phan con lai cua cum tu 3D
  - `MOD-FLOW`: Dinh vi chuoi bieu dien thoi trang co phuc tren san khau theo chieu ngang
- **Bài học chắt lọc:** Ky thuat Chu Noi 3D San Khau & Diem Neo Tien To Ban Phan (3D Stage Physical Typography & Partial OCR Prefix Anchor) trong MOD-OCR buoc he thong OCR phai nhan dang ky tu 3D vat ly co be mat phan quang lap lanh.

### Mẫu `query-p2-18-kis` (L23_V017)
- **Query:** Đoạn phim quay từ phía sau nhóm dẫn đầu, gồm 1 tay đua dẫn trước và 3 tay đua bám phía sau, khi cả nhóm rẽ phải vào đường Hồ Tùng Mậu tại giao lộ có đèn xanh đang đếm ngược đến 13 giây.
- **Dòng 1 CSV:** Video `L23_V017`, Seed Frame `2560`
- **Intervals:** [{"start_frame": 2480, "end_frame": 2680, "event_desc": "May quay phia sau nhom dan dau (1 dan truoc + 3 bam sau) re phai vao duong Ho Tung Mau tai den xanh dem nguoc 13 giay"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca cac chi tiet (may quay phia sau, 1 tay dua truoc 3 tay dua sau, re phai vao duong Ho Tung Mau, den xanh dem nguoc 13s) deu khop 100% frame 2480-2680 cua video L23_V017
- **Phân tích Module:**
  - `MOD-VIS`: Doi hinh di dong bat doi xung (1 dan truoc + 3 bam sau) quay tu goc may xe mo to chay phia sau re phai tai giao lo rong
  - `MOD-AUD`: Loi thuyet minh cua binh luan vien ve doan dua re vao duong Ho Tung Mau va tieng xe mo to
  - `MOD-OCR`: Doc so led dem nguoc tren cot den tin hieu giao thong: den xanh so 13
  - `MOD-WORD`: Ket hop doi hinh the thao (1 truoc 3 sau), dia danh do thi (Ho Tung Mau) va diem neo OCR thoi gian thuc (den xanh 13s)
  - `MOD-FLOW`: Theo doi hanh trinh re phai cua nhom tay dua qua giao lo trong 8 giay
- **Bài học chắt lọc:** Ky thuat Diem Neo Dong Ho Dem Nguoc Den Tin Hieu Giao Thong & Doi Hinh Nhom Di Dong (Dynamic Digital Traffic Light Countdown & Dynamic Formation Chase Cam) trong MOD-OCR buoc he thong OCR phai doc duoc ky tu LED phat sang nho tren cot den ngoai canh di dong.

### Mẫu `query-p2-19-qa` (L30_V043)
- **Query:** Đoạn phim ghi lại cảnh mạnh thường quân hỗ trợ một quán trọ dành cho người cao tuổi, sau đó chuyển sang cảnh một cụ ông trò chuyện với nhóm người nước ngoài. Hỏi quán trọ được nhắc đến trong đoạn phim nằm trên đường nào?
- **Dòng 1 CSV:** Video `L30_V043`, Seed Frame `2681`
- **Intervals:** [{"start_frame": 2500, "end_frame": 3750, "event_desc": "Manh thuong quan ho tro quan tro nguoi cao tuoi ban buoi gay quy chuyen sang canh tro chuyen voi tinh nguyen vien quoc te tai quan tro duong Ly Thuong Kiet"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca cac chi tiet (manh thuong quan ho tro, quan tro nguoi cao tuoi, tro chuyen nguoi nuoc ngoai, dia chi duong Ly Thuong Kiet) deu khop 100% video L30_V043
- **Phân tích Module:**
  - `MOD-VIS`: Chuyen canh tu hoat dong gay quy ban buoi ngoai via he sang khong gian phong ngu tap the tro chuyen voi nguoi nuoc ngoai
  - `MOD-AUD`: Loi thuyet minh ve hoat dong tinh nguyen quoc te va ho tro cua manh thuong quan cho quan tro
  - `MOD-OCR`: Doc thong tin bien hieu va so nha mat tien quan tro: 552/1A5 Ly Thuong Kiet (Quan tro Sai Gon Bao Dung)
  - `MOD-WORD`: Cau hoi QA dia danh xau chuoi 2 phan canh lien tiep trong phong su xa hoi
  - `MOD-FLOW`: Cau noi da chang (Multi-Hop Bridge) ket noi hoat dong tai tro -> tro chuyen quoc te -> dia chi mat tien
- **Bài học chắt lọc:** Ky thuat Cau Noi Truy Vet Dia Danh Da Chang (Multi-Hop Cross-Scene Geographic Landmark Bridge) trong MOD-FLOW va MOD-OCR ep mo hinh phai theo doi toan bo dien tien phong su va doc bien hieu mat tien ngoai canh.

### Mẫu `query-p2-20-kis` (L25_V060)
- **Query:** Clip bài giảng môn Địa lí, có 1 bảng số liệu về mạng lưới đô thị ở Việt Nam. Bảng này thể hiện sự khác nhau về phân bố đô thị giữa các vùng bằng màu sắc: 3 vùng có nhiều đô thị nhất thì con số thể hiện số lượng đô thị được in màu đỏ, còn 2 vùng có ít đô thị nhất thì con số này được in màu xanh. Từ bảng số liệu ta còn có thể thấy rằng vùng có ít đô thị nhất lại là vùng có dân số đô thi cao nhất.
- **Dòng 1 CSV:** Video `L25_V060`, Seed Frame `33600`
- **Intervals:** [{"start_frame": 33200, "end_frame": 34500, "event_desc": "Slide bai giang Dia li ve mang luoi do thi: bang so lieu to mau do 3 vung nhieu do thi nhat (172, 124, 148) va to mau xanh 2 vung it nhat (58, 47 - Dong Nam Bo dan so cao nhat)"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca thong tin (bai giang Dia li, bang mang luoi do thi, 3 so in do, 2 so in xanh, vung it do thi nhat Dong Nam Bo 47 lai co dan so cao nhat 10493,2) deu khop 100% frame 33200-34500 cua video L25_V060
- **Phân tích Module:**
  - `MOD-VIS`: Nhan dien mau sac chu so trong bang (3 so mau do, 2 so mau xanh) va bo cuc slide bai giang dien tu
  - `MOD-AUD`: Loi giang cua giao vien Dia ly ve su phan bo khong dong deu cua do thi va dan so do thi
  - `MOD-OCR`: Doc va phan tich cau truc bang so lieu da cot (Cac vung, Tong so do thi, Dan so do thi), nhan dien so lieu to mau va suy luan tuong phan lien cot
  - `MOD-WORD`: Dien dat menh de suy luan bang bieu so lieu phan tich chuyen sau (vung it do thi nhat lai co dan so do thi cao nhat)
  - `MOD-FLOW`: Phan tich slide thuyet trinh giang day chuyen de THPT trong 52 giay
- **Bài học chắt lọc:** Ky thuat Suy Luan Bang Bieu Da Cot & Ma Hoa Mau Sac Du Lieu (Multi-Column Tabular OCR Reasoning & Color-Coded Statistical Highlighting) trong MOD-OCR buoc he thong phai nhan dien cau truc bang va suy luan logic so lieu.

### Mẫu `query-p2-21-trake` (L30_V031)
- **Query:** 4 cảnh này xảy ra liên tiếp nhau. 
Cảnh 1: Hai người phụ nữ cùng nhau dán niêm phong một thùng carton.
Cảnh 2: Các thùng mì tôm và bọc bánh mì được sắp xếp ngay ngắn.
Cảnh 3: Một người đàn ông nhấc thùng mì tôm lên và xếp lên trên chồng thùng mì.
Cảnh 4: Cảnh quay cận cảnh các thùng mì được xếp chồng trên xe tải.
- **Dòng 1 CSV:** Video `L30_V031`, Seed Frame `2074`
- **Intervals:** [{"start_frame": 2060, "end_frame": 2250, "event_desc": "Chuoi 4 canh lien tiep ve cong tac chuan bi cuu tro: dan niem phong thung carton (2074) -> xep mi tom va banh mi (2128) -> nguoi dan ong xep thung mi len xe (2166) -> can canh thung mi tren xe tai (2214)"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Ca 4 canh deu dien ra chinh xac theo dung thu tu thoi gian tai cac frame 2074, 2128, 2166, 2214 cua video L30_V031, do chinh xac 100%
- **Phân tích Module:**
  - `MOD-VIS`: Nhan dien quy trinh hanh dong vi mo: dan niem phong bang keo, phan loai mi Hao Hao/Gau Do va tui banh mi, bo xep hang hoa len xe tai
  - `MOD-AUD`: Am thanh phong su xa hoi va tieng on hien truong boc xep hang hoa cuu tro
  - `MOD-OCR`: Doc thuong hieu tren bao bi thung mi (Hao Hao, Acecook, Gau Do) va bien so xe tai (17H-013.52)
  - `MOD-WORD`: Dien dat chuoi logic 4 canh dong goi - van chuyen cuu tro tieu chuan TRAKE
  - `MOD-FLOW`: Dinh vi 4 cu may cuc ngan lien tiep (~1.8s/canh) tao thanh chuoi tien trinh nghiep vu hoan chinh
- **Bài học chắt lọc:** Ky thuat Phan Canh Nhip Nhanh 4 Chang & Tien Trinh Dong Goi Cuu Tro (4-Stage Fast-Paced Relief Packaging Workflow & Montage Ordering) trong MOD-FLOW buoc he thong phai bat duoc cac cu cat canh duoi 2 giay.

### Mẫu `query-p2-22-kis` (L26_V470)
- **Query:** Trong video nấu ăn, một loại nguyên liệu hải sản màu trắng được khứa theo những đường thẳng vuông góc nhau, trên cả 2 bề mặt của nguyên liệu này. Nguyên liệu sau đó được cắt thành từng que và cho vào tô, trước khi được trộn đều với các gia vị gồm rượu, tiêu và hạt nêm.
- **Dòng 1 CSV:** Video `L26_V470`, Seed Frame `2039`
- **Intervals:** [{"start_frame": 1980, "end_frame": 2600, "event_desc": "Dau bep so che phi le muc trang: khua ca ro vuong goc 2 mat -> cat que -> cho vao to tron ruou, tieu, hat nem"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca cac chi tiet (hai san mau trang, khua duong vuong goc 2 mat, cat que, cho vao to tron ruou, tieu, hat nem) deu khop 100% frame 1980-2600 cua video L26_V470
- **Phân tích Module:**
  - `MOD-VIS`: Nhan dien thao tac dao ky thuat cao: khua luoi carot vuong goc 2 mat tren than muc trang, cat thanh que dai va tron gia vi uop trong to su
  - `MOD-AUD`: Loi thuyet minh cua dau bep ve cach so che muc va tam uop gia vi
  - `MOD-OCR`: Logo HTV Online goc tren
  - `MOD-WORD`: An danh hoan toan ten thuc the (khong dung tu 'muc', thay bang 'nguyen lieu hai san mau trang') va mo ta chi tiet hinh hoc thao tac dao
  - `MOD-FLOW`: Dinh vi quy trinh so che am thuc lien tuc: khua ca ro -> cat que -> cho vao to -> tron ruou, tieu, hat nem
- **Bài học chắt lọc:** Ky thuat An Danh Thuc The Thuc Pham & Mieu Ta Hinh Hoc Thao Tac Dao Kep (Food Entity Anonymization & Geometric Double-Sided Scoring Micro-Action) trong MOD-WORD va MOD-VIS buoc he thong phai nhan dien hanh vi thi giac tinh vi.

### Mẫu `query-p2-23-qa` (L25_V012)
- **Query:** Câu hỏi môn Sinh học nằm ở số thứ tự 11 trong đề thi THPTQG 2022. Trong câu hỏi có một biểu đồ đưa ra sự so sánh tốc độ sinh trưởng của các loài thực vật trong các hệ sinh thái ven biển. Hãy cho biết loài cây (II) đạt được tốc độ sinh trưởng tốt nhất khi môi trường sống có độ mặn là bao nhiêu phần nghìn?
- **Dòng 1 CSV:** Video `L25_V012`, Seed Frame `14518`
- **Intervals:** [{"start_frame": 14200, "end_frame": 16000, "event_desc": "Slide bai giang Sinh hoc THPT cau 11 de 2022: bieu do so sanh toc do sinh truong 3 loai cay ngap man theo do man (‰), loai II dat dinh tai do man 15-20‰"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca cac chi tiet (mon Sinh hoc cau 11 de 2022, bieu do he sinh thai ngap man, loai II sinh truong tot nhat o 15-20‰) deu khop 100% video L25_V012
- **Phân tích Module:**
  - `MOD-VIS`: Phan tich bieu do toa do 2D da duong voi cac kieu net ve khac nhau (net lien, net dut, net cham gach), xac dinh diem cuc dai cua duong bieu dien loai II
  - `MOD-AUD`: Loi giang cua giao vien Sinh hoc huong dan phuong phap doc bieu do sinh thai va giai de thi
  - `MOD-OCR`: Doc thong tin de thi (Cau 11, de THPTQG 2022 ma 215), doc truc toa do do man (‰) va ky hieu cac loai cay (I, II, III)
  - `MOD-WORD`: Cau hoi QA hoc thuat ve khoa hoc tu nhien yeu cau giai ma so lieu do thi va don vi do luong chuyen nganh (‰)
  - `MOD-FLOW`: Theo doi slide bai giang dien tu chuyen de on thi THPT mon Sinh hoc trong 72 giay
- **Bài học chắt lọc:** Ky thuat Giai Ma Bieu Do Toa Do Da Duong & Don Vi Do Luong Khoa Hoc (Multi-Curve Coordinate Graph Visual Reasoning & Scientific Unit Anchor) trong MOD-VIS va MOD-OCR ep he thong phai co kha nang Chart-QA thi giac.

### Mẫu `query-p2-24-kis` (L23_V013)
- **Query:** Đoạn clip ghi lại khoảnh khắc về đích của một chặng đua xe đạp diễn ra tại thành phố thuộc tỉnh Quảng Nam (cũ, trước ngày 01/7/2025). Vận động viên người Estonia mặc áo xanh nước biển dẫn đầu đoàn. Khi chỉ còn cách đích một đoạn ngắn, anh buông cả hai tay khỏi ghi-đông, giang hai tay lên cao ăn mừng chiến thắng trong khi xe vẫn tiến về phía trước. Ngay phía sau anh là một vận động viên mặc áo vàng và một vận động viên mặc áo cam đang lần lượt lao về đích.
- **Dòng 1 CSV:** Video `L23_V013`, Seed Frame `6777`
- **Intervals:** [{"start_frame": 6650, "end_frame": 6900, "event_desc": "Khoanh khac can dich chang dua xe dap: VDV ao xanh nuoc bien Estonia buong 2 tay khoi ghi-dong giang cao an mung, phia sau la VDV ao vang va ao cam"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca chi tiet (chang dua Quang Nam, VDV Estonia ao xanh buong 2 tay khoi ghi-dong giang cao, VDV ao vang va ao cam lao ve dich) deu khop 100% frame 6650-6900 cua video L23_V013
- **Phân tích Module:**
  - `MOD-VIS`: Goc may truc dien tren cao (Top-Down Overhead) can canh vach dich, nhan dien tu the buong 2 tay khoi ghi-dong giang len troi an mung va phan biet mau sac 3 ao dau (xanh dan dau, vang va cam bam duoi)
  - `MOD-AUD`: Loi binh luan vien soi dong ve khoanh khac rut dich thang chang cua tay dua Estonia
  - `MOD-OCR`: Dong chu Replay va bien quang cao tai vach dich chang dua
  - `MOD-WORD`: Rang buoc da thuc the chi tiet: quoc tich VDV, mau ao chu dao, tu the co hoc dac biet (buong tay lai), va mau ao cua 2 tay dua bam sau
  - `MOD-FLOW`: Dinh vi cao trao ve dich (Climax Sprint Finish) trong 10 giay
- **Bài học chắt lọc:** Ky thuat Rang Buoc Da Thuc The Duoi Bat & Tu The An Mung Roi Tay Lai (Multi-Entity Pursuit Color Binding & No-Hands Victory Gesture) trong MOD-VIS va MOD-WORD ep he thong phai phan giai dong thoi tu the dong va mau ao nhieu doi tuong.

### Mẫu `query-p2-25-kis` (L25_V045)
- **Query:** Cảnh giáo viên nam đeo kính, mặc áo sơ mi kẻ sọc ngắn tay, xuất hiện ở góc dưới bên trái và dùng hai tay làm cử chỉ minh họa khi đang giảng bài.

Khung hình chứa một bức ảnh minh họa cô gái trẻ đeo kính, mặc áo sơ mi trắng, ngồi khoanh chân trên ghế sofa màu xám vừa cầm cốc nước vừa nhìn vào laptop mở trên đùi.
- **Dòng 1 CSV:** Video `L25_V045`, Seed Frame `16500`
- **Intervals:** [{"start_frame": 16000, "end_frame": 16800, "event_desc": "Slide bai giang Ngu van THPT: thay giao deo kinh o goc trai duoi khoa tay giang bai, slide chua anh co gai deo kinh mac ao trang ngoi khoanh chan tren sofa xam cam coc nhin laptop"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca cac chi tiet (giao vien nam deo kinh o goc duoi trai khoa tay, anh minh hoa co gai deo kinh ao trang ngoi khoanh chan tren sofa xam cam coc nhin laptop tren dui) deu khop 100% frame 16000-16800 cua video L25_V045
- **Phân tích Module:**
  - `MOD-VIS`: Rang buoc thi giac long ghep da tang (Dual-Layer Grounding): tang nguoi giang PIP goc duoi trai va tang anh stock photo minh hoa tren slide (co gai ngoi khoanh chan tren sofa xam, cam coc, nhin laptop tren dui)
  - `MOD-AUD`: Loi giang cua thay giao Ngu van ve thoi diem vang de hoc va tang kha nang ghi nho
  - `MOD-OCR`: Tieu de slide: Chon 'thoi diem vang' de hoc va chuong trinh on thi THPT
  - `MOD-WORD`: Mo ta phan tach 2 vung khong gian doc lap trong mot khung hinh video e-learning ma khong dua vao tu khoa OCR
  - `MOD-FLOW`: Dinh vi slide thuyet trinh bai giang dien tu trong 32 giay
- **Bài học chắt lọc:** Ky thuat Rang Buoc Thi Giac Long Ghep Da Tang Nguoi Thuyet Trinh - Anh Minh Hoa Slide (Dual-Layer Nested Visual Grounding: Presenter PIP & Slide Stock Photo Binding) trong MOD-VIS buoc he thong phai phan giai dong thoi ca nguoi thuyet trinh va noi dung anh tren slide.

### Mẫu `query-p2-26-kis` (L25_V062)
- **Query:** Đây là một đoạn trong bài giảng. Trên slide bao gồm:
- Một nhóm nhân vật người 3D màu trắng vây quanh một nhân vật màu đỏ ở chính giữa.

- Hai nhân vật hoạt hình nam đang trong tư thế thi đấu kéo co, đối đầu nhau với sợi dây thừng.
- **Dòng 1 CSV:** Video `L25_V062`, Seed Frame `13800`
- **Intervals:** [{"start_frame": 13400, "end_frame": 14200, "event_desc": "Slide bai giang GDCD Quy luat canh tranh: chua hinh 3D nguoi mau trang chay dua quanh nhan vat mau do o chinh giua va hinh hoat hinh 2 nguoi dan ong keo co doi dau bang soi day thung"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Tat ca cac chi tiet (slide bai giang, nhom nguoi 3D trang quanh nguoi do o giua, 2 nguoi hoat hinh nam keo co bang day thung) deu khop 100% frame 13400-14200 cua video L25_V062
- **Phân tích Module:**
  - `MOD-VIS`: Nhan dien dong thoi 2 phong cach do hoa an du tren slide: nhan vat 3D mau trang quanh nhan vat do o giua va tranh hoat hinh 2D 2 nguoi dan ong thi dau keo co
  - `MOD-AUD`: Loi giang cua co giao GDCD ve quy luat canh tranh va chu the kinh te
  - `MOD-OCR`: Tieu de slide: Noi dung 2 Quy luat canh tranh, Khai niem, Muc dich
  - `MOD-WORD`: An danh hoan toan thuat ngu kinh te / bai giang, chi mieu ta hinh anh an du thi giac da phong cach
  - `MOD-FLOW`: Dinh vi slide bai giang dien tu thuyet trinh so do kinh te trong 32 giay
- **Bài học chắt lọc:** Ky thuat An Du Do Hoa Da Phong Cach & Truu Tuong Hoa Khai Niem Bai Giang (Multi-Style Graphical Metaphor Binding & Lecture Concept Anonymization) trong MOD-VIS va MOD-WORD ep mo hinh phai nhan dien duoc nhieu kieu clipart/vector an du thi giac.

### Mẫu `query-p2-27-qa` (L24_V026)
- **Query:** Cảnh quay một chú lân đang biểu diễn từ đầu video, các cột để chú lân biểu diễn được dán những con số. Phía sau có 1 mô hình con rồng uốn lượn hình xoắn ốc. Trong các số từ 16 giây đầu tiên của video, số nào không được nhìn thấy từ góc nhìn của camera trong các số từ 1-8.
- **Dòng 1 CSV:** Video `L24_V026`, Seed Frame `124`
- **Intervals:** [{"start_frame": 0, "end_frame": 400, "event_desc": "16 giay dau video: chu lan bieu dien tren cac cot Mai Hoa Thung dan so (1, 3, 4, 6, 7, 8 nhin thay tu camera; so 2 va 5 bi khuat khong nhin thay)"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Cac so nhin thay tren cot la 1, 3, 4, 6, 7, 8; cac so 2 va 5 khong nhin thay tu goc may camera, dap an '2 va 5' khop 100% video L24_V026
- **Phân tích Module:**
  - `MOD-VIS`: Kiem ke khong gian tren cac cot tru Mai Hoa Thung hinh tru, nhan dien cac the so va xac dinh goc khuat thi giac cua camera
  - `MOD-AUD`: Tieng trong hoi lan su rong ron ra o dau video
  - `MOD-OCR`: Doc cac the so dan tren than cot (1, 3, 4, 6, 7, 8) va thuc hien phep tru tap hop de tim ra cac so khong nhin thay: 2 va 5
  - `MOD-WORD`: Cau hoi QA theo logic phu dinh tap hop (Negative Set Subtraction): hoi nhung con so KHONG duoc nhin thay tu goc may camera trong day 1-8
  - `MOD-FLOW`: Khoa chat khung thoi gian 16 giay dau tien cua video
- **Bài học chắt lọc:** Ky thuat Phep Tru Tap Hop Ky Tu OCR & Logic Nhan Dien Phan Tu Vang Mat (Negative OCR Set Subtraction & Occluded Pillar Inventory) trong MOD-OCR va MOD-WORD ep he thong phai suy luan logic phu dinh tap hop.

### Mẫu `query-p2-28-qa` (L26_V450)
- **Query:** Cảnh quay một tô cháo đã được nấu và trang trí hoàn chỉnh (đã xong các giai đoạn trang trí). Kế bên tô cháo có 1 chén nhỏ màu đen, để chứa 1 loại topping màu cam kết cấu hơi giống những sợi nhỏ. Loại topping này trước đó đã được rắc lên tô cháo. Xung quanh topping là các loại rau, hành,... Hỏi topping trong video là thịt của con gì?
- **Dòng 1 CSV:** Video `L26_V450`, Seed Frame `6528`
- **Intervals:** [{"start_frame": 6000, "end_frame": 6600, "event_desc": "Canh trinh bay hoan thien to chao ca hoi va chen nho mau den dung cha bong ca hoi mau cam dang soi nho, kem rau củ va am thanh nhan xet cua dau bep"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** To chao ca hoi, chen nho mau den chua cha bong ca hoi mau cam dang soi nho, rau hanh xung quanh va dap an 'con ca hoi' deu khop 100% video L26_V450
- **Phân tích Module:**
  - `MOD-VIS`: Canh quay can canh macro cuc dai voi do sau truong anh nong (shallow DOF) to chao co rac cha bong ca hoi mau cam soi nho, ca rot hat luu, rau xanh va chen nho mau den ke ben
  - `MOD-AUD`: Loi thuyet minh cua dau bep va MC ve mon chao ca hoi nong thom bo duong
  - `MOD-OCR`: Chu Nóng thơm va logo chuong trinh Mon Ngon Moi Ngay
  - `MOD-WORD`: An danh hoan toan ten nguyen lieu ('topping mau cam ket cau hoi giong nhung soi nho trong chen den'), hoi nguoc ve nguon goc dong vat ('thit cua con gi?')
  - `MOD-FLOW`: Cau noi da phuong thuc truy vet nguoc tu canh bay tri thanh pham ve bang nguyen lieu so che ban dau de xac dinh loai ca (ca hoi)
- **Bài học chắt lọc:** Ky thuat An Danh Ket Cau Soi Nho & Truy Vet Nguon Goc Dong Vat Cua Topping (Micro-Fibrous Texture Anonymization & Animal Biological Origin QA Bridge) trong MOD-WORD va MOD-FLOW ep mo hinh phai truy vet nguoc nguon goc sinh hoc nguyen lieu.

### Mẫu `query-p2-29-qa` (L26_V181)
- **Query:** Cảnh quay liệt kê các nguyên liệu để nấu một món ăn. Ảnh nền bao gồm dĩa thịt, bó lá tươi xanh đặt ở góc bên trái, một gói hạt nêm, hũ thủy tinh nhỏ đựng nước cốt dừa, bột cà ri, nấm mèo (mộc nhĩ) khô đặt phía dưới chén gia vị, sả cây và ớt hiểm đỏ đặt ở góc trái phía dưới. Bảng nguyên liệu hiện lên gồm 9 thành phần cụ thể. Hỏi phần thịt có trọng lượng bao nhiêu trong bảng nguyên liệu (số và đơn vị được ghi trong bảng)?
- **Dòng 1 CSV:** Video `L26_V181`, Seed Frame `7808`
- **Intervals:** [{"start_frame": 7750, "end_frame": 7900, "event_desc": "Do hoa bang nguyen lieu mon an hien thi danh sach thanh phan (Thit bo mem 350g, Thit nac dam 100g, Mo heo 100g, La lot 30 la...) tren nen go trang kem cac loai gia vi"}]
- **Đánh giá:** Tier 4 / 5 | Độ chính xác: 100.0% | Quyết định: **LEARNED**
- **Phân tích Vị từ / Độ chính xác:** Bang nguyen lieu ghi ro 'THIT BO MEM 350g' va 'THIT NAC DAM 100g', dap an '350g thit bo mem, 100g thit nac dam' khop 100% video L26_V181
- **Phân tích Module:**
  - `MOD-VIS`: Kiem ke bo cuc hau canh nhieu dao cu nguyen lieu am thuc tinh vi (dia thit, bo la, goi hat nem, hu thuy tinh, bot ca ri, nam meo kho, sa cay, ot hiem)
  - `MOD-AUD`: Am thanh nhac nen gioi thieu mon an chuong trinh Mon Ngon Moi Ngay
  - `MOD-OCR`: Doc chinh xac dinh luong khoi luong va don vi tung loai thit trong bang nguyen lieu: '350g thit bo mem, 100g thit nac dam'
  - `MOD-WORD`: Cau hoi trich xuat so lieu gram kem don vi tinh va ten loai thit chi tiet tu bang danh muc nguyen lieu
  - `MOD-FLOW`: Khoa chat khung thoi gian do hoa bang thanh phan nguyen lieu 6 giay
- **Bài học chắt lọc:** Ky thuat Dinh Vi Bo Cuc Nguyen Lieu Hau Canh Da Thuc The & Trich Xuat Khoi Luong OCR Tung Phan Thit (Multi-Prop Culinary Background Spatial Inventory & Multi-Meat Component Gram OCR) trong MOD-VIS va MOD-OCR ep mo hinh phai doc chinh xac key-value danh muc.
