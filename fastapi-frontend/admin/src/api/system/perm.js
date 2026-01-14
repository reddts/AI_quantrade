import request from '@/utils/request'

// 查询权限列表
export function listPerm(query) {
  return request({
    url: '/system/perm/list',
    method: 'get',
    params: query
  })
}

// 查询权限详细
export function getPerm(permId) {
  return request({
    url: '/system/perm/' + permId,
    method: 'get'
  })
}

// 查询权限下拉树结构
export function treeselect() {
  return request({
    url: '/system/perm/treeselect',
    method: 'get'
  })
}

// 根据角色ID查询权限下拉树结构
export function rolePermTreeselect(roleId) {
  return request({
    url: '/system/perm/rolePermTreeselect/' + roleId,
    method: 'get'
  })
}

// 新增权限
export function addPerm(data) {
  return request({
    url: '/system/perm',
    method: 'post',
    data: data
  })
}

// 修改权限
export function updatePerm(data) {
  return request({
    url: '/system/perm',
    method: 'put',
    data: data
  })
}

// 删除权限
export function delPerm(permId) {
  return request({
    url: '/system/perm/' + permId,
    method: 'delete'
  })
}