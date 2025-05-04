import asyncio
import aiofiles
import aiofiles.os
import aiofiles.ospath
import shutil
from pathlib import Path
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(src_file: Path, output_dir: Path):
    try:
        ext = src_file.suffix[1:] or "no_extension"
        target_dir = output_dir / ext
        await aiofiles.os.makedirs(target_dir, exist_ok=True)
        target_file = target_dir / src_file.name
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, shutil.copy2, src_file, target_file)
        logging.info(f'Copied {src_file} to {target_file}')
    except Exception as e:
        logging.error(f"Error copying {src_file}: {e}")

async def read_folder(source_dir: Path, output_dir: Path):
    tasks = []
    for path in source_dir.rglob("*"):
        if await aiofiles.ospath.isfile(path):
            tasks.append(copy_file(path, output_dir))
    await asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser(description="Sort files by extension asynchronously.")
    parser.add_argument("source", type=str, help="Source directory")
    parser.add_argument("output", type=str, help="Output directory")
    args = parser.parse_args()

    source_dir = Path(args.source)
    output_dir = Path(args.output)

    if not source_dir.exists() or not source_dir.is_dir():
        logging.error("Source directory does not exist or is not a directory.")
        return

    asyncio.run(read_folder(source_dir, output_dir))

if __name__ == "__main__":
    main()