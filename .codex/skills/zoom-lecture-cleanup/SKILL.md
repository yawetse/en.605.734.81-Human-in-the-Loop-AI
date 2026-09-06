---
name: zoom-lecture-cleanup
description: Clean EN.605.734 Zoom lecture recording exports into course-content Markdown. Use when the user has Zoom-generated lecture HTML or a noisy imported Markdown file and wants to keep only the audio transcript and next steps, preserve existing Markdown metadata, and remove player controls, navigation, speaker/avatar markup, footer links, cookie notices, and other non-course HTML/UI content.
---

# Zoom Lecture Cleanup

## Workflow

Use this skill to clean an EN.605.734 Zoom recording export into the same Markdown shape as the user's cleaned lecture notes:

```markdown
---
existing metadata block, if present
---
## Audio Transcript

- transcript segment
- transcript segment

## Next Steps

1. next step
2. next step
```

Keep the transcript and next-step wording as exported. Do not rewrite, summarize, fix typos, or polish the course text unless the user explicitly asks for editing.

## Preferred Script

Use the `scripts/clean_zoom_lecture.py` file in this skill folder for the common case where there is a Zoom HTML file and a matching Markdown file:

```bash
python3 <skill-folder>/scripts/clean_zoom_lecture.py \
  "Module 01/lecture-1-2.html" \
  --markdown "Module 01/lecture-1-2.md"
```

The script:

- extracts transcript items from `ul.transcript-list`
- extracts next steps from `div.step-area`
- preserves Zoom's `Next steps are not available.` message when numbered next steps are absent
- preserves the existing `--- ... ---` metadata block from the Markdown file when present
- writes only `## Audio Transcript` and `## Next Steps`
- removes Zoom UI, player controls, footer, cookie notices, avatars, speaker labels, and raw HTML wrappers

Use `--output <path>` to write to a different file instead of replacing the Markdown file.

## Manual Fallback

If the script cannot parse the export:

1. Read the cleaned example the user points to and match its structure.
2. In the Zoom HTML, find the `Audio Transcript` section and extract only transcript text from transcript list items.
3. Find `Next Steps` and extract only the numbered next-step text.
4. Preserve the frontmatter metadata block from the target Markdown file if it exists.
5. Remove all links, images, base64 avatars, controls, summaries, smart chapters, footers, download links, support links, and cookie/privacy UI unless the user asks to keep them.
6. Verify with a search for leftover UI markers such as `Skip to Main`, `Zoom Logo`, `Cookie Preference`, `Download`, `data:image`, `Resume autoscrolling`, and raw HTML tags.

## Validation

After writing the cleaned Markdown:

```bash
rg -n "Skip to Main|Accessibility Overview|Zoom Logo|Cookie Preference|Download|data:image|Resume autoscrolling|<[^>]+>" "path/to/lecture.md" || true
```

Review the first page and tail of the file to confirm it contains only metadata, `## Audio Transcript`, transcript bullets, `## Next Steps`, and numbered steps.
