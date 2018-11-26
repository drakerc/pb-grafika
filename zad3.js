window.onload = function() {
    function createColoredCube() {
        let faceIndices = ['a', 'b', 'c'];
        let geometry = new THREE.BoxGeometry(1, 1, 1);
        geometry.faces.forEach(face => {
            for (let i = 0; i < 3; i++) {
                point = geometry.vertices[face[faceIndices[i]]];

                color = new THREE.Color(
                  point.x + 0.5,
                  point.y + 0.5,
                  point.z + 0.5
                );
                console.log(color);
                face.vertexColors[i] = color;
            }
        });

        let material = new THREE.MeshBasicMaterial({
            vertexColors: THREE.VertexColors
        });

        return new THREE.Mesh(geometry, material);
    }

    let scene = new THREE.Scene();
    let camera = new THREE.PerspectiveCamera(30, window.innerWidth / window.innerHeight, 1, 250);
    camera.position.z = 5;

    let cube = createColoredCube();
    scene.add(cube);

    let renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    new THREE.OrbitControls(camera, renderer.domElement);

    function render() {
      requestAnimationFrame(render);
      renderer.render(scene, camera);
    };

    render();
};