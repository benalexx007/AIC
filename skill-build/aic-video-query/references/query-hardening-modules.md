# Hướng Dẫn Kỹ Thuật: 5 Module Tăng Độ Khó Truy Vấn AIC (Query Hardening Framework)

Tài liệu này là **bộ quy chuẩn và chỉ dẫn hành động (Instructional & Algorithmic Guide)** dành cho Core LLM (Agent) khi tạo các câu truy vấn kiểm thử (Benchmark Test Cases) có độ khó cao, nhằm đánh giá và thách thức các hệ thống tìm kiếm video thông minh (Video Retrieval Systems) trong cuộc thi AIC 2026.

---

## 🎯 Tổng Quan 5 Module

Hệ thống phân chia thành 2 nhóm module bổ trợ lẫn nhau:
1. **Nhóm Độ Khó Trường Thông Tin (Information Depth - Modality Level):**
   * `MOD-VIS`: Nâng cao độ khó thị giác vi mô & chuyển dịch trạng thái vật lý.
   * `MOD-AUD`: Nâng cao độ khó âm thanh môi trường, tiếng động phi ngôn ngữ & ngữ điệu lời nói.
   * `MOD-OCR`: Nâng cao độ khó văn bản ngoại cảnh, chữ biến dạng 3D & ghép mảnh ký tự.
2. **Nhóm Phương Pháp Sinh & Điều Phối (Generation & Orchestration):**
   * `MOD-WORD`: Lạ hóa ngôn từ, phủ định logic ngầm & bẫy mô hình Re-ranking.
   * `MOD-FLOW`: Nghệ thuật đan cài câu đố đa phương thức (The Storyteller) & Nhạc trưởng điều phối.

---

## 👁️ 1. MODULE 1: `MOD-VIS` (Advanced Visual Reasoning)

### 🎯 Mục tiêu triệt tiêu:
Vượt qua các mô hình Vision-Language cơ bản (như OpenAI CLIP ViT-B/32, SigLIP, BLIP-2) vốn chỉ nhận diện tốt các vật thể nổi bật toàn cục (Global Bag-of-Objects).

### ⚙️ Các kỹ thuật tạo câu hỏi:
1. **Spatial-Temporal Micro-Relationships (Quan hệ không gian vi mô):**
   * Thay vì chỉ nói *"người đàn ông cầm cốc"*, hãy ràng buộc vị trí tương đối đa điểm:
   * *Ví dụ:* *"Bàn tay trái đeo nhẫn bạc ở ngón áp út đặt chiếc cốc sứ màu xanh lam sang bên phải đĩa bánh ngọt trước khi người đối diện nghiêng đầu sang hướng khác."*
2. **Micro-Action & State Transitions (Chuyển dịch trạng thái vật lý):**
   * Bắt trúng khoảnh khắc chuyển giao trạng thái động $\leftrightarrow$ tĩnh hoặc biến đổi hình thái:
   * *Ví dụ:* *"Khoảnh khắc ngọn nến vừa tắt bắt đầu xuất hiện sợi khói mỏng bốc lên"*, *"Khoảnh khắc giọt dầu sôi đầu tiên bắn ra khỏi mép chảo khi miếng thịt vừa chạm bề mặt."*
3. **Low-Saliency Background & Occlusion (Chi tiết hậu cảnh & Che khuất một phần):**
   * Đặt điều kiện vào các chi tiết phản chiếu qua gương/kính (reflection), bóng đổ (shadows), hoặc vật thể bị che khuất $\ge 50\%$ bởi đối tượng khác ở tiền cảnh.
4. **Fine-Grained Attribute Binding (Ràng buộc thuộc tính tinh vi):**
   * Trong một khung hình có 3 người cùng mặc áo tối màu, gán các thuộc tính cực kỳ chi tiết (màu viền cổ áo, hoa văn trên cúc áo, loại quai túi xách) để loại bỏ mọi sự nhầm lẫn chéo.

---

## 🔊 2. MODULE 2: `MOD-AUD` (Acoustic Depth & Paralinguistics)

### 🎯 Mục tiêu triệt tiêu:
Vượt qua các hệ thống tìm kiếm dựa trên văn bản hội thoại (ASR / Whisper Keyword Search) chỉ trích xuất được từ ngữ trong lời thoại chính.

### ⚙️ Các kỹ thuật tạo câu hỏi:
1. **Non-Verbal & Environmental Sounds (Tiếng động môi trường phi ngôn ngữ):**
   * Khai thác các âm thanh cơ học, âm thanh sinh học hoặc tiếng động môi trường đặc thù:
   * *Ví dụ:* *"Tiếng lách cách của chìa khóa cọ vào ổ khóa trước khi cửa mở"*, *"Tiếng động cơ xe gắn máy chuyển số gấp khi leo dốc"*, *"Tiếng đũa gõ nhẹ vào vành bát sành hai lần"*.
