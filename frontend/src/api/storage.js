import api from './index'

// 获取存储信息
export const getStorageInfo = () => {
  return api.get('/storage')
}
