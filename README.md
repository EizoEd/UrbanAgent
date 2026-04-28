# UrbanAgent

> 中文版优先展示。English README follows after the Chinese section.

UrbanAgent 是一个面向城市遥感、城市空间分析和规划问答任务的 Agent 编排框架公开脱敏版本。这个仓库保留了系统的核心结构、模块边界、任务流转方式和可运行的最小源码快照；同时移除了原始资料、运行产物、私有配置、服务连接信息和任何不适合公开发布的内容。

---

## 中文 README

### 1. 项目定位

UrbanAgent 的目标不是把大模型直接包装成一个问答入口，而是把城市分析任务拆解成一条可检查、可治理、可扩展的工程流程。系统围绕“用户问题 -> 任务理解 -> 计划生成 -> 证据检索 -> 工具执行 -> 结果合成 -> 风险校验 -> 人工复核或写回”的链路组织，使城市空间分析类任务可以在明确的边界内运行。

公开版本主要用于说明以下内容：

- 如何把城市遥感、GIS 分析、规划政策问答和多文档分析组织到统一的 Agent 工作流中。
- 如何将 RAG 检索、空间工具、外部工具和人工复核统一到同一套状态图里。
- 如何通过结构化协议减少自由文本中不可控、不稳定和难以追踪的部分。
- 如何在公开仓库中保留系统设计和核心源码，同时完成脱敏处理。

该仓库不是完整生产系统，也不包含私有数据、历史实验结果或部署配置。公开代码的重点是展示系统结构、工程拆分和关键设计思路。

### 2. 设计目标

UrbanAgent 的设计围绕几个核心目标展开。

**任务流可解释**  
每个请求都会被拆成可观察的阶段：路由、规划、检索、工具调用、合成、校验和复核。这样可以清楚知道系统为什么选择某条路径、用了哪些证据、哪些步骤需要人工介入。

**证据优先，而不是直接生成**  
系统默认将城市分析答案建立在检索证据、空间对象、图层信息或工具结果之上。模型的作用更偏向理解、计划、归纳和表达，而不是凭空生成结论。

**工具边界清晰**  
检索、空间分析、外部工具执行和结果合成都通过明确的输入输出协议连接。工具结果不会直接污染主上下文，而是先被标准化，再进入合成和校验阶段。

**高风险输出需要治理**  
当回答涉及规划判断、空间结论、置信度不足、证据缺失或可能影响后续记忆写入时，系统可以进入人工复核流程，而不是直接把结果返回或写入长期状态。

**公开快照可运行、可检查**  
当前公开源码去掉了私有依赖，但保留了一个轻量、可测试的核心流程。它可以用于理解架构，也可以作为后续开源整理的基础。

### 3. 总体架构

系统按层次拆分为接口层、编排层、决策层、工具层、治理层和评估层。公开快照重点保留后五类能力的抽象和最小实现。

```text
用户请求 / 上层服务 / 工作台
        |
        v
UrbanAgentCore
        |
        v
请求规范化 -> 意图路由 -> 任务规划 -> 证据检索
        |                       |
        |                       v
        |              空间工具 / 外部工具 / 技能扩展
        |                       |
        v                       v
结果合成 -> 风险校验 -> 人工复核判断 -> 记忆写回策略
        |
        v
结构化响应
```

核心思想是把 Agent 拆成一组明确节点，而不是把所有逻辑堆在一个提示词或一个函数里。每个节点只承担一类职责：

- 路由节点判断任务类型和执行策略。
- 规划节点将复杂请求拆成目标、子目标和步骤。
- 检索节点提供证据和引用对象。
- 空间工具节点处理区域、距离、图层和时间比较。
- 合成节点将证据和工具结果组织成可读答案。
- 校验节点判断答案是否可回答、是否需要澄清、是否应进入复核。
- 治理节点决定是否允许写回、是否需要人工确认。

