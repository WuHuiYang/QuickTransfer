import api from './index'

// 发送验证码
export const sendVerificationCode = (email) => {
  return api.post('/auth/send-code', null, { params: { email } })
}

// 验证码登录
export const verifyCode = (email, code) => {
  return api.post('/auth/verify-code', { email, code })
}

// 获取当前用户信息
export const getCurrentUser = () => {
  return api.get('/auth/me')
}
