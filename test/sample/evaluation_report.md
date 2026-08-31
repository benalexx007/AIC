# Báo Cáo Đánh Giá & Học Hỏi Từ Query Mẫu (Sample Evaluation Report)

> **Cập nhật lần cuối:** 2026-08-31 08:04:33 UTC  
> **Tổng số mẫu đã đánh giá:** 4 | **Đã học (Learned):** 2 | **Từ chối (Rejected):** 2

## 📊 Bảng Tổng Hợp Đánh Giá

| Sample ID | Video ID | Seed (Line 1) | Extracted Intervals | Tier | Accuracy | Decision | Key Insights |
|---|---|---|---|:---:|:---:|:---:|---|
| `query-p2-1-kis` | `L24_V035` | `488` | `[450, 1600]` | Tier 3 | 100.0% | ✅ **LEARNED** | Ky thuat la hoa thuc the van hoa/bieu dien dac thu (Cultural/Performance Defamil... |
| `query-p2-2-kis` | `L21_V013` | `22410` | `[22335, 22985]` | Tier 3 | 100.0% | ✅ **LEARNED** | Ky thuat Dinh vi Hai Dau Ranh Gioi Thoi Gian (Dual-Boundary Temporal Framing) bu... |
| `query-p2-3-kis` | `L24_V017` | `270` | `[240, 360]` | Tier 2 | 60.0% | ❌ REJECTED | Rejected due to Tier < 3 or Accuracy < 85%... |
| `query-p2-4-kis` | `L25_V083` | `67` | `` | Tier 1 | 0.0% | ❌ REJECTED | Rejected due to Tier < 3 or Accuracy < 85%... |

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
