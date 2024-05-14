/*scripts.js*/
const newDocumentBtn = document.querySelector('.new-document');
const modal = document.getElementById('modal');

newDocumentBtn.addEventListener('click', () => {
    modal.style.display = 'block';
});

// 모달 외부 클릭 시 모달 숨기기
window.addEventListener('click', (event) => {
    // 모달 요소 내부를 클릭한 경우에는 모달을 숨기지 않음
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    if (fileInput && fileInput.files && fileInput.files.length > 0) {
        const file = fileInput.files[0]; // 선택된 파일 가져오기
        const formData = new FormData();
        formData.append('file', file); // FormData에 파일 추가

        // 파일 업로드 요청 보내기
        fetch('http://localhost:3000/uploads', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                console.log('파일 업로드 성공!');
                // 업로드 성공 시 추가적인 동작 수행
                const fileList = document.getElementById('fileList');
                const li = document.createElement('li');
                li.textContent = `${file.name} (${formatFileSize(file.size)})`;
                fileList.appendChild(li);
            } else {
                console.error('파일 업로드 실패');
            }
        })
        .catch(error => {
            console.error('파일 업로드 중 오류 발생:', error);
        });
    } else {
        console.error('파일이 선택되지 않았습니다.');
    }
}

// 파일 크기 포맷 함수 (KB 또는 MB 단위로 변환)
function formatFileSize(bytes) {
    const kb = bytes / 1024;
    if (kb < 1024) {
        return kb.toFixed(2) + ' KB';
    } else {
        const mb = kb / 1024;
        return mb.toFixed(2) + ' MB';
    }
}

// DOM이 로드되면 실행되는 함수
document.addEventListener('DOMContentLoaded', () => {
    const uploadBtn = document.getElementById('uploadBtn');
    if (uploadBtn) {
        uploadBtn.addEventListener('click', uploadFile);
    } else {
        console.error('uploadBtn을 찾을 수 없습니다.');
    }
});
