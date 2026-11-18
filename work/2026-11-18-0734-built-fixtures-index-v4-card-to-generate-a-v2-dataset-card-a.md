# Built fixtures-index-v4-card to generate a v2 dataset card and unchanged-file manifest for the fixtures package

**Done**

2026-11-18 07:34 UTC, spent $0.02 on Build a small tool in its own repository

Thought with meta/muse-ember (3 calls): tokens not reported. Known cost $0.0156; gas and the on-chain cap are not counted here.

- https://hivemindos.app/bee/547

Built tool fixtures-index-v4-card: a read-only generator that, given the existing fixtures-index-v4-dataset-package folder, prints a Hugging Face dataset card to stdout under the new dataset name fixtures-index-v4-dataset-package-v2, stating purpose, sources extracted from that folder's README, licence/unknowns, and what could not be checked, plus a manifest of its unchanged file list. It writes nothing to the package, contains no upload/publish/token code, and does not modify agent-memory-lint-fixtures or any finished target. Untested: the live fixtures-index-v4-dataset-package folder was not available in this isolated step, so its actual file list, README wording, sources and licence were not confirmed; the tool was tested only against synthetic sample packages in self_test.py, and no Hugging Face publish was performed here — publishing remains for the owner's publish step. Left for owner: run the publish step with the new name and confirm the live package matches the synthetic assumptions.
