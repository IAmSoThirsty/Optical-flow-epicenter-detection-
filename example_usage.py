#!/usr/bin/env python3
"""
Example usage script for the Energetic Epicenter Detector.
Demonstrates different ways to use the detector.
"""

import sys
from pathlib import Path

# Ensure the module is in the path
sys.path.insert(0, str(Path(__file__).parent))

from energetic_detector import EnergeticEpicenterDetector
from epicenter_tool import EpicenterTool


def example_basic_usage():
    """Example 1: Basic usage with direct class instantiation."""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # This example requires a video file
    video_path = "sample_video.mp4"
    
    if not Path(video_path).exists():
        print(f"Note: This example needs a video file at '{video_path}'")
        print("Skipping...")
        return
    
    # Create detector
    detector = EnergeticEpicenterDetector(
        video_path,
        output_dir="example_output",
        skip_frames=2
    )
    
    # Analyze video
    results = detector.analyze_video(json_output=True)
    
    # Print results
    print(f"\nFound {len(results['epicenters'])} epicenters")
    for i, ep in enumerate(results['epicenters'][:3], 1):
        print(f"  {i}. Position: ({ep['x']}, {ep['y']}), Score: {ep['score']:.2f}")
    
    # Create visualization
    detector.visualize_results()


def example_ai_integration():
    """Example 2: AI integration using the EpicenterTool wrapper."""
    print("\n" + "=" * 60)
    print("Example 2: AI Integration")
    print("=" * 60)
    
    video_path = "sample_video.mp4"
    
    if not Path(video_path).exists():
        print(f"Note: This example needs a video file at '{video_path}'")
        print("Skipping...")
        return
    
    # Create tool for AI integration
    tool = EpicenterTool(output_dir="example_output")
    
    # Get analysis results
    results = tool.analyze_video(video_path, skip_frames=2)
    
    # Format for LLM
    llm_output = tool.format_for_llm(results)
    print("\nLLM-formatted output:")
    print(llm_output)
    
    # Get top epicenter only
    top = tool.get_top_epicenter(video_path, skip_frames=2)
    if top:
        print(f"\nTop epicenter: ({top['x']}, {top['y']}) with score {top['score']:.2f}")


def example_batch_processing():
    """Example 3: Batch processing multiple videos."""
    print("\n" + "=" * 60)
    print("Example 3: Batch Processing")
    print("=" * 60)
    
    video_paths = [
        "video1.mp4",
        "video2.mp4",
        "video3.mp4",
    ]
    
    # Check if any videos exist
    existing_videos = [v for v in video_paths if Path(v).exists()]
    
    if not existing_videos:
        print("Note: This example needs video files")
        print("Expected files:", ", ".join(video_paths))
        print("Skipping...")
        return
    
    tool = EpicenterTool(output_dir="example_output")
    
    # Process all videos
    results = tool.batch_analyze(existing_videos, skip_frames=3)
    
    # Print summary
    print(f"\nProcessed {len(results)} videos:")
    for result in results:
        if 'error' in result:
            print(f"  ✗ {result['video_path']}: {result['error']}")
        else:
            num_epicenters = len(result.get('epicenters', []))
            print(f"  ✓ {result['video_path']}: {num_epicenters} epicenters found")


def example_synthetic_demo():
    """Example 4: Demonstration with synthetic data."""
    print("\n" + "=" * 60)
    print("Example 4: Synthetic Demo")
    print("=" * 60)
    
    import numpy as np
    import cv2
    
    print("\nCreating synthetic explosion video...")
    
    # Video parameters
    width, height = 640, 480
    fps = 30
    duration = 2  # seconds
    num_frames = fps * duration
    
    # Create video writer
    output_path = "synthetic_explosion.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Explosion center
    cx, cy = width // 2, height // 2
    
    for frame_idx in range(num_frames):
        # Create blank frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Expanding circle (shockwave)
        t = frame_idx / fps
        radius = int(50 + t * 150)
        
        # Draw expanding ring
        cv2.circle(frame, (cx, cy), radius, (0, 0, 255), 3)
        cv2.circle(frame, (cx, cy), max(0, radius - 20), (0, 128, 255), 2)
        
        # Add some particles
        for i in range(10):
            angle = (frame_idx * 15 + i * 36) * np.pi / 180
            px = int(cx + radius * 0.7 * np.cos(angle))
            py = int(cy + radius * 0.7 * np.sin(angle))
            cv2.circle(frame, (px, py), 5, (255, 255, 0), -1)
        
        out.write(frame)
    
    out.release()
    print(f"✓ Created {output_path}")
    
    # Now analyze it
    print("\nAnalyzing synthetic video...")
    detector = EnergeticEpicenterDetector(
        output_path,
        output_dir="example_output",
        skip_frames=1
    )
    
    results = detector.analyze_video(json_output=True)
    
    print(f"\nAnalysis complete!")
    print(f"Expected epicenter at: ({cx}, {cy})")
    
    if results['epicenters']:
        top = results['epicenters'][0]
        print(f"Detected epicenter at: ({top['x']}, {top['y']})")
        
        # Calculate error
        error = np.sqrt((top['x'] - cx)**2 + (top['y'] - cy)**2)
        print(f"Detection error: {error:.1f} pixels")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Energetic Epicenter Detector - Example Usage".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Run synthetic demo (always works)
    example_synthetic_demo()
    
    # Run other examples if videos are available
    # example_basic_usage()
    # example_ai_integration()
    # example_batch_processing()
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)
    print("\nFor more information, see README.md")
    print("")


if __name__ == '__main__':
    main()
