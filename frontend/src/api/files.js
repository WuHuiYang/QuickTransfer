import api from './index'

// 上传文件
export const uploadFile = (file, folderId = null) => {
  const formData = new FormData()
  formData.append('file', file)
  if (folderId) {
    formData.append('folder_id', folderId)
  }

  return api.post('/files/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    onUploadProgress: (progressEvent) => {
      const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
      return percentCompleted
    }
  })
}

// 获取文件列表
export const getFiles = (params) => {
  return api.get('/files', { params })
}

// 获取文件信息
export const getFile = (fileId) => {
  return api.get(`/files/${fileId}`)
}

// 下载文件
export const downloadFile = (fileId) => {
  return api.get(`/files/${fileId}/download`, {
    responseType: 'blob'
  })
}

// 批量下载
export const batchDownload = (fileIds) => {
  return api.post('/files/batch-download', fileIds, {
    responseType: 'blob'
  })
}

// 删除文件
export const deleteFile = (fileId) => {
  return api.delete(`/files/${fileId}`)
}
