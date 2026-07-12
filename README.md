# Audio Converter

A small Python command-line utility by Eddie Saunders for converting audio files for mobile and game development.

This tool is part of the practical tooling around **One Grid at a Time (OGaaT)**: small, useful development tools built to support real game-development workflows without turning every helper script into a giant framework.

Links:

- Main site: https://eddiesaunders.com/
- Code / QA tools: https://eddiesaunders.com/code
- YouTube: https://www.youtube.com/@onegridatatime  


It started as a quick `.ogg` to `.mp3` converter, but now supports three practical conversion modes:

1. Convert one explicit file.
2. Convert all supported audio files in a folder.
3. Convert only files with selected extensions.

FFmpeg does the actual audio conversion. Python handles the workflow, folder scanning, output paths, and useful status reporting.

## Default Behavior

If you run the script with no options, it uses this default workflow:

```bash
python audio_converter.py
```

That means:

```text
./sounds/*.ogg -> ./converted/converted_YYYY-MM-DD_HH-MM-SS/*.mp3
```

Example:

```text
sounds/jump.ogg
sounds/menu_click.ogg
```

becomes:

```text
converted/converted_2026-07-12_10-45-30/jump.mp3
converted/converted_2026-07-12_10-45-30/menu_click.mp3
```

This gives you a safe default for mobile/game audio work: source files stay untouched, converted files go into a timestamped output folder.

## Scope

This project is intentionally focused:

- Convert a single audio file.
- Convert audio files in a folder.
- Convert all supported audio formats in a folder.
- Convert only selected input extensions.
- Optionally search folders recursively.
- Optionally save converted files into a chosen output folder.
- Create timestamped conversion folders when using an output folder.
- Skip files that are already in the requested output format.
- Show a clear summary of converted, skipped, and failed files.

This is not intended to be a full digital audio workstation, editor, tag manager, or batch mastering tool. It is a focused conversion utility for practical game/audio asset workflows.

## Requirements

- Python 3.10 or newer recommended.
- FFmpeg installed separately and available on your system PATH.

FFmpeg website:

```text
https://ffmpeg.org/
```

No Python packages are required.

## Install FFmpeg

macOS with Homebrew:

```bash
brew install ffmpeg
```

Windows with winget:

```powershell
winget install Gyan.FFmpeg
```

Windows with Chocolatey:

```powershell
choco install ffmpeg
```

Ubuntu / Debian Linux:

```bash
sudo apt update
sudo apt install ffmpeg
```

Fedora Linux:

```bash
sudo dnf install ffmpeg
```

Arch Linux:

```bash
sudo pacman -S ffmpeg
```

Check FFmpeg is available after installing:

```bash
ffmpeg -version
```

If that command prints FFmpeg version information, the converter is ready to use.

## Files

```text
audio_converter.py
README.md
```

## Conversion Modes

### 1. Convert one explicit file

Convert a single named file to the default output format, `.mp3`:

```bash
python audio_converter.py --file sounds/eddieSound.ogg
```

Result:

```text
sounds/eddieSound.ogg -> sounds/eddieSound.mp3
```

Convert one file to a specific output format:

```bash
python audio_converter.py --file sounds/eddieSound.ogg --format flac
```

Result:

```text
sounds/eddieSound.ogg -> sounds/eddieSound.flac
```

Save the converted file into a timestamped output folder:

```bash
python audio_converter.py --file sounds/eddieSound.ogg --format mp3 --output-dir converted
```

Result:

```text
converted/converted_YYYY-MM-DD_HH-MM-SS/eddieSound.mp3
```

### 2. Convert an entire folder of supported audio

Convert every supported audio file in a folder to `.mp3`:

```bash
python audio_converter.py --folder sounds --all-audio --format mp3
```

Example input:

```text
sounds/jump.ogg
sounds/hit.wav
sounds/theme.flac
sounds/menu.mp3
sounds/notes.txt
```

Result:

```text
sounds/jump.mp3       created
sounds/hit.mp3        created
sounds/theme.mp3      created
sounds/menu.mp3       skipped, already .mp3
sounds/notes.txt      skipped, unsupported file type
```

Save the results to a timestamped output folder:

```bash
python audio_converter.py --folder sounds --all-audio --format mp3 --output-dir converted
```

Result:

```text
converted/converted_YYYY-MM-DD_HH-MM-SS/jump.mp3
converted/converted_YYYY-MM-DD_HH-MM-SS/hit.mp3
converted/converted_YYYY-MM-DD_HH-MM-SS/theme.mp3
```

### 3. Convert only specific extensions

Convert only `.wav` files in a folder to `.aac`:

```bash
python audio_converter.py --folder sounds --input-formats wav --format aac
```

Example input:

```text
sounds/jump.wav
sounds/hit.wav
sounds/music.ogg
sounds/theme.mp3
```

Result:

```text
sounds/jump.aac       created
sounds/hit.aac        created
sounds/music.ogg      skipped, not part of selected input filter
sounds/theme.mp3      skipped, not part of selected input filter
```

Convert multiple selected input formats:

```bash
python audio_converter.py --folder sounds --input-formats ogg wav flac --format mp3
```

## Recursive Folder Conversion

Use `--recursive` to include subfolders:

```bash
python audio_converter.py --folder sounds --all-audio --format mp3 --recursive --output-dir converted
```

Example input:

```text
sounds/sfx/jump.ogg
sounds/sfx/hit.wav
sounds/music/theme.flac
```

