# Prosostyl: a rule-based prosodic annotator in Metronome format (for Old French mostly)

CLI:

```
# Evaluate the tool on GT
python main.py --eval_path gt_fro_with_preds.tsv --detailed_eval
# Comparing with other annotators
python main.py --eval_path gt_fro_with_preds.tsv --compare
# Annotate unseen files
python main.py --unseen_paths sample/*
```
