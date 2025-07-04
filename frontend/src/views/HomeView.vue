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
    <div class="container">
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
                Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus,
                sem quam semper libero, sit amet adipiscing sem neque sed ipsum.
              </p>
            </div>
          </article>
          <!-- /.card -->

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
                Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus,
                sem quam semper libero, sit amet adipiscing sem neque sed ipsum.
              </p>
            </div>
          </article>
          <!-- /.card -->
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
                Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus,
                sem quam semper libero, sit amet adipiscing sem neque sed ipsum.
              </p>
            </div>
          </article>
          <!-- /.card -->

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
                Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus,
                sem quam semper libero, sit amet adipiscing sem neque sed ipsum.
              </p>
            </div>
          </article>
          <!-- /.card -->
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
                Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus,
                sem quam semper libero, sit amet adipiscing sem neque sed ipsum.
              </p>
            </div>
          </article>
          <!-- /.card -->

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
                Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus,
                sem quam semper libero, sit amet adipiscing sem neque sed ipsum.
              </p>
            </div>
          </article>
          <!-- /.card -->
        </div>
      </div>
    </div>
  </main>
</template>
