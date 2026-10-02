# video-transcript-qa

A Claude Code skill that transcribes a local video or audio file and answers questions about what was said in it.

It works in three steps:
1. **ffmpeg** pulls the audio out of the video as a small mono MP3.
2. **AssemblyAI** turns the audio into English text and labels each speaker.
3. **Claude** reads the transcript and answers your questions, citing timestamps.

## Requirements

| Requirement | How to set it up |
|---|---|
| Python 3 | Must be on PATH |
| `assemblyai` package | `pip install assemblyai` |
| ffmpeg | Install it and make sure `ffmpeg` is on PATH (`winget install ffmpeg` on Windows) |
| AssemblyAI API key | Get a key at https://www.assemblyai.com, then run `setx ASSEMBLYAI_API_KEY "your_key"` |

After `setx`, restart VS Code / Claude Code. Programs that are already running won't see the new variable.

## Installation

Copy the `video-transcript-qa` folder into one of these skill directories:
- `~/.claude/skills/` (available in all your projects), or
- `<project>/.claude/skills/` (available in one project only)

## Usage

In Claude Code, give it a video path and ask a question:

```
Summarize "D:\Videos\team meeting.mp4"
What did Speaker B say about the deadline in "D:\Videos\team meeting.mp4"?
```

Claude uses the skill automatically. You can also run it yourself with `/video-transcript-qa`.

The first time you ask about a video, the skill transcribes it. Follow-up questions about the same video reuse that transcript.

### Running the script directly

```
python video-transcript-qa/scripts/transcribe.py "D:\Videos\team meeting.mp4"
```

## Output

The transcript is saved next to the video with the same name and a `.txt` extension (for example, `team meeting.txt`). Each line is one utterance:

```
[00:00] Speaker A: Good morning, everyone.
[00:04] Speaker B: Morning. Let's start with the release status.
```

## Configuration

Transcription settings are in [scripts/transcribe.py](scripts/transcribe.py):

```python
config = aai.TranscriptionConfig(speaker_labels=True, language_code="en",
                                 language_detection=False)
```

- `language_code="en"` makes AssemblyAI transcribe everything as English. It does **not** translate. Speech in other languages will come out as inaccurate English text.
- `speaker_labels=True` turns on speaker labels (Speaker A, B, …).

## Troubleshooting

- **Transcript didn't change after editing settings:** the script skips any video whose `.txt` file already exists. Delete that `.txt` file and run it again.
- **`ASSEMBLYAI_API_KEY is not set`:** set the key with `setx` (see Requirements), then restart VS Code / Claude Code.
- **`ffmpeg not found on PATH`:** install ffmpeg, then open a new terminal.
- **`Missing package`:** run the `pip install` command shown in the error. It targets the Python interpreter the script is running under.
- **`Transcription returned no speech`:** the file has no audio track, or the audio is silent.
