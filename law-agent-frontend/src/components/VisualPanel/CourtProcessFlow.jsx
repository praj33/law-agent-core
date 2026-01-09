import { Canvas, useFrame } from "@react-three/fiber";
import { Text, Line } from "@react-three/drei";
import { useRef, useMemo } from "react";

function StepNode({ position, label, active }) {
  const meshRef = useRef();

  useFrame(() => {
    if (active && meshRef.current) {
      meshRef.current.rotation.y += 0.008;
    }
  });

  return (
    <group position={position}>
      <mesh ref={meshRef}>
        <sphereGeometry args={[0.28, 32, 32]} />
        <meshStandardMaterial
          color={active ? "#4f46e5" : "#444"}
          emissive={active ? "#4f46e5" : "#000"}
          emissiveIntensity={active ? 0.7 : 0}
        />
      </mesh>

      <Text
        position={[0, -0.55, 0]}
        fontSize={0.16}
        color={active ? "#ffffff" : "#bbbbbb"}
        anchorX="center"
        anchorY="middle"
        maxWidth={1}
        textAlign="center"
      >
        {label}
      </Text>
    </group>
  );
}

export default function CourtProcessFlow({ steps }) {
  const activeIndex = Math.floor((Date.now() / 2200) % steps.length);

  const positions = useMemo(
    () =>
      steps.map((_, i) => [-2 + i * 1, 0, 0]),
    [steps]
  );

  return (
    <>
      <Canvas
        style={{ height: 300, marginTop: 10 }}
        camera={{ position: [0, 0, 5], fov: 50 }}
      >
        <ambientLight intensity={0.6} />
        <pointLight position={[5, 5, 5]} intensity={1} />

        {/* Connecting line */}
        <Line
          points={positions}
          color="#333"
          lineWidth={1}
        />

        {steps.map((step, i) => (
          <StepNode
            key={step}
            position={positions[i]}
            label={step}
            active={i === activeIndex}
          />
        ))}
      </Canvas>

      {/* Current stage indicator */}
      <div
        style={{
          marginTop: 8,
          padding: "8px 12px",
          background: "#262626",
          borderRadius: 10,
          textAlign: "center"
        }}
      >
        <span style={{ opacity: 0.7 }}>Current stage:</span>{" "}
        <b>{steps[activeIndex]}</b>
      </div>
    </>
  );
}
