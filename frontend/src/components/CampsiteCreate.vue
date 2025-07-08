<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <div class="text-center mb-8">
          <h1 class="text-h4 font-weight-bold">새로운 캠핑장 등록</h1>
          <p class="text-medium-emphasis mt-2">
            캠핑장의 정보를 입력하고 멋진 사진을 추가하여 호스트가 되어보세요.
          </p>
        </div>

        <v-card class="mb-6" variant="outlined">
          <v-card-text>
            <h2 class="text-h6 font-weight-medium mb-4">1. 기본 정보</h2>
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="campsiteData.name"
                  label="캠핑장 이름"
                  variant="outlined"
                  prepend-inner-icon="mdi-storefront-outline"
                  :rules="[(v) => !!v || '이름은 필수입니다.']"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="campsiteData.address"
                  label="주소"
                  variant="outlined"
                  prepend-inner-icon="mdi-map-marker-outline"
                  :rules="[(v) => !!v || '주소는 필수입니다.']"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-textarea
              v-model="campsiteData.description"
              label="캠핑장 설명"
              variant="outlined"
              rows="4"
              prepend-inner-icon="mdi-text-box-outline"
            ></v-textarea>
          </v-card-text>
        </v-card>

        <v-card class="mb-6" variant="outlined">
          <v-card-text>
            <h2 class="text-h6 font-weight-medium mb-4">2. 추가 정보 (선택)</h2>
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="campsiteData.phone_number"
                  label="전화번호"
                  variant="outlined"
                  prepend-inner-icon="mdi-phone-outline"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="campsiteData.blog_url"
                  label="블로그 또는 홈페이지"
                  variant="outlined"
                  prepend-inner-icon="mdi-web"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <v-card variant="outlined">
          <v-card-text>
            <h2 class="text-h6 font-weight-medium mb-4">
              3. 사진 등록 (최소 3장)
            </h2>
            <div
              class="dropzone"
              @dragover.prevent="dragOver"
              @dragleave.prevent="dragLeave"
              @drop.prevent="drop"
              :class="{ 'is-dragover': isDragOver }"
              @click="triggerFileInput"
            >
              <div class="text-center">
                <v-icon size="50" color="grey-darken-1">mdi-cloud-upload-outline</v-icon>
                <p class="text-grey-darken-1 mt-2">
                  이곳에 사진을 드래그하거나 클릭하여 선택
                </p>
              </div>
            </div>
            <input
              ref="fileInput"
              type="file"
              multiple
              accept="image/*"
              @change="handleFileSelect"
              hidden
            />
            <v-row class="mt-4">
              <v-col
                v-for="(image, index) in images"
                :key="image.id"
                cols="6" sm="4" md="3"
              >
                <v-card>
                  <v-img :src="image.previewSrc" aspect-ratio="1" cover>
                    <v-btn
                      @click="removeImage(index)"
                      icon="mdi-close"
                      size="x-small"
                      color="white"
                      class="ma-1"
                      style="position: absolute; top: 0; right: 0; background-color: rgba(0, 0, 0, 0.5);"
                    ></v-btn>
                  </v-img>
                  <v-progress-linear
                    v-if="image.status === 'uploading'"
                    :model-value="image.progress"
                    color="primary"
                    height="6"
                  ></v-progress-linear>
                  <v-overlay
                    :model-value="image.status === 'success' || image.status === 'error'"
                    contained
                    scrim="#00000099"
                    class="align-center justify-center"
                  >
                    <v-icon v-if="image.status === 'success'" color="success" size="x-large">mdi-check-circle</v-icon>
                    <v-icon v-if="image.status === 'error'" color="error" size="x-large">mdi-alert-circle</v-icon>
                  </v-overlay>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <v-alert v-if="errorMessage" type="error" closable class="mt-6">
            {{ errorMessage }}
        </v-alert>

        <div class="text-center mt-6">
          <v-btn
            :loading="isLoading"
            :disabled="!isFormValid"
            @click="createCampsite"
            size="large"
            block
            class="btn-signup"
            :class="{ 'is-valid': isFormValid }"
          >
            캠핑장 등록 완료하기
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
// ✅ 'computed'를 vue에서 import합니다.
import { ref, reactive, computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const campsiteData = reactive({
  name: "",
  description: "",
  address: "",
  phone_number: "",
  blog_url: "",
});

const fileInput = ref(null);
const images = ref([]);
const isLoading = ref(false);
const errorMessage = ref("");
const isDragOver = ref(false);
let fileCounter = 0;

// ✅ 모든 입력값이 유효한지 실시간으로 확인하는 computed 속성
const isFormValid = computed(() => {
  return (
    campsiteData.name.trim() !== "" &&
    campsiteData.address.trim() !== "" &&
    images.value.length >= 3
  );
});

const triggerFileInput = () => fileInput.value.click();

const addFiles = (files) => {
  Array.from(files).forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      images.value.push({
        id: fileCounter++,
        file: file,
        previewSrc: e.target.result,
        status: "pending",
        progress: 0,
      });
    };
    reader.readAsDataURL(file);
  });
};

