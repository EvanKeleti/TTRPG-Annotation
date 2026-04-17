# TTRPG_Annotation
For Brandeis Course COSI 230B - Natural Language Annotation for Machine Learning

## Setting Up the Project
1) First, clone this repo locally.
2) Set up the project environment and Label Studio project with `make setup`.
    - If prompted for Label Studio password, you can just hit enter.
3) Run `make label` to open Label Studio.
4) In Label Studio, open the project 'TTRPG-Annotations', then click 'Import' and import `group_data.json`.
    - `group_data.json` contains 10 samples of 10 lines of dialogue each; you will annotate all of this data.
    - `data.json` contains all the samples we took from the data set; do not import this file.

## Labeling
To label, first select the label from the right sidebar.
To label an entire speech block, click the button at the right of its dialogue box.
To label part of a speech block (only when there is more than one label in a speech block), click and drag to select text.
Be sure that the selected regions are non-overlapping and fully cover all words in the speech block.

## Exporting
When you're finished annotating, export them from label studio as a json file. Then, email this file to `evankeleti@brandeis.edu`.
