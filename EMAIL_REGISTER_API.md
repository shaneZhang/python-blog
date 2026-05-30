# 邮箱注册功能 API 文档

## 功能概述

该模块实现了通过邮箱注册新用户的功能。为了方便测试，邮箱验证码暂时统一使用固定值 `123456`。

---

## API 接口列表

### 1. 发送邮箱验证码（注册用）

**接口地址：** `/code/send_emailcode/<email>/`

**请求方式：** GET

**URL 参数：**
- `email`: 邮箱地址

**响应示例：**
```json
{
    "code": "200",
    "errormsg": "ok",
    "data": {
        "email": "test@example.com",
        "code": "123456"
    }
}
```

**说明：**
- 验证码有效期为 10 分钟
- 验证码保存到 Redis 中，key 格式为 `email_{email}`
- 同时会记录到 `t_email_verify_code` 表中

---

### 2. 校验邮箱验证码

**接口地址：** `/code/check_emailcode/<email>/`

**请求方式：** GET

**URL 参数：**
- `email`: 邮箱地址

**查询参数：**
- `emailcode`: 邮箱验证码

**响应示例（成功）：**
```json
{
    "code": "200",
    "errormsg": "ok"
}
```

**响应示例（验证码过期）：**
```json
{
    "code": "4002",
    "errormsg": "验证码已过期"
}
```

**响应示例（验证码错误）：**
```json
{
    "code": "4003",
    "errormsg": "验证码错误"
}
```

---

### 3. 邮箱注册

**接口地址：** `/user/register_by_email/`

**请求方式：** POST

**请求体（JSON）：**
```json
{
    "username": "testuser",
    "password": "testpass123",
    "email": "test@example.com",
    "email_code": "123456"
}
```

**响应示例（成功）：**
```json
{
    "code": 200,
    "errormsg": "注册成功",
    "data": {
        "user_id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }
}
```

**响应示例（用户名已存在）：**
```json
{
    "code": 4002,
    "errormsg": "用户名已存在"
}
```

**响应示例（邮箱已被注册）：**
```json
{
    "code": 4003,
    "errormsg": "邮箱已被注册"
}
```

**响应示例（验证码过期）：**
```json
{
    "code": 4004,
    "errormsg": "验证码已过期"
}
```

**响应示例（验证码错误）：**
```json
{
    "code": 4005,
    "errormsg": "验证码错误"
}
```

---

### 4. 发送邮箱验证码（找回密码用）

**接口地址：** `/code/send_emailcode_reset/<email>/`

**请求方式：** GET

**URL 参数：**
- `email`: 邮箱地址

**响应示例：**
```json
{
    "code": "200",
    "errormsg": "ok",
    "data": {
        "email": "test@example.com",
        "code": "123456"
    }
}
```

**说明：**
- 用于找回密码场景
- 验证码有效期为 10 分钟
- 验证码保存到 Redis 中，key 格式为 `email_reset_{email}`

---

### 5. 通过邮箱重置密码

**接口地址：** `/user/reset_password_by_email/`

**请求方式：** POST

**请求体（JSON）：**
```json
{
    "email": "test@example.com",
    "email_code": "123456",
    "new_password": "newpass123"
}
```

**响应示例（成功）：**
```json
{
    "code": 200,
    "errormsg": "密码重置成功"
}
```

**响应示例（邮箱未注册）：**
```json
{
    "code": 4002,
    "errormsg": "该邮箱未注册"
}
```

---

## 状态码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 操作成功 |
| 4000 | 请求参数格式错误（非JSON格式） |
| 4001 | 缺少必传参数 |
| 4002 | 用户名已存在 / 邮箱未注册 |
| 4003 | 邮箱已被注册 |
| 4004 | 验证码已过期 |
| 4005 | 验证码错误 |
| 5000 | 服务器内部错误 |
| 5001 | 用户创建失败 |

---

## 数据库表结构

### t_email_verify_code（邮箱验证码表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | BigAutoField | 主键 |
| create_time | DateTimeField | 创建时间 |
| update_time | DateTimeField | 更新时间 |
| email | EmailField | 邮箱地址 |
| code | CharField(6) | 验证码 |
| type | CharField(1) | 验证码类型（1-注册，2-找回密码） |

---

## 测试示例

### 完整注册流程测试：

```bash
# 1. 发送邮箱验证码
curl -X GET "http://localhost:8000/code/send_emailcode/test@example.com/"

# 2. 验证邮箱验证码
curl -X GET "http://localhost:8000/code/check_emailcode/test@example.com/?email_code=123456"

# 3. 注册新用户
curl -X POST "http://localhost:8000/user/register_by_email/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "email": "test@example.com",
    "email_code": "123456"
  }'
```

---

## 后续优化计划

1. **接入 SMTP 邮件服务**
   - 配置邮件服务器信息
   - 使用 Django 的 `send_mail` 发送真实邮件
   - 移除测试阶段返回验证码的功能

2. **增强安全性**
   - 添加验证码发送频率限制（如每分钟只能发送一次）
   - 添加 IP 限制
   - 使用随机生成的验证码替代固定验证码

3. **用户体验优化**
   - 添加邮箱格式校验
   - 添加密码强度校验
   - 支持验证码重发
