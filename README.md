# TTRPG_Annotation
For Brandeis Course COSI 230B - Natural Language Annotation for Machine Learning

## Setting Up the Project
1) Set up the project environment and Label Studio project with `make setup`.
    - If prompted for Label Studio password, you can just hit enter.
2) Run `make label` to open Label Studio.
3) In Label Studio, open the project 'TTRPG-Annotations', then click 'Import' and import `data.json`.

## Labeling
To label, first select the label from the right sidebar.
To label an entire speech block, click the button at the right of its dialogue box.
To label part of a speech block (only when there is more than one label in a speech block), click and drag to select text.
Be sure that the selected regions are non-overlapping and fully cover all words in the speech block.
