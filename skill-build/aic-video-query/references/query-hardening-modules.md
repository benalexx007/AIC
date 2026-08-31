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
5. **Multi-Entity Apparel Binding & Micro-Action Coupling (Phân tách trang phục kép & Vi hành động đa thực thể):**
   * Trong bối cảnh có nhiều đối tượng cùng thực hiện hoạt động chung (thể thao, đám đông), gán tổ hợp thuộc tính trang phục kép cho từng chủ thể (*áo đỏ + nón trắng*, *áo xanh đậm*, *áo đen phối cam*) đi liền với vi hành động cục bộ diễn ra trong tích tắc (*lấy nước rưới vào mặt*, *đuổi theo người phía trước*). Ép hệ thống giải phải thực hiện liên kết thuộc tính không gian - thời gian (Spatiotemporal Attribute Binding).
6. **Extreme Pose & Anomaly Action Localization (Nhận diện tư thế bất thường / Hành vi phi chuẩn):**
   * Khai thác các tư thế vật lý hiếm hoặc nguy hiểm nằm ngoài phân phối chuẩn của con người khi điều khiển phương tiện hoặc thao tác đồ vật (*nằm dài trên yên xe máy phóng tốc độ cao*, *buông tay lái*, *đu người ngoài thành xe*). Kỹ thuật này triệt tiêu các mô hình Pose Estimation / Action Classifier chỉ được học trên hành vi chuẩn mực thông thường.
7. **Wide-to-Close Scale Transition & Micro-Morphology (Biến thiên tỉ lệ khung hình Rộng $\rightarrow$ Cận cảnh & Hình thái vi mô):**
   * Khai thác sự biến đổi góc máy từ góc trung/toàn cảnh (thao tác tổng quan của người) cắt nhanh sang góc máy cận cảnh/siêu cận cảnh (macro close-up trực diện trên bề mặt vật thể/món ăn/công cụ). Ép mô hình giải phải nhận diện được hình thái đặc thù cục bộ của thực thể (ví dụ các lát cắt dồi trường hình ống màu trắng, cuống bông hẹ xanh dài) ngay cả khi tỉ lệ phóng to làm biến mất toàn bộ bối cảnh không gian và nhân vật xung quanh.
8. **Geometric Array Counting & Transparent Occlusion Distortion (Đếm mảng bố trí hình học & Biến dạng nắp trong suốt):**
   * Định dạng câu hỏi đếm số lượng vật thể/ngăn khuôn bố trí theo mạng hình học đối xứng (ví dụ khuôn tròn 7 ngăn: 1 tâm + 6 ngoài), đồng thời lồng ghép điều kiện kiểm chứng thành phần vi mô trên từng ô (*mỗi chiếc bánh có 1 hạt sen*) dưới nắp kính có hơi nước ngưng tụ hoặc phản quang. Ép mô hình giải phải thực hiện đếm không gian chính xác (Spatial Visual Counting) và xử lý hình ảnh qua mặt phẳng khúc xạ/phản xạ.
9. **Thermal State Transition & Post-Heat Action Anchor (Chuyển dịch trạng thái nhiệt & Điểm neo thao tác sau khi tắt lửa):**
   * Kết hợp đồng thời sự xuất hiện của tập hợp nhiều nguyên liệu đa màu sắc ($M \ge 5$: thịt gà, ớt đỏ, ớt xanh, đậu phộng, hành tím) với sự kiện **chuyển đổi trạng thái nhiệt vật lý** (*tắt lửa/ngừng cung cấp nhiệt*) trước khi bổ sung gia vị nhạy cảm với nhiệt (*vỏ chanh mài, nước cốt chanh*) và trút ra đĩa thành phẩm. Kỹ thuật này ép hệ thống giải phải theo dõi sự kiện động (bật/tắt lửa) song hành cùng quan hệ liên kết thuộc tính của món ăn.
10. **Sub-Centimeter Accessory Localization & Jersey-Helmet Combinatorial Binding (Định vị phụ kiện vi mô dưới 1cm & Ràng buộc tổ hợp Mũ - Áo):**
    * Trong bối cảnh nhóm đối tượng đông người cùng mặc đồng phục đội tương tự nhau (ví dụ 2 tay đua áo xanh biển), tạo điều kiện phân biệt kép bằng màu sắc mũ bảo hiểm (đỏ vs trắng) và kết hợp với một **chi tiết phụ kiện vi mô cấp dưới centimeter** (*sợi dây tai nghe đàm thoại màu trắng treo lơ lửng dưới quai nón gần cổ*). Kỹ thuật này triệt tiêu hoàn toàn khả năng phân loại tổng thể của các mô hình CLIP/ResNet và ép mô hình giải phải đạt năng lực siêu phân giải thị giác (High-Resolution Visual Grounding).
