#!/usr/bin/env python3
"""Generate the three final DOCX outputs for math exam review workflows."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


FINAL_NAMES = {
    "report": "批改与复盘报告.docx",
    "wrong_book": "错题本.docx",
    "retest": "复测小卷.docx",
}

DOCX_FONT = "宋体"


def as_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, list):
        return "、".join(str(item) for item in value)
    return str(value)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def apply_font(run: Any, size: int | None = None, bold: bool | None = None, color: str | None = None) -> None:
    run.font.name = DOCX_FONT
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for font_key in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(font_key), DOCX_FONT)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)


def configure_doc(doc: Document) -> None:
    section = doc.sections[0]
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    normal = doc.styles["Normal"]
    normal.font.name = DOCX_FONT
    normal_rfonts = normal._element.rPr.rFonts
    for font_key in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        normal_rfonts.set(qn(font_key), DOCX_FONT)
    normal.font.size = Pt(10.5)

    for style_name, size, color in [
        ("Heading 1", 16, "1F4E79"),
        ("Heading 2", 13, "2F5F8F"),
        ("Heading 3", 11, "365F2D"),
    ]:
        style = doc.styles[style_name]
        style.font.name = DOCX_FONT
        style_rfonts = style._element.rPr.rFonts
        for font_key in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            style_rfonts.set(qn(font_key), DOCX_FONT)
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor.from_string(color)


def enforce_doc_font(doc: Document) -> None:
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            apply_font(run)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        apply_font(run)


def add_title(doc: Document, title: str, subtitle: str = "") -> None:
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run(title)
    apply_font(run, size=20, bold=True, color="1F4E79")
    if subtitle:
        sub = doc.add_paragraph()
        sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = sub.add_run(subtitle)
        apply_font(run, size=10, color="666666")


def add_bullets(doc: Document, values: Any) -> None:
    items = as_list(values)
    if not items:
        doc.add_paragraph("暂无。")
        return
    for item in items:
        doc.add_paragraph(as_text(item), style="List Bullet")


def add_label_value(doc: Document, label: str, value: Any) -> None:
    p = doc.add_paragraph()
    label_run = p.add_run(f"{label}：")
    apply_font(label_run, bold=True)
    value_run = p.add_run(as_text(value, "暂无"))
    apply_font(value_run)


def add_table(doc: Document, headers: list[str], rows: list[list[str]]) -> None:
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    header_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        paragraph = header_cells[i].paragraphs[0]
        run = paragraph.add_run(header)
        apply_font(run, bold=True, color="1F4E79")
    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = value


def resolve_image(path_value: Any, image_root: Path | None) -> Path | None:
    if not path_value:
        return None
    path = Path(str(path_value))
    if not path.is_absolute() and image_root is not None:
        path = image_root / path
    return path if path.exists() and path.is_file() else None


def add_image_or_note(doc: Document, image_path: Path | None, fallback_text: str = "") -> None:
    if image_path is not None:
        try:
            doc.add_picture(str(image_path), width=Inches(5.8))
            last = doc.paragraphs[-1]
            last.alignment = WD_ALIGN_PARAGRAPH.CENTER
            return
        except Exception:
            pass
    if fallback_text:
        add_label_value(doc, "原题文字", fallback_text)
    else:
        add_label_value(doc, "原题图片", "需要复核/补图")


def build_report(data: dict[str, Any], output_path: Path) -> None:
    doc = Document()
    configure_doc(doc)
    add_title(doc, "数学试卷批改与复盘报告", as_text(data.get("exam_name")))

    doc.add_heading("1. 批改概览", level=1)
    add_label_value(doc, "学段", data.get("level"))
    add_label_value(doc, "预计得分", data.get("estimated_score"))
    add_label_value(doc, "满分", data.get("total_score"))
    add_label_value(doc, "错题", data.get("wrong_items"))
    add_label_value(doc, "部分得分题", data.get("partial_items"))
    add_label_value(doc, "需要复核题", data.get("needs_review_items"))
    add_label_value(doc, "本次主要问题", data.get("main_problem"))

    doc.add_heading("2. 逐题批改", level=1)
    grading_rows = []
    for item in as_list(data.get("grading")):
        if isinstance(item, dict):
            grading_rows.append([
                as_text(item.get("question_number")),
                as_text(item.get("score")),
                as_text(item.get("judgment")),
                as_text(item.get("main_issue")),
            ])
    if grading_rows:
        add_table(doc, ["题号", "得分", "判断", "主要问题"], grading_rows)
    else:
        doc.add_paragraph("暂无逐题批改数据。")

    review = data.get("review") if isinstance(data.get("review"), dict) else {}
    doc.add_heading("3. 整体复盘", level=1)
    doc.add_heading("做得好的地方", level=2)
    add_bullets(doc, review.get("strengths"))
    doc.add_heading("主要失分原因", level=2)
    add_bullets(doc, review.get("loss_reasons"))
    doc.add_heading("薄弱知识点", level=2)
    add_bullets(doc, review.get("weak_topics"))
    doc.add_heading("下次考试提醒", level=2)
    add_bullets(doc, review.get("next_exam_reminders"))

    doc.add_heading("4. 复习计划", level=1)
    plan = review.get("plan")
    if isinstance(plan, dict):
        for label in ["今天", "3天内", "7天内", "下次考试前"]:
            add_label_value(doc, label, plan.get(label))
    else:
        add_bullets(doc, plan)

    enforce_doc_font(doc)
    doc.save(output_path)


def build_wrong_book(data: dict[str, Any], output_path: Path, image_root: Path | None) -> None:
    doc = Document()
    configure_doc(doc)
    add_title(doc, "错题本", as_text(data.get("exam_name")))

    wrong_questions = [item for item in as_list(data.get("wrong_questions")) if isinstance(item, dict)]
    if not wrong_questions:
        doc.add_paragraph("暂无错题数据。")
        enforce_doc_font(doc)
        doc.save(output_path)
        return

    for index, item in enumerate(wrong_questions):
        if index:
            doc.add_page_break()
        doc.add_heading(as_text(item.get("question_number"), f"错题 {index + 1}"), level=1)
        image_path = resolve_image(item.get("original_image"), image_root)
        add_image_or_note(doc, image_path, as_text(item.get("original_question_text")))

        doc.add_heading("错题分析", level=2)
        add_label_value(doc, "知识点", item.get("topic"))
        add_label_value(doc, "题型", item.get("question_type"))
        add_label_value(doc, "我的错误", item.get("my_error"))
        add_label_value(doc, "正确方法", item.get("correct_method"))
        add_label_value(doc, "错因标签", item.get("error_labels"))
        add_label_value(doc, "下次提醒", item.get("next_reminder"))
        add_label_value(doc, "复练优先级", item.get("priority"))

        doc.add_heading("同类练习", level=2)
        practices = [p for p in as_list(item.get("similar_practice")) if isinstance(p, dict)]
        if not practices:
            doc.add_paragraph("暂无同类练习。")
        for p_index, practice in enumerate(practices, start=1):
            doc.add_heading(f"{p_index}. {as_text(practice.get('title'), '同类练习')}", level=3)
            add_label_value(doc, "训练目标", practice.get("training_goal"))
            add_label_value(doc, "难度", practice.get("difficulty"))
            add_label_value(doc, "预计用时", practice.get("estimated_time"))
            add_label_value(doc, "题目", practice.get("problem"))
            add_label_value(doc, "答案", practice.get("answer"))
            add_label_value(doc, "解析", practice.get("solution"))
            add_label_value(doc, "提醒", practice.get("reminder"))

    enforce_doc_font(doc)
    doc.save(output_path)


def build_retest(data: dict[str, Any], output_path: Path) -> None:
    doc = Document()
    configure_doc(doc)
    paper = data.get("retest_mini_paper") if isinstance(data.get("retest_mini_paper"), dict) else {}
    add_title(doc, as_text(paper.get("title"), "复测小卷"), as_text(data.get("exam_name")))

    add_label_value(doc, "来源", paper.get("source") or data.get("exam_name"))
    add_label_value(doc, "目标知识点", paper.get("target_topics"))
    add_label_value(doc, "建议用时", paper.get("suggested_time"))

    questions = [item for item in as_list(paper.get("questions")) if isinstance(item, dict)]
    doc.add_heading("题目", level=1)
    if not questions:
        doc.add_paragraph("暂无复测题。")
    for index, item in enumerate(questions, start=1):
        p = doc.add_paragraph()
        run = p.add_run(f"{index}. {as_text(item.get('problem'))}")
        apply_font(run)

    doc.add_page_break()
    doc.add_heading("答案与解析", level=1)
    if not questions:
        doc.add_paragraph("暂无答案与解析。")
    for index, item in enumerate(questions, start=1):
        doc.add_heading(f"{index}.", level=2)
        add_label_value(doc, "答案", item.get("answer"))
        add_label_value(doc, "解析", item.get("solution"))

    enforce_doc_font(doc)
    doc.save(output_path)


def is_safe_clean_dir(path: Path) -> bool:
    resolved = path.resolve()
    home = Path.home().resolve()
    protected = {
        home,
        home / "Desktop",
        home / ".codex",
        Path.cwd().resolve(),
    }
    return resolved not in protected and resolved.exists() and resolved.is_dir()


def clean_output_dir(output_dir: Path, keep_paths: set[Path]) -> None:
    if not is_safe_clean_dir(output_dir):
        raise ValueError(f"Refusing to clean unsafe output directory: {output_dir}")
    keep = {path.resolve() for path in keep_paths}
    for child in output_dir.iterdir():
        if child.resolve() in keep:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate final DOCX outputs for a math exam review.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--image-root", type=Path, default=None)
    parser.add_argument("--clean-output", action="store_true", help="Delete non-final files from output_dir after generation.")
    args = parser.parse_args()

    data = json.loads(args.input_json.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("Input JSON must be an object.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        key: args.output_dir / name
        for key, name in FINAL_NAMES.items()
    }
    image_root = args.image_root or args.input_json.parent

    build_report(data, paths["report"])
    build_wrong_book(data, paths["wrong_book"], image_root)
    build_retest(data, paths["retest"])

    if args.clean_output:
        clean_output_dir(args.output_dir, set(paths.values()))

    print(json.dumps({key: str(path) for key, path in paths.items()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