### 4. 公开源码结构

公开源码按功能域组织，而不是按演示脚本简单平铺。目录结构如下：

```text
urban_agent/
  core.py
  schemas/
    request.py
    planning.py
    evidence.py
    workflow.py
  agent/
    router.py
    planner.py
    synthesizer.py
    verifier.py
  tools/
    retrieval.py
    spatial/
      models.py
      actions.py
  governance/
    review.py
    memory_policy.py
  evaluation/
    scenarios.py
docs/
  architecture.md
  workflow.md
  public_release_scope.md
examples/
  basic_workflow.py
  spatial_workflow.py
tests/
  test_public_snapshot.py
```

各部分职责如下：

- `urban_agent/core.py`：公开快照的主编排入口，负责连接路由、规划、检索、空间动作、合成、校验和治理策略。
- `urban_agent/schemas/`：定义请求、计划、证据、工作流状态等结构化协议，保证模块之间通过稳定数据结构通信。
- `urban_agent/agent/`：保存 Agent 决策逻辑，包括任务路由、分层规划、答案合成和风险校验。
- `urban_agent/tools/`：提供工具层适配器，公开版本包含内存检索和空间动作的安全实现。
- `urban_agent/tools/spatial/`：定义空间对象、空间查询和图层比较等公共安全模型。
- `urban_agent/governance/`：处理人工复核、风险状态和记忆写回策略。
- `urban_agent/evaluation/`：提供轻量场景定义，用于公开快照的烟雾测试和后续评估扩展。
- `docs/`：解释架构、工作流和公开发布范围。
- `examples/`：使用合成数据演示基础问答流和空间分析流。
- `tests/`：验证公开快照可以被导入、执行并保持关键语义稳定。

### 5. 核心工作流

UrbanAgent 的一次典型执行可以分为八个阶段。

**阶段一：请求规范化**  
系统先将用户输入整理成结构化请求，包含任务文本、可选上下文、约束条件和运行偏好。这样后续节点不需要反复解析自由文本。

**阶段二：意图路由**  
路由器判断请求更接近普通问答、证据问答、空间分析、对比分析、澄清请求还是高风险任务。路由结果会影响后续是否需要检索、是否调用空间工具、是否进入复核。

**阶段三：任务规划**  
规划器把请求拆成可执行步骤。简单问题可以走短路径；复杂问题会生成分层计划，例如先明确区域，再查找证据，再比较图层，最后组织结论。

**阶段四：证据检索**  
检索层根据任务计划查找相关证据。公开版本使用轻量内存检索，目的是展示接口和数据结构；实际系统可以替换为向量检索、文档索引、知识库或混合检索。

**阶段五：空间或外部工具执行**  
当任务涉及区域筛选、距离搜索、图层比较或时序变化时，系统进入工具层。工具调用被隔离在明确接口后面，返回结果会被压缩为结构化摘要。

**阶段六：结果合成**  
合成器把用户问题、计划、证据和工具结果整理成回答。回答不只是自然语言，还会保留引用、关键发现、后续动作、对象引用和风险标记。

**阶段七：风险校验**  
校验器检查答案是否缺少证据、是否需要更多输入、是否包含空间判断风险、是否应该进入人工复核。不能可靠回答的问题会返回明确状态，而不是强行输出。

**阶段八：复核与写回策略**  
对于高风险或需要确认的结果，系统可以生成待复核状态。只有满足策略的内容才允许写回长期状态；公开快照保留了这类策略的核心表达方式。

### 6. 关键模块设计

#### 6.1 `UrbanAgentCore`

`UrbanAgentCore` 是公开快照的主入口。它不是一个“大函数”，而是一个轻量编排器，负责把各个节点按顺序连接起来。它的职责包括：

- 接收结构化请求。
- 调用路由器确定任务类型。
- 调用规划器生成执行计划。
- 将计划交给检索和工具层。
- 调用合成器生成结构化结果。
- 调用校验器判断最终状态。
- 调用治理策略决定复核和写回行为。

