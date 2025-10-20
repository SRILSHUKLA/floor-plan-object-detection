let scene, camera, renderer, plane, doors = [], controls;

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, 800/600, 0.1, 1000);
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(800, 600);
    document.getElementById('viewer').appendChild(renderer.domElement);

    // Add controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Add light
    const light = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(light);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(0, 10, 0);
    scene.add(directionalLight);

    // Add plane
    const geometry = new THREE.PlaneGeometry(10, 10);
    const material = new THREE.MeshLambertMaterial({color: 0xcccccc, side: THREE.DoubleSide});
    plane = new THREE.Mesh(geometry, material);
    plane.rotation.x = -Math.PI / 2;
    scene.add(plane);

    camera.position.set(0, 5, 5);
    camera.lookAt(0, 0, 0);

    animate();
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

function uploadImage() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Clear previous doors
        doors.forEach(door => scene.remove(door));
        doors = [];

        // Add new doors
        data.doors.forEach(doorData => {
            const doorGeometry = new THREE.BoxGeometry(doorData.w, 2, doorData.h); // Height 2 for 3D effect
            const doorMaterial = new THREE.MeshBasicMaterial({color: 0xff0000});
            const door = new THREE.Mesh(doorGeometry, doorMaterial);
            door.position.set(doorData.x, 1, doorData.z); // Y=1 to place on plane
            scene.add(door);
            doors.push(door);
        });
    })
    .catch(error => console.error('Error:', error));
}

init();
