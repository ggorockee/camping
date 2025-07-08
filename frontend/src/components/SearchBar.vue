<template>
  <header class="mb-12">
    <div class="w-full max-w-4xl mx-auto">
      <div class="flex justify-center mb-4">
        <button class="px-4 py-2 font-semibold text-black border-b-2 border-black">숙소</button>
        <button class="px-4 py-2 font-semibold text-gray-500 hover:text-black">체험</button>
        <button class="px-4 py-2 font-semibold text-gray-500 hover:text-black">서비스</button>
      </div>

      <div class="flex items-center w-full bg-white border border-gray-200 rounded-full shadow-md">
        
        <div class="flex-1 pl-8 pr-4 py-3 cursor-pointer hover:bg-gray-100 rounded-l-full">
          <label for="location" class="block text-xs font-bold text-gray-800">여행지</label>
          <input type="text" id="location" placeholder="여행지 검색" class="w-full text-sm text-gray-500 bg-transparent focus:outline-none placeholder-gray-400">
        </div>
        
        <div class="h-8 border-r border-gray-300"></div>

        <div class="px-4 py-3 cursor-pointer hover:bg-gray-100">
          <p class="text-xs font-bold text-gray-800">체크인</p>
          <p class="text-sm text-gray-500">날짜 추가</p>
        </div>

        <div class="h-8 border-r border-gray-300"></div>

        <div class="px-4 py-3 cursor-pointer hover:bg-gray-100">
          <p class="text-xs font-bold text-gray-800">체크아웃</p>
          <p class="text-sm text-gray-500">날짜 추가</p>
        </div>

        <div class="h-8 border-r border-gray-300"></div>

        <div class="flex items-center pl-4 pr-2 py-2 cursor-pointer hover:bg-gray-100 rounded-r-full">
          <div class="flex-grow">
            <p class="text-xs font-bold text-gray-800">여행자</p>
            <p class="text-sm text-gray-500">게스트 추가</p>
          </div>
          <button class="ml-4 bg-red-500 text-white w-12 h-12 flex items-center justify-center rounded-full hover:bg-red-600">
            <i class="fas fa-search"></i>
          </button>
        </div>

      </div>
    </div>
  </header>
</template>

<script setup>
// 스크립트 로직 없음
</script>