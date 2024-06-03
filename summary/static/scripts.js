const searchBox = document.querySelector(".search-box");
const searchBtn = document.querySelector(".search-icon");
const cancelBtn = document.querySelector(".cancel-icon");
const searchInput = document.querySelector("input");
const searchData = document.querySelector(".search-data");
// const sub1Link = document.getElementById('sub1-Link'); // Note 버튼

// 검색창 버튼
searchBtn.onclick =()=>{
    searchBox.classList.add("active");
    searchBtn.classList.add("active");
    searchInput.classList.add("active");
    cancelBtn.classList.add("active");
    searchInput.focus();
    if(searchInput.value != ""){
      var values = searchInput.value;
      searchData.classList.remove("active");
      searchData.innerHTML = "You just typed " + "<span style='font-weight: 500;'>" + values + "</span>";
    }else{
      searchData.textContent = "";
    }
}
cancelBtn.onclick =()=>{
    searchBox.classList.remove("active");
    searchBtn.classList.remove("active");
    searchInput.classList.remove("active");
    cancelBtn.classList.remove("active");
    searchData.classList.toggle("active");
    searchInput.value = "";
}
console.log(getCookie('csrftoken'));

document.addEventListener('DOMContentLoaded', () => {
    const newDocumentBtn = document.querySelector('.new-document');
    const fileModal = document.getElementById('fileModal');
    const modal = document.getElementById('modal');
    let fileContentEditable = document.getElementById('fileContent'); // 편집 가능한 요소로 변경
    const fileModalTitle = document.getElementById('fileModalTitle');
    const fileInput = document.getElementById('fileInput'); // 파일 불러오기 클릭
    const uploadBtn = document.getElementById('uploadBtn'); // 업로드 버튼
    const modalCancelBtn = document.getElementById('modal-cancelBtn'); // 취소 버튼
    const saveFileBtn = document.getElementById('saveFileBtn'); // 저장 버튼
    const fileList = document.getElementById('fileList');
    const gptBtn = document.getElementById('GPTBtn'); // GPT 버튼
    const ocrBtn = document.getElementById('OCRBtn'); // OCR 버튼
    const sttBtn = document.getElementById('STTBtn'); // STT 버튼
    // 파일 리스트를 가져와 렌더링하는 함수
    function loadFileList() {
        fetch("http://localhost:8000/projectSummary/uploads/list/")
            .then(response => response.json())
            .then(data => {
                fileList.innerHTML = ''; // 기존 리스트 초기화
                data.forEach(file => {
                    var html = "";  // 문자열 저장 방식으로 변경
                    let div = document.createElement("div");
                    div.className = "file-box";
                    html += "<h2>" + file.name + "</h2>";
                    html += "<p>Size:" + formatFileSize(file.size) + "</p>";
                    html += "<button class=file-box-delete></button>"; // !!! 삭제 버튼 추가. 기능 구현해야함
                    div.innerHTML = html;  // 후에 한 번에 합치는 형식으로 변경
                    fileList.appendChild(div);
                });
            })
            .catch(error => {
                console.error('파일 리스트를 불러오는 중 오류 발생:', error);
            });
    }
    // 페이지가 로드될 때 파일 리스트를 로드
    loadFileList();

    // 새 문서 만들기 버튼 클릭 시 새 노트 모달 열기
    if (newDocumentBtn) {
        newDocumentBtn.addEventListener('click', () => {
            modal.style.display = 'block'; // 새 노트 모달 열기
        });
    }

    // 모달 외부나 취소 버튼 클릭 시 파일 입력 초기화
    const closeModal = () => {
        fileInput.value = '';
    };
    // 모달 외부 클릭 시 해당 모달 닫기
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            closeModal();
            modal.style.display = 'none'; // 새 노트 모달 닫기
        } else if (event.target === fileModal) {
            fileModal.style.display = 'none'; // 파일 모달 닫기
        }
    });

    // 취소 버튼 클릭 시 해당 모달 닫기
    modalCancelBtn.addEventListener('click', (event) => {
        if (event.target === modalCancelBtn) {
            modal.style.display = 'none'; // 새 노트 모달 닫기
        } else if (event.target === fileModal) {
            fileModal.style.display = 'none'; // 파일 모달 닫기
        }
    });

    // 파일 리스트 항목 클릭 시 파일 모달 열고 파일 내용 표시
    if (fileList) {
        fileList.addEventListener('click', (event) => {
            if (event.target.tagName === 'DIV') {
                const fileName = event.target.innerHTML.split("<")[1].slice(3); // 파일 이름 추출(추출 방식 변경됨)
                console.log(fileName);
                fileModalTitle.textContent = fileName; // 모달 제목 설정
                // 서버에서 파일 내용을 가져오는 요청
                fetch(`http://localhost:8000/projectSummary/gets/file/content/${encodeURIComponent(fileName)}/`)
                    .then(response => {
                        if (response.ok) {
                            return response.text();
                        }
                        throw new Error('파일 내용을 가져오지 못했습니다.');
                    })
                    .then(data => {
                        fileContentEditable.textContent = data; // 파일 내용을 모달에 표시 (편집 가능한 요소)
                        fileModal.style.display = 'block'; // 파일 모달 열기
                    })
                    .catch(error => {
                        console.error('파일 내용을 불러오는 중 오류 발생:', error);
                    });
            }
        });
    }

    // 파일 저장 버튼 클릭 시 편집된 파일 내용 저장
    if (saveFileBtn) {
        saveFileBtn.addEventListener('click', () => {
            let fileName = fileModalTitle.textContent;
            if (fileName.endsWith('/')) {
                fileName = fileName.slice(0, -1);
            }
            const editedContent = fileContentEditable.textContent; // 수정된 내용 가져오기
            const encodedFileName = encodeURIComponent(fileName);
            // 서버에 수정된 파일 내용을 전송
        fetch(`http://localhost:8000/projectSummary/updates/file/content/${encodedFileName}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'text/plain', // 수정된 내용은 텍스트로 전송
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: editedContent // 수정된 내용을 직접 전송
        })
        .then(response => {
            if (response.ok) { // 성공 시 동작
                console.log('파일 저장 성공!');
                fileModal.style.display = 'none'; // 저장 후 창 닫기
            } else {
                throw new Error('파일 저장 실패');
            }
        })
        .catch(error => {
            console.error('파일 저장 중 오류 발생:', error);
        });
        });
    }

    if (fileList) {
            fileList.addEventListener('click', (event) => {
                if (event.target.tagName === 'DIV') {
                    const selectedFile = event.target;
                    const parent = selectedFile.parentNode;
                    parent.prepend(selectedFile); // 선택한 파일 항목을 맨 앞으로 이동
                }
            });
        }


    gptBtn.addEventListener('click', () => {
        const formData = new FormData(document.getElementById('uploadForm'));
        fetch('http://localhost:8000/projectSummary/gpt/conversion/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // 성공적으로 처리되었을 경우 모달 닫기
            fileModal.style.display = 'none';
            console.log('GPT 처리 성공:', data);
            alert('파일에 있는 내용을 요약했습니다.');

        })
        .catch(error => {
            console.error('GPT 처리 중 오류 발생:', error);
        });
    })

    // OCR 버튼 클릭 시 OCR 처리를 수행하는 함수
    ocrBtn.addEventListener('click', () => {
        const formData = new FormData(document.getElementById('uploadForm'));
        fetch('http://localhost:8000/projectSummary/ocr/conversion/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                // 성공적으로 처리되었을 경우 모달 닫기
                modal.style.display = 'none';
                console.log('OCR 처리 성공:', data);
                alert('이미지에서 텍스트를 추출했습니다.');

            } else {
                console.error(data.error);
                alert('OCR 처리 실패: ' + data.error);
            }
        })
        .catch(error => {
            console.error('OCR 처리 중 오류 발생:', error);
            alert('OCR 처리 중 오류가 발생했습니다.');
        });
    });

    // STT 버튼 클릭 시 STT 변환을 수행하는 함수
    sttBtn.addEventListener('click', () => {
        const formData = new FormData(document.getElementById('uploadForm'));
        fetch('http://localhost:8000/projectSummary/stt/conversion/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.transcript) {
                // 성공적으로 변환이 완료된 경우
                modal.style.display = 'none'; // 모달 닫기
                console.log('STT 변환 성공:', data.transcript);
                // 여기서 변환된 텍스트를 어떻게 처리할지에 대한 로직을 추가할 수 있습니다.
                alert('오디오에서 텍스트를 추출했습니다.');
            } else {
                // 변환이 실패한 경우
                console.error(data.error);
                alert('STT 변환 실패: ' + data.error);
            }
        })
        .catch(error => {
            console.error('STT 변환 중 오류 발생:', error);
            alert('STT 변환 중 오류가 발생했습니다.');
        });
    });

  if (uploadBtn) {
    uploadBtn.addEventListener("click", () => {
      if (fileInput && fileInput.files && fileInput.files.length > 0) {
        let file = fileInput.files[0]; // 선택된 파일 가져오기
        const formData = new FormData();
        formData.append("file", file); // FormData에 파일 추가

        // 파일 업로드 요청 보내기
        fetch("http://localhost:8000/projectSummary/uploads/", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken")
          },
          body: formData,
        })
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
            throw new Error("파일 업로드 실패");
          })
          .then((data) => {
            if (data.message) {
                var html = ""; // 문자열 저장 방식으로 변경
                console.log(data.message);
                let div = document.createElement("div");
                html += "<h2>" + file.name + "</h2>";
                html += "<p>Size:" + formatFileSize(file.size) + "</p>";
                html += "<button class=file-box-delete></button>"; // !!! 삭제 버튼 추가. 기능 구현해야함
                div.className = "file-box";
                div.innerHTML = html; // 후에 한 번에 합치는 형식으로 변경
                // 그 전 코드
                // div.innerHTML =`<h2>${file.name}</h2><p>Size: ${formatFileSize(file.size)}</p><button class=>file-box-delete</button>`;
                fileList.appendChild(div);
                modal.style.display == 'none';
            } else {
                console.error(data.error);
               }
          })
          .catch((error) => {
            console.error("파일 업로드 중 오류 발생:", error);
          });
      } else {
        console.error("파일이 선택되지 않았습니다.");
      }
    });
  }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// sub1Link.onclick = function() {
//     location.href = "{% url 'sub1_page' %}";
//     console.log("good");
// };

function formatFileSize(bytes) {
    const kb = bytes / 1024;
    if (kb < 1024) {
        return kb.toFixed(2) + ' KB';
    } else {
        const mb = kb / 1024;
        return mb.toFixed(2) + ' MB';
    }
}
