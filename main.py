import argparse
import re
import sys

from openai import OpenAI
from tqdm import tqdm

from config import load_api_key, save_api_key


def translate_text(
    client: OpenAI, text: str, source_language: str, target_language: str
) -> str:
    """
    Translate a chunk of SRT content using OpenAI.
    """
    prompt = (
        f"Translate this srt file from {source_language} to {target_language}, "
        "reply only with the translated srt file and add no commentary or information:\n\n"
        f"{text}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-5-chat-latest",  # faster for longer text
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error during translation: {e}")
        sys.exit(1)


def read_srt(file_path: str) -> str:
    with open(file_path, "r") as file:
        content = file.read().strip().split("\n\n")
    return [content[i : i + 50] for i in range(0, len(content), 50)]


def format_subtitles(srt_data: str) -> str:
    # Normalize line endings to Unix-style just in case
    srt_data = srt_data.replace("\r\n", "\n").replace("\r", "\n")

    # Remove file information that Open AI adds
    srt_data = (
        srt_data.replace("```plaintext", "").replace("```srt", "").replace("```", "")
    )

    # Step 1: Clean up the text by removing extra newlines within blocks
    # Replace multiple newlines with a single newline within each block
    srt_data = re.sub(r"(\n)(?!\n)", r"\1", srt_data)

    # Step 2: Insert a blank line between each subtitle block
    # Define a regular expression pattern to match the end of each subtitle block
    # This pattern looks for the end of the text followed by one or more newlines and the start of the next block
    pattern = re.compile(r"(?<=\S)(\n)(?=\d+\n\d{2}:\d{2}:\d{2},\d{3} --> )", re.DOTALL)

    # Insert a newline at each match position to create a blank line between blocks
    formatted_srt = pattern.sub(r"\n\n", srt_data)

    # Ensure the file doesn't start or end with extra newlines
    formatted_srt = formatted_srt.strip() + "\n"

    return formatted_srt


def main():
    parser = argparse.ArgumentParser(
        description="Supply the path to the srt file to be translated, the original language and the target language"
    )
    parser.add_argument("file_path", type=str, help="SRT file path")
    parser.add_argument(
        "source_lang", type=str, help="Language of the SRT file", default="Swedish"
    )
    parser.add_argument(
        "target_lang", type=str, help="Target language", default="English"
    )
    parser.add_argument("--api-key", type=str, help="OpenAI API key", default=None)
    parser.add_argument(
        "--save-key", action="store_true", help="Save the API key for future use"
    )
    parser.add_argument(
        "--output", "-o", type=str, help="Output file path", default="output.srt"
    )
    args = parser.parse_args()

    # Load API key from various sources
    api_key = load_api_key(args.api_key)

    # If API key is provided and --save-key flag is set, save it
    if args.api_key and args.save_key:
        save_api_key(args.api_key)

    # Check if API key is available
    if not api_key:
        print(
            "Error: OpenAI API key not found. Please provide it using one of these methods:"
        )
        print("  1. Set OPENAI_API_KEY environment variable")
        print("  2. Create a .env file with OPENAI_API_KEY=your_key")
        print("  3. Use --api-key command-line argument")
        print("  4. Use --api-key with --save-key to save for future use")
        sys.exit(1)

    lines = read_srt(args.file_path)
    results = ""
    client = OpenAI(api_key=api_key)

    for line in tqdm(lines, desc="Translating srt", unit="chunks"):
        translated_line = translate_text(
            client, "\n".join(line), args.source_lang, args.target_lang
        )
        results += translated_line + "\n"

    formated_results = format_subtitles(results)

    with open(args.output, "w") as file:
        file.write(formated_results)

    print(f"Translation completed. Output saved to {args.output}")


if __name__ == "__main__":
    main()