这种组织方式让核心流程容易替换：实际项目中可以把内存检索换成真实检索服务，把公开空间工具换成 GIS 后端，把规则式规划器换成模型规划器，而不破坏外层协议。

#### 6.2 Schema 层

Schema 层是系统稳定性的基础。它把内部状态拆成几个可测试的数据结构：

- 请求结构：描述用户任务、上下文和运行偏好。
- 计划结构：描述目标、子目标、步骤和所需工具。
- 证据结构：描述检索片段、来源标签、相关性和引用信息。
- 工作流结构：描述执行过程中的阶段、状态和输出。

通过 Schema 层，系统可以避免不同模块直接共享不稳定的字典字段，也方便做测试、审计和后续服务化。

#### 6.3 Router 与 Planner

Router 负责判断“这是什么任务”，Planner 负责判断“这件事如何完成”。两者分离有几个好处：

- 路由可以保持快速、确定和低成本。
- 规划可以根据任务类型生成更细的步骤。
- 失败时可以定位是任务识别错误，还是计划生成不充分。
- 后续可以分别替换路由策略和规划策略。

公开版本使用确定性规则展示结构，实际系统可以接入模型分类、示例驱动路由或更复杂的计划生成策略。

#### 6.4 Retrieval Adapter

检索层被设计成适配器，而不是写死在 Agent 内部。这样做的原因是城市分析任务的证据来源可能很多，包括规划文本、遥感解译结果、指标表、空间对象说明和用户上传材料。

公开版本中的检索实现只使用合成样例数据，但接口表达了真实系统需要的几个关键字段：

- 证据文本或摘要。
- 来源标签。
- 相关性信息。
- 可引用对象。
- 与任务步骤的关联关系。

#### 6.5 Spatial Tool Layer

空间工具层负责把自然语言任务转成可执行的空间动作。公开快照保留了几类典型能力：

- 按区域过滤对象。
- 按距离查找对象。
- 比较不同时间或不同图层的空间信息。
- 生成适合前端地图展示的轻量结果。

真实系统中，这一层可以连接 GIS 引擎、空间数据库、遥感图层服务或自定义分析脚本。公开版本只保留接口和最小行为，避免暴露任何具体数据或内部服务。

#### 6.6 Synthesizer 与 Verifier

Synthesizer 负责把证据和工具结果变成用户可读的回答；Verifier 负责判断这个回答是否应该被交付。

两者分离非常重要。合成器擅长组织语言和结构，校验器则关注风险：

- 是否有足够证据。
- 是否需要用户补充条件。
- 是否存在空间判断风险。
- 是否需要人工复核。
- 是否允许写回长期状态。

这样可以避免系统把“写得像答案”的内容误认为“可以交付的答案”。

#### 6.7 Governance Layer

治理层处理 Agent 系统中容易被忽略但很重要的部分：

- 哪些结果需要人工复核。
- 哪些结果可以直接返回。
- 哪些内容可以进入长期状态。
- 哪些任务应该被标记为需要澄清或无法完成。
- 如何保存可审计的决策摘要。

公开快照保留了治理层的核心接口和策略表达，但不包含任何私有运行记录。

### 7. 响应语义

UrbanAgent 不把所有请求都压成一个普通回答。系统会返回更明确的状态，便于上层服务和人工复核界面处理。

- `answer`：可以基于现有证据和工具结果回答。
- `needs_clarification`：缺少关键输入，需要用户补充条件。
- `cannot_solve`：公开快照或当前工具无法可靠完成。
- `requires_review`：结果可生成，但需要人工复核后再交付或写回。
- `writeback_allowed`：满足策略，可以进入后续长期状态。
- `writeback_blocked`：存在风险或证据不足，不允许写回。

