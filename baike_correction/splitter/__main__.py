import argparse

from baike_correction.splitter import get_splitter
from baike_correction.utils.config import load_config

def main():
    parser = argparse.ArgumentParser("Baike Correction Splitter")
    parser.add_argument("--config", type=str, default="./configs/config.yaml", help="The config file of the splitter")
    parser.add_argument("--input", type=str, default="./input.txt", help="The path of the input file which contains contents to be splitted")
    parser.add_argument("--output", type=str, default="./output.txt", help="The path of the output file")
    args = parser.parse_args()
    config = load_config(args.config)
    splitter_cfgs = config.get('splitter_cfgs')
    splitter = get_splitter(splitter_cfgs)
    with open(args.input, mode='r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace('\n', '')
    chunks = splitter.split_text(text)
    with open(args.output, mode='w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(chunk + '\n')


main()
