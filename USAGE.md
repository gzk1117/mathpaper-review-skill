# Usage Guide

This project can be used as a Codex Skill, a Claude Code workflow, a reference package for other AI agents, or a manual DOCX generation pipeline.

## 1. Codex Skill Usage

Copy or clone this repository into the Codex skills directory:

```text
C:\Users\<your-user-name>\.codex\skills\mathpaper-review-skill
```

Restart Codex if needed, then invoke:

```text
Use $math-exam-review 批改我的数学试卷，并生成三个 Word 文件：复盘报告、错题本和复测小卷。
```

Codex should:

1. Read `SKILL.md`.
2. Load only the necessary files under `references/`.
3. Inspect the uploaded paper images/PDF.
4. Build structured review data.
5. Crop original question images for wrong-question entries when possible.
6. Run `scripts/generate_docx_outputs.py`.
7. Keep only the three final DOCX files unless the user asks to keep intermediates.

## 2. Claude Code Usage

Open this repository in Claude Code and use a prompt like:

```text
Use this repository as a math exam review workflow.

Read SKILL.md first. For this task, load:
- references/workflow.md
- references/grading-policy.md
- references/error-taxonomy.md
- references/output-templates.md
- references/math-topic-map.md
- references/similar-question-generation.md

Review the attached completed math paper.
Generate structured JSON data that matches references/output-templates.md.
Crop original wrong-question images where possible.
Then run scripts/generate_docx_outputs.py to create:
1. 批改与复盘报告.docx
2. 错题本.docx
3. 复测小卷.docx

Use 宋体 throughout the Word documents.
```

If Claude Code cannot execute scripts in your environment, ask it to produce the structured JSON first, then run the script manually.

## 3. Other Agents

For other AI agents, use this repository as a portable instruction package:

- `SKILL.md`: entry point, trigger conditions, default workflow
- `references/workflow.md`: full process and output discipline
- `references/grading-policy.md`: grading rules
- `references/error-taxonomy.md`: mistake labels
- `references/output-templates.md`: final DOCX contract and JSON shape
- `references/math-topic-map.md`: topic tagging
- `references/similar-question-generation.md`: similar practice and retest generation rules
- `scripts/generate_docx_outputs.py`: deterministic DOCX renderer

Recommended agent prompt:

```text
You are using the mathpaper-review-skill repository.
Follow SKILL.md as the entry workflow.
Use the references files as the grading and output specification.
Produce structured review_data.json, crop wrong-question images if available,
then call scripts/generate_docx_outputs.py to produce the three final DOCX files.
Do not leave intermediate files in the final output folder.
```

## 4. Manual Use

Manual use has two stages:

1. Prepare `review_data.json`.
2. Run the DOCX generator.

### 4.1 Minimal JSON Shape

```json
{
  "level": "小学三年级下",
  "exam_name": "数学期末试卷",
  "estimated_score": "仅估算",
  "total_score": "100",
  "wrong_items": ["第1题", "第6题(2)"],
  "partial_items": ["第1题"],
  "needs_review_items": ["第2页缺失"],
  "main_problem": "面积单位和周长面积题型不稳。",
  "grading": [
    {
      "question_number": "第1题",
      "score": "部分正确",
      "judgment": "部分正确",
      "main_issue": "面积单位写成长度单位。"
    }
  ],
  "review": {
    "strengths": ["基础计算较稳。"],
    "loss_reasons": ["单位意识不稳定。"],
    "weak_topics": ["长度单位与面积单位"],
    "next_exam_reminders": ["看到面积要写平方单位。"],
    "plan": {
      "今天": "订正错题。",
      "3天内": "完成同类练习。",
      "7天内": "完成复测小卷。",
      "下次考试前": "复习易错口诀。"
    }
  },
  "wrong_questions": [
    {
      "question_number": "第1题",
      "topic": "长度单位与面积单位",
      "question_type": "单位填空",
      "original_image": "wrong_q1.jpg",
      "my_error": "把面积单位写成长度单位。",
      "correct_method": "面积要使用平方单位。",
      "error_labels": ["concept unclear", "notation issue"],
      "next_reminder": "看到面积就写带“平方”的单位。",
      "priority": "High",
      "similar_practice": [
        {
          "title": "平行同类题",
          "training_goal": "区分长度单位和面积单位",
          "difficulty": "基础",
          "estimated_time": "2分钟",
          "problem": "课桌高约70（  ），桌面面积约24（  ）。",
          "answer": "厘米；平方分米",
          "solution": "高是长度，桌面面积是面积。",
          "reminder": "先判断长度还是面积。"
        }
      ]
    }
  ],
  "retest_mini_paper": {
    "title": "复测小卷",
    "source": "数学期末试卷错题",
    "target_topics": ["长度单位与面积单位"],
    "suggested_time": "10分钟",
    "questions": [
      {
        "problem": "填单位：橡皮长约5（  ）。",
        "answer": "厘米",
        "solution": "橡皮长是长度。"
      }
    ]
  }
}
```

### 4.2 Generate DOCX Files

```bash
python scripts/generate_docx_outputs.py review_data.json output_dir --image-root image_dir --clean-output
```

Arguments:

- `review_data.json`: structured review data.
- `output_dir`: folder for final files.
- `--image-root`: folder containing cropped original question images.
- `--clean-output`: remove non-final files from `output_dir` after generation.

The script outputs:

```text
批改与复盘报告.docx
错题本.docx
复测小卷.docx
```

## 5. Notes

- If a question image cannot be cropped reliably, omit `original_image` and use `original_question_text`.
- If the uploaded paper is incomplete, list missing pages or unclear items in `needs_review_items`.
- If no answer key is available, mark scoring as estimated.
- The DOCX generator enforces 宋体 for titles, headings, body text, tables, exercises, answers, and explanations.
