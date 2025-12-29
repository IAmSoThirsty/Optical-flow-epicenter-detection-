#!/usr/bin/env python3
"""
Epicenter Tool - AI Integration Bridge
---------------------------------------
A wrapper class for integrating the Energetic Epicenter Detector
into AI agents and forensic workflows.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


class EpicenterTool:
    """
    Bridge class for AI integration with the Energetic Epicenter Detector.
    
    This class provides a clean interface for AI agents to analyze videos
    and get structured results about energetic events.
    """
    
    def __init__(self, output_dir: str = "epicenter_analysis"):
        """
        Initialize the epicenter tool.
        
        Args:
            output_dir: Directory for output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def analyze_video(
        self, 
        video_path: str, 
        skip_frames: int = 1,
        use_subprocess: bool = False
    ) -> Dict:
        """
        Analyze a video for energetic epicenters.
        
        Args:
            video_path: Path to the video file
            skip_frames: Process every Nth frame for performance
            use_subprocess: Use subprocess instead of direct import (for isolation)
            
        Returns:
            Dictionary with analysis results including:
            - video_path: Path to analyzed video
            - video_properties: Dict with width, height, fps, frame_count
            - epicenters: List of detected epicenters with x, y, score
        """
        if use_subprocess:
            return self._analyze_subprocess(video_path, skip_frames)
        else:
            return self._analyze_direct(video_path, skip_frames)
    
    def _analyze_direct(self, video_path: str, skip_frames: int) -> Dict:
        """Analyze using direct module import."""
        from energetic_detector import EnergeticEpicenterDetector
        
        detector = EnergeticEpicenterDetector(
            video_path,
            output_dir=str(self.output_dir),
            skip_frames=skip_frames
        )
        
        results = detector.analyze_video(json_output=True)
        return results
    
    def _analyze_subprocess(self, video_path: str, skip_frames: int) -> Dict:
        """Analyze using subprocess for isolation."""
        cmd = [
            sys.executable,
            'energetic_detector.py',
            video_path,
            '--output-dir', str(self.output_dir),
            '--skip', str(skip_frames),
            '--json'
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        return json.loads(result.stdout)
    
    def get_top_epicenter(
        self, 
        video_path: str, 
        skip_frames: int = 1
    ) -> Optional[Dict]:
        """
        Get the single most likely epicenter location.
        
        Args:
            video_path: Path to the video file
            skip_frames: Process every Nth frame
            
        Returns:
            Dictionary with top epicenter or None if no epicenters found
        """
        results = self.analyze_video(video_path, skip_frames)
        
        if results.get('epicenters'):
            return results['epicenters'][0]
        return None
    
    def batch_analyze(
        self, 
        video_paths: List[str], 
        skip_frames: int = 2
    ) -> List[Dict]:
        """
        Analyze multiple videos in batch.
        
        Args:
            video_paths: List of video file paths
            skip_frames: Process every Nth frame
            
        Returns:
            List of result dictionaries, one per video
        """
        results = []
        for video_path in video_paths:
            try:
                result = self.analyze_video(video_path, skip_frames)
                results.append(result)
            except Exception as e:
                results.append({
                    'video_path': video_path,
                    'error': str(e)
                })
        
        return results
    
    def format_for_llm(self, results: Dict) -> str:
        """
        Format results in a human-readable way for LLM consumption.
        
        Args:
            results: Results dictionary from analyze_video
            
        Returns:
            Formatted string description
        """
        video_props = results.get('video_properties', {})
        epicenters = results.get('epicenters', [])
        
        output = []
        output.append(f"Video Analysis: {results.get('video_path', 'Unknown')}")
        output.append(f"Resolution: {video_props.get('width')}x{video_props.get('height')}")
        output.append(f"Frames analyzed: {video_props.get('processed_frames')}")
        output.append("")
        
        if epicenters:
            output.append(f"Detected {len(epicenters)} potential epicenter(s):")
            for i, ep in enumerate(epicenters, 1):
                output.append(
                    f"  {i}. Location: ({ep['x']}, {ep['y']}), "
                    f"Confidence: {ep['score']:.2f}"
                )
        else:
            output.append("No significant epicenters detected.")
        
        return "\n".join(output)


def main():
    """Example usage of the EpicenterTool."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Epicenter Tool - AI Integration Bridge'
    )
    parser.add_argument('video_path', help='Path to video file')
    parser.add_argument('--skip', type=int, default=2,
                       help='Process every Nth frame (default: 2)')
    parser.add_argument('--format', choices=['json', 'llm'], default='json',
                       help='Output format (default: json)')
    
    args = parser.parse_args()
    
    tool = EpicenterTool()
    
    try:
        results = tool.analyze_video(args.video_path, skip_frames=args.skip)
        
        if args.format == 'json':
            print(json.dumps(results, indent=2))
        else:
            print(tool.format_for_llm(results))
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
