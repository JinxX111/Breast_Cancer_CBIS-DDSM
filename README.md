# Xây dựng mô hình học sâu phát hiện và định vị tổn thương trên ảnh X-quang tuyến vú

## Giới thiệu

Khóa luận tập trung nghiên cứu và xây dựng phương pháp học sâu nhằm phát hiện và định vị tổn thương trên ảnh X-quang tuyến vú, sử dụng bộ dữ liệu **CBIS-DDSM** (*Curated Breast Imaging Subset of DDSM*).

Nghiên cứu hướng đến việc khai thác thông tin hình ảnh, annotation và ROI Mask để xây dựng dữ liệu phục vụ bài toán phát hiện, định vị tổn thương. Đồng thời, khảo sát các nhãn pathology nhằm đánh giá khả năng mở rộng sang bài toán phân loại tổn thương lành tính và ác tính.

Phạm vi nghiên cứu và phương pháp thực nghiệm sẽ được xác định dựa trên kết quả khảo sát dữ liệu và đánh giá tính khả thi của nhãn định vị.

## Dataset

**CBIS-DDSM** — Curated Breast Imaging Subset of DDSM, được lưu trữ tại The Cancer Imaging Archive (TCIA).

Dữ liệu nghiên cứu bao gồm:
- Ảnh X-quang tuyến vú (DICOM).
- Metadata mô tả tổn thương.
- Annotation cho hai nhóm Mass và Calcification.
- Các ảnh vùng tổn thương (Cropped Image).
- ROI Mask phục vụ khảo sát và xây dựng nhãn định vị.
- Thông tin pathology và các thuộc tính mô tả tổn thương.

Repository sử dụng duy nhất CBIS-DDSM cho khóa luận này, không kết hợp VinDr-Mammo.

## Tiến độ dự án

| Thành phần | Nội dung | Trạng thái |
|---|---|---|
| Notebook 01 — Data Inventory | Kiểm kê dữ liệu, cấu trúc và quy mô dataset | Hoàn thành |
| Notebook 02 — Data Quality & Linkage | Kiểm tra chất lượng metadata, liên kết ảnh và tính nhất quán dữ liệu | Hoàn thành |
| Notebook 03 — Lesion Dataset Construction | Xây dựng Candidate Master, Annotation Mapping, Image Mapping và ROI Mapping | Hoàn thành |
| Notebook 04 — EDA and Research Scope | Khảo sát phân bố dữ liệu, pathology, đặc điểm ảnh và xác định phạm vi nghiên cứu | Đang thực hiện |

### Một số kết quả xây dựng dữ liệu

Từ 4 bảng annotation Mass/Calcification của tập Train/Test:

| Chỉ tiêu | Số lượng |
|---|---:|
| Bệnh nhân duy nhất | 1.566 |
| Annotation | 3.568 |
| Candidate records | 1.989 |
| Review groups | 140 |
| Quan hệ Annotation–Image | 7.136 |
| ROI mappings | 3.568 |

Phân bố annotation theo loại tổn thương:

| Loại tổn thương | Số annotation |
|---|---:|
| Calcification | 1.872 |
| Mass | 1.696 |

Kết quả kiểm định tổng thể trong Notebook 03: **54/54 phép kiểm tra đạt**.

Lưu ý: Candidate là các bản ghi ứng viên được xây dựng từ annotation và quy tắc ghép CC–MLO, chưa phải số lượng tổn thương độc lập đã được xác minh lâm sàng.

## Cấu trúc dự án

```text
Breast-Cancer-CBIS-DDSM/
│
├── notebooks/
│   ├── 01_data_inventory.ipynb
│   ├── 02_data_quality_and_linkage.ipynb
│   ├── 03_lesion_dataset_construction.ipynb
│   └── 04_eda_and_research_scope.ipynb
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
└── README.md
```

**Lưu ý về dữ liệu:**

- `Data/rawdata/`: lưu trữ dữ liệu DICOM gốc.
- `Data/metadata/`: lưu các bảng metadata và annotation.
- `Data/processed/`: lưu dữ liệu đã xử lý và các bảng mapping được tạo trong quá trình nghiên cứu.

Các thư mục dữ liệu lớn và dữ liệu xử lý không được đưa lên GitHub mặc định. Repository tập trung lưu mã nguồn, notebook và tài liệu nghiên cứu.

## Nguồn dữ liệu

Sawyer-Lee, R., Gimenez, F., Hoogi, A., & Rubin, D. (2016). *A curated mammography data set for use in computer-aided detection and diagnosis research.*

The Cancer Imaging Archive (TCIA).

DOI: [https://doi.org/10.7937/K9/TCIA.2016.7O02S9CY](https://doi.org/10.7937/K9/TCIA.2016.7O02S9CY)

Người sử dụng dữ liệu cần tuân thủ [Chính sách và Hạn chế Sử dụng Dữ liệu của TCIA](https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/).

## Môi trường phát triển

- Python
- Jupyter Notebook
- Visual Studio Code
- Conda Environment

Các thư viện và phiên bản môi trường được quản lý thông qua `environment.yml` và `requirements.txt`.

## Lưu ý

Repository này lưu mã nguồn, notebook, cấu hình môi trường và tài liệu nghiên cứu.

Không lưu trữ ảnh DICOM gốc của CBIS-DDSM hoặc các dữ liệu lớn đã xử lý trên GitHub mặc định.

Các kết quả thống kê và thực nghiệm trong repository cần được cập nhật theo tiến độ thực tế của khóa luận.
