## Xây dựng mô hình học sâu phát hiện và định vị tổn thương trên ảnh X-quang tuyến vú

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Dataset](https://img.shields.io/badge/Dataset-CBIS--DDSM-brightgreen)
![Task](https://img.shields.io/badge/Task-Detection%20%26%20Localization-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 1. Giới thiệu

Khóa luận tập trung nghiên cứu và xây dựng phương pháp học sâu nhằm phát hiện và định vị tổn thương trên ảnh X-quang tuyến vú, sử dụng bộ dữ liệu **CBIS-DDSM** (*Curated Breast Imaging Subset of DDSM*).

Nghiên cứu hướng đến việc khai thác ảnh DICOM, metadata, annotation và ROI Mask để xây dựng dữ liệu thực nghiệm phục vụ bài toán phát hiện và định vị tổn thương. Thông tin `pathology` cũng được khảo sát nhằm hỗ trợ phân tích đặc điểm tổn thương và xem xét khả năng mở rộng sang bài toán phân loại lành tính, ác tính.

Sau giai đoạn khảo sát hai nhóm tổn thương **Mass** và **Calcification**, nghiên cứu lựa chọn **Mass** làm đối tượng thực nghiệm chính trong giai đoạn hiện tại. Việc tập trung vào Mass giúp xây dựng và kiểm chứng quy trình liên kết ảnh, chuẩn hóa ROI Mask và chuẩn bị Ground Truth cho bài toán định vị tổn thương trước khi phát triển mô hình học sâu.

---

## 2. Dataset

**CBIS-DDSM** — *Curated Breast Imaging Subset of DDSM*, được lưu trữ tại *The Cancer Imaging Archive* (TCIA).

Dữ liệu nghiên cứu bao gồm:
* Ảnh X-quang tuyến vú định dạng **DICOM**.
* **Metadata** mô tả bệnh nhân, bên ngực, góc chụp và đặc điểm tổn thương.
* **Annotation** thuộc hai nhóm tổn thương Mass và Calcification.
* Ảnh **Cropped Image** chứa vùng tổn thương.
* **ROI Mask** phục vụ xác định vùng tổn thương.
* Thông tin **pathology** và các thuộc tính mô tả tổn thương.

> [!NOTE]
> Repository sử dụng duy nhất CBIS-DDSM cho khóa luận này, không kết hợp VinDr-Mammo.

---

## 3. Phạm vi nghiên cứu: Lựa chọn Mass

CBIS-DDSM cung cấp hai nhóm annotation chính là **Mass** và **Calcification**. Cả hai nhóm đều được kiểm kê, khảo sát và xây dựng cấu trúc liên kết dữ liệu trong các giai đoạn đầu.

Sau khi đánh giá cấu trúc metadata, khả năng truy xuất ảnh và ROI Mask, nghiên cứu lựa chọn **Mass** làm nhóm tổn thương chính để triển khai thực nghiệm trước.

### Các lý do lựa chọn:
* **Tập trung nguồn lực:** Tập trung vào một nhóm tổn thương để hoàn thiện quy trình thực nghiệm.
* **Khai thác ROI Mask:** Khảo sát vùng tổn thương và xây dựng nhãn định vị.
* **Định hướng Pipeline:** Phù hợp với định hướng phát triển pipeline phát hiện và định vị tổn thương trên ảnh Full Image.
* **Cơ sở đánh giá:** Tạo cơ sở đánh giá chất lượng dữ liệu, khả năng xây dựng Ground Truth và tính khả thi của mô hình học sâu.

> [!IMPORTANT]
> Calcification vẫn nằm trong phạm vi khảo sát dữ liệu ban đầu, nhưng chưa được đưa vào `Mass Experimental Dataset`. Việc mở rộng sang Calcification sẽ được cân nhắc ở giai đoạn tiếp theo tùy theo tiến độ và kết quả thực nghiệm.

---

## 4. Tiến độ dự án

| Thành phần | Nội dung | Trạng thái |
| :--- | :--- | :--- |
| **Notebook 01** — Data Inventory | Kiểm kê dữ liệu, cấu trúc thư mục, quy mô và thành phần dataset | `Hoàn thành` |
| **Notebook 02** — Data Quality & Linkage | Kiểm tra chất lượng metadata, đường dẫn và liên kết giữa metadata với ảnh DICOM | `Hoàn thành` |
| **Notebook 03** — Lesion Dataset Construction | Xây dựng Candidate Master, Annotation Mapping, Image Mapping và ROI Mapping | `Hoàn thành` |
| **Notebook 04** — EDA and Research Scope | Khảo sát phân bố dữ liệu, pathology, đặc điểm ảnh và tính khả thi của phạm vi nghiên cứu | `Đang hoàn thiện` |
| **Notebook 05** — Mass Experimental Dataset | Xây dựng tập dữ liệu Mass, chuẩn hóa ROI Mask, chia Train/Validation/Test và kiểm tra tính toàn vẹn | `Hoàn thành` |

---

## 5. Các công đoạn xây dựng dữ liệu

### 5.1. Kiểm kê và kiểm định dữ liệu
* Kiểm kê cấu trúc thư mục, metadata và dữ liệu DICOM.
* Thống kê số lượng ảnh, bệnh nhân, annotation và các thành phần liên quan.
* Kiểm tra chất lượng metadata, giá trị thiếu và tính nhất quán giữa các bảng.
* Khảo sát khả năng liên kết annotation với ảnh Full Image, Cropped Image và ROI Mask.
* Kiểm tra khả năng truy xuất ảnh thông qua thông tin định danh DICOM.

### 5.2. Xây dựng cấu trúc Annotation và Image Mapping
Từ bốn bảng annotation Mass/Calcification thuộc Train/Test, quá trình xây dựng dữ liệu thu được:

| Chỉ tiêu | Số lượng |
| :--- | :--- |
| **Patient ID** duy nhất theo metadata | `1.566` |
| **Annotation** | `3.568` |
| **Candidate records** | `1.989` |
| **Review groups** | `140` |
| Quan hệ **Annotation – Image** | `7.136` |
| **ROI mappings** | `3.568` |

#### Phân bố annotation theo loại tổn thương:
* **Calcification:** `1.872`
* **Mass:** `1.696`
* **Tổng:** `3.568`

> [!NOTE]
> Candidate là các bản ghi ứng viên được xây dựng từ annotation và quy tắc liên kết CC–MLO, không đồng nghĩa với số lượng tổn thương độc lập đã được xác minh lâm sàng. Số lượng Patient ID trong metadata cũng không nên được diễn giải trực tiếp thành số người tham gia nghiên cứu độc lập. Kết quả kiểm định tổng thể trong Notebook 03: **54/54 phép kiểm tra đạt yêu cầu**.

### 5.3. Xây dựng Mass Experimental Dataset
Notebook 05 tập trung xây dựng tập dữ liệu thực nghiệm cho nhóm tổn thương **Mass**, gồm các công đoạn:
1. Tổng hợp và chuẩn hóa **1.696 Mass Annotations** từ metadata nguồn.
2. Kiểm tra quan hệ giữa Patient ID, annotation và các ảnh Full Image tương ứng.
3. Đối chiếu Image Mapping và ROI Mapping để xác định đường dẫn ảnh có thể truy xuất.
4. Khảo sát khả năng ánh xạ ROI Mask lên Full Image và chuẩn hóa kích thước ROI Mask về kích thước Full Image.
5. Chia dữ liệu theo Patient ID, giữ nguyên tập Test nguồn và tạo tập Validation từ tập Train nguồn.
6. Kiểm tra trùng lặp Annotation ID, khả năng truy xuất tệp, chất lượng mask và rò rỉ Patient ID giữa các tập.
7. Xuất Mass Experimental Dataset cùng các bảng thống kê và báo cáo kiểm định.

### 5.4. Điều chỉnh phương pháp chia dữ liệu
Ban đầu, dữ liệu Train nguồn được chia thành Train và Validation bằng phương pháp `GroupShuffleSplit` theo Patient ID. Kết quả chia ban đầu đảm bảo không có Patient ID giao nhau giữa các tập, nhưng tỷ lệ pathology giữa Train và Validation chưa thực sự cân bằng (đặc biệt nhóm `MALIGNANT` chiếm 46,47% trong Train nhưng lên tới 56,03% trong Validation). 

Do đó, nghiên cứu thực hiện nhiều lần chia ứng viên có kiểm soát, lựa chọn phương án có phân bố pathology giữa Train và Validation gần nhau hơn, đồng thời giữ nguyên các nhóm Patient ID và tập Test nguồn.

#### So sánh số lượng Annotation trước và sau điều chỉnh:
| Dataset | Chia ban đầu | Chia được chọn |
| :--- | :--- | :--- |
| **Train** | `1.061` | `1.054` |
| **Validation** | `257` | `264` |
| **Test** | `378` | `378` |
| **Tổng** | **1.696** | **1.696** |

#### Số lượng Patient ID không thay đổi:
| Dataset | Số Patient ID |
| :--- | :--- |
| **Train** | `552` |
| **Validation** | `139` |
| **Test** | `201` |
| **Tổng** | **892** |

#### So sánh tỷ lệ pathology giữa Train và Validation:
| Pathology | Train ban đầu | Validation ban đầu | Train sau điều chỉnh | Validation sau điều chỉnh |
| :--- | :--- | :--- | :--- | :--- |
| **BENIGN** | 44,67% | 40,08% | 43,93% | 43,18% |
| **BENIGN_WITHOUT_CALLBACK** | 8,86% | 3,89% | 7,87% | 7,95% |
| **MALIGNANT** | 46,47% | 56,03% | 48,20% | 48,86% |

#### Mức chênh lệch tỷ lệ giữa Train và Validation:
| Pathology | Trước điều chỉnh | Sau điều chỉnh |
| :--- | :--- | :--- |
| **BENIGN** | 4,59 điểm % | **0,75 điểm %** |
| **BENIGN_WITHOUT_CALLBACK** | 4,97 điểm % | **0,08 điểm %** |
| **MALIGNANT** | 9,56 điểm % | **0,66 điểm %** |

Phương án được chọn giúp phân bố pathology giữa Train và Validation gần nhau hơn đáng kể. Tập Test nguồn gồm 378 annotations được giữ nguyên, không tham gia quá trình lựa chọn phương án chia Train/Validation.

#### Phân chia cuối cùng được sử dụng trong Mass Experimental Dataset:
| Dataset | Annotations | Patients |
| :--- | :--- | :--- |
| **Train** | `1.054` | `552` |
| **Validation** | `264` | `139` |
| **Test** | `378` | `201` |
| **Tổng** | **1.696** | **892** |

> [!TIP]
> Việc lựa chọn phương án chia dữ liệu dựa trên tỷ lệ pathology ở cấp annotation, đồng thời giữ nguyên nhóm Patient ID. Các bệnh nhân có nhiều annotation hoặc nhiều pathology được giữ trong cùng một tập, không tách annotation của cùng một Patient ID sang các tập khác nhau.

### 5.5. Kết quả chuẩn hóa và kiểm định ROI Mask
| Phương pháp | Số lượng |
| :--- | :--- |
| Giữ nguyên kích thước (`Identity`) | `1.618` |
| Resize bằng `Nearest Neighbor` | `78` |
| **Tổng** | **1.696** |

Trong đó, 78 mask được resize đã được kiểm tra overlay trực quan và xác nhận vị trí vùng tổn thương phù hợp. Với 1.618 mask giữ nguyên kích thước, việc trùng khớp kích thước ảnh mới là điều kiện ứng viên; chưa thực hiện xác nhận overlay riêng cho từng trường hợp.

#### Kết quả kiểm định cuối Notebook 05:
* `1.696` Annotation ID duy nhất, không có bản ghi trùng lặp.
* `1.696/1.696` Full Image tồn tại và truy xuất được.
* `1.696/1.696` Normalized ROI Mask tồn tại và truy xuất được.
* `1.696/1.696` ROI Mask chuẩn hóa thành công.
* Không có mask rỗng.
* Không phát hiện Patient ID giao nhau giữa Train, Validation và Test.
* Giữ nguyên 378 Annotation ID thuộc Test nguồn.
* **10/10 tiêu chí trong Integrity Report đạt PASS (`100%`).**

Các kết quả được xuất thành bốn tệp CSV:
* `mass_experimental_dataset.csv`
* `mass_split_summary.csv`
* `mass_pathology_distribution.csv`
* `mass_integrity_report.csv`

---

## 6. Cấu trúc dự án

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
```
> [!NOTE]
> Tên file Notebook 05 trong cây thư mục cần được điều chỉnh theo tên file thực tế trong repository nếu có khác biệt.

### Quy ước lưu trữ dữ liệu:
* `Data/metadata/`: Metadata và các bảng annotation nguồn.
* `Data/rawdata/`: Ảnh DICOM gốc của CBIS-DDSM.
* `Data/processed/`: Dữ liệu đã xử lý, bảng mapping, mask chuẩn hóa và các kết quả trung gian.
* `notebooks/`: Các notebook thực hiện kiểm kê, kiểm định, phân tích và xây dựng dữ liệu.
* `docs/`: Tài liệu nghiên cứu và ghi chú phương pháp.
* `figures/`: Hình ảnh minh họa, biểu đồ và kết quả trực quan hóa.
* `models/`: Mô hình được huấn luyện và các trọng số.
* `results/`: Kết quả thực nghiệm.

> [!IMPORTANT]
> Các thư mục dữ liệu lớn và dữ liệu xử lý không được đưa lên GitHub mặc định. Repository tập trung lưu mã nguồn, notebook, cấu hình môi trường và tài liệu nghiên cứu.

---

## 6. Nguồn dữ liệu và tài liệu tham khảo

* **Sawyer-Lee, R., Gimenez, F., Hoogi, A., & Rubin, D. (2016).** *A curated mammography data set for use in computer-aided detection and diagnosis research.*
* **The Cancer Imaging Archive (TCIA).** 
* **DOI:** [https://doi.org/10.7937/K9/TCIA.2016.7O02S9CY](https://doi.org/10.7937/K9/TCIA.2016.7O02S9CY)

> [!WARNING]
> Người sử dụng dữ liệu cần tuân thủ **Chính sách và Hạn chế Sử dụng Dữ liệu** của TCIA.

---

## 7. Môi trường phát triển

* `Python`
* `Jupyter Notebook`
* `Visual Studio Code`
* `Conda Environment`
* `Apache Spark` (sử dụng trong các thử nghiệm xử lý dữ liệu liên quan)

Các thư viện và phiên bản môi trường được quản lý thông qua `environment.yml` và `requirements.txt`.

---

## 8. Lưu ý

* Repository này lưu mã nguồn, notebook, cấu hình môi trường và tài liệu nghiên cứu.
* Không lưu trữ ảnh DICOM gốc hoặc các dữ liệu lớn đã xử lý trên GitHub mặc định.
* Không đưa dữ liệu bệnh nhân, dữ liệu ảnh, mask và các tệp kết quả dung lượng lớn lên repository nếu chưa được kiểm tra quy tắc `.gitignore`.
* Các số liệu thống kê trong README phản ánh kết quả của từng giai đoạn xây dựng dữ liệu; cần được cập nhật khi pipeline hoặc phạm vi thực nghiệm thay đổi.
* Việc chuẩn hóa kích thước ROI Mask không tự động chứng minh sự căn chỉnh không gian chính xác với Full Image. Cần tiếp tục đánh giá Ground Truth và hệ tọa độ định vị trước khi sử dụng cho huấn luyện mô hình phát hiện tổn thương.
