import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';

interface StarFieldBackgroundProps {
  className?: string;
  starsCount?: number;
  rotationSpeedX?: number;
  rotationSpeedY?: number;
}

export function StarFieldBackground({ 
  className,
  starsCount = 1500,
  rotationSpeedX = 0.0003,
  rotationSpeedY = 0.0004
}: StarFieldBackgroundProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (!containerRef.current) return;
    
    // Setup scene
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, containerRef.current.clientWidth / containerRef.current.clientHeight, 0.1, 1000);
    
    const renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight);
    containerRef.current.appendChild(renderer.domElement);
    
    // Create stars
    const starsGeometry = new THREE.BufferGeometry();
    const starsMaterial = new THREE.PointsMaterial({
      color: 0xffffff,
      size: 0.7,
      transparent: true,
    });
    
    const starsPositions = new Float32Array(starsCount * 3);
    
    for (let i = 0; i < starsCount * 3; i += 3) {
      starsPositions[i] = (Math.random() - 0.5) * 100;
      starsPositions[i + 1] = (Math.random() - 0.5) * 100;
      starsPositions[i + 2] = (Math.random() - 0.5) * 100;
    }
    
    starsGeometry.setAttribute('position', new THREE.BufferAttribute(starsPositions, 3));
    const stars = new THREE.Points(starsGeometry, starsMaterial);
    scene.add(stars);
    
    // Position camera
    camera.position.z = 20;
    
    // Handle window resize
    const handleResize = () => {
      if (!containerRef.current) return;
      
      camera.aspect = containerRef.current.clientWidth / containerRef.current.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight);
    };
    
    window.addEventListener('resize', handleResize);
    
    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      
      stars.rotation.x += rotationSpeedX;
      stars.rotation.y += rotationSpeedY;
      
      renderer.render(scene, camera);
    };
    
    animate();
    
    // Clean up
    return () => {
      window.removeEventListener('resize', handleResize);
      if (containerRef.current && containerRef.current.contains(renderer.domElement)) {
        containerRef.current.removeChild(renderer.domElement);
      }
      
      scene.remove(stars);
      starsGeometry.dispose();
      starsMaterial.dispose();
      renderer.dispose();
    };
  }, [starsCount, rotationSpeedX, rotationSpeedY]);
  
  return (
    <div 
      ref={containerRef} 
      className={`absolute inset-0 h-full w-full overflow-hidden ${className || ''}`}
      aria-hidden="true"
    /> 
  );
}
