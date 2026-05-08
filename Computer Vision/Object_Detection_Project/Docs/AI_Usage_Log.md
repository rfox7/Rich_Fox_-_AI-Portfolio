# AI Usage Log

---

## 1. Understanding Midterm Requirements & Deliverables

- **Date**: May 8, 2026
- **Tool Used**: NotebookLM
- **Question Asked**: "Can I get a step-by-step guide for what I need to turn in for the midterm?"
- **What I Learned**: I learned that the midterm is not just about the slides; it requires a specific GitHub repository structure (notebooks/, data/, docs/) and a detailed proposal README. I also understood the importance of documenting AI usage in a separate log file to satisfy the grading rubric.
- **How I Applied It**: I organized my local project files into the required GitHub structure and verified that my repository is ready for public submission.

---

## 2. Project Tiering and Model Selection Justification

- **Date**: May 8, 2026
- **Tool Used**: NotebookLM
- **Question Asked**: "Review my midterm slides and confirm if my project aligns with the requirements."
- **What I Learned**: I learned that using **YOLOv8n** for real-time license plate detection is a classic **Tier 1** task. I understood the specific architectural benefits of YOLOv8 Nano, such as the **Decoupled Head** and **Task-Aligned Assigner**, which make it effective for detecting small localized objects like plates at high speeds.
- **How I Applied It**: I updated my project README to include a technical justification for my choice of model, highlighting its balance of speed and precision for edge deployment.

---

## 3. Refining the Technical Pipeline (Two-Stage Approach)

- **Date**: May 8, 2026
- **Tool Used**: NotebookLM
- **Problem Encountered**: "Need help defining the end-to-end technical approach for both detection and recognition."
- **What I Learned**: I learned that a two-stage pipeline is more effective for this task: using **YOLOv8** for high-speed localization and **EasyOCR** (which uses CRAFT and CRNN) for extracting alphanumeric text. This ensures that the recognition stage only processes the relevant cropped region, reducing total pipeline latency.
- **How I Applied It**: I formally documented this two-stage technical approach in my solution overview and added EasyOCR to my requirements.txt file.

---

## 4. Final Pre-Submission Verification

- **Date**: May 8, 2026
- **Tool Used**: NotebookLM
- **Problem Encountered**: "Finalizing my submission before the midnight deadline."
- **What I Learned**: I learned that for the final submission to be valid, all links in the README must be working, the repository must be public, and I must submit both the GitHub link and the slides on Canvas. I also realized that while I don't have a live demo today, the final presentation in December *will* require one.
- **How I Applied It**: I conducted a final review of my repository links and ensured my AI Usage Log was complete and placed in the correct docs/ directory.

---

## 5. Building a License Plate Detection & Recording Pipeline

- **Date**: May 8, 2026
- **Tool Used**: Claude (Anthropic)
- **Problem Encountered**: "How can I brainstorm ways to handle poor detection of plates? I Also want to save the results so that they can be returned in output to the user."
- **What I Learned**: I learned how to structure a full end-to-end detection pipeline in a Jupyter notebook, combining **YOLOv8** for plate localization with **EasyOCR** for text extraction. I also learned how to apply **CLAHE contrast enhancement** and **unsharp mask sharpening** as preprocessing steps to improve OCR accuracy on blurry or low-contrast plate crops. Additionally, I learned how to store structured results — including base64-encoded plate images — in a **Parquet file** using PyArrow, and how to implement a **15-minute deduplication window** to avoid recording the same plate repeatedly within a short time span.
- **How I Applied It**: I now have a working Jupyter notebook (`license_plate_detector.ipynb`) that scans a `watch_videos/` folder at startup, processes all video files found, saves detections to `plate_detections.parquet`, and provides a `view_detections()` function that renders a styled HTML table with plate text, confidence scores, timestamps, source filenames, and inline plate crop images.

---

## 6. Fixing Duplicate & Fragment Detections

- **Date**: May 8, 2026
- **Tool Used**: Claude (Anthropic)
- **Problem Encountered**: "The pipeline was producing repeated records of the same vehicle with slightly different plate text (e.g. HHOICK7763, HHO1CY7763, HH01CV7763), as well as short fragments like 3689 and HORN being logged as valid plates."
- **What I Learned**: I learned that OCR engines naturally produce slightly different readings of the same plate across frames due to motion blur, lighting variation, and character ambiguity (e.g. 0 vs O, 1 vs I). Exact-string deduplication is insufficient for this reason. The correct solution is **Levenshtein edit distance** (fuzzy matching), which measures the minimum number of character insertions, deletions, and substitutions needed to convert one string into another — allowing near-identical plate reads to be collapsed into a single record. I also learned that raising the minimum plate length and OCR confidence threshold are effective first-line filters for eliminating low-quality fragment detections.
- **How I Applied It**: I updated the notebook (`license_plate_detector_v4.ipynb`) with three targeted fixes: (1) a fuzzy dedup function using edit distance with a configurable threshold of 2 characters, applied both within a single video run and against the 15-minute rolling window in the Parquet file; (2) minimum plate length raised from 4 to 6 characters to filter out fragments; and (3) minimum OCR confidence raised from 30% to 50% to reduce noise. All three parameters are exposed in the config cell for easy tuning.

---

## Summary Statistics

- **Total Major AI Interactions**: 6
- **AI Tools Used**: NotebookLM (4 interactions), Claude — Anthropic (2 interactions)
- **Breakdown by Purpose**:
  - Learning CV concepts: 29%
  - Planning & Organization: 29%
  - Technical Justification: 14%
  - Implementation & Coding: 28%
- **Code/Documentation Attribution**:
  - Proposal/README Documentation: 50% written by me, 50% AI-assisted refinement.
  - Technical Pipeline Design: 70% my original plan, 30% AI-refined justification.
  - License Plate Detector Notebook: 60% my direction, code and requirements, 40% AI-generated code.

---

## Reflection

- **What Worked Well**: Using AI allowed me to quickly translate my project ideas into a professional, structured proposal that meets all academic requirements. It helped me understand *why* certain models were better choices, rather than just using them blindly. Using Claude to upgrade the detection notebook saved significant implementation time and surfaced practical considerations (such as Windows file-watcher behaviour and parquet processing) that I would not have anticipated on my own.
- **What I Was Careful About**: I made sure to verify the technical details of YOLOv8 provided by the AI against the official documentation to ensure my technical justification was accurate.
- **Future Improvements**: As I move into the implementation phase in Week 11, I plan to use AI tools primarily for debugging training errors and optimizing my video processing loop.

---

*Confidential — Internal Use Only*
