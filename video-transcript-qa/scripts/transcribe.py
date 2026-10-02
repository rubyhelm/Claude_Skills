import os, shutil, subprocess, sys, tempfile
from pathlib import Path

# Avoid UnicodeEncodeError on Windows consoles with non-UTF-8 code pages
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import assemblyai as aai
except ImportError:
    sys.exit(f"Missing package. Run: \"{sys.executable}\" -m pip install assemblyai")

if len(sys.argv) < 2:
    sys.exit("Usage: python transcribe.py <video_path>")

video = Path(sys.argv[1]).expanduser().resolve()
if not video.is_file():
    sys.exit(f"Video not found: {video}")

out_txt = video.with_suffix(".txt")
if out_txt.exists():
    print(f"Transcript already exists: {out_txt}"); sys.exit(0)

api_key = os.environ.get("ASSEMBLYAI_API_KEY")
if not api_key:
    sys.exit("ASSEMBLYAI_API_KEY is not set. On Windows run:\n"
             '  setx ASSEMBLYAI_API_KEY "your_key"\n'
             "then restart VS Code / Claude Code so it picks up the new variable.")
aai.settings.api_key = api_key

ffmpeg = shutil.which("ffmpeg")
if not ffmpeg:
    sys.exit("ffmpeg not found on PATH.")

with tempfile.TemporaryDirectory() as tmp:
    audio = Path(tmp) / "audio.mp3"
    result = subprocess.run(
        [ffmpeg, "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000",
         "-b:a", "64k", str(audio)],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        sys.exit(f"ffmpeg failed:\n{result.stderr[-2000:]}")

    config = aai.TranscriptionConfig(speaker_labels=True, language_code="en",
                                     language_detection=False)
    transcript = aai.Transcriber().transcribe(str(audio), config)

if transcript.status == aai.TranscriptStatus.error:
    sys.exit(f"Transcription failed: {transcript.error}")

if not transcript.utterances:
    sys.exit("Transcription returned no speech.")

lines = [f"[{u.start//1000//60:02d}:{u.start//1000%60:02d}] Speaker {u.speaker}: {u.text}"
         for u in transcript.utterances]
out_txt.write_text("\n".join(lines), encoding="utf-8")
print(f"Saved: {out_txt}")