11. **Background Monotonous Object Array & Folk Craft Context (Điểm neo mảng đồ vật đơn điệu ở hậu cảnh & Bối cảnh làng nghề dân gian):**
    * Neo điều kiện truy vấn vào một chuỗi/dãy đồ vật gia dụng bình dị lặp lại ở hậu cảnh (ví dụ: *dãy ~10 chiếc thớt gỗ tròn treo thành hàng ngang sát cửa sổ lớn*) kết hợp với hoạt động làng nghề truyền thống và tên gọi nội thất bản địa (*'hai người phụ nữ làm thủ công trên bộ ván ngựa'*). Kỹ thuật này triệt tiêu các mô hình chỉ tập trung vào nhân vật tiền cảnh và buộc hệ thống giải phải thực hiện phân tích không gian hậu cảnh đa tầng (Deep Background Spatial Grounding).

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
5. **Foreign Script Character Count & Fine Print Body Target (Đếm ký tự phi Latin & Đọc mã số nhỏ trên thân vỏ đối tượng):**
   * Sử dụng đặc trưng số lượng ký tự phi Latin (*"biển hiệu màu đỏ gồm 6 ký tự chữ Hán"*) làm mốc neo không gian duy nhất trong hậu cảnh, sau đó đặt câu hỏi về các mã số nhỏ in trên thân vỏ phương tiện/đối tượng (*"con số trên hông xe"*). Kỹ thuật này thách thức các công cụ OCR thông thường vốn chỉ nhận diện bảng chữ cái chuẩn.
6. **3D Stage Physical Typography & Partial OCR Prefix Anchor (Chữ nổi 3D vật lý sân khấu & Điểm neo tiền tố bán phần):**
   * Trích xuất chữ điêu khắc khối 3D vật lý (Stage 3D Physical Letters) có phủ kim tuyến lấp lánh phản chiếu ánh sáng sân khấu, đồng thời chỉ cung cấp tiền tố ngắn gọn kèm dấu ba chấm (*'SẮC CỔ ...'* thay vì toàn bộ cụm từ). Kỹ thuật này làm vô hiệu hóa các thuật toán so khớp chuỗi ký tự chính xác (Exact Match) và bắt buộc mô hình phải giải mã ký tự 3D biến dạng quang học phức tạp.
7. **Dynamic Digital 7-Segment LED Traffic Signal Countdown Reader (Đọc số đếm ngược đèn tín hiệu giao thông LED 7 đoạn ngoài trời):**
   * Khai thác các con số đếm ngược thời gian phát sáng dạng LED 7 đoạn trên các cột đèn tín hiệu giao thông tại ngã tư (*đèn xanh đếm ngược đến 13 giây*) trong bối cảnh máy quay gắn trên phương tiện di chuyển với vận tốc cao và rung lắc mạnh. Kỹ thuật này triệt tiêu các mô hình OCR văn bản thông thường và đòi hỏi năng lực nhận dạng ký tự quang học phát quang ma trận (Luminous Matrix OCR).
8. **Multi-Column Tabular OCR Reasoning & Color-Coded Statistical Highlighting (Suy luận bảng biểu thống kê đa cột & Phân hóa màu sắc số liệu):**
   * Trích xuất và suy luận trên dữ liệu cấu trúc bảng nhiều cột trong các video bài giảng/thuyết trình số liệu, đặt ràng buộc phân hóa ngữ nghĩa theo màu sắc phông chữ số liệu (*Top 3 in đỏ, Bottom 2 in xanh*) kết hợp mệnh đề **suy luận logic tương phản liên cột** (*'vùng có số lượng đô thị ít nhất ở cột A lại có quy mô dân số đô thị cao nhất ở cột B'*). Kỹ thuật này triệt tiêu các bộ OCR văn bản thuần túy và bắt buộc mô hình phải giải mã được cấu trúc bảng (Table Structure Parsing) và thực hiện suy luận logic số liệu đa biến.

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
5. **Cultural & Domain Defamiliarization (Lạ hóa thực thể văn hóa / biểu diễn đặc thù):**
   * Thay vì dùng danh từ định danh phổ biến (ví dụ: *'con lân sư rồng'*, *'đạo cụ biểu diễn'*, *'võ phục'*), miêu tả bằng hình học, màu sắc và thuộc tính thuần túy (*'con vật màu vàng'*, *'vật trông như trái bí đỏ'*). Kỹ thuật này vô hiệu hóa nhãn phân lớp định sẵn của Object Detection/CLIP và bắt buộc hệ thống giải phải suy luận thị giác nguyên bản.
6. **Pure Geometric & Chromatic Entity Anonymization (Ẩn danh hóa thực thể bằng hình học & màu sắc thuần túy):**
   * Triệt tiêu hoàn toàn danh từ định danh riêng biệt (*cá xiên que, ớt băm, ngò rí, bột chiên giòn*) và thay thế 100% bằng tập hợp thuộc tính hình học và màu sắc cơ bản (*'nguyên liệu dài được xiên que'*, *'hỗn hợp màu xanh lá cây và màu đỏ băm nhỏ'*, *'bột trắng'*). Kỹ thuật này làm vô hiệu hóa các bộ mở rộng từ khóa (LLM Expansion) và ép các mô hình Vision-Language phải suy luận trực tiếp trên đặc trưng thị giác nguyên thủy.

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

