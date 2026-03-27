# TTRPG_Annotation
For Brandeis Course COSI 230B - Natural Language Annotation for Machine Learning

## Setting Up the Project
1) Set up the project environment with `uv sync`.
2) Initialize the Label Studio project with `make setup`.
3) In Label Studio, open the project 'TTRPG-Annotations', then click 'Import' and import `data.json`.

## Labeling
To label, first select the label from the right sidebar.
To label an entire speech block, click the button at the right of its dialogue box.
To label part of a speech block (only when there is more than one label in a speech block), click and drag to select text.
Be sure that the selected regions are non-overlapping and fully cover all words in the speech block.

To start Label Studio, you can run `make label`.
