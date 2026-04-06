"""Command-line interface for taocore-human pipelines."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence


def _write_output(payload: str, output: Optional[str]) -> None:
    if output:
        Path(output).write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
        if not payload.endswith("\n"):
            sys.stdout.write("\n")


def _photo_folder(args: argparse.Namespace) -> int:
    from taocore_human.pipeline.photo_folder import PhotoFolderPipeline, PipelineConfig

    config = PipelineConfig(
        min_coverage=args.min_coverage,
        min_confidence=args.min_confidence,
        min_images=args.min_images,
        co_occurrence_threshold=args.co_occurrence_threshold,
        max_iterations=args.max_iterations,
        tolerance=args.tolerance,
        strict_mode=args.strict,
    )

    pipeline = PhotoFolderPipeline(args.folder, config=config)
    result = pipeline.run()
    _write_output(pipeline.to_json(result), args.output)
    return 0


def _video(args: argparse.Namespace) -> int:
    from taocore_human.pipeline.video_interaction import (
        VideoInteractionPipeline,
        VideoPipelineConfig,
    )

    config = VideoPipelineConfig(
        window_duration=args.window_duration,
        window_overlap=args.window_overlap,
        sample_fps=args.sample_fps,
        min_coverage=args.min_coverage,
        min_confidence=args.min_confidence,
        min_duration=args.min_duration,
        max_iterations=args.max_iterations,
        tolerance=args.tolerance,
        strict_mode=args.strict,
    )

    pipeline = VideoInteractionPipeline(args.video, config=config)
    result = pipeline.run()
    _write_output(pipeline.to_json(result), args.output)
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taocore-human",
        description="Run taocore-human analysis pipelines.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    photo = subparsers.add_parser(
        "photo-folder",
        help="Analyze a folder of photos using the photo pipeline.",
    )
    photo.add_argument("folder", help="Path to folder of images.")
    photo.add_argument("--min-coverage", type=float, default=0.3)
    photo.add_argument("--min-confidence", type=float, default=0.5)
    photo.add_argument("--min-images", type=int, default=3)
    photo.add_argument("--co-occurrence-threshold", type=int, default=2)
    photo.add_argument("--max-iterations", type=int, default=100)
    photo.add_argument("--tolerance", type=float, default=1e-4)
    photo.add_argument("--strict", action=argparse.BooleanOptionalAction, default=True)
    photo.add_argument("--output", help="Write JSON output to this file.")
    photo.set_defaults(func=_photo_folder)

    video = subparsers.add_parser(
        "video",
        help="Analyze a video using the interaction pipeline.",
    )
    video.add_argument("video", help="Path to video file.")
    video.add_argument("--window-duration", type=float, default=5.0)
    video.add_argument("--window-overlap", type=float, default=1.0)
    video.add_argument("--sample-fps", type=float, default=2.0)
    video.add_argument("--min-coverage", type=float, default=0.3)
    video.add_argument("--min-confidence", type=float, default=0.5)
    video.add_argument("--min-duration", type=float, default=10.0)
    video.add_argument("--max-iterations", type=int, default=100)
    video.add_argument("--tolerance", type=float, default=1e-4)
    video.add_argument("--strict", action=argparse.BooleanOptionalAction, default=True)
    video.add_argument("--output", help="Write JSON output to this file.")
    video.set_defaults(func=_video)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
