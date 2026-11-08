# Xây dựng mô hình học sâu phát hiện và định vị tổn thương trên ảnh X-quang tuyến vú

## 1. Giới thiệu
Khóa luận tập trung nghiên cứu và xây dựng phương pháp học sâu nhằm phát hiện và định vị tổn thương trên ảnh X-quang tuyến vú (mammography), sử dụng bộ dữ liệu **CBIS-DDSM** (Curated Breast Imaging Subset of DDSM).

Nghiên cứu hướng đến việc khai thác ảnh DICOM, metadata, annotation và ROI Mask để xây dựng dữ liệu thực nghiệm phục vụ bài toán phát hiện và định vị tổn thương. Thông tin pathology cũng được khảo sát nhằm hỗ trợ phân tích đặc điểm tổn thương và xem xét khả năng mở rộng sang bài toán phân loại lành tính, ác tính.

Phạm vi thực nghiệm được triển khai theo từng giai đoạn, bắt đầu từ kiểm kê và kiểm định dữ liệu, xây dựng tập dữ liệu tổn thương **Mass**, sau đó tiếp tục nghiên cứu tiền xử lý ảnh, xây dựng Ground Truth và phát triển mô hình học sâu.

---

## 2. Dataset
* **Nguồn:** CBIS-DDSM — Curated Breast Imaging Subset of DDSM, được lưu trữ tại The Cancer Imaging Archive (TCIA).
* **Thành phần dữ liệu:**
  * Ảnh X-quang tuyến vú định dạng DICOM.
  * Metadata mô tả bệnh nhân, bên ngực, góc chụp và đặc điểm tổn thương.
  * Annotation thuộc hai nhóm tổn thương: **Mass** và **Calcification**.
  * Ảnh Cropped Image chứa vùng tổn thương.
  * ROI Mask phục vụ xác định vùng tổn thương.
  * Thông tin pathology và các thuộc tính mô tả tổn thương.
* **Lưu ý:** Repository sử dụng duy nhất CBIS-DDSM cho khóa luận này, không kết hợp VinDr-Mammo.

---

## 3. Tiến độ dự án

| Thành phần | Nội dung | Trạng thái |
| :--- | :--- | :--- |
| **Notebook 01** — Data Inventory | Kiểm kê dữ liệu, cấu trúc thư mục, quy mô và thành phần dataset | Hoàn thành |
| **Notebook 02** — Data Quality & Linkage | Kiểm tra chất lượng metadata, đường dẫn và liên kết giữa metadata với ảnh DICOM | Hoàn thành |
| **Notebook 03** — Lesion Dataset Construction | Xây dựng Candidate Master, Annotation Mapping, Image Mapping và ROI Mapping | Hoàn thành |
| **Notebook 04** — EDA and Research Scope | Khảo sát phân bố dữ liệu, pathology, đặc điểm ảnh và tính khả thi của phạm vi nghiên cứu | Đang hoàn thiện |
| **Notebook 05** — Mass Experimental Dataset | Xây dựng tập dữ liệu Mass, chuẩn hóa ROI Mask, chia Train/Validation/Test và kiểm tra tính toàn vẹn | Hoàn thành |

---

## 4. Các công đoạn xây dựng dữ liệu

### 4.1. Kiểm kê và kiểm định dữ liệu
* Kiểm kê cấu trúc thư mục, metadata và dữ liệu DICOM.
* Thống kê số lượng ảnh, bệnh nhân, annotation và các thành phần liên quan.
* Kiểm tra chất lượng metadata, giá trị thiếu và tính nhất quán giữa các bảng.
* Khảo sát khả năng liên kết annotation với ảnh Full Image, Cropped Image và ROI Mask.
* Kiểm tra khả năng truy xuất ảnh thông qua thông tin định danh DICOM.

### 4.2. Xây dựng cấu trúc Annotation và Image Mapping
Từ bốn bảng annotation Mass/Calcification thuộc Train/Test, quá trình xây dựng dữ liệu thu được:

| Chỉ tiêu | Số lượng |
| :--- | :--- |
| Patient ID duy nhất theo metadata | 1.566 |
| Annotation | 3.568 |
| Candidate records | 1.989 |
| Review groups | 140 |
| Quan hệ Annotation – Image | 7.136 |
| ROI mappings | 3.568 |

