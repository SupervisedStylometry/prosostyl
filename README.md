# Prosostyl: a rule-based prosodic annotator in Metronome format (for Old French mostly)

## CLI

```
# Evaluate the tool on GT
python main.py --eval_path gt_fro_with_preds.tsv --detailed_eval
# Comparing with other annotators
python main.py --eval_path gt_fro_with_preds.tsv --compare
# Annotate unseen files
python main.py --unseen_paths sample/*
```

## Current scores (Levenshtein ratio)

The scores are based on normalized indel similarity with gt strings, i.e. 1 - (levenshtein distance / (len1 + len2)).

```
count  101.000000
mean     0.976153
std      0.042478
min      0.785714
25%      0.962963
50%      1.000000
75%      1.000000
max      1.000000
```
