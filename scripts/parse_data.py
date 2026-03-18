from pathlib import Path
import re
import json
import random
from itertools import groupby
from collections import Counter

BASE_PATH = Path(__file__).parent.parent
DATA_PATH = BASE_PATH / Path('mcutler-thesis-TTRPGcorpus/dimension20.txt')


def load_data(file: Path) -> list[tuple[int, str]]:
    """
    Returns a list of all non blank lines in file.
    """
    lines = []
    with open(file, 'r', encoding='utf8') as f:
        prev_blank = True
        for line_num, line in enumerate(f, 1):
            s = line.strip()
            if not s:
                prev_blank = True
            else:
                if prev_blank:
                    lines.append((line_num, s))
                    prev_blank = False
                else:
                    lines[-1] = (lines[-1][0], lines[-1][1] + " " + s)
        # return [(i, s) for i, line in enumerate(f, 1) if (s := line.strip())]
    return lines


def parse_speakers(data: list[tuple[int, str]]) -> list[tuple[str, str]]:
    """
    Parses the speaker for each line.
    """
    speech_blocks = []
    for line_num, line in data:
        split_result = tuple(filter(None, re.split(r'^([^:]+):\s*', line, maxsplit=1)))
        if len(split_result) < 2:
            speech_blocks.append((None, line))
            #raise Exception(f'Cannot match speaker in line: "{line}"') 
            #print(f'Cannot match speaker in line {line_num}: "{line}"') 
        else:
            speech_blocks.append(tuple(split_result))
    return speech_blocks


def substitute_speaker_names(speech_blocks: list[tuple[str, str]], name_dict: dict[str, str]) -> list:
    """
    Uses name_dict to convert all speaker tags into the form 'Actual-Name (Character-Name)' for players
    and 'Actual-Name (Dungeon Master) (Character-Name-If-Exists)' for the dungeon master.
    """
    # name_dict is playername: charactername OR "Dungeon Master" (value is person's main role in the game)
    reversed_dict = {v: k for k, v in name_dict.items()}
    subbed_blocks = []
    for speaker, speech in speech_blocks:
        if speaker in name_dict:
            subbed_blocks.append((f"{speaker} ({name_dict[speaker]})", speech))
        elif speaker in reversed_dict:
            subbed_blocks.append((f"{reversed_dict[speaker]} ({speaker})", speech))
        elif speaker is not None:
            subbed_blocks.append((f"{reversed_dict['Dungeon Master']} (Dungeon Master) ({speaker})", speech))
        else:
            subbed_blocks.append((speaker, speech))
    return subbed_blocks


def sample_subsequences(seq: list[any], l: int, valid_key, k: int = 1, max_k: bool = False) -> list[any]:
    """
    Samples k continuous subsequences of l items that all meet the valid_key condition.
    """
    valid_subseq = [g for valid, group in groupby(seq, key=valid_key) if valid and len(g := list(group)) >= l]
    max_per_subseq = [len(seq) // l for seq in valid_subseq]  
    max_total = sum(max_per_subseq)
    if k > max_total:
        print(f"Cannot sample {k} sequences of length {l}, sampling {max_k} instead")
        max_k = True
    if max_k:
        k = max_total

    samples = []
    random.seed(123)
    subseq_choices = random.sample(range(len(valid_subseq)), counts=max_per_subseq, k=k)
    choice_counts = Counter(subseq_choices)
    for seq_idx, count in choice_counts.items():
        seq = valid_subseq[seq_idx]
        indices = range(len(seq) - (l - 1) * count)
        offset = 0
        for i in sorted(random.sample(indices, count)):
            i += offset
            samples.append(seq[i:i+l])
            offset += l - 1

    assert len(samples) == k
    random.shuffle(samples)
    return samples


def main():
    roles = {
        'Brennan': 'Dungeon Master',
        'Emily': 'Fig',
        'Zac': 'Gorgug',
        'Siobhan': 'Adaine',
        'Lou': 'Fabian',
        'Ally': 'Kristen',
        'Murph': 'Riz',
    }
    lines = load_data(DATA_PATH)
    speech_blocks = parse_speakers(lines)
    subbed_speech_blocks = substitute_speaker_names(speech_blocks, roles)
    samples = sample_subsequences(subbed_speech_blocks, 10, lambda x: x[0] is not None, max_k=True)
    with open(BASE_PATH / Path('samples.json'), 'w', encoding='utf8') as f:
        json.dump(samples, f, indent=4)


if __name__ == '__main__':
    main()