**Phân bố annotation theo loại tổn thương:**
* **Calcification:** 1.872
* **Mass:** 1.696
* **Tổng:** 3.568

> **Lưu ý:** Candidate là các bản ghi ứng viên được xây dựng từ annotation và quy tắc liên kết CC–MLO, không đồng nghĩa với số lượng tổn thương độc lập đã được xác minh lâm sàng. Số lượng Patient ID trong metadata cũng không nên được diễn giải trực tiếp thành số người tham gia nghiên cứu độc lập. Kết quả kiểm định tổng thể trong Notebook 03: **54/54 phép kiểm tra đạt yêu cầu**.

### 4.3. Xây dựng Mass Experimental Dataset
Notebook 05 tập trung xây dựng tập dữ liệu thực nghiệm cho nhóm tổn thương **Mass**, gồm các công đoạn:
* Tổng hợp và chuẩn hóa 1.696 Mass Annotations từ metadata nguồn.
* Kiểm tra quan hệ giữa Patient ID, annotation và các ảnh Full Image tương ứng.
* Đối chiếu Image Mapping và ROI Mapping để xác định đường dẫn ảnh có thể truy xuất.
* Khảo sát khả năng ánh xạ ROI Mask lên Full Image và chuẩn hóa kích thước ROI Mask về kích thước Full Image.
* Chia dữ liệu theo Patient ID, giữ nguyên tập Test nguồn và tạo tập Validation từ tập Train nguồn.
* Kiểm tra trùng lặp Annotation ID, khả năng truy xuất tệp, chất lượng mask và rò rỉ Patient ID giữa các tập.
* Xuất Mass Experimental Dataset cùng các bảng thống kê và báo cáo kiểm định.

**Kết quả Mass Experimental Dataset:**
* Mass Annotations: **1.696**
* Patient ID: **892**
* Full Image truy xuất được: **1.696**
* Normalized ROI Mask: **1.696**

**Phân chia dữ liệu:**

| Tập dữ liệu | Annotations | Patients |
| :--- | :--- | :--- |
| **Train** | 1.054 | 552 |
| **Validation** | 264 | 139 |
| **Test** | 378 | 201 |
| **Tổng** | **1.696** | **892** |

**Quá trình chuẩn hóa ROI Mask:**
* Giữ nguyên kích thước (Identity): 1.618
* Resize bằng Nearest Neighbor: 78
* **Tổng:** 1.696

*Trong đó, 78 mask được resize đã được kiểm tra overlay trực quan và xác nhận vị trí vùng tổn thương phù hợp. Với 1.618 mask giữ nguyên kích thước, việc trùng khớp kích thước ảnh mới là điều kiện ứng viên; chưa thực hiện xác nhận overlay riêng cho từng trường hợp.*

**Kết quả kiểm định cuối Notebook 05:**
* 1.696 Annotation ID duy nhất, không có bản ghi trùng lặp.
* 1.696/1.696 Full Image tồn tại và truy xuất được.
* 1.696/1.696 Normalized ROI Mask tồn tại và truy xuất được, không có mask rỗng.
* Không phát hiện Patient ID giao nhau giữa Train, Validation và Test.
* Giữ nguyên 378 Annotation ID thuộc Test nguồn.
* **10/10 tiêu chí trong Integrity Report đạt PASS.**
* Các kết quả được xuất thành bốn tệp CSV: `mass_experimental_dataset.csv`, `mass_split_summary.csv`, `mass_pathology_distribution.csv` và `mass_integrity_report.csv`.

---

## 5. Cấu trúc dự án

```text
Breast-Cancer-CBIS-DDSM/
│
├── notebooks/
│   ├── 01_data_inventory.ipynb
│   ├── 02_data_quality_and_linkage.ipynb
│   ├── 03_lesion_dataset_construction.ipynb
│   ├── 04_eda_and_research_scope.ipynb
│   └── 05_mass_experimental_dataset.ipynb
│
├── Data/
│   ├── metadata/
│   ├── rawdata/
│   └── processed/
│
├── docs/
├── figures/
├── models/
├── results/
├── src/
├── tests/
│
├── environment.yml
├── requirements.txt
├── .gitignore
└── README.md
