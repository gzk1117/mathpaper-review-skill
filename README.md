# mathpaper-review-skill

面向学生的数学试卷批改、复盘、错题整理和同类题巩固工作流。

这个仓库既可以作为 Codex Skill 使用，也可以被 Claude Code、其它 AI agent 或人工脚本流程复用。核心目标是把一份已完成的数学试卷转化为三个可直接交付给学生的 Word 文件：

1. `批改与复盘报告.docx`
2. `错题本.docx`
3. `复测小卷.docx`

## 能做什么

- 批改数学试卷并估算得分
- 分析错因、薄弱知识点和可提分方向
- 生成学生友好的复盘报告
- 生成带原题图片的错题本
- 在每道错题下面生成同类练习、答案和解析
- 单独生成复测小卷
- 完整流程结束后只保留三个最终 Word 文件

## 适用范围

- 小学数学
- 初中数学
- 高中数学
- 常见大学数学：微积分、线性代数、概率统计

## 目录结构

```text
mathpaper-review-skill/
  SKILL.md
  USAGE.md
  agents/
    openai.yaml
  references/
    workflow.md
    grading-policy.md
    error-taxonomy.md
    output-templates.md
    math-topic-map.md
    similar-question-generation.md
  scripts/
    generate_docx_outputs.py
```

## 快速使用

### Codex

将整个仓库文件夹放入本地 Codex skills 目录：

```text
C:\Users\<你的用户名>\.codex\skills\mathpaper-review-skill
```

然后在 Codex 中调用：

```text
Use $math-exam-review 批改我的数学试卷，并生成三个 Word 文件：复盘报告、错题本和复测小卷。
```

### Claude Code

在 Claude Code 中打开本仓库，要求它读取 `SKILL.md` 和 `references/` 中的相关规则：

```text
Use this repository as a math exam review workflow.
Read SKILL.md first, then load the needed files under references/.
Review the attached math paper and generate the final three DOCX files:
批改与复盘报告.docx, 错题本.docx, 复测小卷.docx.
Follow output-templates.md and use scripts/generate_docx_outputs.py when structured data is ready.
```

### Other Agents Or Manual Use

其它 AI agent 或人工流程可以把 `SKILL.md` 当作入口说明，把 `references/` 当作规则库，并在最后调用：

```bash
python scripts/generate_docx_outputs.py review_data.json output_dir --image-root image_dir --clean-output
```

详细说明见 [USAGE.md](USAGE.md)。

## 输出规范

- 三份 Word 文档统一使用宋体。
- `错题本.docx` 不使用大表格，而是每道错题一个章节。
- 每道错题尽量嵌入原题截图。
- 每道错题下面直接附同类练习、答案和解析。
- `复测小卷.docx` 单独成卷，题目和答案解析分开。

## 依赖

脚本生成 DOCX 需要 Python 和 `python-docx`：

```bash
pip install python-docx
```

如果要自动裁剪试卷图片，可额外使用 Pillow：

```bash
pip install pillow
```
