# math-exam-review

面向学生的数学试卷批改、复盘、错题整理和同类题生成 Codex Skill。

这个 skill 用来处理用户上传的已完成数学试卷图片、PDF 或扫描件，帮助学生完成从批改到复习的闭环：

- 批改试卷并估算得分
- 分析错因和薄弱知识点
- 生成学生版复盘报告
- 整理带原题图片的错题本
- 在每道错题下生成同类练习
- 单独生成复测小卷

## 适用范围

- 小学数学
- 初中数学
- 高中数学
- 常见大学数学：微积分、线性代数、概率统计

## 默认输出

完整流程默认只保留三个 Word 文件：

1. `批改与复盘报告.docx`
2. `错题本.docx`
3. `复测小卷.docx`

其中：

- `错题本.docx` 按每道错题分章节组织，不使用大表格。
- 每道错题尽量嵌入原题截图。
- 每道错题下面直接附同类练习、答案和解析。
- 三份 Word 文档统一使用宋体。

## 目录结构

```text
math-exam-review/
  SKILL.md
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

## 核心脚本

`scripts/generate_docx_outputs.py`

根据结构化 JSON 数据生成三份最终 DOCX：

- `批改与复盘报告.docx`
- `错题本.docx`
- `复测小卷.docx`

支持把错题原图嵌入错题本，并可在完整流程结束后清理中间文件。

## 使用方式

在 Codex 中调用：

```text
Use $math-exam-review 批改我的数学试卷，并生成三个 Word 文件：复盘报告、错题本和复测小卷。
```

如果需要安装到本地 Codex skills 目录，可将整个 `math-exam-review` 文件夹复制到：

```text
C:\Users\<你的用户名>\.codex\skills\
```
