import argparse
import json

from baike_correction.splitter import get_splitter
from baike_correction.utils.config import load_config
from baike_correction.key_word_extractor import get_key_word_extractor

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
    extractor_cfgs = config.get('extractor_cfgs')
    key_word_extractor = get_key_word_extractor(extractor_cfgs=extractor_cfgs)
    result = []
    for chunk in chunks:
        result.append({
            "text": chunk,
            "key_words": [kw.model_dump() for kw in key_word_extractor.extract_key_words(chunk)]
        })
    with open(args.output, mode='w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


main()
