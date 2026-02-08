<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
            </div>
            <h1 class="ml-3 text-xl font-bold text-gray-900">快传</h1>
          </div>

          <!-- 存储空间 -->
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div class="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  class="h-full bg-primary-500 transition-all"
                  :style="{ width: `${storageInfo.usage_percentage}%` }"
                  :class="{ 'bg-red-500': storageInfo.usage_percentage > 80 }"
                />
              </div>
              <span class="text-sm text-gray-600">
                {{ formatSize(storageInfo.storage_used) }} / {{ formatSize(storageInfo.storage_limit) }}
              </span>
            </div>

            <!-- 用户菜单 -->
            <div class="relative">
              <button
                @click="showUserMenu = !showUserMenu"
                class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 transition"
              >
                <div class="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center text-white font-medium">
                  {{ userStore.user?.email?.[0]?.toUpperCase() }}
                </div>
              </button>

              <div v-if="showUserMenu" class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-1 z-10">
                <button
                  @click="logout"
                  class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  退出登录
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- 主内容 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 上传区域 -->
      <div
        @drop.prevent="handleDrop"
        @dragover.prevent
        @dragenter.prevent
        class="mb-8 border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-primary-500 transition-colors"
        :class="{ 'border-primary-500 bg-primary-50': isDragging }"
      >
        <input
          ref="fileInput"
          type="file"
          multiple
          @change="handleFileSelect"
          class="hidden"
        />
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        <p class="mt-2 text-sm text-gray-600">
          拖拽文件到此处，或
          <button @click="$refs.fileInput?.click()" class="text-primary-500 hover:text-primary-600 font-medium">
            点击选择文件
          </button>
        </p>
        <p class="mt-1 text-xs text-gray-500">支持所有文件类型，单文件最大 10GB</p>
      </div>

      <!-- 上传进度 -->
      <div v-if="fileStore.uploading" class="mb-6 bg-white rounded-lg shadow p-4">
        <h3 class="text-sm font-medium text-gray-900 mb-3">上传中</h3>
        <div class="space-y-2">
          <div v-for="(progress, filename) in fileStore.uploadProgress" :key="filename" class="flex items-center space-x-3">
            <div class="flex-1">
              <div class="flex items-center justify-between text-sm mb-1">
                <span class="text-gray-700 truncate">{{ filename }}</span>
                <span class="text-gray-500">{{ progress }}%</span>
              </div>
              <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                <div class="h-full bg-primary-500 transition-all" :style="{ width: `${progress}%` }" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 工具栏 -->
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center space-x-4">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索文件..."
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>

        <div v-if="fileStore.selectedFiles.length > 0" class="flex items-center space-x-2">
          <span class="text-sm text-gray-600">已选择 {{ fileStore.selectedFiles.length }} 个文件</span>
          <button
            @click="handleBatchDownload"
            class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition text-sm"
          >
            批量下载
          </button>
          <button
            @click="handleBatchDelete"
            class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition text-sm"
          >
            批量删除
          </button>
          <button
            @click="fileStore.clearSelection"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition text-sm"
          >
            取消选择
          </button>
        </div>
      </div>

      <!-- 文件列表 -->
      <div class="bg-white rounded-lg shadow">
        <div class="grid grid-cols-12 gap-4 px-6 py-3 bg-gray-50 border-b text-sm font-medium text-gray-700">
          <div class="col-span-1">
            <input
              type="checkbox"
              @change="toggleSelectAll"
              :checked="fileStore.selectedFiles.length === fileStore.files.length && fileStore.files.length > 0"
              class="w-4 h-4 text-primary-500 rounded"
            />
          </div>
          <div class="col-span-5">文件名</div>
          <div class="col-span-2">大小</div>
          <div class="col-span-2">上传时间</div>
          <div class="col-span-2">操作</div>
        </div>

        <div v-if="fileStore.loading" class="px-6 py-12 text-center text-gray-500">
          加载中...
        </div>

        <div v-else-if="fileStore.files.length === 0" class="px-6 py-12 text-center text-gray-500">
          暂无文件，上传文件开始使用吧
        </div>

        <div v-else class="divide-y divide-gray-200">
          <div
            v-for="file in filteredFiles"
            :key="file.id"
            class="grid grid-cols-12 gap-4 px-6 py-4 hover:bg-gray-50 transition items-center"
          >
            <div class="col-span-1">
              <input
                type="checkbox"
                :checked="fileStore.selectedFiles.some(f => f.id === file.id)"
                @change="fileStore.toggleFileSelection(file)"
                class="w-4 h-4 text-primary-500 rounded"
              />
            </div>
            <div class="col-span-5 flex items-center space-x-3">
              <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <span class="text-sm text-gray-900 truncate">{{ file.filename }}</span>
            </div>
            <div class="col-span-2 text-sm text-gray-600">{{ formatSize(file.file_size) }}</div>
            <div class="col-span-2 text-sm text-gray-600">{{ formatDate(file.upload_time) }}</div>
            <div class="col-span-2 flex items-center space-x-2">
              <button
                @click="handleDownload(file)"
                class="p-2 text-gray-400 hover:text-primary-500 transition"
                title="下载"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
              </button>
              <button
                @click="handleDelete(file)"
                class="p-2 text-gray-400 hover:text-red-500 transition"
                title="删除"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useFileStore } from '@/stores/files'
