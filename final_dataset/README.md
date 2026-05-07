# TTRPG Dataset

This dataset contains a total of 200 lines of annotated dialogue.
The data is grouped into into tasks of 10 lines each.
10 tasks were annotated by us (internal) and 10 tasks were annotated by others (external).

## Data Format

### Gold Annotations
The gold adjudicated data is in the two files `gold_data_internal.json` and `gold_data_external.json`.
Each file is an array of json objects for each annotation task of 10 dialogue lines.
Each task is identified by the `start_line` attribute, which corresponds to the line in the original data file of the first line of dialogue in the task.
The `data` attribute contains the ten lines of dialogue, their speaker tags, and their line numbers.
The `annotations` attribute contains the adjudicated annotations, where:
- `task_line` -> the index (0-9) of which of the 10 lines the annotation is for
- `startOffset` and `endOffset` -> the character range for the annotated span
- `text` -> the dialogue content of that span
- `label` -> the label for that span

### Original Annotations
The individual annotators' annotations are in `internal_annotations.json` and `external_annotations.json`.
The `start_line` and `data` attributes are the same as in the gold data files.
The `annotations` attribute is a json dict mapping the original data line numbers to a list of annotations, where each annotation has an additional `annotator` attribute, along with those in the gold data.