const handleFileSelect = (event) => addFiles(event.target.files);

const removeImage = (index) => images.value.splice(index, 1);

const dragOver = () => (isDragOver.value = true);

const dragLeave = () => (isDragOver.value = false);

const drop = (event) => {
  isDragOver.value = false;
  addFiles(event.dataTransfer.files);
};

async function createCampsite() {
  // ✅ isFormValid로 유효성 검사를 한 번에 처리
  if (!isFormValid.value) {
    errorMessage.value = "모든 필수 항목을 올바르게 입력해주세요.";
    return;
  }
  
  errorMessage.value = "";
  isLoading.value = true;

  try {
    const token = localStorage.getItem("accessToken");
    if (!token) throw new Error("인증 토큰이 없습니다. 로그인 후 이용해주세요.");

    const pendingImages = images.value.filter((img) => img.status === "pending");
    const urlPromises = pendingImages.map(() =>
      fetch("/api/v1/campsites/images/upload-url/", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      }).then((res) =>
        res.ok ? res.json() : Promise.reject(new Error("URL 발급 실패"))
      )
    );

    const urlResults = await Promise.all(urlPromises);

    const uploadPromises = pendingImages.map((image, index) => {
      image.status = "uploading";
      return new Promise((resolve, reject) => {
        // fetch 부분을 실제 업로드 시뮬레이션으로 변경하여 즉시 완료되도록 수정
        // 실제 프로젝트에서는 이 부분을 원래 로직으로 유지해야 합니다.
        setTimeout(() => {
            const formData = new FormData();
            formData.append("file", image.file);
            fetch(urlResults[index].uploadURL, {
                method: "POST",
                body: formData,
            }).then(res => {
                if (res.ok) {
                    image.status = "success";
                    image.progress = 100;
                    image.cloudflareId = urlResults[index].id;
                    resolve(true);
                } else {
                    image.status = "error";
                    reject(new Error(`Image ${image.file.name} upload failed`));
                }
            }).catch(err => {
                image.status = 'error';
                reject(err);
            });
        }, 500); // 0.5초 후 업로드 시도
      });
    });

    await Promise.all(uploadPromises);

    if (images.value.some((img) => img.status === "error")) {
      throw new Error("일부 이미지 업로드에 실패했습니다.");
    }

    const finalPayload = {
      ...campsiteData,
      image_ids: images.value.map((img) => img.cloudflareId),
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

    alert("🎉 캠핑장이 성공적으로 등록되었습니다!");
    router.push({ name: "home" });

  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.dropzone {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 40px;
  transition: all 0.3s ease;
  cursor: pointer;
}
.dropzone.is-dragover {
  border-color: #2196f3;
  background-color: #f0f8ff;
}

/* ✅ 버튼 기본 스타일 및 유효할 때 적용될 스타일 추가 */
.btn-signup {
  /* 비활성화 상태일 때의 기본 스타일 */
  background-color: #e0e0e0 !important;
  color: #a0a0a0 !important;
  transition: background-color 0.3s ease, color 0.3s ease;
}
.btn-signup.is-valid {
  /* 활성화 상태일 때의 스타일 */
  background-color: black !important;
  color: white !important;
  font-weight: bold;
}
</style>