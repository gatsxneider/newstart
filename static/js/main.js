document.addEventListener('DOMContentLoaded', function() {
    // 프로필 이미지 미리보기 기능 (선택적)
    const photoInput = document.getElementById('photo');
    const profileImgPreview = document.getElementById('profileImgPreview');

    if (photoInput && profileImgPreview) {
        photoInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    profileImgPreview.src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // 알림 메시지 5초 후 자동 숨김
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });
});