Result:

```text
converted/converted_YYYY-MM-DD_HH-MM-SS/sfx/jump.mp3
converted/converted_YYYY-MM-DD_HH-MM-SS/sfx/hit.mp3
converted/converted_YYYY-MM-DD_HH-MM-SS/music/theme.mp3
```

The folder structure is preserved when using `--recursive` with `--output-dir`.

## Timestamped Output Folders

When `--output-dir` is used, the converter creates a timestamped folder inside it by default:

```bash
python audio_converter.py --folder sounds --all-audio --output-dir converted
```

Example output folder:

```text
converted/converted_2026-07-12_10-45-30/
```

This makes conversion runs easy to separate and avoids accidentally mixing old and new files.

To write directly into the output folder without creating a timestamped subfolder, use:

```bash
python audio_converter.py --folder sounds --all-audio --output-dir converted --no-run-folder
```

## Dry Run

Preview what would happen without creating files:

```bash
python audio_converter.py --folder sounds --all-audio --format mp3 --output-dir converted --dry-run
```

This prints the FFmpeg commands that would run.

## Overwriting Existing Files

By default, existing converted files are skipped.

Use `--overwrite` to replace them:

```bash
python audio_converter.py --folder sounds --input-formats ogg --format mp3 --overwrite
```

## Supported Input Formats

The `--all-audio` option currently recognizes these input formats:

```text
aac, aif, aiff, flac, m4a, mp3, oga, ogg, opus, wav, wma
```

FFmpeg may support more formats, but this list keeps the tool predictable for game/audio asset workflows.

## Output Formats

Common output formats:

```text
mp3, aac, m4a, ogg, opus, flac, wav
```

Examples:

```bash
python audio_converter.py --folder sounds --all-audio --format mp3
python audio_converter.py --folder sounds --all-audio --format flac
python audio_converter.py --folder sounds --input-formats wav --format aac
python audio_converter.py --file sounds/theme.flac --format m4a
```

## Status Output

The converter reports what happened to each file:

```text
[CONVERT]   sounds/jump.ogg -> converted/converted_YYYY-MM-DD_HH-MM-SS/jump.mp3
[SKIPPED]   sounds/theme.mp3 - already .mp3
[SKIPPED]   sounds/notes.txt - Unsupported file type.
[SKIPPED]   sounds/hit.wav - output already exists: sounds/hit.mp3
[FAILED]    sounds/broken.ogg
```

At the end, it prints a summary:

```text
Audio conversion complete.
Converted: 12
Would convert: 0
Already target format: 4
Unsupported files skipped: 2
Existing outputs skipped: 1
Missing files: 0
Failed: 0
```

## Options

| Option | Purpose |
|---|---|
| `--file` | Convert one explicit file. |
| `--folder` | Convert files in a folder. |
| `--all-audio` | Convert every supported audio file in folder mode. |
| `--input-formats` | Convert only selected extensions in folder mode. Example: `--input-formats ogg wav flac`. |
| `--format` | Output format. Default: `mp3`. |
| `--bitrate` | Audio bitrate for compressed formats. Default: `192k`. |
| `--output-dir` | Place converted files in a chosen folder. Creates a timestamped run folder by default. |
| `--no-run-folder` | Do not create a timestamped folder inside `--output-dir`. |
| `--recursive` | Include subfolders in folder mode. |
| `--overwrite` | Replace existing output files. |
| `--dry-run` | Print conversion commands without running them. |

## Practical Examples

Default mobile/game audio conversion:

```bash
python audio_converter.py
```

Convert all `.ogg` files in `sounds` to `.mp3` beside the originals:

```bash
python audio_converter.py --folder sounds --input-formats ogg --format mp3
```

Convert every supported audio file in `sounds` to `.mp3`:

```bash
python audio_converter.py --folder sounds --all-audio --format mp3
```

Convert every supported audio file recursively and save to a dated output folder:

```bash
python audio_converter.py --folder sounds --all-audio --recursive --output-dir converted --format mp3
```

Convert only `.wav` files to `.aac`:

```bash
python audio_converter.py --folder sounds --input-formats wav --format aac
```

Convert `.ogg`, `.wav`, and `.flac` files to `.m4a`:

```bash
python audio_converter.py --folder sounds --input-formats ogg wav flac --format m4a
```

Preview a conversion run:

```bash
python audio_converter.py --folder sounds --all-audio --format mp3 --output-dir converted --dry-run
```

## Freeware and Optional Support

This software is freeware. You can use it for personal projects, game-development experiments, learning, content creation, and internal tooling.

If you like the tool, use it in your own workflow, and want to support more small utilities, OGaaT content, and Eddie Saunders projects, you can optionally buy me a coffee here:

https://paypal.me/edwynsaunders1

Support is completely optional. The tool remains free to use.

## Project Links

- Main site: https://eddiesaunders.com/
- Code / QA tools: https://eddiesaunders.com/code
- YouTube: https://www.youtube.com/@onegridatatime  

## Notes for Mobile/Game Development

- `.mp3` is broadly compatible and a safe first target for many mobile workflows.
- `.aac` / `.m4a` can be useful for mobile audio too, especially for music or longer clips.
- Keep your original source audio files.
- Use `--output-dir converted` when you want clean export batches.
- Use `--recursive` when your game audio is organized into folders like `sfx`, `music`, and `ui`.
- Use `--dry-run` before big conversions so you can confirm exactly what will happen before files are created.
