# 零个工人，提前完工——无效配置的四种静默死法

> 2026-10-03 · TypeScript / 软件工程 / LLM 代码质量
> 前篇：《活干完了，状态说它失败了——Agent 工作流的状态谎言与对账式运维》(2026-10-02)

## 一、案发现场：十二个红灯，一个家族

一个闲置了两个半月的 TypeScript 库（langgraph-bridge，25 个源码模块、261 个测试），我最近用红先行的循环给它做了四轮体检：每轮先写会失败的测试、确认它真的红、再修到绿。四个循环共加了 19 个测试，其中 12 个首跑即红——库里真实潜伏着 12 个可复现的行为缺陷。

修完回头归类，发现它们不属于"判断写错"或"边界差一"，而是共享同一段 DNA：**配置参数落进"类型合法但业务无意义"的区间时，代码不报错，而是带着无效配置继续跑，产出一个看起来正常的结果。**

上一篇讲的是汇报层怎么骗你（活干完了，状态说它失败了）；这一篇讲执行层怎么骗你——骗得更彻底，因为它连状态都不给你看。

## 二、四宗罪（全部真实代码）

### 1. batch：零个工人的圆满

`batch()` 接收一组节点函数并发执行，配置项 `concurrency: number?`，默认 Infinity。旧实现的核心：

```ts
const { nodes, concurrency = Infinity } = config;
// ...
const limit = Math.min(concurrency, nodes.length);
const workers = Array.from({ length: limit }, () => runNext());
await Promise.all(workers);
return { merged, completedCount: results.length };
```

现在传入 `concurrency: 0`。类型检查通过——0 是 number。`Math.min(0, 5)` 得 0，`Array.from({length: 0})` 得空数组，`Promise.all([])` 立即 resolve，函数返回 `{ completedCount: 0 }`：**一个节点都没执行，汇报圆满完成。**没有异常、没有日志、没有警告；NaN 同理。在监控面板上，这是一片祥和的绿色。

### 2. throttle：同一个函数，两种死法

限流器 `throttle(node, { limit, windowMs })` 的入队条件是 `timestamps.length < config.limit`。传入 `limit: 0`：`0 < 0` 永假，每个调用都进队列等释放——而释放走的也是同一个永假表达式。**永久死锁**，调用方挂在 await 上直到进程被杀。

更妙的是 `windowMs: 0`：窗口清理每次都把时间戳清空，入队条件恒真——**限流器退化成直通车**，本该拦下的调用一个不拦。同一个函数、两种参数、两种死法：一个卡死你，一个放走一切。类型 `number` 对这两者都点头放行。

### 3. withRetry：throw undefined

重试器的契约写在文档注释里："If all attempts fail, throws the last error."

```ts
let lastError: unknown;
for (let attempt = 1; attempt <= maxAttempts; attempt++) {
  try { return await node(state); }
  catch (err) { lastError = err; /* ...backoff... */ }
}
throw lastError;
```

传入 `maxAttempts: 0`：循环体一次都不执行，`lastError` 保持 undefined，函数 **`throw undefined`**。调用方写 `catch (e) { log(e.message) }`，当场 TypeError。最讽刺的是：一个重试器，自己违反了自己的契约——什么都没尝试，也谈不上"最后一次错误"。

### 4. withTimeout：消息匹配吞掉真错误

超时包装器需要区分"超时了"和"节点自己抛错"，旧实现用字符串匹配：

```ts
catch (err: any) {
  if (err.message?.includes?.("timed out")) {
    return { ...fallbackState, _timeoutError: err.message };
  }
  throw err;
}
```

上游错误完全可能合法地包含这个子串：节点内部 `fetch` 失败，错误消息是 "connect timed out at gateway"——一个真实的外部故障，被 `includes` 判定为"超时"，吞进降级状态，节点带着 fallback state "成功"返回。**错误不是被处理了，是被蒸发 了。**

修法是哨兵类 + instanceof：超时是"我们抛的那个类的实例"，而不是"一段恰好长这样的字符串"。**消息内容不是类型，字符串匹配是错误分类的赝品机制。**

```ts
class TimeoutError extends Error {
  constructor(ms: number) { super(`Node timed out after ${ms}ms`); }
}
// reject(new TimeoutError(ms)) ...
if (err instanceof TimeoutError) { /* 真超时，走降级 */ }
```

## 三、家族在传播

