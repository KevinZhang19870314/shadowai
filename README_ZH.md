# MockAI

🚀 一个基于AI的智能Mock数据生成库

MockAI是一个强大的Python库，使用AI技术生成高质量的模拟数据。通过灵活的规则引擎，您可以轻松生成结构化的JSON数据。

## 🎯 设计理念

MockAI 提供灵活且易用的API设计，支持从简单到复杂的各种使用场景，让用户能够快速上手同时保持强大的定制能力。

## 🆚 与传统Mock库的比较

### 核心差异

| 特性 | MockAI | 传统Mock库 (如 faker.js) |
|------|--------|------------------------|
| **生成方式** | AI智能生成 | 预定义算法 |
| **配置复杂度** | 极简（描述即可） | 中等（需要组合API） |
| **数据质量** | 高（语义理解） | 中（模板化） |
| **业务相关性** | 强（上下文感知） | 弱（通用模式） |
| **生成速度** | 慢（AI调用） | 极快（本地计算） |
| **扩展能力** | 高（AI适应） | 中（需要开发） |

### MockAI的独特优势

#### 🧠 智能化理解
```python
# MockAI - 一行代码，智能理解业务含义
shadow_ai.generate("company_email")  # 自动生成符合公司格式的邮箱

# 传统库 - 需要手动组合多个API
faker.internet.email(
    faker.person.firstName(),
    faker.person.lastName(), 
    faker.internet.domainName()
)
```

#### 🎯 业务场景驱动
```python
# MockAI - 业务规则包，确保数据逻辑一致性
developer_profile = RulePackage(
    name="senior_developer",
    rules=["name", "email", "programming_language", "years_experience", "github_username"]
)
# 生成的数据自动保持逻辑关联：高经验值对应高级编程语言
```

#### 🔧 极简配置
```python
# MockAI - 描述性配置
Rule(
    name="medical_record_id", 
    description="Generate HIPAA-compliant patient ID",
    constraints={"format": "anonymized"}
)

# 传统库 - 需要自定义开发
def generate_medical_id():
    # 大量自定义逻辑...
```

### 适用场景选择

#### ✅ 推荐使用MockAI的场景
- **复杂业务测试**: 需要数据间逻辑关联
- **原型演示**: 需要真实感强的示例数据  
- **行业特定数据**: 医疗、金融等专业领域
- **API文档示例**: 自动生成符合业务的响应示例
- **快速迭代**: 频繁调整数据生成规则

#### ✅ 推荐使用传统库的场景
- **高性能需求**: 大量数据批量生成
- **CI/CD流水线**: 自动化测试环境
- **简单标准数据**: 基础的姓名、邮箱、电话
- **离线环境**: 无网络连接限制
- **成本敏感**: 避免AI API调用费用

### 💡 最佳实践建议

**混合使用策略** - 充分发挥两者优势：
```python
# 1. 使用ShadowAI设计数据模板
business_template = shadow_ai.generate(complex_business_package)

# 2. 使用传统库进行大量数据填充  
for i in range(1000):
    test_data = apply_template_with_faker(business_template)
```

**选择指南**：
- 🎯 追求**数据质量**和**业务相关性** → 选择 **MockAI**
- ⚡ 追求**生成速度**和**简单性** → 选择 **传统Mock库**
- 🔄 两者结合使用 → 获得**最佳开发体验**

## ✨ 特性

- 🤖 **AI驱动**: 基于Agno框架，支持多种LLM模型
- 📝 **灵活规则**: 支持规则记录、规则组合和规则包
- 📄 **多格式支持**: 支持JSON和YAML格式的规则定义
- 🎯 **精确输出**: 生成结构化的JSON数据
- 📦 **开箱即用**: 内置常用规则包
- ⚡ **极简配置**: 描述性配置，快速上手

## 📦 安装

```bash
pip install shadowai
```

## 🚀 快速开始

### 基本使用

```python
from shadow_ai import ShadowAI

# 创建ShadowAI实例
shadow_ai = ShadowAI()

# 直接使用字符串
result = shadow_ai.generate("email")
print(result)  # {"email": "john.doe@example.com"}

# 生成多个字段
result = shadow_ai.generate(["email", "name", "age"])
print(result)  # {"email": "...", "name": "...", "age": ...}

# 快速方法
result = shadow_ai.quick("email", "name", "phone")
print(result)  # {"email": "...", "name": "...", "phone": "..."}
```

### 创建自定义规则

```python
from shadow_ai import Rule, RuleCombination, RulePackage

# 创建单个规则
email_rule = Rule(name="email")
company_rule = Rule(name="company_name")

# 生成数据
result = shadow_ai.generate(email_rule)
print(result)  # {"email": "user@example.com"}

# 创建规则组合
user_combo = RuleCombination(
    name="user_profile",
    rules=["name", "email", "phone"]
)

# 创建规则包
user_package = RulePackage(
    name="user", 
    rules=["username", "email", "age", "location"]
)

result = shadow_ai.generate(user_package)
print(result)  # 完整的用户信息
```

### 使用预构建规则

```python
from shadow_ai.rules import email_rule, name_rule
from shadow_ai.rules.packages import person_package

# 使用预定义规则
result = shadow_ai.generate(email_rule)
print(result)  # {"email": "john.doe@example.com"}

# 使用预定义包
result = shadow_ai.generate(person_package)
print(result)
# {
#   "fullname": "John Smith", 
#   "age": 25,
#   "email": "john.smith@email.com"
# }
```

### 高级自定义规则

```python
from shadow_ai import Rule

# 详细配置规则
custom_rule = Rule(
    name="company",
    description="Generate a technology company name",
    examples=["TechCorp", "DataFlow", "CloudByte"],
    constraints={"type": "string", "style": "modern"}
)

result = shadow_ai.generate(custom_rule)
```

## 📖 文档

详细文档请查看 [docs/](docs/) 目录。

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📄 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件。 