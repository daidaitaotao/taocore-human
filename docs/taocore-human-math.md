# TaoCore-Human: Math and Logic Explained (Engineer-Friendly Deep Dive)

This document explains how `taocore-human` uses TaoCore’s math to analyze photos and videos. It’s written for software engineers without a data science background.

## 1. Big Picture

`taocore-human` is a pipeline package. It does not “read minds.” It extracts measurable signals, runs structural and stability metrics, and then applies conservative rules to decide whether interpretation is safe.

The pipeline flow:

1. **Load media** (images or video).
2. **Extract signals** (faces, pose, scene).
3. **Build graph** (people as nodes, co-occurrence as edges).
4. **Run metrics** (balance, clusters, hubs, flow for video).
5. **Run equilibrium solver** (fixed-point iteration).
6. **Apply decider rules** (allow or reject interpretation).
7. **Generate report**.

## 2. Inputs and Adapters

### Photo Folder

- Input: a folder of images.
- Adapter enumerates files by extension, loads with PIL or OpenCV, and yields `ImageFrame`.

Implementation reference:
- `taocore_human/adapters/images.py`

### Video

- Input: a video file.
- Adapter uses OpenCV to read frames, converts BGR→RGB, and yields `VideoFrame`.
- `get_windows()` slices the video into time windows by duration and overlap.

Implementation reference:
- `taocore_human/adapters/video.py`

## 3. Extractors (Signals)

Extractors produce signals per frame:

- Face detection confidence.
- Expression proxies like valence/arousal.
- Scene quality indicators (illumination, blur).

By default, the package can use **stub extractors** (random but seeded outputs) to test the pipeline without ML dependencies.

Implementation reference:
- `taocore_human/extractors/base.py` (data contracts)
- `taocore_human/extractors/stub.py` (stub outputs)

## 4. Graph Construction

### Photo Pipeline

- Each unique tracked person becomes a `PersonNode` with aggregated features.
- Edges connect people who co-occur in the same frames.

Implementation reference:
- `taocore_human/pipeline/photo_folder.py`
- `taocore_human/nodes/person.py`
- The graph is a structural snapshot of “who appears with whom.”

### Video Pipeline

Two levels of graphs:

- **Per-window graphs**: each time window is a small graph of co-occurring people.
- **Aggregated graph**: merges across windows to represent the entire video.

Implementation reference:
- `taocore_human/pipeline/video_interaction.py`
- `taocore_human/nodes/temporal.py`

This allows both temporal and global analysis.

## 5. Metrics Applied

`taocore-human` reuses TaoCore metrics:

- **BalanceMetric**: checks whether signals are in safe bounds.
- **ClusterMetric**: finds groups and separation.
- **HubMetric**: highlights structurally central people.
- **FlowMetric** (video only): measures how interactions evolve.

These metrics are descriptive; they do not diagnose or prescribe.

## 6. Equilibrium Solver

After metrics, the pipeline runs the TaoCore equilibrium solver:

```
x_{t+1} = f(x_t)
```

This fixed-point iteration finds a stable state or reports oscillation. It is used as a sanity check: if the system does not stabilize, the pipeline tends to reject interpretation.

## 7. Decider Rules (Safety)

The decider is deliberately conservative. Examples:

- If no person has enough coverage/confidence → reject.
- If equilibrium fails to converge → reject.
- If temporal volatility is too high → reject.

Concrete thresholds:
- `min_coverage`, `min_confidence`, `min_images` in `PipelineConfig`
- `min_duration`, `window_duration`, `window_overlap` in `VideoPipelineConfig`

Implementation reference:
- `taocore_human/pipeline/photo_folder.py`
- `taocore_human/pipeline/video_interaction.py`

This means the system will often say “no interpretation” rather than guess.

## 8. Why This Is Engineer-Friendly

Everything is explicit:

- Each metric is inspectable.
- The equilibrium solver exposes convergence diagnostics.
- “Reject” reasons are listed, not hidden.

The package is designed for **bounded claims** and **explicit uncertainty**.

## 9. Evidence in the Codebase

Tests cover:

- Pipeline structure and edge cases.
- TaoCore metric behavior.
- Equilibrium convergence and oscillation detection.

See `tests/` and `taocore_human/pipeline/` for concrete implementations.

Recommended files to read:
- `taocore_human/reports/generator.py` (language, refusal logic)
- `taocore_human/nodes/context.py` (context confidence reduction)

If you want, I can add a tutorial with example inputs and sample outputs.

## References

- TaoCore math deep dive: ../taocore/docs/taocore-math.md
- Fixed-point iteration (definition and convergence framing): https://en.wikipedia.org/wiki/Fixed-point_iteration