这种状态设计比单纯返回自然语言更适合城市分析任务，因为许多结论都需要证据、边界条件和风险说明。

### 8. 数据与工具边界

公开版本没有发布原始数据，也没有发布内部服务连接方式。数据和工具边界按照以下原则处理：

- 输入样例使用合成内容，不指向真实项目材料。
- 检索结果使用公共安全的短文本和来源标签。
- 空间对象使用抽象区域、图层和几何描述，不包含真实敏感对象。
- 工具接口保留结构，具体后端由使用者自行替换。
- 评估场景只保留任务类型和期望行为，不包含原始样本。

这个边界可以让仓库表达系统设计，同时避免公开不应发布的资料。

### 9. 脱敏处理范围

公开发布前已按以下范围进行脱敏和缩减：

- 移除个人路径、本地运行环境信息和机器相关配置。
- 移除私有仓库名称、分支信息和内部提交标识。
- 移除原始文档、抽取文本、历史样本和生成数据集。
- 移除运行产物、缓存、审计文件、长期记忆文件和中间结果。
- 移除模型凭据、服务凭据、外部服务地址和环境专用设置。
- 移除包含运营细节或不可公开上下文的内部说明。
- 保留公开安全的架构说明、核心接口、最小源码和测试。

如果后续继续开源更多模块，也应按同样标准逐个审查。

### 10. 如何运行公开快照

公开快照使用轻量依赖，主要用于结构验证和示例运行。

运行测试：

```bash
python -m pytest -q
```

运行基础工作流示例：

```bash
python examples/basic_workflow.py
```

运行空间工作流示例：

```bash
python examples/spatial_workflow.py
```

这些示例只使用合成数据，适合检查模块关系、状态流转和公开接口。

### 11. 适合的使用场景

UrbanAgent 的公开快照适合用于：

- 理解城市空间分析 Agent 的工程组织方式。
- 参考如何把 RAG、工具执行、空间分析和人工复核放入同一工作流。
- 构建自己的城市问答、遥感分析或规划辅助系统原型。
- 设计带有风险状态、澄清状态和复核状态的 Agent 响应协议。
- 作为进一步开源整理的基础代码骨架。

不适合直接用于：

- 生产环境部署。
- 真实城市数据处理。
- 高风险规划结论自动生成。
- 无人工复核的长期状态写入。

### 12. 后续扩展方向

公开快照可以沿以下方向扩展：

- 替换检索层：接入向量检索、关键词检索、知识库或混合检索。
- 扩展空间工具：连接空间数据库、GIS 引擎、遥感图层服务或专题分析脚本。
- 增强规划器：加入模型规划、示例驱动规划或多轮任务分解。
- 增强校验器：加入更细的证据覆盖率、空间一致性和不确定性判断。
- 接入复核界面：把 `requires_review` 状态连接到人工审核工作台。
- 完善评估体系：加入更多场景、指标和回归检查。
- 服务化封装：在保持 Schema 稳定的前提下接入上层 API 或前端工作台。

### 13. 当前状态

当前公开仓库包含一个已脱敏、可运行、结构化的源码快照。它表达了 UrbanAgent 的主要设计方式，但不是完整私有工程的简单复制。后续如果继续公开更多源码、示例或文档，需要对每个模块单独进行脱敏审查。

---

## English README

### 1. Overview

UrbanAgent is a sanitized public snapshot of an agent orchestration framework for urban remote sensing, spatial analysis, and planning-oriented question answering. The repository keeps the core architecture, module boundaries, workflow contracts, and a runnable minimal source snapshot while excluding raw materials, runtime artifacts, private configuration, service connection details, and any content that should not be published.

The project is designed around a structured workflow:

```text
user request -> routing -> planning -> evidence retrieval -> tool execution
  -> synthesis -> verification -> review or writeback decision
```

The public version is intended to explain how the system is organized and why it is designed this way. It is not a full production release and does not include private datasets, deployment configuration, or historical experiment material.

