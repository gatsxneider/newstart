document.addEventListener("DOMContentLoaded", function() {
    if (typeof VANTA !== 'undefined') {
        VANTA.CLOUDS({
            el: "#vanta-bg",
            mouseControls: true,
            touchControls: true,
            gyroControls: false,
            minHeight: 200.00,
            minWidth: 200.00,
            backgroundColor: 0xffffff,
            skyColor: 0x68b8d7, // 맑고 밝은 하늘색
            cloudColor: 0xffffff, // 하얀 구름
            cloudShadowColor: 0x3d7090,
            sunColor: 0xff9919, // 따뜻한 햇빛 느낌
            sunGlareColor: 0xff6633,
            sunPosition: new THREE.Vector3(1, 2, 0), // 태양 위치
            speed: 0.8 // 구름 이동 속도
        });
    } else {
        console.warn('Vanta is not loaded.');
    }
});
