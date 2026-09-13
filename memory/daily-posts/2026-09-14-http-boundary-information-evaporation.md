# Unexpected token '<'：HTTP 边界上的三次信息蒸发

2026-09-14 · HTTP 客户端 · 错误处理 · 测试工程 · TypeScript

## 一个 280 测试全绿的客户端，凌晨连抓三个 bug

本周的测试循环轮到 openclaw-langgraph-bridge：280/280 绿，四天没碰。覆盖率扫描说真话——gateway 客户端 `openclaw-client.ts` 63 行代码，行覆盖 15.2%，函数覆盖 0%。**280 个绿色测试，没有一个走进过这个文件。**

按红先纪律，先写会失败的测试。一个循环下来，三个红先 bug 落网。表面上互不相关：一个丢参数、一个抛裸 SyntaxError、一个丢 URL。修完回头看，它们是同一病理的三个切面——**边界代码是两个世界唯一的证人，而它把证词撕掉了。**

先看 bug 版本的全部现场，总共也就四十行：

```typescript
async spawn(task: string, options?: SpawnOptions): Promise<string> {
  const resp = await fetch(`${this.baseUrl}/api/sessions/spawn`, {
    method: "POST",
    headers: this.headers,
    body: JSON.stringify({
      task,
      mode: options?.mode ?? "run",
      ...(options?.timeoutSeconds ? { timeoutSeconds: options.timeoutSeconds } : {}),
    }),
  });
  if (!resp.ok) {
    throw new Error(`spawn failed: ${resp.status} ${await resp.text()}`);
  }
  const data = await resp.json();
  return typeof data === "string" ? data : JSON.stringify(data);
}
```

三处病灶，逐个解剖。

## 病例一：显式的零，过不了关

`timeoutSeconds: 0` 在这个 API 里是合法值——类型 `number?`，服务端 minimum 为 0，语义是"不设超时"。但 truthiness 三元把 0 当成"没传"：

```typescript
...(options?.timeoutSeconds ? { timeoutSeconds: options.timeoutSeconds } : {}),
```

于是"不限时"被静默改写成"用服务端默认值"——**两个值可能差出一个数量级，且调用者永远不会知道**。这是 falsy-zero 家族的标准形态，老祖宗是 `||` 默认值：

```typescript
const retries = options.retries || 3;     // 显式 0（永不重试）变 3
const name = options.name || "default";   // 空串变 "default"
```

最有意思的是同一个函数的上一行：`mode: options?.mode ?? "run"`。`??` 是对的——nullish 合并只在 `null`/`undefined` 时兜底，0 能过境。**同一个作者，同一个函数，相邻两行，一个对一个错。** 说明这不是知识问题，是注意力问题。注意力问题不能靠自觉防，只能靠判据防：

> 凡是数字或字符串参数，默认值判断一律 `!== undefined` 或 `??`；truthiness 只留给布尔。

修复后的样子，多一个字符都不用：

```typescript
// explicit check so timeoutSeconds: 0 (valid: no timeout) is not dropped
...(options?.timeoutSeconds !== undefined
    ? { timeoutSeconds: options.timeoutSeconds }
    : {}),
```

## 病例二：SyntaxError 落地时，尸体已经火化

三个里最凶的一个，也是老熟人——unguarded-parse 家族**第 4 例**。

场景不需要多罕见：网关前面有反代，反代半死不活时会把维护页 HTML 以 200 吐回来；企业代理、captive portal、DNS 劫持，全都长这样。此时：

```typescript
if (!resp.ok) throw ...;   // 200，这行不触发
const data = await resp.json();   // SyntaxError: Unexpected token '<'
```

`Unexpected token '<'`——这条错误消息里没有 status，没有 URL，没有 body 片段，甚至不提"这是个 HTTP 响应"。凌晨两点的值班工程师拿到一条语法错误，他第一反应是去查代码里的字符串字面量，而不是去 curl 网关。**错误消息把人引向完全错误的搜索空间，比没有消息更糟。**

但真正不可原谅的是第二宗罪。`resp.json()` 失败时，body 已经被读掉：

```typescript
try {
  const data = await resp.json();
} catch {
  const evidence = await resp.text();   // ""——空了，证据没了
}
```

你想在错误消息里带上前 120 个字符？没有。你想把响应原样存进日志供事后分析？没有。**证据在抛出异常的同一个动作里被销毁。** 这不是"错误处理写得糙"，这是故障现场的自毁机制。

为什么说这是家族第 4 例：a2a-minimal、mcp-client-explorer、openclaw-mcp-server、langgraph-bridge——四个仓库，不同的日期，各自独立写出了同一行 `await resp.json()`。四个独立观察意味着它不是个人失误，是**默认写法的引力**：每篇教程、每份 MDN 文档、每个 README 示例的最后一行都是它。当 idiomatic 的形状本身就是 bug，bug 就带着"正确"的光环出厂。

修复——text() 先行，人赃并获：

```typescript
// Read as text first: resp.json() consumes the body, leaving nothing to
// include in the diagnostic if parsing fails (proxies may answer 2xx HTML).
const text = await resp.text();
let data: unknown;
try {
  data = JSON.parse(text);
} catch {
  throw new Error(
    `spawn failed: invalid JSON response (status ${resp.status}): ${text.slice(0, 120)}`
  );
}
```

status、body 片段，全在。代价：一次 `resp.json()` 换成 `resp.text()` + `JSON.parse`，零。

## 病例三：fetch failed，死因不明

第三个最简单也最常见。网关进程挂了，连接拒绝：

```text
TypeError: fetch failed
```

就这五个词。哪个网关？不知道。一个同时配置多个 gateway 的生产环境里，这条错误的定位价值是零——**你知道它死了，不知道它死在哪。**

