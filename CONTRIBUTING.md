# 贡献指南

感谢您对 Cozlive 项目的关注！我们欢迎所有形式的贡献，包括但不限于：

- 提交 Bug 报告
- 提出新功能建议
- 改进文档
- 提交代码修复
- 分享使用经验

---

## 开发环境设置

### 前置要求

- Node.js >= 18.0.0
- Python >= 3.11
- pnpm >= 8.0.0
- Docker >= 20.0
- Git

### 克隆项目

```bash
git clone https://github.com/chenliulian/cozlive.git
cd cozlive
```

### 安装依赖

```bash
# 安装前端依赖
pnpm install

# 安装 Python 依赖
cd services/ai-agent-engine
pip install -r requirements.txt
cd ../..

# 安装测试依赖
cd tests
pip install -r requirements.txt
cd ..
```

### 启动开发环境

```bash
# 启动基础设施服务
docker-compose -f infrastructure/docker/docker-compose.dev.yml up -d

# 启动所有服务
./scripts/start-dev.sh
```

---

## 代码规范

### 提交信息规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型 (type)**:

- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

**示例**:

```
feat(agent): 添加 Agent 情感计算功能

- 实现情感状态检测
- 添加情感响应生成
- 更新相关测试

Closes #123
```

### 代码风格

#### TypeScript/JavaScript

