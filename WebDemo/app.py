
from pathlib import Path
import io
import hashlib
import sys
import base64

import numpy as np
import pandas as pd
import streamlit as st
import torch
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageOps,
    ImageEnhance,
)

# ============================================================
# 1. CẤU HÌNH ỨNG DỤNG
# ============================================================

st.set_page_config(
    page_title="Breast Cancer Detection Demo",
    page_icon="🎗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

WEBDEMO_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = WEBDEMO_DIR.parent

YOLO_REPO = PROJECT_ROOT / "external" / "yolov5"

YOLO_CHECKPOINT = (
    PROJECT_ROOT
    / "Data" / "processed" / "nb08_model_training"
    / "nb08_7_3_yolov5_640_finetuning"
    / "yolov5n_640_finetune_lr001_20261116_205312"
    / "weights" / "best.pt"
)

INCEPTION_CHECKPOINT = (
    PROJECT_ROOT
    / "Data" / "processed" / "nb08_model_training"
    / "nb08_8_cnn_training" / "nb08_8_6_cnn_training"
    / "InceptionV3" / "best_checkpoint.pth"
)

DATASET_MANIFEST = (
    PROJECT_ROOT
    / "Data" / "processed" / "nb08_model_training"
    / "nb08_3_yolo_dataset" / "dataset_manifest.csv"
)

LABEL_MANIFEST = (
    PROJECT_ROOT
    / "Data" / "processed" / "nb08_model_training"
    / "nb08_3_yolo_dataset" / "label_manifest.csv"
)

CROP_MANIFEST = (
    PROJECT_ROOT
    / "Data" / "processed" / "nb08_model_training"
    / "nb08_7_classification_dataset"
    / "mass_crops_20261117_015211"
    / "nb08_7_9_mass_crop_manifest.csv"
)

RIBBON_PATH = (
    WEBDEMO_DIR / "assets" / "breast_cancer_pink_ribbon.png"
)

IMAGE_SIZE = 640
YOLO_CONFIDENCE = 0.20
YOLO_NMS_IOU = 0.60
CLASSIFICATION_THRESHOLD = 0.30
MATCH_IOU_THRESHOLD = 0.50

PLACEHOLDER = "-- Chọn ảnh từ tập Test --"

# Màu hiển thị
COLOR_PREDICTION = (245, 35, 55)
COLOR_GROUND_TRUTH = (35, 115, 220)
COLOR_WHITE = (255, 255, 255)

# Cấu hình ảnh crop chỉ dành cho hiển thị
CROP_DISPLAY_PADDING = 0.25
CROP_DISPLAY_CONTRAST = 1.45

# ============================================================
# 2. GIAO DIỆN HỒNG - TRẮNG
# ============================================================

CUSTOM_CSS = r"""
<style>
:root {
    --pink-50: #fff7fb;
    --pink-100: #ffedf5;
    --pink-150: #ffe4ef;
    --pink-200: #ffd4e5;
    --pink-300: #f7b5d0;
    --pink-400: #ed8fb8;
    --pink-500: #df6399;
    --pink-600: #c94380;
    --pink-700: #a92e68;
    --pink-800: #86224f;
    --white: #ffffff;
}

html, body, [data-testid="stAppViewContainer"] {
    background: #fff2f8 !important;
    color: #a92e68 !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stAppViewContainer"] > .main {
    background:
        radial-gradient(circle at 8% 5%, #ffe4ef 0, transparent 28%),
        linear-gradient(135deg, #fff2f8 0%, #ffedf5 52%, #fff7fb 100%) !important;
}

.block-container {
    max-width: 100% !important;
    padding: 1.2rem 2.2rem 3rem 2.2rem !important;
}

/* Màu chữ chung */

h1, h2, h3, h4, h5, h6,
p, span, label, div, li,
[data-testid="stMarkdownContainer"] {
    color: #a92e68;
}

h1, h2, h3, h4 {
    color: #a92e68 !important;
    font-weight: 750 !important;
}

p, li, label {
    color: #a94476 !important;
}

a {
    color: #c94380 !important;
}

/* Banner */

.hero-banner {
    width: calc(100% + 4.4rem);
    box-sizing: border-box;
    display: flex;
    align-items: center;
    gap: 25px;
    padding: 22px 34px;
    margin: 0 -2.2rem 22px -2.2rem;
    border: 2px solid #df8eb4;
    border-radius: 0 0 22px 22px;
    background: linear-gradient(
        110deg,
        #ffe0ed 0%,
        #ffd0e4 42%,
        #fff0f7 100%
    );
    box-shadow: 0 8px 24px rgba(194, 69, 126, 0.12);
}

.hero-ribbon {
    width: 88px;
    height: 88px;
    object-fit: contain;
    flex: 0 0 88px;
    filter: drop-shadow(0 4px 7px rgba(169, 46, 104, 0.13));
}

.hero-copy {
    min-width: 0;
}

.hero-eyebrow {
    font-size: 12px;
    letter-spacing: 2.3px;
    font-weight: 800;
    color: #b33c77 !important;
    margin-bottom: 5px;
}

.hero-title {
    font-size: clamp(27px, 3vw, 39px);
    line-height: 1.12;
    font-weight: 850;
    color: #a92e68 !important;
    margin: 0 0 7px 0;
}

.hero-description {
    font-size: 15px;
    line-height: 1.55;
    color: #a94476 !important;
    margin: 0;
}

.hero-models {
    display: inline-block;
    margin-top: 10px;
    padding: 6px 13px;
    border: 1px solid #e8a2c2;
    border-radius: 30px;
    background: rgba(255,255,255,0.58);
    color: #a92e68 !important;
    font-size: 12px;
    font-weight: 750;
}

/* Tiêu đề và thẻ nội dung */

.section-heading {
    font-size: 21px;
    font-weight: 800;
    color: #a92e68 !important;
    margin: 9px 0 13px 0;
}

.section-description {
    color: #a94476 !important;
    font-size: 14px;
    line-height: 1.65;
    margin: 0 0 10px 0;
}

.pink-card {
    background: linear-gradient(
        145deg,
        #ffffff 0%,
        #fff8fb 58%,
        #ffedf5 100%
    );
    border: 1.5px solid #e7a2c1;
    border-radius: 18px;
    padding: 19px 21px;
    box-shadow: 0 5px 18px rgba(185, 66, 121, 0.075);
    height: 100%;
}

.author-name {
    font-size: 21px;
    font-weight: 850;
    color: #a92e68 !important;
    margin-bottom: 8px;
}

.author-detail {
    font-size: 14px;
    line-height: 1.8;
    color: #a94476 !important;
}

.info-label {
    font-size: 11px;
    letter-spacing: 1.1px;
    text-transform: uppercase;
    font-weight: 800;
    color: #c45a8d !important;
    margin-bottom: 5px;
}

.info-value {
    font-size: 17px;
    font-weight: 800;
    color: #a92e68 !important;
}

.model-name {
    font-size: 18px;
    font-weight: 850;
    color: #a92e68 !important;
    margin-bottom: 8px;
}

.model-detail {
    font-size: 13px;
    line-height: 1.8;
    color: #a94476 !important;
}

.pink-divider {
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        #e7a2c1,
        transparent
    );
    margin: 20px 0;
}

/* Trạng thái chưa chọn ảnh */

.empty-state {
    text-align: center;
    padding: 34px 20px;
    border: 1.5px dashed #df8eb4;
    border-radius: 18px;
    background: linear-gradient(135deg, #fffafd, #ffedf5);
    color: #a92e68 !important;
}

.empty-state-title {
    font-size: 19px;
    font-weight: 850;
    color: #a92e68 !important;
    margin-bottom: 7px;
}

.empty-state-text {
    font-size: 14px;
    color: #b45180 !important;
}

/* Thẻ kết quả */

.result-card {
    border: 1.5px solid #e7a2c1;
    border-radius: 16px;
    padding: 16px 18px;
    background: linear-gradient(145deg, #ffffff, #fff3f8);
    margin-bottom: 12px;
}

.result-label {
    color: #c45a8d !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.8px;
}

.result-value {
    color: #a92e68 !important;
    font-size: 24px;
    font-weight: 850;
    margin-top: 4px;
}

/* Khung chọn ảnh: nhãn và giá trị đều dùng hồng đậm */

div[data-testid="stSelectbox"] label,
div[data-testid="stFileUploader"] label {
    color: #a92e68 !important;
    font-weight: 800 !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] {
    background: #fffafd !important;
    border: 1.5px solid #d879a5 !important;
    border-radius: 12px !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] *,
div[data-testid="stSelectbox"] [data-baseweb="select"] input {
    color: #a92e68 !important;
    font-weight: 750 !important;
    -webkit-text-fill-color: #a92e68 !important;
}

div[data-testid="stSelectbox"] [role="listbox"],
div[data-testid="stSelectbox"] [role="option"] {
    color: #a92e68 !important;
    background: #fffafd !important;
}

div[data-testid="stSelectbox"] [role="option"] {
    font-weight: 650 !important;
}

div[data-testid="stSelectbox"] [role="option"]:hover {
    background: #ffe4ef !important;
}

/* Khu vực tải ảnh */

div[data-testid="stFileUploader"] section {
    background: linear-gradient(135deg, #fffafd, #ffedf5) !important;
    border: 1.5px dashed #df8eb4 !important;
    border-radius: 15px !important;
}

div[data-testid="stFileUploader"] section *,
div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploader"] button {
    color: #a92e68 !important;
    font-weight: 700 !important;
}

/* Nút: chữ trắng in đậm */

.stButton > button {
    border: 1.5px solid #a92e68 !important;
    border-radius: 12px !important;
    background: linear-gradient(
        110deg,
        #c94380,
        #a92e68
    ) !important;
    color: #ffffff !important;
    font-weight: 900 !important;
    min-height: 45px;
    padding: 0.55rem 1.4rem;
    box-shadow: 0 5px 13px rgba(169, 46, 104, 0.16);
    transition: all 0.2s ease;
}

.stButton > button *,
.stButton > button p,
.stButton > button span {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 900 !important;
}

.stButton > button:hover {
    border-color: #86224f !important;
    background: linear-gradient(
        110deg,
        #b93675,
        #86224f
    ) !important;
    color: #ffffff !important;
    transform: translateY(-1px);
}

.stButton > button:disabled {
    background: #e9b8ce !important;
    border-color: #e9b8ce !important;
    color: #ffffff !important;
}

/* Bảng và thông báo */

div[data-testid="stDataFrame"] {
    border: 1px solid #e7a2c1;
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stAlert"] {
    border-radius: 12px !important;
}

footer {
    visibility: hidden;
}

@media (max-width: 850px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .hero-banner {
        width: calc(100% + 2rem);
        margin-left: -1rem;
        margin-right: -1rem;
        padding: 17px;
        gap: 14px;
    }

    .hero-ribbon {
        width: 65px;
        height: 65px;
        flex-basis: 65px;
    }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================
# 3. HÀM GIAO DIỆN VÀ QUẢN LÝ TRẠNG THÁI
# ============================================================

def render_section_title(title, description=None):
    st.markdown(
        f'<div class="section-heading">{title}</div>',
        unsafe_allow_html=True,
    )

    if description:
        st.markdown(
            f'<div class="section-description">{description}</div>',
            unsafe_allow_html=True,
        )


def render_empty_state(title, message):
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="empty-state-title">{title}</div>
            <div class="empty-state-text">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric(label, value):
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">{label}</div>
            <div class="result-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def clear_analysis():
    st.session_state.pop("analysis_result", None)
    st.session_state.pop("analysis_image_key", None)


def clear_external_upload():
    """
    Tăng phiên bản khóa uploader để Streamlit tạo một uploader mới.
    Không xóa trực tiếp trạng thái của widget đang hoạt động.
    """
    current_version = st.session_state.get(
        "external_upload_widget_version",
        0,
    )

    st.session_state["external_upload_widget_version"] = (
        current_version + 1
    )

    st.session_state.pop("analysis_result", None)
    st.session_state.pop("analysis_image_key", None)


st.session_state.setdefault("external_upload_widget_version", 0)

# ============================================================
# 4. KIỂM TRA VÀ NẠP MANIFEST
# ============================================================

@st.cache_data(show_spinner=False)
def load_manifests():
    required_files = [
        DATASET_MANIFEST,
        LABEL_MANIFEST,
        CROP_MANIFEST,
    ]

    missing = [
        str(path)
        for path in required_files
        if not path.exists()
    ]

    if missing:
        raise FileNotFoundError(
            "Không tìm thấy các manifest cần thiết:\n"
            + "\n".join(missing)
        )

    dataset_df = pd.read_csv(DATASET_MANIFEST)
    label_df = pd.read_csv(LABEL_MANIFEST)
    crop_df = pd.read_csv(CROP_MANIFEST)

    required_dataset = {
        "image_id",
        "image_file_name",
        "dataset_split",
        "source_image_path",
        "patient_id",
        "image_view",
        "laterality",
    }

    required_label = {
        "annotation_id",
        "image_id",
        "dataset_split",
        "pathology",
    }

    required_crop = {
        "annotation_id",
        "image_id",
        "patient_id",
        "dataset_split",
        "original_pathology",
        "binary_pathology",
        "source_image_path",
        "gt_x_min",
        "gt_y_min",
        "gt_x_max",
        "gt_y_max",
    }

    for name, df, required in [
        ("dataset_manifest", dataset_df, required_dataset),
        ("label_manifest", label_df, required_label),
        ("crop_manifest", crop_df, required_crop),
    ]:
        missing_columns = required - set(df.columns)

        if missing_columns:
            raise ValueError(
                f"{name} thiếu cột: {sorted(missing_columns)}"
            )

    dataset_df["dataset_split"] = (
        dataset_df["dataset_split"].astype(str).str.lower()
    )

    label_df["dataset_split"] = (
        label_df["dataset_split"].astype(str).str.lower()
    )

    crop_df["dataset_split"] = (
        crop_df["dataset_split"].astype(str).str.lower()
    )

    test_images = dataset_df[
        dataset_df["dataset_split"] == "test"
    ].copy()

    test_labels = label_df[
        label_df["dataset_split"] == "test"
    ].copy()

    test_crops = crop_df[
        crop_df["dataset_split"] == "test"
    ].copy()

    test_images = (
        test_images
        .drop_duplicates(subset=["image_id"])
        .reset_index(drop=True)
    )

    return test_images, test_labels, test_crops


try:
    TEST_IMAGES, TEST_LABELS, TEST_CROPS = load_manifests()

except Exception as exc:
    st.error(f"Không thể nạp dữ liệu CBIS-DDSM: {exc}")
    st.stop()


if len(TEST_IMAGES) != 361:
    st.error(
        "Số ảnh Test không đúng cấu hình đã xác nhận. "
        f"Mong đợi 361 ảnh, hiện có {len(TEST_IMAGES)} ảnh."
    )
    st.stop()


if len(TEST_CROPS) != 378:
    st.error(
        "Số annotation Test không đúng cấu hình đã xác nhận. "
        f"Mong đợi 378, hiện có {len(TEST_CROPS)} ảnh."
    )
    st.stop()

# ============================================================
# 5. NẠP MODULE XỬ LÝ ẢNH VÀ MÔ HÌNH
# ============================================================

if str(WEBDEMO_DIR) not in sys.path:
    sys.path.insert(0, str(WEBDEMO_DIR))


try:
    from app.utils.image_preprocessing import (
        load_medical_image,
        ImageProcessingError,
    )

    from app.utils.yolo_detector import YOLOMassDetector

    from app.utils.inception_classifier import (
        InceptionMassClassifier,
    )

except Exception as exc:
    st.error(
        f"Không thể nạp module xử lý hoặc mô hình: {exc}"
    )
    st.stop()


@st.cache_resource(
    show_spinner="Đang khởi tạo mô hình YOLOv5n..."
)
def load_yolo_model():
    if not YOLO_REPO.exists():
        raise FileNotFoundError(
            f"Không tìm thấy YOLOv5: {YOLO_REPO}"
        )

    if not YOLO_CHECKPOINT.exists():
        raise FileNotFoundError(
            f"Không tìm thấy checkpoint YOLO: {YOLO_CHECKPOINT}"
        )

    return YOLOMassDetector(
        weights=str(YOLO_CHECKPOINT),
        conf_threshold=YOLO_CONFIDENCE,
        nms_iou=YOLO_NMS_IOU,
        image_size=IMAGE_SIZE,
        device=None,
    )


@st.cache_resource(
    show_spinner="Đang khởi tạo InceptionV3..."
)
def load_inception_model():
    if not INCEPTION_CHECKPOINT.exists():
        raise FileNotFoundError(
            "Không tìm thấy checkpoint InceptionV3: "
            f"{INCEPTION_CHECKPOINT}"
        )

    return InceptionMassClassifier(
        checkpoint_path=str(INCEPTION_CHECKPOINT),
        image_size=299,
        threshold=CLASSIFICATION_THRESHOLD,
        device=None,
    )

# ============================================================
# 6. HÀM ĐỌC ẢNH, HIỂN THỊ CROP VÀ VẼ BOX
# ============================================================

def load_rgb_image(source, filename=None):
    loaded = load_medical_image(
        source,
        filename=filename,
    )

    image_rgb = loaded.get("image_rgb")

    if image_rgb is None:
        raise ValueError(
            "Không thể tạo ảnh RGB từ dữ liệu đầu vào."
        )

    image_rgb = np.asarray(image_rgb)

    if image_rgb.ndim == 2:
        image_rgb = np.stack(
            [image_rgb, image_rgb, image_rgb],
            axis=-1,
        )

    if image_rgb.shape[-1] == 4:
        image_rgb = image_rgb[:, :, :3]

    if image_rgb.dtype != np.uint8:
        image_rgb = np.clip(
            image_rgb,
            0,
            255,
        ).astype(np.uint8)

    return image_rgb, loaded.get("metadata", {})


def get_font(size=18, bold=True):
    candidates = []

    if bold:
        candidates.extend([
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/Arial Bold.ttf",
        ])

    candidates.extend([
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/Arial.ttf",
        "arial.ttf",
    ])

    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except Exception:
            continue

    return ImageFont.load_default()


def draw_boxes(
    image_rgb,
    boxes,
    color,
    prefix,
    width=4,
):
    """
    Vẽ bounding box có nhãn nền màu tương ứng.
    Prediction dùng đỏ; Ground Truth dùng xanh dương.
    """

    canvas = Image.fromarray(
        image_rgb.copy()
    ).convert("RGB")

    draw = ImageDraw.Draw(canvas)

    image_width, image_height = canvas.size

    line_width = max(
        width,
        int(round(min(image_width, image_height) / 350)),
    )

    font_size = max(
        16,
        min(24, int(round(min(image_width, image_height) / 45))),
    )

    font = get_font(font_size, bold=True)

    for index, box in enumerate(boxes, start=1):
        x1 = int(round(float(box["x1"])))
        y1 = int(round(float(box["y1"])))
        x2 = int(round(float(box["x2"])))
        y2 = int(round(float(box["y2"])))

        x1 = max(0, min(image_width - 1, x1))
        x2 = max(0, min(image_width - 1, x2))
        y1 = max(0, min(image_height - 1, y1))
        y2 = max(0, min(image_height - 1, y2))

        if x2 <= x1 or y2 <= y1:
            continue

        draw.rectangle(
            [x1, y1, x2, y2],
            outline=color,
            width=line_width,
        )

        label = box.get(
            "label",
            f"{prefix} {index}",
        )

        text_bbox = draw.textbbox(
            (0, 0),
            label,
            font=font,
            stroke_width=0,
        )

        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        padding_x = 8
        padding_y = 5

        label_width = text_width + padding_x * 2
        label_height = text_height + padding_y * 2

        label_x1 = x1
        label_x2 = min(
            image_width - 1,
            label_x1 + label_width,
        )

        # Ưu tiên đặt nhãn phía trên box.
        label_y2 = y1
        label_y1 = y1 - label_height

        # Nếu không đủ chỗ phía trên, đặt nhãn bên trong box.
        if label_y1 < 0:
            label_y1 = y1
            label_y2 = min(
                image_height - 1,
                y1 + label_height,
            )

        draw.rectangle(
            [
                label_x1,
                label_y1,
                label_x2,
                label_y2,
            ],
            fill=color,
        )

        text_x = label_x1 + padding_x
        text_y = label_y1 + padding_y - text_bbox[1]

        draw.text(
            (text_x, text_y),
            label,
            fill=COLOR_WHITE,
            font=font,
            stroke_width=0,
        )

    return np.asarray(canvas)


def create_display_crop(image_rgb, box):
    """
    Tạo crop dành riêng cho hiển thị.

    Hàm này:
    - Mở rộng vùng crop quanh bounding box.
    - Tăng tương phản grayscale để quan sát dễ hơn.
    - Không thay đổi ảnh crop gốc dùng cho InceptionV3.
    """

    height, width = image_rgb.shape[:2]

    x1 = float(box["x1"])
    y1 = float(box["y1"])
    x2 = float(box["x2"])
    y2 = float(box["y2"])

    box_width = max(1.0, x2 - x1)
    box_height = max(1.0, y2 - y1)

    padding_x = box_width * CROP_DISPLAY_PADDING
    padding_y = box_height * CROP_DISPLAY_PADDING

    crop_x1 = max(
        0,
        int(round(x1 - padding_x)),
    )

    crop_y1 = max(
        0,
        int(round(y1 - padding_y)),
    )

    crop_x2 = min(
        width,
        int(round(x2 + padding_x)),
    )

    crop_y2 = min(
        height,
        int(round(y2 + padding_y)),
    )

    if crop_x2 <= crop_x1 or crop_y2 <= crop_y1:
        return image_rgb.copy()

    display_crop = image_rgb[
        crop_y1:crop_y2,
        crop_x1:crop_x2,
    ].copy()

    pil_image = Image.fromarray(
        display_crop
    ).convert("RGB")

    # Chỉ áp dụng tăng tương phản cho bản xem trên giao diện.
    # Không sử dụng bản này làm đầu vào phân loại.
    pil_image = ImageOps.autocontrast(
        pil_image,
        cutoff=1,
    )

    pil_image = ImageEnhance.Contrast(
        pil_image
    ).enhance(CROP_DISPLAY_CONTRAST)

    return np.asarray(pil_image)


def get_ground_truth_boxes(
    crop_rows,
    image_width,
    image_height,
):
    boxes = []

    for _, row in crop_rows.iterrows():
        try:
            x1 = float(row["gt_x_min"])
            y1 = float(row["gt_y_min"])
            x2 = float(row["gt_x_max"])
            y2 = float(row["gt_y_max"])

            manifest_width = row.get(
                "image_width",
                image_width,
            )

            manifest_height = row.get(
                "image_height",
                image_height,
            )

            if (
                pd.notna(manifest_width)
                and float(manifest_width) > 0
            ):
                sx = image_width / float(manifest_width)
                x1, x2 = x1 * sx, x2 * sx

            if (
                pd.notna(manifest_height)
                and float(manifest_height) > 0
            ):
                sy = image_height / float(manifest_height)
                y1, y2 = y1 * sy, y2 * sy

            x1 = max(
                0,
                min(image_width - 1, x1),
            )

            x2 = max(
                0,
                min(image_width - 1, x2),
            )

            y1 = max(
                0,
                min(image_height - 1, y1),
            )

            y2 = max(
                0,
                min(image_height - 1, y2),
            )

            if x2 <= x1 or y2 <= y1:
                continue

            pathology = str(
                row.get(
                    "binary_pathology",
                    "UNKNOWN",
                )
            ).upper()

            boxes.append({
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "label": pathology,
                "annotation_id": str(
                    row["annotation_id"]
                ),
            })

        except Exception:
            continue

    return boxes


def calculate_iou(box_a, box_b):
    x_left = max(
        box_a["x1"],
        box_b["x1"],
    )

    y_top = max(
        box_a["y1"],
        box_b["y1"],
    )

    x_right = min(
        box_a["x2"],
        box_b["x2"],
    )

    y_bottom = min(
        box_a["y2"],
        box_b["y2"],
    )

    intersection = (
        max(0, x_right - x_left)
        * max(0, y_bottom - y_top)
    )

    area_a = (
        max(0, box_a["x2"] - box_a["x1"])
        * max(0, box_a["y2"] - box_a["y1"])
    )

    area_b = (
        max(0, box_b["x2"] - box_b["x1"])
        * max(0, box_b["y2"] - box_b["y1"])
    )

    union = area_a + area_b - intersection

    return (
        intersection / union
        if union > 0
        else 0.0
    )


def match_predictions_to_ground_truth(
    predictions,
    ground_truth,
):
    pairs = []
    used_gt = set()

    ordered_predictions = sorted(
        enumerate(predictions),
        key=lambda item: float(
            item[1].get("confidence", 0)
        ),
        reverse=True,
    )

    for pred_index, prediction in ordered_predictions:
        best_iou = 0.0
        best_gt_index = None

        for gt_index, gt in enumerate(ground_truth):
            if gt_index in used_gt:
                continue

            iou = calculate_iou(
                prediction,
                gt,
            )

            if iou > best_iou:
                best_iou = iou
                best_gt_index = gt_index

        if (
            best_gt_index is not None
            and best_iou >= MATCH_IOU_THRESHOLD
        ):
            used_gt.add(best_gt_index)

            pairs.append({
                "prediction_index": pred_index,
                "ground_truth_index": best_gt_index,
                "iou": best_iou,
            })

    matched_pred = {
        pair["prediction_index"]
        for pair in pairs
    }

    unmatched_pred = [
        index
        for index in range(len(predictions))
        if index not in matched_pred
    ]

    unmatched_gt = [
        index
        for index in range(len(ground_truth))
        if index not in used_gt
    ]

    return (
        pairs,
        unmatched_pred,
        unmatched_gt,
    )

# ============================================================
# 7. CHẠY QUY TRÌNH HAI GIAI ĐOẠN
# ============================================================

def run_two_stage_pipeline(
    image_rgb,
    include_ground_truth=False,
    ground_truth=None,
):
    yolo_model = load_yolo_model()
    inception_model = load_inception_model()

    detection_result = yolo_model.detect(image_rgb)

    predictions = detection_result.get(
        "boxes",
        [],
    )

    classification_results = []

    height, width = image_rgb.shape[:2]

    for index, box in enumerate(
        predictions,
        start=1,
    ):
        x1 = max(
            0,
            min(width, int(round(box["x1"]))),
        )

        y1 = max(
            0,
            min(height, int(round(box["y1"]))),
        )

        x2 = max(
            0,
            min(width, int(round(box["x2"]))),
        )

        y2 = max(
            0,
            min(height, int(round(box["y2"]))),
        )

        if x2 <= x1 or y2 <= y1:
            continue

        # Crop gốc: giữ nguyên để InceptionV3 phân loại.
        crop = image_rgb[
            y1:y2,
            x1:x2,
        ]

        if crop.size == 0:
            continue

        classification = inception_model.classify(
            crop
        )

        # Crop hiển thị: có thêm vùng xung quanh và tăng tương phản.
        # Không dùng crop hiển thị cho suy luận.
        display_crop = create_display_crop(
            image_rgb,
            box,
        )

        classification_results.append({
            "box_index": index,
            "box": box,
            "crop": crop.copy(),
            "display_crop": display_crop,
            "classification": classification,
        })

    result = {
        "detection": detection_result,
        "predictions": predictions,
        "classifications": classification_results,
        "ground_truth": ground_truth or [],
        "include_ground_truth": include_ground_truth,
    }

    if include_ground_truth:
        (
            pairs,
            unmatched_pred,
            unmatched_gt,
        ) = match_predictions_to_ground_truth(
            predictions,
            ground_truth or [],
        )

        result["matches"] = pairs
        result["unmatched_predictions"] = unmatched_pred
        result["unmatched_ground_truth"] = unmatched_gt

    return result

# ============================================================
# 8. HIỂN THỊ KẾT QUẢ
# ============================================================

def render_pipeline_results(
    image_rgb,
    result,
):
    predictions = result["predictions"]
    classifications = result["classifications"]
    include_gt = result["include_ground_truth"]
    ground_truth = result["ground_truth"]

    st.markdown(
        '<div class="pink-divider"></div>',
        unsafe_allow_html=True,
    )

    render_section_title("Kết quả phân tích")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        render_metric(
            "SỐ VÙNG MASS DỰ ĐOÁN",
            len(predictions),
        )

    with col_b:
        render_metric(
            "SỐ VÙNG ĐƯỢC PHÂN LOẠI",
            len(classifications),
        )

    with col_c:
        malignant_count = sum(
            item["classification"]["predicted_label"]
            == "MALIGNANT"
            for item in classifications
        )

        render_metric(
            "DỰ ĐOÁN MALIGNANT",
            malignant_count,
        )

    if not predictions:
        st.warning(
            "YOLOv5n không phát hiện được vùng Mass trong ảnh này. "
            "Hệ thống không thực hiện phân loại InceptionV3 và "
            "không kết luận ảnh là BENIGN."
        )

        st.image(
            image_rgb,
            caption="Ảnh X-quang đầu vào",
            use_container_width=True,
        )

        return

    # Ground Truth: xanh dương.
    gt_overlay = None

    if include_gt:
        gt_overlay = draw_boxes(
            image_rgb,
            ground_truth,
            color=COLOR_GROUND_TRUTH,
            prefix="GT",
            width=4,
        )

    # Prediction: đỏ tươi, nhãn nền đỏ và chữ trắng.
    pred_boxes_for_draw = []

    for index, box in enumerate(
        predictions,
        start=1,
    ):
        pred_boxes_for_draw.append({
            **box,
            "label": (
                f"Mass {index} | "
                f"{float(box.get('confidence', 0)):.4f}"
            ),
        })

    pred_overlay = draw_boxes(
        image_rgb,
        pred_boxes_for_draw,
        color=COLOR_PREDICTION,
        prefix="YOLO",
        width=5,
    )

    if include_gt:
        image_columns = st.columns(3)

        with image_columns[0]:
            st.markdown("**Ảnh X-quang gốc**")

            st.image(
                image_rgb,
                use_container_width=True,
            )

        with image_columns[1]:
            st.markdown(
                "**Ground Truth Bounding Box**"
            )

            st.image(
                gt_overlay,
                use_container_width=True,
            )

        with image_columns[2]:
            st.markdown(
                "**YOLOv5n Predicted Bounding Box**"
            )

            st.image(
                pred_overlay,
                use_container_width=True,
            )

    else:
        image_columns = st.columns([1, 1])

        with image_columns[0]:
            st.markdown("**Ảnh X-quang gốc**")

            st.image(
                image_rgb,
                use_container_width=True,
            )

        with image_columns[1]:
            st.markdown(
                "**YOLOv5n Predicted Bounding Box**"
            )

            st.image(
                pred_overlay,
                use_container_width=True,
            )

    st.markdown(
        '<div class="pink-divider"></div>',
        unsafe_allow_html=True,
    )

    render_section_title(
        "Kết quả phân loại từng vùng Mass"
    )

    rows = []

    for item in classifications:
        classification = item["classification"]
        box = item["box"]

        rows.append({
            "Vùng Mass": item["box_index"],
            "Confidence YOLO": round(
                float(box.get("confidence", 0)),
                4,
            ),
            "BENIGN (%)": round(
                float(
                    classification["benign_probability"]
                ) * 100,
                2,
            ),
            "MALIGNANT (%)": round(
                float(
                    classification["malignant_probability"]
                ) * 100,
                2,
            ),
            "Kết quả": classification["predicted_label"],
        })

    if rows:
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )

    # Hiển thị crop đã mở rộng và tăng tương phản.
    # Ảnh này chỉ dùng để quan sát, không phải ảnh suy luận.
    if classifications:
        st.markdown(
            "**Ảnh vùng Mass sau khi mở rộng khung nhìn**"
        )

        crop_columns = st.columns(
            min(3, len(classifications))
        )

        for index, item in enumerate(classifications):
            with crop_columns[
                index % len(crop_columns)
            ]:
                classification = item["classification"]

                st.markdown(
                    f"**Vùng Mass {item['box_index']}**"
                )

                st.image(
                    item["display_crop"],
                    caption=(
                        "Ảnh hiển thị đã tăng tương phản · "
                        f"{classification['predicted_label']}"
                    ),
                    use_container_width=True,
                )

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">
                            BENIGN
                        </div>
                        <div class="info-value">
                            {classification['benign_probability'] * 100:.2f}%
                        </div>
                        <div class="result-label">
                            MALIGNANT
                        </div>
                        <div class="info-value">
                            {classification['malignant_probability'] * 100:.2f}%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Đối chiếu Ground Truth chỉ dành cho ảnh Test CBIS-DDSM.
    if include_gt:
        pairs = result.get("matches", [])
        unmatched_pred = result.get(
            "unmatched_predictions",
            [],
        )
        unmatched_gt = result.get(
            "unmatched_ground_truth",
            [],
        )

        st.markdown(
            '<div class="pink-divider"></div>',
            unsafe_allow_html=True,
        )

        render_section_title(
            "Đối chiếu Ground Truth và kết quả phát hiện",
            "Ghép cặp dựa trên IoU ≥ 0.50. "
            "Đây là đối chiếu định vị, không phải kết luận lâm sàng.",
        )

        comparison_rows = []

        for pair in pairs:
            pred = predictions[
                pair["prediction_index"]
            ]

            gt = ground_truth[
                pair["ground_truth_index"]
            ]

            pred_classification = next(
                (
                    item["classification"]["predicted_label"]
                    for item in classifications
                    if item["box"] is pred
                ),
                "Không có kết quả",
            )

            comparison_rows.append({
                "Ground Truth": gt["label"],
                "Dự đoán InceptionV3": pred_classification,
                "IoU": round(pair["iou"], 4),
                "Đối chiếu nhãn": (
                    "Khớp nhãn"
                    if pred_classification == gt["label"]
                    else "Không khớp nhãn"
                ),
            })

        if comparison_rows:
            st.dataframe(
                pd.DataFrame(comparison_rows),
                use_container_width=True,
                hide_index=True,
            )

        c1, c2, c3 = st.columns(3)

        with c1:
            render_metric(
                "GHÉP CẶP ĐƯỢC",
                len(pairs),
            )

        with c2:
            render_metric(
                "GT BỊ BỎ SÓT",
                len(unmatched_gt),
            )

        with c3:
            render_metric(
                "DỰ ĐOÁN KHÔNG GHÉP",
                len(unmatched_pred),
            )

        if unmatched_gt:
            st.warning(
                f"Có {len(unmatched_gt)} Ground Truth "
                "không được ghép với dự đoán YOLOv5n."
            )

        if unmatched_pred:
            st.info(
                f"Có {len(unmatched_pred)} vùng YOLOv5n "
                "dự đoán không ghép được với Ground Truth "
                "theo IoU ≥ 0.50."
            )

# ============================================================
# 9. BANNER
# ============================================================

if RIBBON_PATH.exists():
    ribbon_base64 = base64.b64encode(
        RIBBON_PATH.read_bytes()
    ).decode("utf-8")

    ribbon_html = (
        '<img class="hero-ribbon" '
        f'src="data:image/png;base64,{ribbon_base64}" '
        'alt="Ruy-băng hồng nâng cao nhận thức ung thư vú">'
    )

else:
    ribbon_html = (
        '<div class="hero-ribbon" '
        'style="display:flex;align-items:center;'
        'justify-content:center;font-size:60px;'
        'color:#c94380;">🎗</div>'
    )


st.markdown(
    f"""
    <div class="hero-banner">
        {ribbon_html}
        <div class="hero-copy">
            <div class="hero-eyebrow">
                NÂNG CAO NHẬN THỨC VỀ UNG THƯ VÚ
            </div>
            <div class="hero-title">
                Breast Cancer Detection Demo
            </div>
            <p class="hero-description">
                Hệ thống học sâu hai giai đoạn hỗ trợ phát hiện,
                định vị vùng Mass và phân loại đặc điểm tổn thương
                trên ảnh X-quang tuyến vú.
            </p>
            <div class="hero-models">
                YOLOv5n Detection &nbsp;|&nbsp;
                InceptionV3 Classification
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# 10. THÔNG TIN TÁC GIẢ
# ============================================================

render_section_title("Thông tin tác giả")

author_col, project_col = st.columns([
    1.05,
    1.95,
])

with author_col:
    st.markdown(
        """
        <div class="pink-card">
            <div class="info-label">TÁC GIẢ</div>
            <div class="author-name">
                Lương Hoàng Yến
            </div>
            <div class="author-detail">
                <b>Trường:</b>
                Nguyen Tat Thanh University (NTTU)<br>
                <b>Ngành:</b> Data Science
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with project_col:
    st.markdown(
        """
        <div class="pink-card">
            <div class="info-label">
                TỔNG QUAN HỆ THỐNG
            </div>
            <div class="model-name">
                Quy trình học sâu hai giai đoạn
            </div>
            <div class="model-detail">
                <b>Giai đoạn 1 — YOLOv5n:</b>
                phát hiện và định vị các vùng Mass trên ảnh
                X-quang tuyến vú.<br>
                <b>Giai đoạn 2 — InceptionV3:</b>
                phân loại từng vùng được phát hiện thành
                BENIGN hoặc MALIGNANT.<br>
                Kết quả chỉ phục vụ mục đích nghiên cứu và
                trình diễn mô hình, không thay thế chẩn đoán
                của bác sĩ.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# 11. CẤU HÌNH MÔ HÌNH
# ============================================================

st.markdown(
    '<div class="pink-divider"></div>',
    unsafe_allow_html=True,
)

render_section_title(
    "Cấu hình mô hình sử dụng"
)

model_col1, model_col2 = st.columns(2)

with model_col1:
    st.markdown(
        """
        <div class="pink-card">
            <div class="model-name">
                YOLOv5n — Mass Detection
            </div>
            <div class="model-detail">
                <b>Checkpoint:</b> Fine-tuned YOLOv5n<br>
                <b>Kích thước đầu vào:</b> 640 × 640<br>
                <b>Confidence threshold:</b> 0.20<br>
                <b>NMS IoU threshold:</b> 0.60
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with model_col2:
    st.markdown(
        """
        <div class="pink-card">
            <div class="model-name">
                InceptionV3 — Pathology Classification
            </div>
            <div class="model-detail">
                <b>Checkpoint:</b> Fine-tuned InceptionV3<br>
                <b>Kích thước đầu vào:</b> 299 × 299<br>
                <b>Classification threshold:</b> 0.30<br>
                <b>Nhãn:</b> BENIGN / MALIGNANT
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# 12. KHU VỰC CHỌN ẢNH
# ============================================================

st.markdown(
    '<div class="pink-divider"></div>',
    unsafe_allow_html=True,
)

render_section_title(
    "Chọn hình ảnh kiểm tra",
    "Chọn ảnh từ tập Test CBIS-DDSM hoặc tải ảnh X-quang bên ngoài "
    "để thử nghiệm mô hình.",
)

mode = st.selectbox(
    "Nguồn ảnh",
    options=[
        "CBIS-DDSM — Bộ kiểm tra",
        "Tải ảnh bên ngoài",
    ],
    key="image_mode",
    on_change=clear_analysis,
)

selected_image_rgb = None
selected_image_key = None
selected_metadata = {}
selected_gt_rows = pd.DataFrame()
selected_patient = None
selected_view = None
selected_laterality = None
selected_image_id = None
can_run = False

# ------------------------------------------------------------
# 12A. CHẾ ĐỘ CBIS-DDSM TEST
# ------------------------------------------------------------

if mode == "CBIS-DDSM — Bộ kiểm tra":

    image_lookup = {
        str(row["image_id"]): row
        for _, row in TEST_IMAGES.iterrows()
    }

    image_options = (
        [PLACEHOLDER]
        + list(image_lookup.keys())
    )

    selected_id = st.selectbox(
        "Chọn một ảnh trong 361 ảnh Test",
        options=image_options,
        index=0,
        key="test_image_selector",
        on_change=clear_analysis,
        format_func=lambda value: (
            value
            if value == PLACEHOLDER
            else f"Ảnh Test — {value}"
        ),
    )

    if selected_id != PLACEHOLDER:
        selected_row = image_lookup[selected_id]

        selected_image_id = selected_id

        selected_image_key = (
            f"CBIS_TEST::{selected_id}"
        )

        selected_patient = str(
            selected_row.get(
                "patient_id",
                "Không có thông tin",
            )
        )

        selected_view = str(
            selected_row.get(
                "image_view",
                "Không có thông tin",
            )
        )

        selected_laterality = str(
            selected_row.get(
                "laterality",
                "Không có thông tin",
            )
        )

        selected_gt_rows = TEST_CROPS[
            TEST_CROPS["image_id"].astype(str)
            == selected_id
        ].copy()

        source_path = Path(
            str(selected_row["source_image_path"])
        )

        if not source_path.exists():
            st.error(
                "Không tìm thấy ảnh nguồn trong manifest: "
                f"{source_path}"
            )

        else:
            try:
                (
                    selected_image_rgb,
                    selected_metadata,
                ) = load_rgb_image(
                    str(source_path)
                )

                can_run = True

            except Exception as exc:
                st.error(
                    f"Không thể đọc ảnh Test: {exc}"
                )

        if selected_image_rgb is not None:
            benign_count = int(
                (
                    selected_gt_rows["binary_pathology"]
                    .astype(str)
                    .str.upper()
                    == "BENIGN"
                ).sum()
            )

            malignant_count = int(
                (
                    selected_gt_rows["binary_pathology"]
                    .astype(str)
                    .str.upper()
                    == "MALIGNANT"
                ).sum()
            )

            render_section_title(
                "Thông tin ảnh đã chọn"
            )

            info_cols = st.columns(5)

            with info_cols[0]:
                render_metric(
                    "PATIENT ID",
                    selected_patient,
                )

            with info_cols[1]:
                render_metric(
                    "IMAGE VIEW",
                    selected_view,
                )

            with info_cols[2]:
                render_metric(
                    "LATERALITY",
                    selected_laterality,
                )

            with info_cols[3]:
                render_metric(
                    "GROUND TRUTH",
                    len(selected_gt_rows),
                )

            with info_cols[4]:
                render_metric(
                    "BENIGN / MALIGNANT",
                    f"{benign_count} / {malignant_count}",
                )

            gt_boxes = get_ground_truth_boxes(
                selected_gt_rows,
                selected_image_rgb.shape[1],
                selected_image_rgb.shape[0],
            )

            gt_preview = draw_boxes(
                selected_image_rgb,
                gt_boxes,
                color=COLOR_GROUND_TRUTH,
                prefix="GT",
                width=4,
            )

            preview_col1, preview_col2 = st.columns(2)

            with preview_col1:
                st.markdown(
                    "**Ảnh X-quang gốc**"
                )

                st.image(
                    selected_image_rgb,
                    use_container_width=True,
                )

            with preview_col2:
                st.markdown(
                    "**Ground Truth Bounding Box**"
                )

                st.image(
                    gt_preview,
                    use_container_width=True,
                )

            st.caption(
                "Ground Truth được lấy từ crop manifest của tập Test. "
                "Nhãn BENIGN_WITHOUT_CALLBACK được gộp vào BENIGN "
                "theo quy ước phân loại nhị phân của thí nghiệm."
            )

    else:
        render_empty_state(
            "Chưa chọn ảnh kiểm tra",
            "Vui lòng chọn một ảnh trong danh sách 361 ảnh Test. "
            "Thông tin bệnh nhân, ảnh X-quang và Ground Truth "
            "sẽ chỉ xuất hiện sau khi bà chọn ảnh.",
        )

# ------------------------------------------------------------
# 12B. CHẾ ĐỘ TẢI ẢNH BÊN NGOÀI
# ------------------------------------------------------------

else:
    st.markdown(
        """
        <div class="pink-card">
            <div class="model-name">
                Tải ảnh X-quang bên ngoài
            </div>
            <div class="section-description">
                Tải ảnh X-quang tuyến vú để thử nghiệm mô hình.
                Ảnh tải lên không có Ground Truth được xác minh,
                vì vậy hệ thống chỉ hiển thị kết quả dự đoán.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    upload_version = st.session_state.get(
        "external_upload_widget_version",
        0,
    )

    upload_widget_key = (
        f"external_upload_{upload_version}"
    )

    uploaded_file = st.file_uploader(
        "Chọn ảnh X-quang",
        type=[
            "png",
            "jpg",
            "jpeg",
            "dcm",
        ],
        key=upload_widget_key,
        help="Hỗ trợ PNG, JPG, JPEG và DICOM.",
    )

    if uploaded_file is not None:
        uploaded_bytes = uploaded_file.getvalue()

        selected_image_key = (
            "EXTERNAL::"
            + hashlib.sha256(
                uploaded_bytes
            ).hexdigest()
        )

        try:
            (
                selected_image_rgb,
                selected_metadata,
            ) = load_rgb_image(
                io.BytesIO(uploaded_bytes),
                filename=uploaded_file.name,
            )

            can_run = True

            st.markdown(
                "**Ảnh xem trước**"
            )

            st.image(
                selected_image_rgb,
                use_container_width=True,
            )

            st.button(
                "Xóa ảnh đã chọn",
                key="clear_external_image",
                use_container_width=False,
                on_click=clear_external_upload,
            )

        except Exception as exc:
            st.error(
                f"Không thể đọc ảnh tải lên: {exc}"
            )

            can_run = False

    else:
        render_empty_state(
            "Chưa có ảnh được tải lên",
            "Chọn ảnh X-quang tuyến vú để xem trước và chạy thử nghiệm.",
        )

# ============================================================
# 13. NÚT XÁC NHẬN DUY NHẤT
# ============================================================

st.markdown(
    '<div class="pink-divider"></div>',
    unsafe_allow_html=True,
)

button_col1, button_col2, button_col3 = st.columns([
    1,
    1.2,
    1,
])

with button_col2:
    confirm_clicked = st.button(
        "Xác Nhận",
        key="confirm_analysis",
        use_container_width=True,
        disabled=(
            not can_run
            or selected_image_rgb is None
        ),
    )

# ============================================================
# 14. THỰC THI PHÂN TÍCH
# ============================================================

if confirm_clicked:
    if (
        selected_image_rgb is None
        or selected_image_key is None
    ):
        st.warning(
            "Vui lòng chọn ảnh trước khi xác nhận."
        )

    else:
        try:
            gt_boxes_for_analysis = []

            if mode == "CBIS-DDSM — Bộ kiểm tra":
                gt_boxes_for_analysis = (
                    get_ground_truth_boxes(
                        selected_gt_rows,
                        selected_image_rgb.shape[1],
                        selected_image_rgb.shape[0],
                    )
                )

            with st.spinner(
                "Đang chạy YOLOv5n phát hiện Mass và "
                "InceptionV3 phân loại vùng tổn thương..."
            ):
                result = run_two_stage_pipeline(
                    selected_image_rgb,
                    include_ground_truth=(
                        mode == "CBIS-DDSM — Bộ kiểm tra"
                    ),
                    ground_truth=gt_boxes_for_analysis,
                )

            st.session_state["analysis_result"] = result

            st.session_state["analysis_image_key"] = (
                selected_image_key
            )

        except Exception as exc:
            st.session_state.pop(
                "analysis_result",
                None,
            )

            st.session_state.pop(
                "analysis_image_key",
                None,
            )

            st.error(
                f"Quá trình phân tích gặp lỗi: {exc}"
            )

# ============================================================
# 15. CHỈ HIỂN THỊ KẾT QUẢ ĐÚNG VỚI ẢNH HIỆN TẠI
# ============================================================

analysis_result = st.session_state.get(
    "analysis_result"
)

analysis_image_key = st.session_state.get(
    "analysis_image_key"
)

if (
    analysis_result is not None
    and selected_image_rgb is not None
    and selected_image_key is not None
    and analysis_image_key == selected_image_key
):
    render_pipeline_results(
        selected_image_rgb,
        analysis_result,
    )

elif (
    analysis_result is not None
    and analysis_image_key != selected_image_key
):
    st.session_state.pop(
        "analysis_result",
        None,
    )

    st.session_state.pop(
        "analysis_image_key",
        None,
    )

# ============================================================
# 16. CHÂN TRANG
# ============================================================

st.markdown(
    """
    <div class="pink-divider"></div>
    <div style="
        text-align:center;
        padding:12px 5px 4px 5px;
        color:#bd5b8b;
        font-size:12px;
        line-height:1.7;
    ">
        <b style="color:#a92e68;">
            Breast Cancer Detection Demo
        </b><br>
        YOLOv5n Mass Detection ·
        InceptionV3 Pathology Classification<br>
        Nghiên cứu học thuật —
        Nguyen Tat Thanh University (NTTU)
    </div>
    """,
    unsafe_allow_html=True,
)
