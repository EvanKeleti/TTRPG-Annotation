from pathlib import Path
from collections import defaultdict
import itertools
import json
import numpy as np

BASE_PATH = Path(__file__).parent.parent
INTERNAL = BASE_PATH / Path('annotations_internal')
EXTERNAL = BASE_PATH / Path('annotations_external')
FINAL_DATA = BASE_PATH / Path('final_dataset')

labels = [
    "in_character_speech",
    "narrative_speech",
    "game_mechanics",
    "narrative_suggestions",
    "gameplay_negotiations",
    "off_record_related",
    "off_record_unrelated"
]


def load_annotations(directory: Path | str) -> tuple[dict[int, dict[str, list[int, int, str]]], dict[int, dict]]:
    files = list(Path(directory).glob('*.json'))
    annotations = {}
    for file in files:
        with open(file, 'r') as f:
            annotations[file.stem] = json.load(f)

    results = defaultdict(lambda: defaultdict(list))
    # ID for task is line number of first line in task
    tasks = {}
    for k, v in annotations.items():
        for task in v:
            data = task['data']['dialogue']
            task_id = int(data[0]['line_num'])
            tasks[task_id] = data
            line_nums = [int(d['line_num']) for d in data]
            assert isinstance(data, list), "Expected to be list"
            values = [x['value'] for x in task['annotations'][0]['result']]
            for val in values:
                results[line_nums[int(val['start'])]][k].append(
                    (int(val['startOffset']), int(val['endOffset']), val['paragraphlabels'][0])
                )
    return results, tasks


def find_disagreeing_tasks(results, tasks):
    dis_tasks = set()
    for tid, task in tasks.items():
        for line_num in task['lines']:
            result = results[line_num]
            agree = (num_labels := len(set(len(spans) for spans in result.values()))) == 1 and \
                    len(set(span for spans in result.values for span in spans)) == num_labels
            if not agree:
                dis_tasks.add(tid)
    return list(dis_tasks)


def fleiss_kappa(results: dict[int, dict[str, list[tuple[int, int, str]]]], tasks: dict[int, dict]) -> float:
    label_vals = {label: i for i, label in enumerate(labels)}
    n = 0
    per_item = 0
    label_counts = np.zeros(len(labels))
    for task in tasks.values():
        for line in task:
            line_num = line['line_num']
            annotations = results[line_num]
            length = len(line['speech'])
            matrix = np.zeros((len(labels), length))
            num_annotators = len(annotations)
            for annotator, annotation in annotations.items():
                for span in annotation:
                    matrix[label_vals[span[2]]][span[0]:span[1]] += 1
            per_item += np.sum(matrix * (matrix - 1)) / (num_annotators * (num_annotators - 1))
            n += length
            label_counts += np.sum(matrix, axis=1)
    mean_observed_agr = per_item / n
    label_proportions = label_counts / np.sum(label_counts)
    expected_agr = np.sum(np.square(label_proportions))
    kappa = (mean_observed_agr - expected_agr) / (1 - expected_agr)
    return kappa


def majority_vote(results, tasks):
    data = []
    label_vals = {label: i for i, label in enumerate(labels)}
    for tid, task in tasks.items():
        majority_annotations = [] 
        for i, line in enumerate(task):
            line_num = line['line_num']
            length = len(line['speech'])
            annotations = results[line_num]
            votes = np.zeros((len(labels), length))
            for annotator, annotation in annotations.items():
                for span in annotation:
                    votes[label_vals[span[2]]][span[0]:span[1]] += 1
            majority = np.argmax(votes, axis=0)
            changes = np.flatnonzero(np.diff(majority) != 0) + 1
            idxs = np.r_[0, changes, majority.size]
            ends = np.r_[changes, majority.size]
            for start, end in itertools.pairwise(idxs):
                majority_annotations.append(
                    {
                        'task_line': i,
                        'startOffset': int(start),
                        'endOffset': int(end),
                        'text': line['speech'][start:end],
                        'label': labels[majority[start]],
                    }
                )
        data.append({'start_line': tid, 'data': task, 'annotations': majority_annotations})
    return data


def create_final_annotation_file(results, tasks, file: Path | str) -> None:
    data = []
    for tid, task in tasks.items():
        annotations = {}
        for line in task:
            line_num = line['line_num']
            line_annotations = []
            for annotator, annotation in results[line_num].items():
                for span in annotation:
                    line_annotations.append({
                        'annotator': annotator,
                        'startOffset': span[0],
                        'endOffset': span[1],
                        'text': line['speech'][span[0]:span[1]],
                        'label': span[2],
                    })
            annotations[line_num] = line_annotations
        data.append({'start_line': tid, 'data': task, 'annotations': annotations})

    with open(Path(file), 'w') as f:
        json.dump(data, f, indent=2)


def main():
    results_int, tasks_int = load_annotations(INTERNAL)
    kappa = fleiss_kappa(results_int, tasks_int)
    print(f"Internal annotations kappa: {kappa:.2f}")
    results_ext, tasks_ext = load_annotations(EXTERNAL)
    kappa = fleiss_kappa(results_ext, tasks_ext)
    print(f"External annotations kappa: {kappa:.2f}")

    majority_annotations_int = majority_vote(results_int, tasks_int)
    with open(FINAL_DATA / Path('gold_data_internal.json'), 'w') as f:
        json.dump(majority_annotations_int, f, indent=2)
    majority_annotations_ext = majority_vote(results_ext, tasks_ext)
    with open(FINAL_DATA / Path('gold_data_external.json'), 'w') as f:
        json.dump(majority_annotations_ext, f, indent=2)

    create_final_annotation_file(results_int, tasks_int, FINAL_DATA / Path('internal_annotations.json'))
    create_final_annotation_file(results_ext, tasks_ext, FINAL_DATA / Path('external_annotations.json'))


if __name__ == '__main__':
    main()
