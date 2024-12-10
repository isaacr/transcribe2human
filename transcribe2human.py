#!/usr/local/bin/python3

# Used to take a speaker diariazed .json from Amazon Transcribe, and convert it into a human-readable txt
#
# (just a dad happy to be helping my daughter)


import json
import argparse

def convert_transcribe_json_to_text(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)

        if "results" not in data or "items" not in data["results"]:
            raise ValueError("Invalid Amazon Transcribe JSON structure.")

        items = data["results"]["items"]
        segments = data["results"].get("speaker_labels", {}).get("segments", [])

        transcript = []

        for segment in segments:
            speaker_label = segment["speaker_label"]
            start_time = float(segment["start_time"])
            end_time = float(segment["end_time"])

            text = ""

            for item in items:
                if "start_time" in item and "end_time" in item:
                    item_start_time = float(item["start_time"])
                    item_end_time = float(item["end_time"])

                    if item_start_time >= start_time and item_end_time <= end_time:
                        if item.get("alternatives"):
                            text += item["alternatives"][0].get("content", "") + " "

            transcript.append(f"[Speaker {speaker_label.split('_')[-1]}] ({start_time:.2f}-{end_time:.2f}): {text.strip()}")

        with open(output_file, 'w') as out:
            out.write("\n".join(transcript))

        print(f"Transcript successfully written to {output_file}")

    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Amazon Transcribe JSON to human-readable text.")
    parser.add_argument("input_file", help="Path to the input JSON file.")
    parser.add_argument("output_file", help="Path to the output text file.")

    args = parser.parse_args()
    convert_transcribe_json_to_text(args.input_file, args.output_file)