- 使用 ESLint 和 Prettier
- 遵循 [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- 使用 TypeScript 严格模式

```bash
# 检查代码风格
pnpm lint

# 自动修复
pnpm lint:fix

# 格式化代码
pnpm format
```

#### Python

- 遵循 [PEP 8](https://pep8.org/) 规范
- 使用 Black 格式化
- 使用 isort 排序导入

```bash
# 格式化 Python 代码
cd services/ai-agent-engine
black src/
isort src/

# 类型检查
mypy src/
```

---

## 开发流程

### 1. 创建分支

```bash
# 从 main 分支创建新分支
git checkout -b feature/your-feature-name

# 分支命名规范
# feature/*   - 新功能
# fix/*       - Bug 修复
# docs/*      - 文档更新
# refactor/*  - 代码重构
```

### 2. 开发代码

- 编写清晰的代码注释
- 添加必要的单元测试
- 确保代码通过所有测试

### 3. 运行测试

```bash
# 运行所有测试
python3 -m pytest tests/ -v

# 运行特定测试
python3 -m pytest tests/unit/test_personality_engine.py -v

# 检查测试覆盖率
python3 -m pytest tests/ --cov=services --cov-report=html
```

### 4. 提交代码

```bash
# 添加更改
git add .

# 提交（遵循提交信息规范）
git commit -m "feat(agent): 添加新功能"

# 推送到远程
git push origin feature/your-feature-name
```

### 5. 创建 Pull Request

1. 访问 https://github.com/chenliulian/cozlive
2. 点击 "New Pull Request"
3. 选择你的分支
4. 填写 PR 描述
5. 等待代码审查

**PR 描述模板**:

```markdown
## 描述
简要描述这个 PR 做了什么

## 更改类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 性能优化

## 测试
- [ ] 添加了单元测试
- [ ] 添加了集成测试
- [ ] 所有测试通过

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 添加了必要的注释
- [ ] 更新了相关文档
- [ ] 本地测试通过

## 相关 Issue
Closes #123
```

---

## 代码审查

### 审查清单

**代码质量**:
- [ ] 代码是否清晰易懂
- [ ] 是否有适当的注释
- [ ] 是否遵循命名规范
- [ ] 是否有重复代码

**功能**:
- [ ] 功能是否完整实现
- [ ] 是否处理了边界情况
- [ ] 是否有适当的错误处理

**测试**:
- [ ] 是否添加了单元测试
- [ ] 测试是否覆盖主要逻辑
- [ ] 所有测试是否通过

**性能**:
- [ ] 是否有性能问题
- [ ] 是否有不必要的资源消耗

**安全**:
- [ ] 是否有安全风险
- [ ] 是否处理了敏感数据

---

## 项目结构

```
cozlive/
├── apps/                    # 应用程序
│   └── web/                 # Web 前端 (Next.js)
├── services/                # 后端服务
│   ├── ai-agent-engine/     # AI Agent 引擎 (Python)
│   └── user-service/        # 用户服务 (NestJS)
├── packages/                # 共享包
│   └── shared-types/        # 共享类型定义
├── tests/                   # 测试套件
│   ├── unit/                # 单元测试
│   ├── integration/         # 集成测试
│   └── e2e/                 # 端到端测试
├── docs/                    # 文档
├── infrastructure/          # 基础设施配置
│   ├── docker/              # Docker 配置
│   ├── kubernetes/          # K8s 配置
│   └── terraform/           # Terraform 配置
└── scripts/                 # 脚本工具
```

---

## 测试指南

### 编写单元测试

```python
# tests/unit/test_example.py
import pytest

class TestExample:
    """测试示例类"""
    
    def test_something(self):
        """测试某个功能"""
        # Arrange
        input_data = "test"
        
        # Act
        result = process_data(input_data)
        
        # Assert
        assert result == expected_output
    
    @pytest.mark.parametrize("input,expected", [
        ("a", 1),
        ("b", 2),
    ])
    def test_with_params(self, input, expected):
        """参数化测试"""
        assert process(input) == expected
```

### 编写集成测试

```python
# tests/integration/test_api.py
def test_create_agent(client):
    """测试创建 Agent API"""
    response = client.post("/api/v1/agents", json={
        "name": "测试助手",
        "role_identity": "助手"
    })
    
    assert response.status_code == 201
    assert response.json()["success"] is True
```

### 测试覆盖率要求

- 单元测试覆盖率 >= 80%
- 核心模块覆盖率 >= 90%
- 所有 Bug 修复必须包含回归测试

---

## 文档贡献

### 文档位置

- `README.md` - 项目主文档
- `docs/API.md` - API 文档
- `docs/ARCHITECTURE.md` - 架构文档
- `docs/DEPLOYMENT.md` - 部署指南

### 文档规范

- 使用 Markdown 格式
- 添加必要的代码示例
- 保持中英文术语一致
- 更新目录结构

---

## 报告 Bug

### Bug 报告模板

```markdown
## Bug 描述
清晰简洁地描述 Bug

## 复现步骤
1. 进入 '...'
2. 点击 '...'
3. 滚动到 '...'
4. 出现错误

## 预期行为
描述你期望发生什么

## 实际行为
描述实际发生了什么

## 截图
如果适用，添加截图

## 环境信息
- OS: [例如 macOS, Windows]
- Browser: [例如 Chrome, Safari]
- Version: [例如 22]

## 附加信息
其他相关信息
```

---

## 提出功能建议

### 功能建议模板

```markdown
## 功能描述
清晰简洁地描述这个功能

## 使用场景
描述这个功能的使用场景

## 预期行为
描述这个功能应该如何工作

## 替代方案
描述你考虑过的替代方案

## 附加信息
其他相关信息或截图
```

---

## 发布流程

### 版本号规范

使用 [Semantic Versioning](https://semver.org/lang/zh-CN/):

- `MAJOR.MINOR.PATCH`
- MAJOR: 不兼容的 API 修改
- MINOR: 向下兼容的功能新增
- PATCH: 向下兼容的问题修复

### 发布步骤

1. 更新版本号
2. 更新 CHANGELOG.md
3. 创建 Release PR
4. 合并到 main 分支
5. 创建 Git Tag
6. 发布 Release

```bash
# 创建标签
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

---

## 社区

### 交流渠道

- **GitHub Issues**: Bug 报告和功能建议
- **GitHub Discussions**: 技术讨论
- **Discord**: 实时交流 [邀请链接]
- **邮件列表**: dev@cozlive.com

### 行为准则

- 尊重所有参与者
- 接受建设性批评
- 关注对社区最有利的事情
- 展现同理心

---

## 许可证

通过贡献代码，你同意将你的贡献在 [MIT 许可证](./LICENSE) 下发布。

---

## 感谢

感谢所有为 Cozlive 做出贡献的开发者！

[贡献者列表](https://github.com/chenliulian/cozlive/graphs/contributors)
