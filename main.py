from baike_correction.embedding import get_embedding
from baike_correction.merger import SemanticsMerger
from baike_correction.splitter import SentenceSplitter, MergeSplitter

def main():
    embedding_cfgs = {
        "embedding_type": "bge",
        "model_name": "BAAI/bge-base-zh-v1.5",
        "device": "cuda",
        "normalize_embeddings": False,
        "max_batch_size": 32,
    }
    embedding = get_embedding(embedding_cfgs)
    merger = SemanticsMerger(embedding=embedding, threshold=0.45)
    splitter = MergeSplitter(SentenceSplitter(), merger)
    with open('./temp.txt', mode='r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace('\n', '')
    chunks = splitter.split_text(text)
    with open('./result.txt', mode='w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(chunk + '\n')


if __name__ == "__main__":
    main()
