---
name: video-transcript-qa
description: Transcribe a local video file (extract audio with ffmpeg, transcribe
  with AssemblyAI) and answer questions about its content. Use when the user gives
  a path to a video/audio recording and wants a transcript, summary, or answers
  based on what was said.
---

# Video transcript Q&A

## Workflow
1. Run: `python "${CLAUDE_SKILL_DIR}/scripts/transcribe.py" "<video_path>"`
   - Always use the absolute script path above; the working directory is the
     user's project, not this skill folder.
   - Quote the video path (Windows paths often contain spaces).
   - Skips work if `<video_name>.txt` already exists next to the video.
   - Requires `pip install assemblyai`, `ASSEMBLYAI_API_KEY` in the environment,
     and `ffmpeg` on PATH. If the script reports one of these missing, tell the
     user how to fix it instead of retrying.
2. Read the transcript file saved next to the video.
3. Answer the user's questions using only the transcript. Quote or cite
   timestamps when helpful. If the answer isn't in the transcript, say so.

## Notes
- For long transcripts, grep/read relevant sections instead of loading everything.
- Follow-up questions should reuse the existing transcript, not re-transcribe.