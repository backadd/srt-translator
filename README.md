# SRT Translator

A tool to translate subtitle files (.srt) using OpenAI's GPT models.

## Installation

```bash
pip install -e .
```

## API Key Setup

There are several ways to provide your OpenAI API key:

1. **Environment variable**:

   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

2. **.env file**:
   Create a `.env` file in the project directory:

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Command-line argument**:

   ```bash
   python main.py input.srt Swedish English --api-key your_api_key_here
   ```

4. **Save for future use**:
   ```bash
   python main.py input.srt Swedish English --api-key your_api_key_here --save-key
   ```
   This will save the key to `~/.srt-translator/config.json`

## Usage

```bash
python main.py input.srt source_language target_language [options]
```

### Options

- `--api-key KEY`: Provide OpenAI API key
- `--save-key`: Save the provided API key for future use
- `--output PATH, -o PATH`: Specify output file path (default: output.srt)

### Examples

```bash
# Translate from Swedish to English
python main.py subtitles.srt Swedish English

# Specify output file
python main.py subtitles.srt Swedish English -o translated.srt

# Provide API key and save it
python main.py subtitles.srt Swedish English --api-key sk-... --save-key

```
