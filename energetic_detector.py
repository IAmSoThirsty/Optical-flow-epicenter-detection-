#!/usr/bin/env python3
"""
Energetic Epicenter Detector (EED)
-----------------------------------
An advanced computer vision engine that detects and triangulates the origin
of energetic events (impacts, explosions, shockwaves) within video feeds.

Uses fluid dynamics principles to map kinetic energy propagation via:
- Divergence (expansion)
- Curl (rotation)
- Strain Tensors (deformation)
"""

import argparse
import json
import os
import sys
from pathlib import Path

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter


class EnergeticEpicenterDetector:
    """Main detector class for analyzing energetic events in video."""
    
    def __init__(self, video_path, output_dir="epicenter_analysis", skip_frames=1):
        """
        Initialize the detector.
        
        Args:
            video_path: Path to the video file
            output_dir: Directory for output files
            skip_frames: Process every Nth frame for performance
        """
        self.video_path = video_path
        self.output_dir = Path(output_dir)
        self.skip_frames = skip_frames
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Analysis results
        self.energy_map = None
        self.divergence_map = None
        self.curl_map = None
        self.epicenter_candidates = []
        
    def compute_optical_flow(self, prev_gray, curr_gray):
        """
        Compute dense optical flow using Farneback method.
        
        Args:
            prev_gray: Previous frame (grayscale)
            curr_gray: Current frame (grayscale)
            
        Returns:
            flow: Optical flow field (u, v components)
        """
        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, curr_gray,
            None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0
        )
        return flow
    
    def compute_divergence(self, flow):
        """
        Compute divergence of the flow field (expansion/compression).
        
        Args:
            flow: Optical flow field
            
        Returns:
            divergence: Scalar field representing expansion
        """
        # Get u and v components
        u = flow[:, :, 0]
        v = flow[:, :, 1]
        
        # Compute partial derivatives
        du_dx = np.gradient(u, axis=1)
        dv_dy = np.gradient(v, axis=0)
        
        # Divergence = du/dx + dv/dy
        divergence = du_dx + dv_dy
        return divergence
    
    def compute_curl(self, flow):
        """
        Compute curl of the flow field (rotation).
        
        Args:
            flow: Optical flow field
            
        Returns:
            curl: Scalar field representing rotation
        """
        # Get u and v components
        u = flow[:, :, 0]
        v = flow[:, :, 1]
        
        # Compute partial derivatives
        du_dy = np.gradient(u, axis=0)
        dv_dx = np.gradient(v, axis=1)
        
        # Curl (z-component) = dv/dx - du/dy
        curl = dv_dx - du_dy
        return curl
    
    def compute_strain_energy(self, flow):
        """
        Compute strain energy based on deformation tensors.
        
        Args:
            flow: Optical flow field
            
        Returns:
            strain_energy: Energy metric
        """
        u = flow[:, :, 0]
        v = flow[:, :, 1]
        
        # Compute strain rate tensor components
        du_dx = np.gradient(u, axis=1)
        du_dy = np.gradient(u, axis=0)
        dv_dx = np.gradient(v, axis=1)
        dv_dy = np.gradient(v, axis=0)
        
        # Normal strain rates
        e_xx = du_dx
        e_yy = dv_dy
        
        # Shear strain rate
        e_xy = 0.5 * (du_dy + dv_dx)
        
        # Strain energy (simplified von Mises)
        strain_energy = np.sqrt(e_xx**2 + e_yy**2 + 2 * e_xy**2)
        return strain_energy
    
    def detect_epicenters(self, energy_map, divergence_map, threshold_percentile=95):
        """
        Detect potential epicenter locations.
        
        Args:
            energy_map: Accumulated energy field
            divergence_map: Accumulated divergence field
            threshold_percentile: Percentile for thresholding
            
        Returns:
            epicenters: List of (x, y, score) tuples
        """
        # Combine energy and divergence
        combined_metric = energy_map * np.abs(divergence_map)
        
        # Apply Gaussian smoothing
        smoothed = gaussian_filter(combined_metric, sigma=5)
        
        # Threshold
        threshold = np.percentile(smoothed, threshold_percentile)
        hotspots = smoothed > threshold
        
        # Find local maxima
        from scipy.ndimage import label
        labeled, num_features = label(hotspots)
        
        epicenters = []
        for i in range(1, num_features + 1):
            region = labeled == i
            y_coords, x_coords = np.where(region)
            
            if len(y_coords) > 0:
                # Compute center of mass weighted by intensity
                weights = smoothed[region]
                center_x = int(np.average(x_coords, weights=weights))
                center_y = int(np.average(y_coords, weights=weights))
                score = float(smoothed[center_y, center_x])
                
                epicenters.append({
                    'x': center_x,
                    'y': center_y,
                    'score': score
                })
        
        # Sort by score
        epicenters.sort(key=lambda e: e['score'], reverse=True)
        return epicenters
    
    def analyze_video(self, json_output=False):
        """
        Analyze the video and detect energetic epicenters.
        
        Args:
            json_output: If True, return JSON instead of showing visualizations
            
        Returns:
            results: Dictionary with analysis results
        """
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {self.video_path}")
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Initialize accumulation maps
        energy_map = np.zeros((height, width), dtype=np.float32)
        divergence_map = np.zeros((height, width), dtype=np.float32)
        curl_map = np.zeros((height, width), dtype=np.float32)
        
        # Temporal decay factor (prioritize early events)
        temporal_weights = []
        
        # Read first frame
        ret, prev_frame = cap.read()
        if not ret:
            raise ValueError("Cannot read video frames")
        
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        
        frame_idx = 0
        processed_frames = 0
        
        if not json_output:
            print(f"Analyzing video: {self.video_path}")
            print(f"Resolution: {width}x{height}, FPS: {fps:.2f}, Frames: {frame_count}")
        
        while True:
            ret, curr_frame = cap.read()
            if not ret:
                break
            
            frame_idx += 1
            
            # Skip frames for performance
            if frame_idx % (self.skip_frames + 1) != 0:
                continue
            
            curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
            
            # Compute optical flow
            flow = self.compute_optical_flow(prev_gray, curr_gray)
            
            # Compute fluid dynamics metrics
            divergence = self.compute_divergence(flow)
            curl = self.compute_curl(flow)
            strain_energy = self.compute_strain_energy(flow)
            
            # Temporal weighting (early frames get higher weight)
            time_weight = np.exp(-processed_frames / 10.0)
            temporal_weights.append(time_weight)
            
            # Accumulate weighted metrics
            energy_map += strain_energy * time_weight
            divergence_map += divergence * time_weight
            curl_map += curl * time_weight
            
            prev_gray = curr_gray
            processed_frames += 1
            
            if not json_output and processed_frames % 10 == 0:
                print(f"Processed {processed_frames} frames...")
        
        cap.release()
        
        if processed_frames == 0:
            raise ValueError("No frames processed")
        
        # Normalize maps
        self.energy_map = energy_map / processed_frames
        self.divergence_map = divergence_map / processed_frames
        self.curl_map = curl_map / processed_frames
        
        # Detect epicenters
        self.epicenter_candidates = self.detect_epicenters(
            self.energy_map, 
            self.divergence_map
        )
        
        results = {
            'video_path': self.video_path,
            'video_properties': {
                'width': width,
                'height': height,
                'fps': fps,
                'frame_count': frame_count,
                'processed_frames': processed_frames
            },
            'epicenters': self.epicenter_candidates[:5]  # Top 5
        }
        
        if not json_output:
            print(f"\nAnalysis complete! Processed {processed_frames} frames.")
            print(f"Found {len(self.epicenter_candidates)} potential epicenters.")
            
            if self.epicenter_candidates:
                print("\nTop 3 epicenter candidates:")
                for i, ep in enumerate(self.epicenter_candidates[:3], 1):
                    print(f"  {i}. Position: ({ep['x']}, {ep['y']}), Score: {ep['score']:.2f}")
        
        return results
    
    def visualize_results(self):
        """Create and save visualization of the analysis results."""
        if self.energy_map is None:
            raise ValueError("Must run analyze_video() first")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        # Energy map
        im1 = axes[0, 0].imshow(self.energy_map, cmap='hot')
        axes[0, 0].set_title('Strain Energy Map')
        axes[0, 0].axis('off')
        plt.colorbar(im1, ax=axes[0, 0])
        
        # Divergence map
        im2 = axes[0, 1].imshow(self.divergence_map, cmap='seismic', 
                                vmin=-np.abs(self.divergence_map).max(),
                                vmax=np.abs(self.divergence_map).max())
        axes[0, 1].set_title('Divergence Map (Expansion/Compression)')
        axes[0, 1].axis('off')
        plt.colorbar(im2, ax=axes[0, 1])
        
        # Curl map
        im3 = axes[1, 0].imshow(self.curl_map, cmap='twilight',
                                vmin=-np.abs(self.curl_map).max(),
                                vmax=np.abs(self.curl_map).max())
        axes[1, 0].set_title('Curl Map (Rotation)')
        axes[1, 0].axis('off')
        plt.colorbar(im3, ax=axes[1, 0])
        
        # Combined with epicenters
        combined = self.energy_map * np.abs(self.divergence_map)
        im4 = axes[1, 1].imshow(combined, cmap='hot')
        axes[1, 1].set_title('Combined Energy + Divergence (with Epicenters)')
        
        # Mark epicenters
        for ep in self.epicenter_candidates[:5]:
            axes[1, 1].plot(ep['x'], ep['y'], 'c*', markersize=20, markeredgecolor='blue')
            axes[1, 1].text(ep['x'], ep['y'] - 20, f"#{self.epicenter_candidates.index(ep) + 1}",
                          color='cyan', fontsize=12, fontweight='bold', ha='center')
        
        axes[1, 1].axis('off')
        plt.colorbar(im4, ax=axes[1, 1])
        
        plt.tight_layout()
        
        # Save the figure
        output_path = self.output_dir / 'epicenter_heatmap.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"\nVisualization saved to: {output_path}")
        
        plt.show()


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Energetic Epicenter Detector - Detect origin of energetic events in video'
    )
    parser.add_argument('video_path', help='Path to input video file')
    parser.add_argument('--output-dir', default='epicenter_analysis',
                       help='Directory for output files (default: epicenter_analysis)')
    parser.add_argument('--skip', type=int, default=1,
                       help='Process every Nth frame (default: 1, no skipping)')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON (no visualizations)')
    
    args = parser.parse_args()
    
    # Validate input
    if not os.path.exists(args.video_path):
        print(f"Error: Video file not found: {args.video_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Create detector
        detector = EnergeticEpicenterDetector(
            args.video_path,
            output_dir=args.output_dir,
            skip_frames=args.skip
        )
        
        # Analyze video
        results = detector.analyze_video(json_output=args.json)
        
        if args.json:
            # Output JSON for AI integration
            print(json.dumps(results, indent=2))
        else:
            # Create visualizations
            detector.visualize_results()
            
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        if not args.json:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
