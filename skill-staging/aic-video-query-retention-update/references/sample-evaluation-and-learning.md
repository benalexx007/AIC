# Quy Chuẩn Kỹ Thuật: Đánh Giá, Truy Vết Đa Phân Đoạn & Học Hỏi Từ Query Mẫu (Sample Evaluation & Continuous Learning Framework)

Tài liệu này là **hướng dẫn hành động và quy chuẩn kỹ thuật (Technical & Operational Guide)** cho Core LLM khi xử lý tập dữ liệu mẫu (Sample Queries & Answers), trích xuất frame interval (kể cả đa phân đoạn rời nhau), đánh giá 2 chỉ số độc lập và tự động chắt lọc tri thức để cập nhật **5 Module Tăng Độ Khó Truy Vấn (AIC Query Hardening Framework)**.

---

## 🎯 1. Các Ràng Buộc Cốt Lõi (Mandatory Constraints)

1. **Ràng buộc File CSV Đáp án:**
   * **CHỈ ĐƯỢC PHÉP ĐỌC DÒNG ĐẦU TIÊN (Line 1)** của file `ans/*.csv` để lấy `video_id` và `seed_frame_csv`.
   * **TUYỆT ĐỐI KHÔNG đọc các dòng 2, 3, 4...** để tránh bị nhiễu bởi các kết quả sai lệch (false positives) từ hệ thống xếp hạng của thí sinh.
2. **Ràng buộc Quản lý Bộ nhớ & Video Đơn Lẻ (Single-Video Retention Rule):**
   * Tại mỗi thời điểm, thư mục `video-runs/` chỉ được phép chứa **đúng 1 video** đang xử lý.
   * Trước khi bắt đầu tải video $n+1$, hệ thống **bắt buộc phải chạy `purge_previous_runs.py`** để xóa sạch toàn bộ video $n$, frame ảnh, âm thanh, ma trận embedding của video $n$.
3. **Ràng buộc Cổng Học Hỏi (Learning Gate):**
   $$\mathbf{Kích\ hoạt\ học\ hỏi\ cập\ nhật\ 5\ Module} \iff (\text{Độ khó} \ge 3) \land (\text{Độ chính xác} \ge 85\%)$$

---

## 🧩 2. Quy Trình Truy Vết Đa Phân Đoạn (Multi-Segment Narrative Resolution)

Khi câu truy vấn mô tả một câu chuyện gồm nhiều phân cảnh rời nhau (Non-contiguous intervals), hệ thống tự lực tìm kiếm dựa trên nội dung video mà không cần gợi ý thêm từ file CSV:

```mermaid
graph TD
    CSV["Dòng 1 File CSV<br/>(video_id, seed_frame_csv)"] --> V["1. Tải video_id & Lập Semantic Index toàn video (OpenCLIP + YOLO)"]
    
    Q["Query Mẫu (Cốt truyện phức tạp)"] --> DEC["2. Phân rã Ngữ nghĩa (Clause Decomposition)<br/>Tách thành E1, E2, ..., Ek"]
    
    V --> SCAN["3. Quét Ngữ Nghĩa Toàn Video (Whole-Video Scan)"]
    DEC --> SCAN
    
    SCAN --> LOC1["Sub-Event E1 -> Neo tại seed_frame_csv (Dòng 1)"]
    SCAN --> LOC2["Sub-Events E2..Ek -> Tự động dò qua clip_search & transcript_search toàn video"]
    
    LOC1 --> STEP1["4. Căn biên độc lập từng vị trí (extract_window step=1)"]
    LOC2 --> STEP1
    
    STEP1 --> MERGE{"5. Kiểm tra khoảng cách thời gian"}
    MERGE -->|Liền kề / Trùng lặp| OUT1["Hợp nhất thành 1 Interval duy nhất [s1, ek]"]
    MERGE -->|Rời nhau (Disjoint)| OUT2["Xuất danh sách Đa Interval [s1, e1], [s2, e2], ..."]
```

### Chi Tiết 4 Bước Triển Khai:

#### 🔹 Bước 2.1: Phân rã câu truy vấn thành các Sub-Events (`Clause Decomposition`)
Core LLM đọc câu query và tách thành các mệnh đề sự kiện độc lập:
* $E_1$: Sự kiện mở đầu (neo tại `seed_frame_csv` ở dòng 1 CSV).
* $E_2, \dots, E_k$: Các sự kiện diễn biến hoặc kết quả được liên kết trong câu chuyện.

#### 🔹 Bước 2.2: Tự động quét ngữ nghĩa toàn video (`Autonomous Whole-Video Scan`)
* Với $E_1$: Sử dụng `seed_frame_csv` làm điểm khởi đầu.
* Với $E_2 \dots E_k$: Hệ thống tự động tạo các prompt thị giác độc lập cho từng $E_i$, chạy `clip_search.py` trên ma trận `semantic-index.json` và `transcript_search.py` để xác định các đỉnh tương đồng (peaks) trên toàn bộ thời lượng video.

