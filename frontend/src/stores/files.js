import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getFiles, uploadFile, deleteFile } from '@/api/files'

export const useFileStore = defineStore('file', () => {
  const files = ref([])
  const currentFolder = ref(null)
  const loading = ref(false)
  const selectedFiles = ref([])
  const uploadProgress = ref({})
  const uploading = ref(false)

  const fetchFiles = async (params = {}) => {
    loading.value = true
    try {
      const data = await getFiles({
        folder_id: currentFolder.value?.id,
        ...params
      })
      files.value = data.files
    } catch (error) {
      console.error('获取文件列表失败', error)
    } finally {
      loading.value = false
    }
  }

  const uploadFiles = async (fileList) => {
    uploading.value = true
    const promises = []

    for (const file of fileList) {
      const promise = uploadFile(file, currentFolder.value?.id)
        .then((data) => {
          delete uploadProgress.value[file.name]
          return data
        })
        .catch((error) => {
          delete uploadProgress.value[file.name]
          throw error
        })

      uploadProgress.value[file.name] = 0
      promises.push(promise)
    }

    try {
      const results = await Promise.all(promises)
      await fetchFiles()
      return results
    } catch (error) {
      console.error('文件上传失败', error)
      throw error
    } finally {
      uploading.value = false
    }
  }

  const removeFile = async (fileId) => {
    try {
      await deleteFile(fileId)
      await fetchFiles()
    } catch (error) {
      console.error('删除文件失败', error)
      throw error
    }
  }

  const toggleFileSelection = (file) => {
    const index = selectedFiles.value.findIndex(f => f.id === file.id)
    if (index > -1) {
      selectedFiles.value.splice(index, 1)
    } else {
      selectedFiles.value.push(file)
    }
  }

  const clearSelection = () => {
    selectedFiles.value = []
  }

  const setCurrentFolder = (folder) => {
    currentFolder.value = folder
    selectedFiles.value = []
  }

  return {
    files,
    currentFolder,
    loading,
    selectedFiles,
    uploadProgress,
    uploading,
    fetchFiles,
    uploadFiles,
    removeFile,
    toggleFileSelection,
    clearSelection,
    setCurrentFolder
  }
})