### 2. Design Goals

**Transparent task flow**  
Requests are processed through explicit stages: routing, planning, retrieval, tool execution, synthesis, verification, and review. This makes it easier to inspect why the system selected a path, which evidence was used, and where human review is required.

**Evidence-first behavior**  
Urban analysis answers should be grounded in retrieved evidence, spatial objects, layer information, or tool outputs. The model is treated as a planner, synthesizer, and explainer rather than the only source of truth.

**Clear tool boundaries**  
Retrieval, spatial analysis, external tools, and response synthesis communicate through structured contracts. Tool outputs are normalized before they enter the main synthesis and verification stages.

**Governance for high-risk outputs**  
When an answer involves planning judgment, spatial conclusions, missing evidence, or long-term state changes, the workflow can route it to human review instead of returning or writing it automatically.

**Runnable public snapshot**  
The public source removes private dependencies but keeps a small, testable workflow. It can be used to understand the architecture and as a foundation for later open-source cleanup.

### 3. Architecture

UrbanAgent is organized into interface, orchestration, decision, tool, governance, and evaluation layers. The public snapshot focuses on the core abstractions and minimal implementations behind these layers.

```text
Upper service / workbench / user request
        |
        v
UrbanAgentCore
        |
        v
normalize -> route -> plan -> retrieve
        |              |
        |              v
        |      spatial tools / external tools / skill extensions
        |              |
        v              v
synthesize -> verify -> review decision -> memory policy
        |
        v
structured response
```

The system is intentionally split into nodes instead of concentrating all logic in one prompt or one function. Each node has one clear responsibility:

- The router identifies task intent and execution style.
- The planner converts complex requests into goals, subgoals, and executable steps.
- The retriever supplies evidence and reference objects.
- The spatial tool layer handles region, distance, layer, and temporal operations.
- The synthesizer turns evidence and tool outputs into a readable response.
- The verifier checks whether the answer is grounded, incomplete, risky, or review-bound.
- The governance layer controls review and writeback decisions.

### 4. Repository Layout

```text
urban_agent/
  core.py
  schemas/
    request.py
    planning.py
    evidence.py
    workflow.py
  agent/
    router.py
    planner.py
    synthesizer.py
    verifier.py
  tools/
    retrieval.py
    spatial/
      models.py
      actions.py
  governance/
    review.py
    memory_policy.py
  evaluation/
    scenarios.py
docs/
  architecture.md
  workflow.md
  public_release_scope.md
examples/
  basic_workflow.py
  spatial_workflow.py
tests/
  test_public_snapshot.py
```

- `urban_agent/core.py`: main orchestration entry for the public snapshot.
- `urban_agent/schemas/`: request, planning, evidence, and workflow contracts.
- `urban_agent/agent/`: deterministic routing, planning, synthesis, and verification logic.
- `urban_agent/tools/`: retrieval and public-safe tool adapters.
- `urban_agent/tools/spatial/`: spatial models and minimal spatial actions.
- `urban_agent/governance/`: human review and memory policy decisions.
- `urban_agent/evaluation/`: lightweight public scenario definitions.
- `docs/`: architecture, workflow, and public release notes.
- `examples/`: synthetic examples for basic and spatial workflows.
- `tests/`: checks that the public snapshot remains importable and executable.

### 5. End-to-End Workflow

**Request normalization**  
User input is converted into a structured request with task text, optional context, constraints, and run preferences.

**Intent routing**  
The router classifies whether the task is a direct answer, evidence-grounded answer, spatial analysis, comparison task, clarification case, or high-risk task.

**Task planning**  
The planner produces executable steps. Simple tasks can take a short path; complex tasks can be decomposed into region selection, evidence lookup, layer comparison, and final synthesis.

**Evidence retrieval**  
The retrieval layer finds supporting evidence for the plan. The public version uses a small in-memory retriever to demonstrate the contract. Real deployments can replace it with document indexes, knowledge bases, or hybrid retrieval.

