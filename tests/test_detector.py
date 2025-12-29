"""Tests for the Energetic Epicenter Detector."""

import unittest
import numpy as np
import cv2
from pathlib import Path
import tempfile
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from energetic_detector import EnergeticEpicenterDetector


class TestEnergeticDetector(unittest.TestCase):
    """Test cases for EnergeticEpicenterDetector."""
    
    @classmethod
    def setUpClass(cls):
        """Create a synthetic test video."""
        cls.temp_dir = tempfile.mkdtemp()
        cls.test_video_path = Path(cls.temp_dir) / "test_video.mp4"
        
        # Create a simple test video with an expanding circle
        width, height = 320, 240
        fps = 10
        num_frames = 20
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(cls.test_video_path), fourcc, fps, (width, height))
        
        cx, cy = width // 2, height // 2
        
        for i in range(num_frames):
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            radius = 10 + i * 5
            cv2.circle(frame, (cx, cy), radius, (255, 255, 255), 2)
            out.write(frame)
        
        out.release()
    
    def test_detector_initialization(self):
        """Test detector can be initialized."""
        detector = EnergeticEpicenterDetector(
            str(self.test_video_path),
            output_dir=self.temp_dir
        )
        self.assertIsNotNone(detector)
        self.assertEqual(detector.video_path, str(self.test_video_path))
    
    def test_optical_flow_computation(self):
        """Test optical flow computation."""
        detector = EnergeticEpicenterDetector(
            str(self.test_video_path),
            output_dir=self.temp_dir
        )
        
        # Create two simple frames
        frame1 = np.zeros((100, 100), dtype=np.uint8)
        frame2 = np.zeros((100, 100), dtype=np.uint8)
        cv2.circle(frame1, (40, 50), 10, 255, -1)
        cv2.circle(frame2, (50, 50), 10, 255, -1)
        
        flow = detector.compute_optical_flow(frame1, frame2)
        
        self.assertEqual(flow.shape, (100, 100, 2))
        # Check that there is some flow detected
        self.assertGreater(np.abs(flow).max(), 0)
    
    def test_divergence_computation(self):
        """Test divergence computation."""
        detector = EnergeticEpicenterDetector(
            str(self.test_video_path),
            output_dir=self.temp_dir
        )
        
        # Create a simple flow field (expansion from center)
        y, x = np.mgrid[0:100, 0:100]
        cx, cy = 50, 50
        u = (x - cx) * 0.1
        v = (y - cy) * 0.1
        flow = np.stack([u, v], axis=-1)
        
        divergence = detector.compute_divergence(flow)
        
        self.assertEqual(divergence.shape, (100, 100))
        # Expansion should have positive divergence
        self.assertGreater(divergence[cy, cx], 0)
    
    def test_curl_computation(self):
        """Test curl computation."""
        detector = EnergeticEpicenterDetector(
            str(self.test_video_path),
            output_dir=self.temp_dir
        )
        
        # Create a rotational flow field
        y, x = np.mgrid[0:100, 0:100]
        cx, cy = 50, 50
        dx = x - cx
        dy = y - cy
        u = -dy * 0.1  # Rotational flow
        v = dx * 0.1
        flow = np.stack([u, v], axis=-1)
        
        curl = detector.compute_curl(flow)
        
        self.assertEqual(curl.shape, (100, 100))
        # Should detect rotation
        self.assertNotEqual(curl[cy, cx], 0)
    
    def test_strain_energy_computation(self):
        """Test strain energy computation."""
        detector = EnergeticEpicenterDetector(
            str(self.test_video_path),
            output_dir=self.temp_dir
        )
        
        # Create a simple flow field
        flow = np.random.randn(100, 100, 2) * 0.5
        
        strain_energy = detector.compute_strain_energy(flow)
        
        self.assertEqual(strain_energy.shape, (100, 100))
        self.assertTrue(np.all(strain_energy >= 0))  # Energy should be non-negative
    
    def test_video_analysis(self):
        """Test full video analysis."""
        detector = EnergeticEpicenterDetector(
            str(self.test_video_path),
            output_dir=self.temp_dir,
            skip_frames=2
        )
        
        results = detector.analyze_video(json_output=True)
        
        # Check results structure
        self.assertIn('video_path', results)
        self.assertIn('video_properties', results)
        self.assertIn('epicenters', results)
        
        # Check video properties
        props = results['video_properties']
        self.assertEqual(props['width'], 320)
        self.assertEqual(props['height'], 240)
        self.assertGreater(props['processed_frames'], 0)
    
    def test_epicenter_detection(self):
        """Test epicenter detection."""
        detector = EnergeticEpicenterDetector(
            str(self.test_video_path),
            output_dir=self.temp_dir
        )
        
        # Create mock energy and divergence maps
        energy_map = np.zeros((100, 100))
        divergence_map = np.zeros((100, 100))
        
        # Create a hotspot at (50, 50)
        energy_map[45:55, 45:55] = 10.0
        divergence_map[45:55, 45:55] = 5.0
        
        epicenters = detector.detect_epicenters(energy_map, divergence_map)
        
        self.assertGreater(len(epicenters), 0)
        # Check that detected epicenter is near the hotspot
        top_epicenter = epicenters[0]
        self.assertAlmostEqual(top_epicenter['x'], 50, delta=10)
        self.assertAlmostEqual(top_epicenter['y'], 50, delta=10)


if __name__ == '__main__':
    unittest.main()
