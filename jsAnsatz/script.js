// Importiere Three.js (lokal installiert)
import * as THREE from './node_modules/three/build/three.module.js';

// Scene erstellen
const scene = new THREE.Scene();

// Kamera erstellen
//const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
camera.position.z = 5;

// Renderer erstellen
const renderer = new THREE.WebGLRenderer();
//renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setSize(600,600);
document.body.appendChild(renderer.domElement);

// Würfel und Kanten erstellen
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshStandardMaterial({ color: 0x0077ff });
const cube = new THREE.Mesh(geometry, material);
geometry.scale(2,2,2)
scene.add(cube);

//Kanten hinzufügen
const edges = new THREE.EdgesGeometry(geometry);
const lineMaterial = new THREE.LineBasicMaterial({ color: 0xffffff });
const edgeLines = new THREE.LineSegments(edges, lineMaterial);
scene.add(edgeLines);

//Eckpunkte hinzufügen
const verticesMaterial = new THREE.PointsMaterial({ color: 0xff0000, size: 0.1 });
const verticesPoints = new THREE.Points(geometry, verticesMaterial);
scene.add(verticesPoints);


//Erstelle eine Gruppe und füge Würfel, Kanten und Eckpunkte hinzu
const cubeGroup = new THREE.Group();
cubeGroup.add(cube);
cubeGroup.add(edgeLines);
cubeGroup.add(verticesPoints);
scene.add(cubeGroup);

//Beleuchtung
const ambientLight = new THREE.AmbientLight(0x404040, 2);
scene.add(ambientLight);

//Schieberegler für Rotation
const xRotationSlider = document.getElementById('x-rotation');
const yRotationSlider = document.getElementById('y-rotation');
const zRotationSlider = document.getElementById('z-rotation');

// Event-Listener für Schieberegler
xRotationSlider.addEventListener('input', () => {
    cubeGroup.rotation.x = parseFloat(xRotationSlider.value);
    cube.rota
});
yRotationSlider.addEventListener('input', () => {
    cubeGroup.rotation.y = parseFloat(yRotationSlider.value);
});
zRotationSlider.addEventListener('input', () => {
    cubeGroup.rotation.z = parseFloat(zRotationSlider.value);
});

// Animationsschleife
function animate() {
    requestAnimationFrame(animate);

    // Rotation des Würfels
    cubeGroup.rotation.x += 0.01;
    cubeGroup.rotation.y += 0.01;
    

    renderer.render(scene, camera);
}
console.log("hallo!");
animate();