### 🔑 Các Kỹ Thuật Điều Phối Dòng Chảy Kể Chuyện Cốt Lõi (`MOD-FLOW` Patterns):
1. **Định Vị Hai Đầu Ranh Giới Thời Gian (Dual-Boundary Temporal Framing / Start-End Anchor Pairing):**
   * Cấu trúc: *"Đoạn clip bắt đầu với cảnh [Sự kiện A]... Đoạn clip kết thúc với cảnh [Sự kiện B]"*.
   * Triệt tiêu hoàn toàn khả năng giải bằng tìm kiếm đơn điểm (Single-frame similarity search); bắt buộc hệ thống giải phải tìm độc lập hai điểm biên A và B rồi cắt chính xác phân đoạn bao trùm.
2. **Cầu Nối Đa Phương Thức Bắc Cầu (Multi-Modal Bridge):**
   * Sự kiện ở Phân đoạn 1 chỉ được giải mã trọn vẹn khi kết hợp với manh mối âm thanh hoặc OCR xuất hiện ở Phân đoạn 2.
3. **Chuyển Tiếp Đa Góc Nhìn Xuyên Buồng Lái - Ngoại Cảnh (Cross-Perspective POV Shift / Interior-Exterior Continuity):**
   * Xâu chuỗi 2 góc quay tương phản của cùng một sự kiện: bắt đầu từ góc nhìn nội bộ (First-Person Interior POV - vô lăng tự xoay trong cabin xe tự lái) rồi cắt sang góc nhìn toàn cảnh ngoại vi (Third-Person Exterior POV - chiếc xe rẽ trên đường phố). Buộc mô hình giải phải theo dõi thực thể xuyên góc máy (Cross-view Entity Tracking) thay vì trích xuất đặc trưng rời rạc.
4. **Multi-Event Strict Sequential Ordering ($N$-Stage Succession / TRAKE Logic):**
   * Cấu trúc truy vấn thành một chuỗi $N$ sự kiện liên tiếp ($E_1 \rightarrow E_2 \rightarrow \dots \rightarrow E_N$), trong đó mỗi sự kiện định nghĩa một thuộc tính phân loại hình ảnh vi mô riêng biệt (ví dụ 4 loại hoa quả nhiệt đới khác nhau) và yêu cầu bắt trúng khung hình chuyển cảnh đầu tiên (`First appearance of entity`). Kỹ thuật này ép hệ thống giải phải vượt qua bài toán phối hợp Temporal Logic + Shot Boundary Detection + Fine-Grained Classification.
5. **Cầu Nối Thao Tác - Siêu Dữ Liệu Bảng Nguyên Liệu / Thông Số (Action-to-Metadata Cross-Bridge / Fine-Grained QA):**
   * Miêu tả chi tiết thao tác thị giác vi mô gắn với danh sách và số lượng nguyên phụ liệu (*nhét tiêu xanh, lá chanh, sả vào bụng 4 con cá*), nhưng mục tiêu câu hỏi lại nhắm vào định danh thực thể chính (*đây là loài cá gì?*). Bắt buộc hệ thống giải phải định vị được phân đoạn thao tác rồi truy vết ngược về bảng thông tin OCR (Ingredient Card) hoặc lời thoại thuyết minh ở đầu chương trình để trích xuất đáp án.
6. **Cinematographic Camera Kinematics & Multi-Shot Montage Grammar (Ngữ pháp dựng phim & Chuỗi động lực học máy quay):**
   * Cấu trúc câu hỏi ràng buộc sự liên kết của chuỗi $K$ cú máy liên tiếp ($K \ge 3$) với các vector chuyển động máy quay cụ thể (*lia chéo góc thấp hướng lên $\rightarrow$ góc cao quét từ trên xuống $\rightarrow$ cú máy tĩnh toàn cảnh flat-lay*) kết hợp biến đổi tiêu điểm đối tượng qua từng cú máy. Ép hệ thống giải phải phân tích được ngữ pháp biên tập video (Shot Boundary & Video Syntax) và vector chuyển động thị giác của camera (Camera Motion Dynamics).
7. **Multi-Hop Cross-Scene Geographic Landmark Bridge (Cầu nối truy vết địa danh đa chặng):**
   * Cấu trúc câu hỏi QA xâu chuỗi hai phân cảnh hành động cách xa nhau trong phóng sự (ví dụ: *mạnh thường quân hỗ trợ ngoài vỉa hè $\rightarrow$ chuyển sang trò chuyện cùng tình nguyện viên quốc tế trong phòng nghỉ*) và đặt câu hỏi truy xuất địa danh/tên đường cụ thể của địa điểm. Buộc hệ thống giải phải theo dõi toàn bộ diễn tiến phóng sự và liên kết dữ liệu OCR mặt tiền hoặc lời thoại thuyết minh.

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
