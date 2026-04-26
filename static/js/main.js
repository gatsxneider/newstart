// DOMContentLoaded: HTML 문서가 완전히 로드되고 파싱된 후 스크립트를 실행합니다.
document.addEventListener('DOMContentLoaded', function() {
    
    // 1. 프로필 이미지 업로드 시 미리보기 기능 (사용자 경험 개선 목적)
    const photoInput = document.getElementById('photo');
    const profileImgPreview = document.getElementById('profileImgPreview');

    // 입력 요소와 미리보기 이미지가 모두 DOM에 존재하는지 확인
    if (photoInput && profileImgPreview) {
        // 파일 업로드 창에서 파일을 선택(변경)했을 때 이벤트 발생
        photoInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                // 파일 읽기가 성공적으로 완료되면 미리보기 이미지의 소스(src)를 업데이트
                reader.onload = function(e) {
                    profileImgPreview.src = e.target.result;
                }
                // 파일을 Base64 데이터 URL로 읽어들임
                reader.readAsDataURL(file);
            }
        });
    }

    // 2. 알림 메시지(Flash Message) 자동 숨김 처리
    // 화면에 나타난 플래시 메시지를 5초 후에 부드럽게 사라지게 합니다.
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            // CSS 트랜지션을 설정하여 투명도(opacity)를 서서히 낮춤 (페이드 아웃 효과)
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            
            // 애니메이션이 완료된 후 DOM 트리에서 요소 완전 제거 (메모리 관리 및 레이아웃 유지)
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000); // 5000ms = 5초 대기
    });
});
