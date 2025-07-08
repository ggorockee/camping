<script setup>
import { onMounted } from "vue";
import { render } from "timeago.js";

// onMounted: 컴포넌트가 화면에 마운트(표시)된 직후에 실행됩니다.
onMounted(() => {
  // 클래스가 'timeago'인 모든 요소를 찾아 timeago.js 기능을 적용합니다.
  render(document.querySelectorAll(".timeago"));
});
</script>

<template>
  <main class="main pt-4">
    <div class="container-fluid">
      <div class="row">
        
        <div class="col-md-3 ms-auto">
          <aside class="sidebar">
            <div class="card mb-4">
              <div class="card-body">
                <h4 class="card-title">About</h4>
                <p class="card-text">
                  Etiam rhoncus. Maecenas tempus, tellus eget condimentum
                  rhoncus, sem quam <a href="#">semper libero</a>, sit amet
                  adipiscing sem neque sed ipsum.
                </p>
              </div>
            </div>
            </aside>

          <aside class="sidebar sidebar-sticky">
            <div class="card mb-4">
              <div class="card-body">
                <h4 class="card-title">Tags</h4>
                <a class="btn btn-light btn-sm mb-1" href="page-category.html"
                  >Journey</a
                >
                <a class="btn btn-light btn-sm mb-1" href="page-category.html"
                  >Work</a
                >
                <a class="btn btn-light btn-sm mb-1" href="page-category.html"
                  >Lifestype</a
                >
                <a class="btn btn-light btn-sm mb-1" href="page-category.html"
                  >Photography</a
                >
                <a class="btn btn-light btn-sm mb-1" href="page-category.html"
                  >Food & Drinks</a
                >
              </div>
            </div>
            <div class="card mb-4">
              <div class="card-body">
                <h4 class="card-title">Popular stories</h4>

                <a href="post-image.html" class="d-inline-block">
                  <h4 class="h6">The blind man</h4>
                  <img class="card-img" src="/img/articles/2.jpg" alt="" />
                </a>
                <time class="timeago" datetime="2021-09-03 20:00"
                  >3 october 2021</time
                >
                in Lifestyle

                <a href="post-image.html" class="d-inline-block mt-3">
                  <h4 class="h6">Crying on the news</h4>
                  <img class="card-img" src="/img/articles/3.jpg" alt="" />
                </a>
                <time class="timeago" datetime="2021-07-16 20:00"
                  >16 july 2021</time
                >
                in Work
              </div>
            </div>
            </aside>
        </div>
      </div>
    </div>
  </main>

  <div class="site-newsletter">
    <div class="container">
      <div class="text-center">
        <h3 class="h4 mb-2">Subscribe to our newsletter</h3>
        <p class="text-muted">
          Join our monthly newsletter and never miss out on new stories and
          promotions.
        </p>

        <div class="row">
          <div class="col-xs-12 col-sm-9 col-md-7 col-lg-5 ms-auto me-auto">
            <div class="input-group mb-3 mt-3">
              <input
                type="text"
                class="form-control"
                placeholder="Email address"
                aria-label="Email address"
              />
              <span class="input-group-btn">
                <button class="btn btn-secondary" type="button">
                  Subscribe
                </button>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="site-instagram">
    <div class="action">
      <a class="btn btn-light" href="#"> Follow us @ Instagram </a>
    </div>
    <div class="row g-0">
      <div class="col-sm-6">
        <div class="row g-0">
          <div class="col-3">
            <a class="photo" href="#">
              <img class="img-fluid" src="/img/instagram/1.jpg" alt="" />
            </a>
          </div>
          <div class="col-3">
            <a class="photo" href="#">
              <img class="img-fluid" src="/img/instagram/2.jpg" alt="" />
            </a>
          </div>
          <div class="col-3">
            <a class="photo" href="#">
              <img class="img-fluid" src="/img/instagram/3.jpg" alt="" />
            </a>
          </div>
          <div class="col-3">
            <a class="photo" href="#">
              <img class="img-fluid" src="/img/instagram/4.jpg" alt="" />
            </a>
          </div>
        </div>
      </div>
      <div class="col-sm-6">
        <div class="row g-0">
          <div class="col-3">
            <a class="photo" href="#">
              <img class="img-fluid" src="/img/instagram/5.jpg" alt="" />
            </a>
          </div>
          <div class="col-3">
            <a class="photo" href="#">
              <img class="img-fluid" src="/img/instagram/6.jpg" alt="" />
            </a>
          </div>
          <div class="col-3">
            <a class="photo" href="#">
              <img class="img-fluid" src="/img/instagram/7.jpg" alt="" />
            </a>
          </div>
          <div class="col-3">
            <a class="photo" href="#">
              <img class="img-fluid" src="/img/instagram/8.jpg" alt="" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.main-content {
  position: relative;
}

.btn-plus {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  
  width: 58px;
  height: 58px;
  border-radius: 50%;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  padding: 0;
}
</style>