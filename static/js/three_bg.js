// 3D 구름 배경 애니메이션 설정 (Vanta.js + Three.js 사용)
// Three.js의 WebGL 렌더링을 활용하여 브라우저에서 동적인 배경을 생성합니다.

document.addEventListener("DOMContentLoaded", function() {
    // Vanta 스크립트가 정상적으로 로드되었는지 확인하여 에러 방지
    if (typeof VANTA !== 'undefined') {
        VANTA.CLOUDS({
            el: "#vanta-bg", // 애니메이션이 그려질 HTML 요소의 ID
            
            // 상호작용 설정
            mouseControls: true, // 마우스 이동에 반응하여 배경 구름이 약간 움직임
            touchControls: true, // 모바일 화면 터치 및 스와이프에 반응
            gyroControls: false, // 자이로센서(기기 기울임) 제어 비활성화
            
            // 화면 최소 크기 제약 (반응형 대응)
            minHeight: 200.00,
            minWidth: 200.00,
            
            // 색상 및 테마 설정 (밝고 아름다운 자연의 느낌)
            backgroundColor: 0xffffff, // 전체 바탕색 (흰색)
            skyColor: 0x68b8d7,        // 맑고 화창한 푸른 하늘색 (주요 색상)
            cloudColor: 0xffffff,      // 포근하고 하얀 구름 색상
            cloudShadowColor: 0x3d7090,// 구름 아래 생기는 입체감 있는 그림자 색상
            sunColor: 0xff9919,        // 밝고 따뜻한 햇살 느낌의 주황빛 색상
            sunGlareColor: 0xff6633,   // 햇살이 번지는 효과의 눈부심 색상
            
            // 태양의 상대적 위치 (X, Y, Z 좌표)
            sunPosition: new THREE.Vector3(1, 2, 0), 
            
            speed: 0.8 // 바람이 부는 듯한 구름의 자연스러운 이동 속도 조절
        });
    } else {
        // 네트워크 지연이나 스크립트 차단 등의 이유로 Vanta.js를 불러오지 못했을 때의 콘솔 경고
        console.warn('Vanta.js 라이브러리가 로드되지 않았습니다.');
    }
});
