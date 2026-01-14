import http from '@/http/httpClient';

//更新用户头像
export const uploadAvatar = async (file: File) => {
  const formData = new FormData()
  formData.append('avatarfile', file)

  return await http.post('/profile/avatar', {
    data: formData
  })
}


// 修改用户信息
export const updateUserProfile = async (userInfo: {
  nickName?: string
  sex?: string
  birthday?: number
  phonenumber?: string
  signature?: string
  remark?: string
  theme?: string
  email?: string
}) => {
  const allowedFields = ['nickName', 'sex', 'birthday', 'phonenumber', 'signature', 'remark','theme', 'email'];
  const filteredUserInfo = Object.keys(userInfo)
    .filter(key => allowedFields.includes(key))
    .reduce((obj, key) => {
      obj[key] = userInfo[key];
      return obj;
    }, {} as Record<string, any>);

  return await http.put('/profile', {
    data: filteredUserInfo,
    header: {
      'Content-Type': 'application/json',
    },
  });
}

//更新用户密码
export const updateUserPassword = async (oldPassword: string, newPassword: string) => {
  return await http.put('/profile/updatePwd', {
    data: {
      oldPassword,
      newPassword,
    },
    header: {
      'Content-Type': 'application/json',
    },
  });
};


//获取用户信息
export const getUserProfile = async () => {
  return await http.get('/profile', {
    header: {
      'Content-Type': 'application/json',
    },
  });
};
