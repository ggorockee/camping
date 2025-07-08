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
        <div class="col-md-9 main-content">
          <!-- 게시물 목록 -->
          <div class="row">
            <div class="col-md-4">
              <article class="card mb-4">
                <header class="card-header">
                  <div class="card-meta">
                    <a href="#"
                      ><time class="timeago" datetime="2021-09-26 20:00"
                        >26 october 2021</time
                      ></a
                    >
                    in <a href="page-category.html">Journey</a>
                  </div>
                  <a href="post-image.html">
                    <h4 class="card-title">How can we sing about love?</h4>
                  </a>
                </header>
                <a href="post-image.html">
                  <img class="card-img" src="/img/articles/18.jpg" alt="" />
                </a>
                <div class="card-body">
                  <p class="card-text">
                    Etiam rhoncus. Maecenas tempus, tellus eget condimentum
                    rhoncus, sem quam semper libero, sit amet adipiscing sem
                    neque sed ipsum.
                  </p>
                </div>
              </article>
              <article class="card mb-4">
                <header class="card-header">
                  <div class="card-meta">
                    <a href="#"
                      ><time class="timeago" datetime="2021-09-03 20:00"
                        >3 october 2021</time
                      ></a
                    >
                    in <a href="page-category.html">Lifestyle</a>
                  </div>
                  <a href="post-image.html">
                    <h4 class="card-title">Oh, I guess they have the blues</h4>
                  </a>
                </header>
                <a href="post-image.html">
                  <img class="card-img" src="/img/articles/22.jpg" alt="" />
                </a>
                <div class="card-body">
                  <p class="card-text">
                    Etiam rhoncus. Maecenas tempus, tellus eget condimentum
                    rhoncus, sem quam semper libero, sit amet adipiscing sem
                    neque sed ipsum.
                  </p>
                </div>
              </article>
            </div>
            <div class="col-md-4">
              <article class="card mb-4">
                <header class="card-header">
                  <div class="card-meta">
                    <a href="#"
                      ><time class="timeago" datetime="2021-07-16 20:00"
                        >16 july 2021</time
                      ></a
                    >
                    in <a href="page-category.html">Work</a>
                  </div>
                  <a href="post-image.html">
                    <h4 class="card-title">
                      How can we, how can we sing about ourselves?
                    </h4>
                  </a>
                </header>
                <a href="post-image.html">
                  <img class="card-img" src="/img/articles/3.jpg" alt="" />
                </a>
                <div class="card-body">
                  <p class="card-text">
                    Etiam rhoncus. Maecenas tempus, tellus eget condimentum
                    rhoncus, sem quam semper libero, sit amet adipiscing sem
                    neque sed ipsum.
                  </p>
                </div>
              </article>
              <article class="card mb-4">
                <header class="card-header">
                  <div class="card-meta">
                    <a href="#"
                      ><time class="timeago" datetime="2021-09-15 20:00"
                        >15 october 2021</time
                      ></a
                    >
                    in <a href="page-category.html">Lifestyle</a>
                  </div>
                  <a href="post-image.html">
                    <h4 class="card-title">The king is made of paper</h4>
                  </a>
                </header>
                <a href="post-image.html">
                  <img class="card-img" src="/img/articles/20.jpg" alt="" />
                </a>
                <div class="card-body">
                  <p class="card-text">
                    Etiam rhoncus. Maecenas tempus, tellus eget condimentum
                    rhoncus, sem quam semper libero, sit amet adipiscing sem
                    neque sed ipsum.
                  </p>
                </div>
              </article>
            </div>
            <div class="col-md-4">
              <article class="card mb-4">
                <header class="card-header">
                  <div class="card-meta">
                    <a href="#"
                      ><time class="timeago" datetime="2021-08-24 20:00"
                        >24 august 2021</time
                      ></a
                    >
                    in <a href="page-category.html">Work</a>
                  </div>
                  <a href="post-image.html">
                    <h4 class="card-title">Crying on the news</h4>
                  </a>
                </header>
                <a href="post-image.html">
                  <img class="card-img" src="/img/articles/5.jpg" alt="" />
                </a>
                <div class="card-body">
                  <p class="card-text">
                    Etiam rhoncus. Maecenas tempus, tellus eget condimentum
                    rhoncus, sem quam semper libero, sit amet adipiscing sem
                    neque sed ipsum.
                  </p>
                </div>
              </article>
              <article class="card mb-4">
                <header class="card-header">
                  <div class="card-meta">
                    <a href="#"
                      ><time class="timeago" datetime="2021-05-08 20:00"
                        >8 may 2021</time
                      ></a
                    >
                    in <a href="page-category.html">Journey</a>
                  </div>
                  <a href="post-image.html">
                    <h4 class="card-title">How can you not sing about love?</h4>
                  </a>
                </header>
                <a href="post-image.html">
                  <img class="card-img" src="/img/articles/1.jpg" alt="" />
                </a>
                <div class="card-body">
                  <p class="card-text">
                    Etiam rhoncus. Maecenas tempus, tellus eget condimentum
                    rhoncus, sem quam semper libero, sit amet adipiscing sem
                    neque sed ipsum.
                  </p>
                </div>
              </article>
            </div>
          </div>
        </div>
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
</template>

<!-- ✅ 이 컴포넌트에는 더 이상 버튼 스타일이 필요 없으므로 <style> 태그를 삭제했습니다. -->
<style scoped>
.main-content {
  position: relative;
}
</style>
