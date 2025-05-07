import sys
import argparse
import os
import subprocess
import tempfile

def main():
    # Use argparse to take a single command-line argument, the directory to process
    parser = argparse.ArgumentParser(description="Fix hev1 x265 files in a directory.")
    parser.add_argument("directory", type=str, help="Directory containing the x265 files to process.")
    args = parser.parse_args()

    # Recursively find all .mp4 files that are x265 but have an hev1 tag
    directory = args.directory
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)
    # make temporary directory for ffmpeg outputs
    temp_dir = tempfile.mkdtemp()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp4"):
                # use exiftool to check if the file is x265 and hev1 encoded
                full_path = os.path.join(root, file)
                compressor_id = subprocess.check_output(["exiftool", "-s3", "-CompressorID", full_path], stderr=subprocess.DEVNULL)
                if compressor_id.strip() == b"hev1":
                    # re-encode the file with ffmpeg as hvc1
                    output_file = os.path.join(temp_dir, file)
                    print(f"Re-encoding {full_path} to {output_file}...")
                    subprocess.check_call([
                        "ffmpeg", "-i", full_path, "-c:v", "copy", "-c:a", "copy",
                        "-tag:v", "hvc1", output_file
                    ], stderr=subprocess.DEVNULL)
                    # replace the original file with the new one
                    os.remove(full_path)
                    os.rename(output_file, full_path)
                    print(f"Re-encoded {full_path} to hvc1 format.")

if __name__ == "__main__":
    main()