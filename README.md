# AIC 2026 - Video Query, Ground Truth & Semantic Retrieval Framework

Hệ thống tự động hóa và chuẩn hóa quy trình tạo câu truy vấn, xác minh tính duy nhất (Uniqueness Verification), gán nhãn Ground Truth và đánh giá hiệu năng mô hình tìm kiếm video phục vụ cuộc thi **AI Challenge (AIC) 2026**.

---

## 📋 Yêu cầu hệ thống (Prerequisites)

* **Hệ điều hành:** Windows 10/11 64-bit.
* **Python:** Python 3.10 trở lên (đã thêm vào `PATH`).
* **FFmpeg:** Đã cài đặt và có trong `PATH` (hoặc đặt tại `tools/ffmpeg/bin`).
* **Phần cứng hỗ trợ AI (Khuyến nghị):**
  * Intel GPU / Intel Arc (sử dụng Intel XPU qua PyTorch XPU).
  * Hoặc NVIDIA GPU (CUDA).
  * Hoặc CPU (hỗ trợ tự động fallback).

---

## 🚀 Hướng dẫn cài đặt môi trường (Quick Start)

Dự án sử dụng cơ chế **2 môi trường ảo Python độc lập** để tối ưu hóa hiệu năng và tránh xung đột thư viện giữa xử lý âm thanh/video và tính toán vector ngữ nghĩa.

### Bước 1: Cài đặt môi trường xử lý Video (`.venv-video`)
Môi trường này phục vụ: Tải Google Drive tốc độ cao (`gdown`), chuyển giọng nói thành văn bản (`faster-whisper`), phát hiện chuyển cảnh (`scenedetect`), và xử lý frame (`opencv-python`).

Mở PowerShell tại thư mục gốc dự án và chạy:
```powershell
powershell -ExecutionPolicy Bypass -File .\install_video_python_tools.ps1
```

### Bước 2: Cài đặt môi trường AI Semantic Vision (`.venv-semantic`)
Môi trường này phục vụ: Trích xuất đặc trưng đa phương thức (`open_clip_torch`), phát hiện đối tượng (`ultralytics` YOLO), tính toán ma trận tương đồng và gom cụm (`scikit-learn`, `numpy`).

Chạy lệnh:
```powershell
powershell -ExecutionPolicy Bypass -File .\install-semantic-vision.ps1
```

> **Ghi chú về thiết bị phần cứng:**  
> Mặc định script sẽ cài PyTorch XPU (dành cho Intel Arc / Intel GPU). Nếu bạn sử dụng NVIDIA CUDA hoặc CPU thuần, có thể chỉ định tham số:
> * NVIDIA CUDA: `.\install-semantic-vision.ps1 -TorchDevice cuda`
> * CPU thuần: `.\install-semantic-vision.ps1 -TorchDevice cpu`

### Bước 3: Kiểm tra hoạt động môi trường (Smoke Test)
Sau khi cài đặt xong, bạn có thể chạy script kiểm tra:
```powershell
.\.venv-semantic\Scripts\python.exe .\semantic_vision_smoke_test.py --models-dir .\models\semantic --report .\semantic-install-report.json
```

---

## 📂 Cấu trúc thư mục dự án (Project Structure)