import { getStorageInfo } from '@/api/storage'
import { downloadFile, batchDownload } from '@/api/files'

const router = useRouter()
const userStore = useUserStore()
const fileStore = useFileStore()

const showUserMenu = ref(false)
const storageInfo = ref({
  storage_used: 0,
  storage_limit: 10737418240,
  storage_available: 10737418240,
  usage_percentage: 0
})
const searchQuery = ref('')
const isDragging = ref(false)
const fileInput = ref(null)

const filteredFiles = computed(() => {
  if (!searchQuery.value) {
    return fileStore.files
  }
  return fileStore.files.filter(file =>
    file.filename.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 格式化文件大小
const formatSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) {
    const hours = Math.floor(diff / (1000 * 60 * 60))
    if (hours === 0) {
      const minutes = Math.floor(diff / (1000 * 60))
      return minutes <= 0 ? '刚刚' : `${minutes}分钟前`
    }
    return `${hours}小时前`
  } else if (days === 1) {
    return '昨天'
  } else if (days < 7) {
    return `${days}天前`
  } else {
    return date.toLocaleDateString('zh-CN')
  }
}

// 加载存储信息
const loadStorageInfo = async () => {
  try {
    storageInfo.value = await getStorageInfo()
  } catch (error) {
    console.error('获取存储信息失败', error)
  }
}

// 拖拽处理
const handleDrop = async (e) => {
  isDragging.value = false
  const files = Array.from(e.dataTransfer.files)
  if (files.length > 0) {
    await fileStore.uploadFiles(files)
    await loadStorageInfo()
  }
}

// 文件选择
const handleFileSelect = async (e) => {
  const files = Array.from(e.target.files)
  if (files.length > 0) {
    await fileStore.uploadFiles(files)
    await loadStorageInfo()
  }
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// 全选
const toggleSelectAll = () => {
  if (fileStore.selectedFiles.length === fileStore.files.length) {
    fileStore.clearSelection()
  } else {
    fileStore.selectedFiles = [...fileStore.files]
  }
}

// 下载文件
const handleDownload = async (file) => {
  try {
    const blob = await downloadFile(file.id)
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = file.filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('下载失败', error)
  }
}

// 批量下载
const handleBatchDownload = async () => {
  if (fileStore.selectedFiles.length === 0) return
  try {
    const fileIds = fileStore.selectedFiles.map(f => f.id)
    const blob = await batchDownload(fileIds)
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'files.zip'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
    fileStore.clearSelection()
  } catch (error) {
    console.error('批量下载失败', error)
  }
}

// 删除文件
const handleDelete = async (file) => {
  if (!confirm(`确定要删除 "${file.filename}" 吗？`)) return
  try {
    await fileStore.removeFile(file.id)
    await loadStorageInfo()
  } catch (error) {
    console.error('删除失败', error)
  }
}

// 批量删除
const handleBatchDelete = async () => {
  if (!confirm(`确定要删除选中的 ${fileStore.selectedFiles.length} 个文件吗？`)) return
  try {
    for (const file of fileStore.selectedFiles) {
      await fileStore.removeFile(file.id)
    }
    fileStore.clearSelection()
    await loadStorageInfo()
  } catch (error) {
    console.error('批量删除失败', error)
  }
}

// 退出登录
const logout = () => {
  userStore.logout()
  router.push('/login')
}

onMounted(async () => {
  await fileStore.fetchFiles()
  await loadStorageInfo()
})
</script>