2. **Paralinguistic & Prosodic Cues (Ngữ điệu, Cảm xúc & Âm vị học):**
   * Khai thác tiếng thở dài ngắt quãng, giọng nói thì thầm (whispering), tiếng cười gượng, sự ngập ngừng (hesitation/pause) trước một từ then chốt.
   * *Ví dụ:* *"Đoạn hội thoại mà người nói ngập ngừng thở dài rồi mới thốt ra tên của địa danh..."*
3. **Multi-Source Acoustic Overlap (Giao thoa nguồn âm nền):**
   * Chi tiết quyết định nằm ở tiếng loa phát thanh xa xa, bài hát radio đang phát trong quán cà phê, hoặc âm thanh TV nền trong khi nhân vật chính đang trò chuyện.
4. **Cross-Modal Audio-Visual Asynchrony (Bất đồng bộ âm - hình):**
   * Tiếng chuông cửa vang lên trong khi màn hình đang chiếu cận cảnh gương mặt người ngồi trong phòng giật mình ngước nhìn (buộc mô hình phải liên kết tín hiệu âm thanh với hành động thị giác).

---

## 📝 3. MODULE 3: `MOD-OCR` (In-The-Wild & Fragmented OCR)

### 🎯 Mục tiêu triệt tiêu:
Vượt qua các công cụ OCR thông thường (PaddleOCR, EasyOCR, CRNN) chỉ đọc được văn bản in ấn phẳng, độ tương phản cao.

### ⚙️ Các kỹ thuật tạo câu hỏi:
1. **Perspective Distortion & Curved 3D Text (Chữ méo góc & Chữ trên bề mặt cong/nhăn):**
   * Chữ in trên áo thun bị nhăn theo nếp gấp cơ thể khi vận động.
   * Chữ dán vòng cung quanh thân chai nhựa, thân xe bus bị chụp ở góc xiên cực hẹp ($< 30^\circ$).
2. **Low Contrast, Glare & Neon Diffusion (Chữ tương phản thấp & Lóa sáng):**
   * Chữ đèn LED/Neon phát sáng làm nhòe viền ký tự.
   * Chữ khắc dập nổi trên kim loại cùng màu, chữ in mờ sau lớp kính bám bụi/nước mưa.
3. **Fragmented & Multi-Frame Text Stitching (Ghép mảnh chữ chuyển động):**
   * Ký tự trên biển quảng cáo bị cây cối che khuất một nửa; chỉ khi camera lia qua nhiều frame thì người giải mới ghép đủ các chữ cái để suy ra từ hoàn chỉnh.
4. **Technical Codes & Semantic Acronyms (Ký hiệu kỹ thuật & Chữ viết tắt):**
   * Mã số hiệu chuyến bay, mã vạch/QR ở góc bao bì, đuôi biển số xe kết hợp chữ viết tắt tỉnh thành.

---

## 🎭 4. MODULE 4: `MOD-WORD` (Adversarial Phrasing & Linguistic Obfuscation)

### 🎯 Mục tiêu triệt tiêu:
Vượt qua các chiến thuật tối ưu hóa truy vấn hiện đại của thí sinh:
* **Dense Semantic Retrieval (BGE, Contriever, CLIP Text-Encoder):** Làm lệch vector embedding bề mặt.
* **LLM Multi-Query Expansion:** Làm cho việc paraphrase câu hỏi của LLM bị mất dấu các ràng buộc ngầm.
* **Cross-Encoder Re-rankers:** Cài bẫy các từ khóa gây nhiễu (Distractors) khiến mô hình xếp hạng nhầm các phân cảnh tương tự.

### ⚙️ Các kỹ thuật tạo câu hỏi:
1. **Defamiliarization / Periphrasis (Lạ hóa khái niệm & Nói vòng):**
   * Không dùng tên gọi trực tiếp của đồ vật/hành động thông thường; thay bằng miêu tả cơ học/hình học/vật lý:
   * *Thay vì:* `"Người phụ nữ mặc áo vàng mở ô che mưa"`
   * *Lạ hóa:* `"Cá nhân trong trang phục mang sắc màu hoa dã quỳ mở bung kết cấu vòm cầm tay nhằm ngăn những hạt chất lỏng rơi tự do từ bầu trời."`
2. **Implicit Logic Negation (Phủ định ngầm & Ràng buộc loại trừ):**
   * Sử dụng mệnh đề phụ định logic mà các mô hình embedding rất dễ bỏ qua:
   * *Ví dụ:* *"Khoảnh khắc mà cá nhân duy nhất KHÔNG đeo găng tay lại là người trực tiếp tiếp xúc với bề mặt hộp kim loại..."*
3. **Temporal Inversion & Anaphora (Đảo ngược trình tự thời gian & Đại từ thay thế):**
   * Kể kết quả trước, nguyên nhân sau, kết hợp chuỗi đại từ liên kết:
   * *Ví dụ:* *"Sau khi âm thanh kim loại va chạm vang lên chấm dứt, người vừa đánh rơi nó mới bắt đầu cúi gập người tìm kiếm dưới gầm bàn."*