```text
AIC/
├── .gitignore                      # Cấu hình bỏ qua virtualenv, model weights, video runs
├── README.md                       # Hướng dẫn tổng quan và cài đặt
├── HUONG_DAN_VIDEO_TASK.md         # Quy trình chuẩn chi tiết để xử lý từng video
├── HUONG_DAN_TAO_TAP_TEST.md       # Hướng dẫn tạo tập Ground Truth Benchmark
│
├── install_video_python_tools.ps1  # Script tự động tạo và cài đặt .venv-video
├── install-semantic-vision.ps1     # Script tự động tạo và cài đặt .venv-semantic
├── semantic_vision_smoke_test.py   # Script kiểm tra tích hợp phần cứng và thư viện
│
├── skill-staging/                  # Bộ công cụ và kịch bản thực thi chính
│   └── aic-video-query-retention-update/
│       ├── SKILL.md                # Tài liệu định nghĩa kỹ năng (Skill documentation)
│       └── scripts/                # Toàn bộ script xử lý luồng:
│           ├── download_drive.py   # Tải video từ Google Drive với cơ chế resume
│           ├── prepare_video.py    # Xử lý video, audio, Whisper, scene cut, contact sheets
│           ├── semantic_index.py   # Lập ma trận embedding OpenCLIP và YOLO
│           ├── check_uniqueness.py # Quét và xác minh tính duy nhất trên toàn video
│           ├── extract_window.py   # Trích xuất frame chi tiết tìm ranh giới interval (step=1)
│           ├── transcript_search.py# Tìm kiếm phân đoạn hội thoại từ transcript
│           ├── clip_search.py      # Tìm kiếm frame qua mô tả văn bản
│           ├── ocr_frames.py       # Nhận diện chữ viết trên frame
│           ├── export_result.py    # Xuất file kết quả (query, answer, yaml)
│           └── purge_previous_runs.py # Dọn dẹp an toàn các file chạy tạm
│
├── data/
│   └── benchmark/
│       └── ground_truth.json       # Bộ dữ liệu Ground Truth chuẩn đánh giá Benchmark
│
└── test/                           # Tập kết quả truy vấn kiểm thử đã hoàn thành
    ├── query/                      # Danh sách file query (query-*.txt)
    ├── answer/                     # Danh sách file answer (ans-*.txt)
    ├── yaml/                       # File metadata chi tiết (result-*.yaml)
    └── ground_truth.json           # File tổng hợp toàn bộ test cases
```

---

## 🔄 Quy trình chuẩn xử lý một tác vụ Video (Standard Pipeline)

Quy trình chuẩn gồm 5 bước được quy định tại [HUONG_DAN_VIDEO_TASK.md](HUONG_DAN_VIDEO_TASK.md):

1. **Thăm dò và Tải video (Probe & Download):**
   ```powershell
   $env:PYTHONUTF8=1; & '.\.venv-video\Scripts\python.exe' '.\skill-staging\aic-video-query-retention-update\scripts\download_drive.py' --url '<DRIVE_URL>' --output-dir '.\video-runs\probe' --probe-only
   ```
2. **Tiền xử lý và tạo Contact Sheets:**
   ```powershell
   $env:PYTHONUTF8=1; & '.\.venv-video\Scripts\python.exe' '.\skill-staging\aic-video-query-retention-update\scripts\prepare_video.py' --input '<DRIVE_URL_OR_LOCAL>' --query-type kis --profile high --runs-root '.\video-runs'
   ```
3. **Lập chỉ mục ngữ nghĩa (Semantic Indexing):**
   ```powershell
   $env:PYTHONUTF8=1; & '.\.venv-semantic\Scripts\python.exe' '.\skill-staging\aic-video-query-retention-update\scripts\semantic_index.py' --manifest '.\video-runs\<RUN_DIR>\manifest.json'
   ```
4. **Kiểm tra tính duy nhất trên toàn video (Uniqueness Verification):**
   ```powershell
   $env:PYTHONUTF8=1; & '.\.venv-semantic\Scripts\python.exe' '.\skill-staging\aic-video-query-retention-update\scripts\check_uniqueness.py' --index '.\video-runs\<RUN_DIR>\semantic\semantic-index.json' --prompt "<MÔ_TẢ_QUERY>" --target-start-frame <START> --target-end-frame <END> --output '.\video-runs\<RUN_DIR>\evidence\uniqueness.json'
   ```
5. **Xuất kết quả đạt chuẩn:**
   ```powershell
   $env:PYTHONUTF8=1; & '.\.venv-video\Scripts\python.exe' '.\skill-staging\aic-video-query-retention-update\scripts\export_result.py' --query-type kis --query "<QUERY>" --video-id <VIDEO_ID> --interval <START> <END> --fps 25.0 --index <NUM> --root '.\test' --confidence high --evidence '.\video-runs\<RUN_DIR>\manifest.json'
   ```