这不是一个仓库的特例。同一套体检循环跑过的工作区里，同族病例还有：

- **skill-doctor CLI**：flag 拼错不报错，参数静默丢失，行为悄然改变；
- **gateway client**：`timeoutSeconds: 0` 是 falsy，被 `||` 默认值悄悄吃掉——本想禁用超时，结果配了个默认值；
- **npm scripts 自递归**：`"test": "npm test --"` 看起来是测试脚本，实际是无限循环，`npm install` 时 core dump。

行业也早交过学费。Kubernetes 的 API server 长期默认 Warn 模式：manifest 里 `spec.replicas` 拼成 `spec.replics`，字段被**静默剪掉**——dry-run 干净、apply 成功、你的改动从未发生。kubectl 如今默认发送 `fieldValidation=Strict`，就是被这类事故教育出来的；第三方客户端只要忘了带这个参数（Headlamp 到 2026 年 8 月还挂着这个 issue），就重新裸奔。Python 的 requests 库则因为"无默认 timeout、挂到天荒地老"在文档里专门加粗警告。

## 四、为什么 AI 写的代码偏爱这条路

这些库大多在 AI 编码循环里生长。回头看，它们偏爱这条路径不是偶然：

1. **快乐路径心智**。模型学的是"正确使用"的代码：concurrency 总是 8 或 16，maxAttempts 总是 3。无效值在训练分布里近乎不存在，生成的防御自然也轮不到它。
2. **礼貌默认值审美**。`Math.min`、`?? 3`、`.includes`——每一行读起来都很"防御性"，实际上一个都没防。礼貌不是防线，只是礼貌。
3. **类型系统的盲区**。TypeScript 的 `number` 包含 NaN、Infinity 和一切实数；`optional number` 意味着调用方传什么都合法。**业务不变量（limit ≥ 1）住在类型外面**，得自己写岗哨。
4. **失败的形态变了**。这个家族的失败不是 exception——是一个合法值（0、undefined、false、空数组）流经正常控制流。try/catch 抓不到，日志打不出，APM 看不见。

## 五、防线：把校验搬回构造期

四个 bug 的修复点惊人一致：都不在使用处，而在工厂函数体的最前面。**错误配置应该在对象被创建的那一刻爆炸，而不是在第十次调用时静默堕落。**

```ts
export function batch(config: BatchConfig) {
  const { name, nodes, concurrency = Infinity } = config;
  if (concurrency !== Infinity &&
      (!Number.isFinite(concurrency) || concurrency < 1)) {
    throw new RangeError(
      `batch("${name}"): concurrency must be >= 1 or Infinity, got ${concurrency}`);
  }
  // ...
}
```

注意 `concurrency` 允许 Infinity 而 `throttle` 的 `limit` 不允许——**每个 API 合法值的边界是它自己的业务决策，校验的形状跟着契约走**，而不是套一个万能帮手。比帮手更值钱的是配套的红灯测试，把行为锁死：

```ts
describe("throttle config gates", () => {
  for (const bad of [0, -1, 0.5, NaN]) {
    it(`rejects limit=${bad}`, () => {
      expect(() => throttle(node, { limit: bad, windowMs: 1000 }))
        .toThrow(RangeError);
    });
  }
  it("rejects windowMs=0 (silent no-op)", () => {
    expect(() => throttle(node, { limit: 1, windowMs: 0 }))
      .toThrow(RangeError);
  });
});
```

红灯先行在这里有额外价值：先确认测试在旧代码上真的红，再修绿——保证你测的是 bug 本身，而不是测试自己的拼写错误。

## 六、带走三条

1. **每个数值参数追问一句**：它落在 0、负数、NaN 时，控制流走到哪？顺着追到第一个使用点为止。`Array.from({length: 0})` 和 `for (i=1; i<=0)` 都会"合法地"什么都不做。
2. **消息内容不是类型**：错误分类一律 instanceof / 哨兵对象，永不 `.includes(message)`。
3. **构造期爆炸，运行期免谈**：配置校验写在工厂函数第一行；边界即契约，用红灯测试钉住。

上一篇说，状态字段是缓存，产物才是真相。这一篇是它的地基：**汇报层可以骗你，执行层也可以——零个工人，也能提前完工，只要汇报机制足够礼貌。**对半自主 agent 写出的代码，这道构造期防线不是洁癖，是地板。
