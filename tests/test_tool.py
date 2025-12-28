"""Tests for the Epicenter Tool AI integration wrapper."""

import unittest
import tempfile
import sys
from pathlib import Path
import cv2
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from epicenter_tool import EpicenterTool


class TestEpicenterTool(unittest.TestCase):
    """Test cases for EpicenterTool."""
    
    @classmethod
    def setUpClass(cls):
        """Create a synthetic test video."""
        cls.temp_dir = tempfile.mkdtemp()
        cls.test_video_path = Path(cls.temp_dir) / "test_video.mp4"
        
        # Create a simple test video
        width, height = 320, 240
        fps = 10
        num_frames = 15
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(cls.test_video_path), fourcc, fps, (width, height))
        
        cx, cy = width // 2, height // 2
        
        for i in range(num_frames):
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            radius = 10 + i * 5
            cv2.circle(frame, (cx, cy), radius, (255, 255, 255), 2)
            out.write(frame)
        
        out.release()
    
    def test_tool_initialization(self):
        """Test tool can be initialized."""
        tool = EpicenterTool(output_dir=self.temp_dir)
        self.assertIsNotNone(tool)
        self.assertTrue(tool.output_dir.exists())
    
    def test_analyze_video_direct(self):
        """Test video analysis using direct mode."""
        tool = EpicenterTool(output_dir=self.temp_dir)
        
        results = tool.analyze_video(
            str(self.test_video_path),
            skip_frames=2,
            use_subprocess=False
        )
        
        self.assertIn('video_path', results)
        self.assertIn('video_properties', results)
        self.assertIn('epicenters', results)
    
    def test_get_top_epicenter(self):
        """Test getting the top epicenter."""
        tool = EpicenterTool(output_dir=self.temp_dir)
        
        top = tool.get_top_epicenter(str(self.test_video_path), skip_frames=2)
        
        if top:  # May be None if no epicenters detected
            self.assertIn('x', top)
            self.assertIn('y', top)
            self.assertIn('score', top)
    
    def test_format_for_llm(self):
        """Test LLM output formatting."""
        tool = EpicenterTool(output_dir=self.temp_dir)
        
        # Create mock results
        results = {
            'video_path': '/path/to/video.mp4',
            'video_properties': {
                'width': 640,
                'height': 480,
                'processed_frames': 100
            },
            'epicenters': [
                {'x': 320, 'y': 240, 'score': 95.5},
                {'x': 100, 'y': 150, 'score': 78.2}
            ]
        }
        
        formatted = tool.format_for_llm(results)
        
        self.assertIsInstance(formatted, str)
        self.assertIn('Video Analysis', formatted)
        self.assertIn('640x480', formatted)
        self.assertIn('(320, 240)', formatted)
    
    def test_batch_analyze(self):
        """Test batch analysis."""
        tool = EpicenterTool(output_dir=self.temp_dir)
        
        # Create list with one existing video and one non-existent
        video_paths = [
            str(self.test_video_path),
            '/nonexistent/video.mp4'
        ]
        
        results = tool.batch_analyze(video_paths, skip_frames=3)
        
        self.assertEqual(len(results), 2)
        
        # First should succeed
        self.assertIn('video_properties', results[0])
        
        # Second should have error
        self.assertIn('error', results[1])


if __name__ == '__main__':
    unittest.main()
