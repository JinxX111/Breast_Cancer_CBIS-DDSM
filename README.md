# Xây dựng mô hình học sâu phát hiện và định vị tổn thương có chọn lọc lành tính và ác tính trên ảnh X-quang tuyến vú

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Dataset](https://img.shields.io/badge/Dataset-CBIS--DDSM-brightgreen)
![Framework](https://img.shields.io/badge/Framework-PyTorch%20%7C%20YOLOv5-orange)
![Application](https://img.shields.io/badge/Web%20Demo-Streamlit-ff4b4b)

Khóa luận tốt nghiệp ngành Khoa học dữ liệu — 2026.

## 1. Giới thiệu

Dự án nghiên cứu và xây dựng quy trình học sâu hai giai đoạn nhằm phát hiện, định vị vùng tổn thương Mass và phân loại tính chất mô bệnh học lành tính/ác tính trên ảnh X-quang tuyến vú. Dữ liệu sử dụng là **CBIS-DDSM (Curated Breast Imaging Subset of DDSM)** từ The Cancer Imaging Archive (TCIA).

Phạm vi thực nghiệm chính tập trung vào **Mass**. Calcification được khảo sát trong giai đoạn tìm hiểu dữ liệu nhưng không thuộc phạm vi mô hình chính.

> **Lưu ý:** Đây là sản phẩm nghiên cứu học thuật, không phải thiết bị y tế và không thay thế đánh giá hoặc chẩn đoán của bác sĩ.

## 2. Kiến trúc nghiên cứu

Dự án sử dụng kiến trúc **Two-stage Pipeline**:

1. **Mass Detection & Localization:** YOLOv5n phát hiện vùng Mass và trả về Bounding Box cùng confidence.
2. **Pathology Classification:** vùng Mass được trích xuất và đưa vào CNN để phân loại BENIGN/MALIGNANT.

Các kiến trúc phân loại được huấn luyện và so sánh gồm **VGG16, ResNet50 và InceptionV3**. Web Demo hiện sử dụng YOLOv5n và InceptionV3 làm mô hình trình diễn.

Nhãn pathology gốc gồm `BENIGN`, `BENIGN_WITHOUT_CALLBACK` và `MALIGNANT`. Trong thí nghiệm nhị phân, hai nhãn lành tính được ánh xạ về `BENIGN`, còn `MALIGNANT` được giữ riêng; nhãn gốc được bảo toàn trong metadata.

## 3. Dữ liệu

Nguồn: [CBIS-DDSM — The Cancer Imaging Archive](https://www.cancerimagingarchive.net/collection/cbis-ddsm/).

Dự án khai thác DICOM, metadata, full images, cropped images, ROI masks và pathology annotations.

### Quy mô Mass

| Thành phần | Số lượng |
|---|---:|
| Mass annotations | 1.696 |
| Full images duy nhất | 1.592 |
| Patient ID | 892 |
| Train annotations | 1.054 |
| Validation annotations | 264 |
| Test annotations | 378 |

Việc chia tập được thực hiện theo Patient ID để hạn chế rò rỉ giữa Train, Validation và Test. Tập Test được giữ riêng cho đánh giá cuối cùng. Trong cấu hình Web Demo đã kiểm tra, tập Test có 361 ảnh, 378 annotations và 201 bệnh nhân.

Dữ liệu ảnh CBIS-DDSM không được lưu trong repository. Người dùng cần tự tải dữ liệu từ TCIA và tuân thủ điều khoản sử dụng, trích dẫn của nguồn dữ liệu.

## 4. Quy trình và notebooks

| Notebook | Nội dung |
|---|---|
| 01 | Kiểm kê dữ liệu (Data Inventory) |
| 02 | Kiểm định chất lượng và liên kết dữ liệu |
| 03 | Xây dựng cấu trúc dữ liệu tổn thương |
| 04 | Phân tích dữ liệu và xác định phạm vi nghiên cứu |
| 05 | Xây dựng Mass Experimental Dataset |
| 06 | Tiền xử lý ảnh và xây dựng Detection Labels |
| 07 | Thiết kế mô hình và chiến lược thực nghiệm |
| 08 | Huấn luyện và tối ưu mô hình |
| 09 | Đánh giá mô hình và phân tích lỗi |
| 10 | Trực quan hóa nghiên cứu và trình bày kết quả |
| 11 | Phát triển Web Demo |

Các notebook ghi lại quy trình xử lý, cấu hình, thực nghiệm, đánh giá và trực quan hóa. Số liệu báo cáo chính thức cần được đối chiếu trực tiếp với output và báo cáo sinh ra từ các notebook tương ứng.

## 5. Web Demo

Ứng dụng được xây dựng bằng Streamlit, trình diễn quy trình phát hiện Mass bằng YOLOv5n và phân loại bằng InceptionV3.

Các chức năng chính:
- Chọn ảnh từ danh sách ảnh Test hoặc tải ảnh lên.
- Hiển thị ảnh đầu vào và các vùng Mass được mô hình phát hiện.
- Hiển thị kết quả BENIGN/MALIGNANT cùng xác suất dự đoán.
- Với ảnh Test có Ground Truth, hiển thị đối chiếu định vị và nhãn.
- Với ảnh tải lên không có Ground Truth xác minh, chỉ hiển thị kết quả dự đoán; không tự tạo nhãn thật.

Web Demo phục vụ minh họa và kiểm tra mô hình, không đưa ra kết luận chẩn đoán y khoa.

## 6. Cấu trúc repository

```text
Breast_Cancer_CBIS-DDSM/
├── Data/
│   ├── metadata/              # Metadata được quản lý theo chính sách chia sẻ
│   ├── rawdata/               # Dữ liệu gốc — không đưa lên Git
│   └── processed/             # Dữ liệu xử lý — không đưa lên Git
├── notebooks/
│   ├── 01_...ipynb
│   ├── ...
│   ├── 08_model_training_and_optimization.ipynb
│   ├── 09_model_evaluation_and_error_analysis.ipynb
│   ├── 10_Research_Visualization_and_Results_Presentation.ipynb
│   └── 11_Web_Demo_Development.ipynb
├── WebDemo/
│   ├── app.py
│   ├── app/
│   │   └── utils/
│   ├── assets/
│   ├── config/
│   └── reports/
├── external/
│   └── yolov5/                # Clone YOLOv5 theo commit được ghim
├── environment.yml
├── requirements.txt
└── README.md
```

Tên và sự hiện diện của một số thư mục dữ liệu phụ thuộc vào việc người dùng đã tải và chuẩn bị dataset ở máy cục bộ hay chưa. Các thư mục dữ liệu lớn và model checkpoints được loại khỏi Git.

## 7. Môi trường

Khuyến nghị Python 3.11 và Conda.

### Tạo môi trường bằng Conda

```bash
conda env create -f environment.yml
conda activate cbis-thesis
python -m ipykernel install --user --name cbis-thesis --display-name "Python (cbis-thesis)"
```

### Hoặc cài bằng pip

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**PyTorch/CUDA:** phiên bản PyTorch có thể cần điều chỉnh theo hệ điều hành, GPU và CUDA runtime. Nếu cần CUDA, hãy cài đúng wheel theo hướng dẫn chính thức tại [PyTorch — Get Started](https://pytorch.org/get-started/locally/). Không nên xem CUDA runtime hiển thị trong máy là bảo đảm rằng mọi môi trường Python đều dùng cùng một bản CUDA.

## 8. YOLOv5 dependency

Mã nguồn YOLOv5 upstream được quản lý riêng và không nên lồng nguyên thư mục `.git` của repository khác vào Git project này. Phiên bản sử dụng trong môi trường phát triển được ghim tại commit:

```text
915bbf294bb74c859f0b41f1c23bc395014ea679
```

Clone và checkout đúng phiên bản:

```bash
git clone https://github.com/ultralytics/yolov5.git external/yolov5
git -C external/yolov5 checkout 915bbf294bb74c859f0b41f1c23bc395014ea679
```

Cài các dependency bổ sung của YOLOv5 theo `external/yolov5/requirements.txt` nếu môi trường chưa có.

## 9. Chạy Web Demo

Sau khi đã chuẩn bị dữ liệu, checkpoint và YOLOv5 source theo cấu hình đường dẫn trong ứng dụng:

```bash
streamlit run WebDemo/app.py
```

Các checkpoint huấn luyện không được phân phối trong repository. Người chạy cần đặt checkpoint đúng vị trí mà cấu hình Web Demo yêu cầu hoặc điều chỉnh cấu hình cục bộ tương ứng. Không tải checkpoint từ nguồn không xác minh.

## 10. Đánh giá

Hai giai đoạn được đánh giá riêng và trong quy trình kết hợp:

- **Detection:** Precision, Recall, IoU, mAP@50 và mAP@50–95.
- **Classification:** Accuracy, Precision, Recall, F1-score, ROC-AUC và Confusion Matrix.
- **Pipeline:** đánh giá tác động của Bounding Box dự đoán so với Ground Truth crop đến kết quả phân loại.

Kết quả, biểu đồ và phân tích lỗi chi tiết được lưu trong Notebook 09–10 và các báo cáo thực nghiệm tương ứng. Khi trích dẫn số liệu trong báo cáo khóa luận, cần ghi rõ tập dữ liệu, ngưỡng, cách ghép cặp và cấu hình thí nghiệm.

## 11. Giới hạn

- Phạm vi mô hình chính tập trung vào Mass; không khẳng định mô hình xử lý đầy đủ mọi dạng tổn thương tuyến vú.
- Dự đoán không thay thế chẩn đoán chuyên môn.
- Dự đoán không ghép được với Ground Truth theo ngưỡng IoU không mặc nhiên được xác nhận là tổn thương giả về mặt lâm sàng.
- Hiệu năng trên CBIS-DDSM không tự động khái quát sang cơ sở dữ liệu, thiết bị chụp hoặc quần thể bệnh nhân khác.
- Ảnh upload không có Ground Truth xác minh chỉ được trình diễn kết quả dự đoán.

## 12. Tài liệu tham khảo và nguồn dữ liệu

Sawyer-Lee, R., Gimenez, F., Hoogi, A., & Rubin, D. (2016). *A curated mammography data set for use in computer-aided detection and diagnosis research.*

The Cancer Imaging Archive (TCIA): [CBIS-DDSM collection](https://www.cancerimagingarchive.net/collection/cbis-ddsm/).

DOI: [10.7937/K9/TCIA.2016.7O02S9CY](https://doi.org/10.7937/K9/TCIA.2016.7O02S9CY).

Người sử dụng dữ liệu cần tuân thủ chính sách, hạn chế và yêu cầu trích dẫn của TCIA.

---

**Khóa luận tốt nghiệp · Khoa học dữ liệu · 2026**
