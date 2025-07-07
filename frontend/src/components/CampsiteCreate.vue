<template>
  <main class="main pt-4">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-9">
          <div class="card mb-4">
            <div class="card-body">
              <h3 class="card-title">새로운 캠핑장 등록</h3>

              <div class="mb-3">
                <label for="campsiteName" class="form-label">캠핑장 이름</label>
                <input
                  type="text"
                  class="form-control"
                  id="campsiteName"
                  v-model="campsiteData.name"
                  placeholder="예: 꼬록키 캠핑장"
                />
              </div>
              <div class="mb-3">
                <label for="campsiteDesc" class="form-label">캠핑장 설명</label>
                <textarea
                  class="form-control"
                  id="campsiteDesc"
                  rows="3"
                  v-model="campsiteData.description"
                ></textarea>
              </div>

              <hr class="my-4" />

              <div class="photo-uploader">
                <h4>캠핑장 사진 등록 (최소 3장)</h4>
                <p class="text-muted">
                  대표 사진을 포함하여 캠핑장의 매력을 보여줄 사진을
                  등록해주세요.
                </p>

                <div class="preview-container">
                  <div
                    v-for="(src, index) in imagePreviews"
                    :key="index"
                    class="preview-item"
                  >
                    <img :src="src" alt="Image preview" />
                    <button
                      @click="removeImage(index)"
                      class="remove-btn"
                      title="삭제"
                    >
                      &times;
                    </button>
                  </div>

                  <div
                    v-if="imagePreviews.length < 10"
                    class="add-photo-box"
                    @click="triggerFileInput"
                  >
                    <div class="add-photo-content">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="32"
                        height="32"
                        fill="currentColor"
                        class="bi bi-images"
                        viewBox="0 0 16 16"
                      >
                        <path
                          d="M4.502 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3"
                        />
                        <path
                          d="M14.002 13a2 2 0 0 1-2 2h-10a2 2 0 0 1-2-2V5A2 2 0 0 1 2 3a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2zM12 3a1 1 0 0 0-1-1h-10a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V3zM1 4a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V14a1 1 0 0 0-1-1H1z"
                        />
                      </svg>
                      <div class="mt-2">사진 추가하기</div>
                    </div>
                  </div>
                </div>
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept="image/*"
                  @change="handleFileSelect"
                  style="display: none"
                />
              </div>

              <div v-if="errorMessage" class="alert alert-danger mt-3">
                {{ errorMessage }}
              </div>

              <button
                @click="createCampsite"
                :disabled="isLoading || selectedFiles.length < 3"
                class="btn btn-primary w-100 mt-4"
              >
                <span
                  v-if="isLoading"
                  class="spinner-border spinner-border-sm"
                  role="status"
                  aria-hidden="true"
                ></span>
                <span v-if="isLoading"> 등록 중...</span>
                <span v-else>캠핑장 등록하기</span>
              </button>
            </div>
          </div>
        </div>

        <div class="col-md-3 ms-auto">
          <aside class="sidebar sidebar-sticky">
            <div class="card mb-4">
              <div class="card-body">
                <h4 class="card-title">등록 가이드</h4>
                <p class="card-text small">
                  - 대표 사진은 가장 잘 나온 사진으로 선택해주세요.<br />
                  - 다양한 각도에서 찍은 사진을 올리면 좋습니다.<br />
                  - 최소 3장 이상의 사진이 필요합니다.
                </p>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const campsiteData = reactive({ name: "", description: "" });
const fileInput = ref(null);
const selectedFiles = ref([]);
const imagePreviews = ref([]);
const isLoading = ref(false);
const errorMessage = ref("");

const triggerFileInput = () => fileInput.value.click();

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files);
  if (!files.length) return;

  selectedFiles.value.push(...files);

  files.forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => imagePreviews.value.push(e.target.result);
    reader.readAsDataURL(file);
  });
};

const removeImage = (index) => {
  selectedFiles.value.splice(index, 1);
  imagePreviews.value.splice(index, 1);
};

async function createCampsite() {
  errorMessage.value = "";
  if (!campsiteData.name.trim()) {
    errorMessage.value = "캠핑장 이름을 입력해주세요.";
    return;
  }
  if (selectedFiles.value.length < 3) {
    errorMessage.value = "최소 3장 이상의 사진을 선택해야 합니다.";
    return;
  }

  isLoading.value = true;
  try {
    const token = localStorage.getItem("accessToken");
    if (!token)
      throw new Error("인증 토큰이 없습니다. 로그인 후 이용해주세요.");

    // 1. URL 병렬 요청
    const urlPromises = selectedFiles.value.map(() =>
      fetch("/api/v1/campsites/images/upload-url/", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      }).then((res) => {
        if (!res.ok)
          return Promise.reject(new Error("업로드 URL 발급에 실패했습니다."));
        return res.json();
      })
    );
    const urlResults = await Promise.all(urlPromises);

    // 2. 파일 병렬 업로드
    const uploadPromises = selectedFiles.value.map((file, index) => {
      const formData = new FormData();
      formData.append("file", file);
      return fetch(urlResults[index].uploadURL, {
        method: "POST",
        body: formData,
      });
    });
    await Promise.all(uploadPromises);

    // 3. 최종 데이터 백엔드 전송
    const uploadedImageIds = urlResults.map((result) => result.id);
    const finalPayload = {
      name: campsiteData.name,
      description: campsiteData.description,
      image_ids: uploadedImageIds,
    };

    const finalResponse = await fetch("/api/v1/campsites/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(finalPayload),
    });

    if (!finalResponse.ok) {
      const errorData = await finalResponse.json();
      throw new Error(errorData.detail || "캠핑장 등록에 실패했습니다.");
    }

    alert("캠핑장이 성공적으로 등록되었습니다!");
    router.push({ name: "home" });
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.photo-uploader {
  border-top: 1px solid #eee;
  padding-top: 1.5rem;
}
.preview-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
.preview-item {
  position: relative;
  width: 100%;
  padding-top: 100%;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f0f0f0;
}
.preview-item img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.remove-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 16px;
  line-height: 24px;
  text-align: center;
  padding: 0;
}
.add-photo-box {
  border: 2px dashed #ccc;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  width: 100%;
  padding-top: 100%;
  position: relative;
  transition: border-color 0.2s;
}
.add-photo-box:hover {
  border-color: #0d6efd;
}
.add-photo-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #555;
  font-size: 0.9rem;
}
</style>