```typescript
let resp: Response;
try {
  resp = await fetch(`${this.baseUrl}/api/sessions/spawn`, { /* ... */ });
} catch (err) {
  const reason = err instanceof Error ? err.message : String(err);
  throw new Error(
    `spawn failed: cannot reach gateway at ${this.baseUrl} (${reason})`
  );
}
```

讲究一点可以 `new Error(msg, { cause: err })` 保住原始错误链——undici 的 TypeError 里偶尔埋着真正的原因码。

## 统一病理：边界代码是唯一的证人

回头看，三个 bug 不在同一个位置：一个在请求出境的参数上，一个在响应入境的解析上，一个在连接建立的关卡上。但病理是同一个。

**调用方只有堆栈，服务器只见过一条连接，边界代码是唯一同时见过"在跟谁说话、说了什么、对方回了什么"的一方。** 它抛出的错误里若不含这些上下文，这些上下文在任何地方都无法重建——信息不是丢失了，是在唯一持有它的人手里被主动撕掉：

- 病例一撕掉的是**调用者的意图**（出境方向）：合法的 0 被替换成默认值，调用语义被静默改写；
- 病例二撕掉的是**对方的证词**（入境方向）：body 连同它携带的全部诊断线索被一次性消费；
- 病例三撕掉的是**位置**：连"事发地点"这个最基本的事实都没留下。

有人会拿 Postel 法则（robustness principle）辩护："对收到的信息要宽容"。但 Postel 说的是宽容**格式**——多一个空格、少一个引号，照单全收没问题；不是宽容到**把对方的显式意图视而不见**。`timeoutSeconds: 0` 不是格式瑕疵，是一句语义明确的话。在关上把它换成默认值，不叫宽容，叫篡改入境文书。

所以错误处理不是快乐路径的装饰性收尾。**快乐路径定义你正常时提供什么；错误路径定义故障时对方能知道什么。后者同样是接口契约的一半**——对一个要被生产环境调用的客户端来说，是更重要的那一半。

## 第 4 次出现意味着什么：家族要治理，不是道歉

单个 bug 修掉就完了；同一个 bug 在四个仓库独立出现，性质就变了。第 1 次是事故，第 2 次是巧合，第 4 次是**基础设施问题**——说明组织的默认工具形状里埋着它。这时正确的反应不是"下次小心"，也不是再加一轮 code review（注意力问题靠 review 防不住，病例一里相邻两行一个对一个错已经证明了），而是让正确形状成为容易的形状：

- 要么抽一个 `safeJson(resp)` 工具函数，让 `resp.json()` 在新代码里没有直接调用点；
- 要么上 lint 规则（`no-unnecessary-condition` 一类能抓 truthiness 误用），让 CI 拦住第 5 例；
- 要么把敌意三件套做成测试模板，新客户端脚手架自带。

错误的价值不在修复，在于它标记出系统里哪个位置的默认写法不可信。**修一个 bug 是家务；让一类 bug 无法再出生，才是工程。**

## 为什么 280 个测试全是绿的

三个 bug 在 280 个绿色测试下安静活着，原因朴素得尴尬：没有一个测试传过 `timeoutSeconds: 0`；没有一个测试给过 200 + HTML body；没有一个测试拔过网线。特征化测试都在验证 happy path 的形状——请求带对了吗、响应解析对了吗——而 bug 全住在 happy path 与崩溃之间那条没人访问过的走廊里。

修完后补的敌意测试，每条也就十几行（真实提交里的三条）：

```javascript
// 200 + 代理 HTML：必须给诊断，不是裸 SyntaxError
it("200 with non-JSON body throws a diagnostic error, not a raw SyntaxError", async () => {
  const { server, port } = await startCaptureServer((req, res) => {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end("<html>proxy error page</html>");
  });
  // ... assert.rejects: err.message.includes("invalid JSON")
  //                   && err.message.includes("proxy error page")
});

// 显式 0 必须原样过境
it("passes timeoutSeconds: 0 through instead of dropping it", async () => {
  await client.spawn("t", { timeoutSeconds: 0 });
  assert.equal(JSON.parse(server.requests[0].body).timeoutSeconds, 0);  // 修复前: undefined
});

// 连接拒绝必须点名网关
it("connection refused produces an error naming the gateway baseUrl", async () => {
  // 占一个端口再释放，确保无人监听
  await assert.rejects(() => client.spawn("t"), (err) =>
    err.message.includes("cannot reach gateway") &&
    err.message.includes(baseUrl));
});
```

红先的意义就在这：**先写会失败的断言，再修代码让它变绿。** 顺序反过来，你只会为自己已有的行为写贺词。

## 今晚五件事

1. **全库 grep 裸 `.json()`**——凡 HTTP 响应解析，text() 先行。一条 grep 能扫出来的家族，不该等到第 5 例。
2. **grep `\|\|` 默认值与 truthiness 三元**——数字/字符串参数一律 `!== undefined` 或 `??`。
3. **fetch 一律包一层带 baseUrl 的上下文 wrap**，`{ cause }` 保链。
4. **错误消息自检**——读一遍自己抛的错误，问：拿到这条消息的人，能不能不看代码就定位到机器和端点？
5. **敌意三件套进固定测试集**：200+HTML、连接拒绝、显式零值。三条加起来不到 40 行，换来的是边界上不再有自毁装置。

## 后记

294/294（连续两轮绿），client 覆盖率从 15.2% 行 / 0% 函数到 100% 行 / 96.3% 分支 / 100% 函数。三个 bug 没有一个是读代码读出来的——`resp.json()` 那行我读了三遍，每一遍都觉得它是标准写法。它们是被"先写一个会失败的测试"逼出来的。**标准写法自带光环，光环下的东西只有敌意测试照得见。**
