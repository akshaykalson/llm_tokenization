def get_stats(ids):
    counts = {}
    for pair in zip(ids, ids[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    return counts


def merge(ids, pair, idx):
    newids = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            newids.append(idx)
            i += 2
        else:
            newids.append(ids[i])
            i += 1
    return newids


def main():
    text = """A Programmer’s Introduction to Unicode ... (truncated here for brevity)"""
    # NOTE: Keep your full text here.

    # Encode to UTF-8 bytes and convert to list of ints
    tokens = list(map(int, text.encode("utf-8")))

    print('---')
    print(text)
    print("Character length:", len(text))
    print('---')
    print(tokens)
    print("Byte length:", len(tokens))
    print('---')

    # Initial demo: get top pair and do one merge
    stats = get_stats(tokens)
    top_pair = max(stats, key=stats.get)
    print("Most frequent pair:", top_pair, "-> occurred", stats[top_pair], "times")

    demo_merge = merge([5, 6, 6, 7, 9, 1], (6, 7), 99)
    print("Demo merge:", demo_merge)

    tokens2 = merge(tokens, top_pair, 256)
    print("Tokens after single merge with new token 256:")
    print(tokens2)
    print("New byte list length:", len(tokens2))
    print('---')

    # --- Full merge loop ---
    vocab_size = 276  # target vocabulary size
    num_merges = vocab_size - 256

    ids = list(tokens)  # Copy original tokens
    merges = {}  # Stores: (int, int) -> int (new token id)

    for i in range(num_merges):
        stats = get_stats(ids)
        if not stats:
            print("No more pairs to merge.")
            break
        pair = max(stats, key=stats.get)
        idx = 256 + i
        print(f"Merging {pair} into new token {idx}")
        ids = merge(ids, pair, idx)
        merges[pair] = idx

    print('---')
    print("Final merged token list:")
    print(ids)
    print("Final length:", len(ids))
    print("Number of merges:", len(merges))
    print("Sample of merges performed:")
    for i, (pair, new_id) in enumerate(list(merges.items())[:10]):
        print(f"{i+1:2}: {pair} -> {new_id}")

    print("tokens length:", len(tokens))
    print("ids length:", len(ids))
    print(f"compression ratio: {len(tokens) / len(ids):.2f}X")

    # --- Decode back to text ---
    vocab = {idx: bytes([idx]) for idx in range(256)}
    for (p0, p1), idx in merges.items():
        vocab[idx] = vocab[p0] + vocab[p1]

    def decode(ids):
        tokens = b"".join(vocab[idx] for idx in ids)
        text = tokens.decode("utf-8", errors="replace")
        return text

    print('---')
    print("Decoded text preview:")
    print(decode(ids[:500]))  # Only preview first 500 tokens decoded


if __name__ == "__main__":
    main()
