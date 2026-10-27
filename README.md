# Xây dựng mô hình học sâu phát hiện và định vị tổn thương trên ảnh X-quang tuyến vú

## Giới thiệu

Khóa luận tập trung nghiên cứu phương pháp học sâu để phát hiện, định vị tổn thương và phân loại tổn thương lành tính – ác tính trên ảnh X-quang tuyến vú, sử dụng bộ dữ liệu CBIS-DDSM.

## Tiến độ dự án

- Notebook 01 — Data Inventory: kiểm kê dữ liệu.
- Notebook 02 — Data Quality & Linkage: kiểm tra chất lượng metadata và tính nhất quán UID.
- Notebook 03 — Lesion Dataset Construction: chưa triển khai.

## Cấu trúc hiện tại

- `notebooks/`: các notebook phân tích dữ liệu.
- `Data/metadata/`: các bảng CSV mô tả tổn thương.
- `Data/rawdata/`: dữ liệu gốc, không được đưa lên repository.
- `Data/processed/`: dữ liệu xử lý, không đưa lên repository mặc định.

## Nguồn dữ liệu

Sawyer-Lee, R., Gimenez, F., Hoogi, A., & Rubin, D. (2016). *A curated mammography data set for use in computer-aided detection and diagnosis research.* The Cancer Imaging Archive.

DOI: https://doi.org/10.7937/K9/TCIA.2016.7O02S9CY

Người sử dụng dữ liệu cần tuân thủ [Chính sách và Hạn chế Sử dụng Dữ liệu của TCIA](https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/).

## Lưu ý

Repository này lưu mã nguồn, notebook và tài liệu nghiên cứu. Không lưu trữ ảnh DICOM của CBIS-DDSM.