**Spatial and external tool execution**  
Spatial tasks can call actions such as region filtering, distance search, and layer comparison. Tool calls are isolated behind adapters and summarized before entering the main response context.

**Response synthesis**  
The synthesizer combines the request, plan, evidence, and tool outputs into a structured result with findings, citations, object references, follow-up actions, and risk state.

**Verification**  
The verifier checks for missing evidence, unclear inputs, spatial risk, and review requirements. The system can return a clarification or cannot-solve state instead of forcing a low-confidence answer.

**Review and writeback policy**  
High-risk results can be marked for review. Long-term state changes are controlled by policy and are blocked when the evidence or confidence is insufficient.

### 6. Important Design Choices

**Orchestration is separate from tools**  
The core workflow does not need to know how a retrieval engine or GIS backend is implemented. It only depends on stable tool contracts.

**Routing is separate from planning**  
Routing answers “what kind of task is this,” while planning answers “how should it be completed.” This keeps task classification fast and makes plan generation easier to replace.

**Synthesis is separate from verification**  
A fluent answer is not automatically a reliable answer. The verifier is responsible for deciding whether the synthesized result can be delivered, needs clarification, or requires review.

**Public data is synthetic**  
Examples and tests use synthetic public-safe data. The repository is meant to explain structure and behavior, not to publish private materials.

**Structured states are first-class**  
The system treats `needs_clarification`, `cannot_solve`, and `requires_review` as normal outcomes. This is important for urban analysis, where missing conditions and high-risk conclusions are common.

### 7. Response Semantics

UrbanAgent does not collapse every request into a plain text answer. It can return explicit states that are easier for an upper service or review workflow to handle:

- `answer`: the request can be answered with available evidence and tool outputs.
- `needs_clarification`: important input is missing.
- `cannot_solve`: the current public snapshot or current tools cannot solve the task reliably.
- `requires_review`: a result can be drafted but should be reviewed before delivery or writeback.
- `writeback_allowed`: the result satisfies policy and can enter later long-term state.
- `writeback_blocked`: the result should not be written because evidence, confidence, or risk conditions are insufficient.

### 8. Public Release Scope

The public release was reduced and sanitized before publication. The following categories are excluded:

- Personal paths, local environment information, and machine-specific configuration.
- Private repository names, branch names, and internal commit identifiers.
- Raw documents, extracted document text, historical samples, and generated datasets.
- Runtime artifacts, caches, audit files, long-term memory files, and intermediate results.
- Model credentials, service credentials, external service endpoints, and environment-specific settings.
- Internal notes containing operational context that is not needed for public understanding.

The repository keeps only public-safe architecture notes, core interfaces, minimal source code, examples, and tests.

### 9. Running the Public Snapshot

Run the tests:

```bash
python -m pytest -q
```

Run the basic workflow example:

```bash
python examples/basic_workflow.py
```

Run the spatial workflow example:

```bash
python examples/spatial_workflow.py
```

These commands use only synthetic data included in the public snapshot.

### 10. Suggested Extension Points

- Replace the in-memory retriever with vector, keyword, knowledge-base, or hybrid retrieval.
- Connect the spatial tool layer to a GIS engine, spatial database, remote-sensing layer service, or custom analysis script.
- Replace deterministic planning with model-assisted planning or example-guided decomposition.
- Add stronger verification for evidence coverage, spatial consistency, and uncertainty.
- Connect `requires_review` to a human review interface.
- Expand evaluation scenarios and regression checks.
- Wrap the stable schemas with an upper API or workbench interface.

### 11. Current Status

This repository contains a sanitized, runnable, structured source snapshot. It demonstrates the main design of UrbanAgent but is not a direct copy of the full private engineering workspace. Any future source, example, or documentation release should be reviewed module by module before publication.