#### 🔹 Bước 2.3: Căn biên chi tiết độc lập (`extract_window.py` step=1)
* Tại mỗi mốc thời gian của $E_i$, mở bracket cục bộ $\pm 8s$, trích xuất frame ở độ phân giải `step=1`.
* Xác nhận frame bắt đầu ($s_i$), frame kết thúc ($e_i$) cùng 2 frame negative ngay trước và sau.

#### 🔹 Bước 2.4: Hợp nhất hoặc Xuất danh sách Đa Phân Đoạn
* Nếu $e_i \approx s_{i+1}$: Hợp nhất thành $[s_{\text{min}}, e_{\text{max}}]$.
* Nếu các phân đoạn cách xa nhau: Xuất dạng chuỗi interval:
  $$\text{Ground Truth: } \text{video\_id}, [s_1, e_1], [s_2, e_2], \dots, [s_k, e_k]$$

---

## 📊 3. Ma Trận Đánh Giá 2 Chiều (2D Evaluation Matrix)

Với mỗi mẫu kiểm thử, hệ thống tính toán 2 chỉ số độc lập:

### 1. Đánh giá Độ Khó (Difficulty Tier: 1 $\to$ 5)
Phân tích sự đóng góp của **5 Module Tăng Độ Khó**:
* **Tier 1 (Standard):** Mô tả 1-2 vị từ trực diện, vật thể cơ bản.
* **Tier 2 (Hard):** Xuất hiện vi hành động (`MOD-VIS`), quan hệ không gian vi mô hoặc từ ngữ nói vòng (`MOD-WORD`).
* **Tier 3 (Very Hard):** Xuất hiện tiếng động môi trường / ngữ điệu (`MOD-AUD`), phủ định logic ngầm hoặc đảo ngược trật tự thời gian (`MOD-WORD`).
* **Tier 4 (Adversarial):** Kết hợp đủ 3 kênh Visual + Audio + OCR (`MOD-OCR`), câu từ cài bẫy phân tán vector embedding (anti-reranker).
* **Tier 5 (Grandmaster):** Cấu trúc câu đố trinh thám phi tuyến tính (`MOD-FLOW`), bắt buộc suy luận bắc cầu 3 kênh mới giải được.

### 2. Đánh giá Độ Chính Xác (Accuracy Score: 0% $\to$ 100%)
So sánh từng vị từ mô tả trong query với hình ảnh/âm thanh thực tế diễn ra trong interval(s):
* **100% (Hoàn hảo):** Mọi chi tiết mô tả đều xuất hiện trọn vẹn trong interval tìm được.
* **85% – 99% (Khớp cao):** Đại đa số các vị từ chính xác, chỉ có 1 chi tiết nhỏ phụ thuộc góc nhìn hoặc thời lượng chênh lệch không đáng kể.
* **< 85% (Không đạt):** Video không chứa đúng sự kiện, hoặc thiếu các vị từ cốt lõi, hoặc câu trả lời bị lệch ngữ cảnh (false positive).

---

## 🧠 4. Cơ Chế Học Hỏi & Cập Nhật Tri Thức (Pattern Distillation)

Khi thỏa mãn điều kiện $(\text{Độ khó} \ge 3 \land \text{Độ chính xác} \ge 85\%)$:
1. **Bóc tách chiến thuật của Query:**
   * Cách tác giả đặt câu để giấu keyword (kỹ thuật `MOD-WORD`).
   * Cách tác giả kết hợp tín hiệu âm thanh hoặc chữ viết để disambiguate (kỹ thuật `MOD-AUD`, `MOD-OCR`).
   * Cách đan cài câu chuyện nhiều mẩu ghép (kỹ thuật `MOD-FLOW`).
2. **Cập nhật tri thức:** Tự động ghi nhận bài học rút ra vào [query-hardening-modules.md](query-hardening-modules.md).

---

## 💾 5. Định Dạng File Log Đánh Giá (`test/sample/evaluation_log.json`)

Toàn bộ quá trình đánh giá được tự động lưu trữ và tích lũy vào `test/sample/evaluation_log.json` và bảng báo cáo tổng kết `test/sample/evaluation_report.md`.

### Cấu trúc JSON Schema:
```json
{
  "sample_id": "query-p2-1-kis",
  "query_file": "test/sample/query/query-p2-1-kis.txt",
  "answer_file": "test/sample/ans/query-p2-1-kis.csv",
  "query_text": "...",
  "target_video_id": "L24_V035",
  "seed_frame_csv_line1": 488,
  "extracted_intervals": [
    {"start_frame": 450, "end_frame": 520, "event_desc": "E1: Nhóm người chơi đùa bên con vật"}
  ],
  "evaluation": {
    "difficulty_tier": 3,
    "difficulty_breakdown": {
      "MOD-VIS": "...",
      "MOD-AUD": "...",
      "MOD-OCR": "...",
      "MOD-WORD": "...",
      "MOD-FLOW": "..."
    },
    "accuracy_score": 92.5,
    "accuracy_analysis": "..."
  },
  "learning_decision": "LEARNED",
  "distilled_insights": "..."
}
```
