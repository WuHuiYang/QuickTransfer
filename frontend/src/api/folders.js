import api from './index'

// 创建文件夹
export const createFolder = (data) => {
  return api.post('/folders', data)
}

// 获取文件夹列表
export const getFolders = (params) => {
  return api.get('/folders', { params })
}

// 获取文件夹信息
export const getFolder = (folderId) => {
  return api.get(`/folders/${folderId}`)
}

// 删除文件夹
export const deleteFolder = (folderId) => {
  return api.delete(`/folders/${folderId}`)
}
