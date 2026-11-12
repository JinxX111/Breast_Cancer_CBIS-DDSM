# Xây dựng mô hình học sâu phát hiện và định vị tổn thương có chọn lọc lành tính và ác tính trên ảnh X-quang tuyến vú

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Dataset](https://img.shields.io/badge/Dataset-CBIS--DDSM-brightgreen)
![Task](https://img.shields.io/badge/Task-Detection%20%26%20Localization-orange)
![Status](https://img.shields.io/badge/Status-Model%20Design%20Completed-success)

---

## 1. Giới thiệu

Khóa luận tập trung nghiên cứu và xây dựng mô hình học sâu nhằm phát hiện, định vị và phân loại tổn thương lành tính, ác tính trên ảnh X-quang tuyến vú.

Nghiên cứu sử dụng bộ dữ liệu **CBIS-DDSM (Curated Breast Imaging Subset of DDSM)**. Dữ liệu ảnh DICOM, metadata, annotation và ROI Mask được khai thác để xây dựng quy trình xử lý, kiểm định và chuẩn bị nhãn phục vụ bài toán phát hiện, định vị tổn thương.

Sau khi khảo sát hai nhóm tổn thương Mass và Calcification, nghiên cứu lựa chọn **Mass** làm đối tượng thực nghiệm chính trong giai đoạn hiện tại.

## 2. Dữ liệu nghiên cứu

**CBIS-DDSM – Curated Breast Imaging Subset of DDSM**

Nguồn dữ liệu: [The Cancer Imaging Archive (TCIA)](https://www.cancerimagingarchive.net/collection/cbis-ddsm/)

Các thành phần dữ liệu được sử dụng:

- Ảnh X-quang tuyến vú định dạng DICOM.
- Metadata mô tả thông tin ảnh và tổn thương.
- Annotation thuộc hai nhóm Mass và Calcification.
- Full Image, Cropped Image và ROI Mask.
- Thông tin pathology và các thuộc tính hình thái tổn thương.

### Quy mô tập dữ liệu Mass

| Thành phần | Số lượng |
|:--|--:|
| Mass Annotations | 1.696 |
| Full Images duy nhất | 1.592 |
| Patient ID | 892 |
| Train | 1.054 annotations |
| Validation | 264 annotations |
| Test | 378 annotations |

Dữ liệu được chia theo Patient ID nhằm hạn chế rò rỉ dữ liệu giữa các tập. Tập Test nguồn được giữ nguyên trong quá trình xây dựng Train và Validation.

## 3. Mục tiêu nghiên cứu

1. Khảo sát và kiểm định cấu trúc dữ liệu CBIS-DDSM.
2. Xây dựng tập dữ liệu thực nghiệm Mass có khả năng truy xuất từ annotation đến ảnh và ROI Mask.
3. Tiền xử lý ảnh DICOM và xây dựng Bounding Box phục vụ phát hiện, định vị tổn thương.
4. Nghiên cứu mô hình học sâu phát hiện và định vị Mass.
5. Khảo sát khả năng phân loại tổn thương thành BENIGN và MALIGNANT.
6. Đánh giá hiệu quả từng giai đoạn và toàn bộ quy trình hai giai đoạn.

## 4. Quy trình thực hiện

| Notebook | Nội dung | Trạng thái |
|:--|:--|:--:|
| 01 | Kiểm kê dữ liệu (Data Inventory) | Hoàn thành |
| 02 | Kiểm định chất lượng và liên kết dữ liệu | Hoàn thành |
| 03 | Xây dựng cấu trúc dữ liệu tổn thương | Hoàn thành |
| 04 | Phân tích dữ liệu và xác định phạm vi nghiên cứu | Hoàn thành |
| 05 | Xây dựng Mass Experimental Dataset | Hoàn thành |
| 06 | Tiền xử lý ảnh và xây dựng Detection Labels | Hoàn thành |
| 07 | Thiết kế mô hình và chiến lược thực nghiệm | Hoàn thành |
| 08 | Thiết lập huấn luyện và đánh giá tính khả thi | Tiếp theo |

Chi tiết quá trình xử lý, phân tích và kiểm định được trình bày trong các notebook tương ứng.

## 5. Kết quả chính

### 5.1. Xây dựng dữ liệu thực nghiệm

- Hoàn thiện 1.696 Mass Annotations.
- Liên kết với 1.592 ảnh Full Image duy nhất.
- Chuẩn hóa thành công 1.696 ROI Masks.
- Xây dựng Bounding Box và Detection Labels cho 1.696 annotations.
- Hoàn thiện ba tập Train, Validation và Test theo Patient ID.
- Không phát hiện Patient ID giao nhau giữa các tập dữ liệu.

### 5.2. Tiền xử lý và kiểm định

- Kiểm tra khả năng đọc metadata và giải mã Pixel Data của toàn bộ 1.592 DICOM duy nhất.
- Khảo sát và lựa chọn phương pháp chuẩn hóa cường độ ảnh P1–P99.
- 78 ROI Masks cần resize được xử lý bằng Nearest Neighbor và kiểm tra overlay trực quan.
- Kiểm tra ngẫu nhiên 100 ảnh cùng Bounding Box tương ứng.
- Notebook 06 đạt **21/21 tiêu chí PASS** trong báo cáo kiểm định chất lượng.

### 5.3. Thiết kế thực nghiệm

- Hoàn thành thiết kế Two-stage Pipeline.
- Xác định YOLOv5n làm kiến trúc ứng viên cho Detection.
- Xác định VGG16, ResNet50 và InceptionV3 cho Classification.
- Xây dựng các phương án đầu vào Full Image và Patch.
- Hoàn thành các bảng thiết kế pipeline, phân chia dữ liệu và tiêu chí đánh giá trong Notebook 07.

**Lưu ý:** Các kết quả trên phản ánh giai đoạn xây dựng dữ liệu và thiết kế thực nghiệm. Mô hình chưa được huấn luyện và chưa có kết quả đánh giá hiệu năng.

## 6. Kiến trúc mô hình dự kiến

Nghiên cứu lựa chọn hướng tiếp cận **Two-stage Pipeline**, trong đó nhiệm vụ phát hiện và phân loại được thực hiện ở hai giai đoạn riêng biệt.

### Giai đoạn 1 – Phát hiện và định vị tổn thương

**YOLOv5n**

- Đầu vào: ảnh Full Image hoặc các Patch được xây dựng từ ảnh gốc.
- Nhiệm vụ: phát hiện và định vị vùng tổn thương Mass.
- Đầu ra: Bounding Box và độ tin cậy dự đoán.

### Giai đoạn 2 – Phân loại pathology

Ba kiến trúc CNN được đưa vào so sánh:

| Kiến trúc | Nhiệm vụ |
|:--|:--|
| VGG16 | Phân loại BENIGN / MALIGNANT |
| ResNet50 | Phân loại BENIGN / MALIGNANT |
| InceptionV3 | Phân loại BENIGN / MALIGNANT |

Đầu vào là vùng tổn thương được trích xuất từ Bounding Box. Thực nghiệm dự kiến đánh giá cả trường hợp sử dụng Ground Truth Bounding Box và Predicted Bounding Box để khảo sát ảnh hưởng của sai số phát hiện đến kết quả phân loại.

### Quy ước nhãn phân loại

Dữ liệu gốc có ba nhãn pathology:

- `BENIGN`
- `BENIGN_WITHOUT_CALLBACK`
- `MALIGNANT`

Đối với thí nghiệm phân loại nhị phân:

| Nhãn gốc | Nhãn thực nghiệm |
|:--|:--|
| BENIGN | BENIGN |
| BENIGN_WITHOUT_CALLBACK | BENIGN |
| MALIGNANT | MALIGNANT |

Việc ánh xạ chỉ áp dụng cho thí nghiệm nhị phân; nhãn pathology gốc vẫn được bảo toàn.

### Chiến lược đầu vào dự kiến

| Phương án | Vai trò |
|:--|:--|
| Full Image 640 | Baseline |
| Full Image 1024 | Ưu tiên khảo sát |
| Full Image 1280 | Khảo sát có điều kiện |
| Patch 1024, overlap 20% | Phương án so sánh |
| Patch 1280, overlap 20% | Phương án khảo sát bổ sung |

### Tiêu chí đánh giá

- **Detection:** Precision, Recall, IoU, mAP@50 và mAP@50–95.
- **Classification:** Accuracy, Precision, Recall, F1-score, ROC-AUC và Confusion Matrix.
- **Two-stage Pipeline:** Đánh giá ảnh hưởng của sai số Bounding Box đến kết quả phân loại ở giai đoạn tiếp theo.

## 7. Môi trường phát triển

| Thành phần | Cấu hình |
|:--|:--|
| Hệ điều hành | Windows |
| Python | 3.11.18 |
| PyTorch | 2.5.1+cu121 |
| CUDA Runtime | 12.1 |
| GPU | NVIDIA GeForce RTX 4050 Laptop GPU |
| VRAM | 6 GB |
| Công cụ | VS Code, Jupyter Notebook, Conda |

## 8. Định hướng tiếp theo

1. Thiết lập môi trường huấn luyện và kiểm tra khả năng thực thi mô hình trên phần cứng hiện có.
2. Thử nghiệm YOLOv5n với các phương án đầu vào đã đề xuất.
3. Huấn luyện và so sánh VGG16, ResNet50 và InceptionV3.
4. Đánh giá riêng Detection, Classification và toàn bộ Two-stage Pipeline.
5. Phân tích kết quả, đối chiếu với các nghiên cứu liên quan và xem xét xây dựng ứng dụng minh họa.

## 9. Ghi chú nghiên cứu

- Phạm vi thực nghiệm hiện tại tập trung vào Mass.
- Các kiến trúc YOLOv5n, VGG16, ResNet50 và InceptionV3 là lựa chọn thiết kế, chưa phải mô hình đã huấn luyện.
- 78 ROI Masks được resize đã được kiểm tra overlay trực quan. 1.618 ROI Masks giữ nguyên kích thước chưa được kiểm tra overlay riêng từng trường hợp.
- Việc kiểm tra kích thước và sự tương ứng giữa Bounding Box với ROI Mask không tự động chứng minh tính chính xác lâm sàng của Ground Truth.
- Việc chia dữ liệu theo Patient ID không đảm bảo độc lập tuyệt đối ở cấp người tham gia nghiên cứu.
- Kết quả nghiên cứu phục vụ mục đích học thuật, không thay thế chẩn đoán y khoa.

## 10. Nguồn dữ liệu và tài liệu tham khảo

**Sawyer-Lee, R., Gimenez, F., Hoogi, A., & Rubin, D. (2016).** *A curated mammography data set for use in computer-aided detection and diagnosis research.*

**The Cancer Imaging Archive (TCIA).**

**DOI:** [https://doi.org/10.7937/K9/TCIA.2016.7O02S9CY](https://doi.org/10.7937/K9/TCIA.2016.7O02S9CY)

> [!WARNING]
> Người sử dụng dữ liệu cần tuân thủ **Chính sách và Hạn chế Sử dụng Dữ liệu** của TCIA. Việc trích dẫn bộ dữ liệu CBIS-DDSM theo yêu cầu của TCIA là bắt buộc.

---

**Khóa luận tốt nghiệp · Khoa học dữ liệu · 2026**