4. **Adversarial Distractor Injection (Cài cắm từ khóa bẫy):**
   * Chèn các từ ngữ dễ gợi liên tưởng đến một phân cảnh phổ biến khác trong video (ví dụ: nhắc đến *"cảnh chợ hoa"* trong một câu hỏi thực chất nằm ở phân cảnh *"trong nhà bếp"* qua một vật thể liên đới), khiến các hệ thống search top-100 bị hút về phân cảnh bẫy.

---

## 🧩 5. MODULE 5: `MOD-FLOW` (Narrative Flow & Master Orchestration)

### 🎯 Vai trò:
**Nhạc trưởng (Orchestrator)** điều phối toàn bộ các module và xây dựng cấu trúc **"Vụ án / Câu đố ghép hình đa phương thức" (Multi-modal Jigsaw Puzzle)**.

### ⚙️ Triết lý "The Storyteller" (Người kể chuyện):
* Một câu query không phải là một danh sách kiểm tra (checklist) các thuộc tính rời rạc.
* Câu query được cấu trúc như **một câu chuyện nhỏ có mở đầu, diễn biến và cao trào logic**, trong đó mỗi module thông tin đóng vai trò là một mảnh ghép không thể thiếu:
  $$\text{Chỉ có Hình ảnh (Visual)} \to 10 \text{ đoạn giống nhau (Không Unique)}$$
  $$\text{Chỉ có Âm thanh (Audio)} \to 5 \text{ đoạn giống nhau (Không Unique)}$$
  $$\text{Chỉ có OCR} \to 4 \text{ đoạn giống nhau (Không Unique)}$$
  $$\mathbf{Hình\ ảnh \cap Âm\ thanh \cap OCR \cap Logic\ Kể\ chuyện} \to \mathbf{Duy\ nhất\ 1\ khoảng\ Frame\ (100\%\ Unique)}$$

---

## 📊 Bảng Phân Cấp Độ Khó (Difficulty Tiers)

Khi tạo tập dữ liệu Benchmark, Core LLM áp dụng bảng phân cấp sau để gắn nhãn độ khó:

| Cấp độ | Tên gọi | Modules Kích Hoạt | Đặc Điểm Cốt Lõi | Mục Tiêu Thử Thách |
|:---|:---|:---|:---|:---|
| **Level 1** | **Standard** | Base Pipeline | Mô tả trực diện, từ ngữ chuẩn mực, 1–2 vị từ rõ ràng. | Baseline systems |
| **Level 2** | **Hard** | `MOD-VIS` + `MOD-WORD` | Vi hành động, quan hệ không gian, nói vòng (periphrasis). | Dense CLIP / BM25 |
| **Level 3** | **Very Hard** | `MOD-VIS` + `MOD-AUD` + `MOD-WORD` | Tiếng động phi ngôn ngữ, ngữ điệu, phủ định ngầm, đảo trật tự thời gian. | Whisper search, Simple RAG |
| **Level 4** | **Adversarial** | `MOD-VIS` + `MOD-AUD` + `MOD-OCR` + `MOD-WORD` | Đan cài đủ 3 kênh, chữ biến dạng 3D, bẫy từ khóa gây nhiễu (distractor). | Multi-query, Cross-encoder |
| **Level 5** | **Grandmaster** | **Toàn bộ 5 Modules (`MOD-FLOW` chủ đạo)** | **Câu đố liên hoàn đa phương thức phi tuyến tính**, bắt buộc suy luận bắc cầu 3 kênh thông tin. | Toàn bộ hệ thống AI tự động |

---

## 🛠️ Quy Trình 5 Bước Tạo Query Chuẩn Cấp Độ Cao

1. **Khảo sát đa kênh (Multi-modal Scouting):** Mở video, xác định các điểm giao thoa có cả chi tiết thị giác vi mô, âm thanh môi trường và văn bản nền.
2. **Trích xuất thuộc tính khó (Clue Extraction):** Thu thập các vị từ đạt chuẩn theo `MOD-VIS`, `MOD-AUD`, `MOD-OCR`.
3. **Thẩm định tính duy nhất đa mảnh ghép (Interlocking Uniqueness Check):**
   * Chạy `check_uniqueness.py` kiểm tra từng thuộc tính riêng lẻ $\to$ xác nhận có ứng viên trùng lặp.
   * Kết hợp cả 3 thuộc tính $\to$ xác nhận kết quả trả về `no_alternate_cluster_detected`.
4. **Biến đổi ngôn từ (Adversarial Phrasing via `MOD-WORD`):** Viết lại câu truy vấn bằng thủ pháp lạ hóa, câu phức logic, phủ định ngầm.
5. **Căn biên chính xác & Xuất kết quả:** Trích xuất frame `step=1` ở 2 đầu ranh giới, ghi nhận đầy đủ metadata vào `result-xxx.yaml` và đồng bộ `ground_truth.json`.
