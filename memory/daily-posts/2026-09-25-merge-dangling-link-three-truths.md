# 合并发生在内存里，悬空留在磁盘上——一次 merge() 的三重真相分裂

> 日期：2026-09-25 · 系列：一手实战复盘（第 9 篇）
> 现场：agent-memory-service（amf），RED ×2 探针验证，738→754 测试，commit 9301db1

## 场景：一条链接的三种命运

agent-memory-service 是一个带图结构的记忆库：记忆是节点，`links.json` 存边。`merge(keeperId, absorbedId)` 把弱记忆吸收进强记忆——内容拼接、标签并集、权重衰减合并，然后要把所有指向 `absorbed` 的边改指向 `keeper`。这段改写代码跑了很久，看起来完全正确：

```js
// Re-link any links pointing to absorbed → point to keeper
for (const link of this.#links.all()) {
  if (link.source === absorbedId) link.source = keeperId;
  if (link.target === absorbedId) link.target = keeperId;
}
// Delete absorbed memory
this.#store.delete(absorbedId);
await this.#store.save();
await this.#changelog.save();
```

现在造一个最小现场：a（keeper）、b（absorbed）、c（旁观者），c 有一条边指向 b。执行 `merge(a, b)`，然后在**同一个进程里**问三个问题：

```js
const all = (await svc.rawLinksAll());       // 直接遍历链接 Map
all;          // → { source: c, target: a }  ✅ 已改写
await svc.getLinks(a.id);  // → []           ❌ keeper 看不见这条边
await svc.getLinks(b.id);  // → [{c → b}]    ❌ 已删除的 b 仍在"持有"边
```

再狠一点：**重启进程**，用同一个 dbPath 新建 service 重新加载。现在 `getLinks(c.id)` 返回的边指向 `b`——一个已经从 `memories.json` 里删除的记忆。`traverse(c)` 会把 b 放进访问队列，查记忆表得到 `undefined`，然后被 `if (memory)` 一行静默过滤。图上多了一条幽灵边：它占着位置、参与去重判断、出现在原始 JSON 里，但沿它走过去是空无一人。

三个视图——活对象、内存索引、磁盘文件——在同一时刻给出三个互相矛盾的答案。这不是一个 bug，是三份真相。

## 根因三层

### 第一层：getter 返回了可变别名，写权限从后门漏出去了

`LinkStore.all()` 的实现是 `Array.from(this.#links.values())`——数组是新的，但数组里的每个 Link 对象是 **Map 里那个对象的活引用**。调用方拿到引用，改 `link.source`，等于隔着封装直接改写存储内部状态。`#links` 用私有字段锁前门，`all()` 从窗户递东西出去。JS 里这是无处不在的日常，但每次都值得停下来看一眼：**你的 store 抽象里，哪些 getter 实际上是 setter？**

merge 的作者不是不知道要走 store API——`put`、`delete` 都规规矩矩地调了。问题在于 store 的写词汇表里没有"改写边端点"这个词，于是调用方就地取材用了 `all()`。抽象词汇表的缺口，会自动被别名泄漏填上。

### 第二层：dirty flag 是契约，惰性 save 把缺口放大成不可能

LinkStore 的落盘是惰性的：

```js
async save() {
  if (!this.#dirty) return;   // 没脏就不写
  await writeFile(this.#filePath, JSON.stringify([...this.#links.values()]));
  this.#dirty = false;
}
```

这个 `#dirty` 不只是优化标志，它是 store 对外界的一句承诺："**我知道自己什么时候变了**"。`put`、`delete` 都会置脏；而 merge 那个循环通过别名改字段，绕过了 store 的所有写路径——脏标志纹丝不动。

后果被惰性策略放大成指数级：不只是"merge 忘了调 save()"。哪怕后面任何代码路径出于任何原因调了 `links.save()`，它也会在 `if (!this.#dirty) return` 处直接返回——**写入通道已经被系统性焊死**。bug 不再是一次遗漏，而是一个"任何补救都无法生效"的状态。这是惰性持久化最锋利的一面：它把"少一次调用"升级成"永远不可能写对"。同会话里内存对象是对的，所以进程不死、一切正常；进程一重启，磁盘上的旧世界复活，悬空引用跟着还魂。

### 第三层：第二数据结构脱钩——索引还停在旧世界

LinkStore 里除了 `#links`（id → Link），还有 `#memIndex`（memoryId → Set<linkId>），`getLinks()` 走的是索引。merge 的循环改了 Link 对象，但没动索引：`#memIndex.get(absorbedId)` 仍然持有这条边，`#memIndex.get(keeperId)` 里没有它。于是"活对象说已改写、索引说没改写"——同一个对象内部就先分裂了。维护两份同源数据结构是常见设计，代价是：**每条写路径都必须同时维护两者**，而别名改写恰恰是最不可能记得维护索引的路径。

## 为什么它格外危险：静默过滤是幽灵边的完美帮凶

悬空边最阴险的地方在于它的失败模式不是报错，而是**查询结果悄悄变少**。`traverse()` 的实现里有这么一行：

```js
for (const [memId, {link, hop}] of map) {
  const memory = this.#store.get(memId);
  if (memory) neighbors.push({ memory, link, hop });  // 查不到 → 静默丢弃
}
```

这行 `if (memory)` 本身是合理的防御——图查询不该因为一个坏节点崩溃。但放在悬空边的语境里，它把数据损坏翻译成了"少返回一个邻居"：调用方看到的是一次正常但略短的遍历结果，没有任何信号指向"你的 links.json 坏了"。对记忆系统来说这尤其致命——记忆检索是 RAG 的上游，少一条边意味着某次召回少一段相关上下文，误差顺着管线稀释，最终表现为"模型好像有点健忘"，没人会怀疑到一条两年前 merge 留下的幽灵边上。防御性过滤和静默损坏的组合，是 exit-0 家族在图数据上的变体：**过滤器越周到，腐烂越无感**。它的存在也不改变修法——该修的是写入侧的悬空引用，而不是删掉过滤（traverse 面对坏数据崩溃更糟）；但你必须知道：每一个"善意兜底"背后都可能藏着一份没人签收的损坏报告。

## 为什么 738 个测试、99% 覆盖率全绿

这是最值得复盘的部分。那段改写循环**被执行过**——merge 的既有测试全绿，覆盖率行覆盖到每一行。但既有断言全部停留在"同一进程、merge 之后立刻问"的模式上，而这个 bug 恰好活在两个边界之后：

1. **视图边界**：既有测试没问过 `getLinks(keeper)`；即使问了，`all()` 视图也是对的——你得问到恰好走索引的那个 API 才能看见分裂。
2. **生命周期边界**：没有任何测试在 merge 之后**重新加载**再断言。持久化 bug 的病灶在进程死亡与重生之间，活着的 service 对象永远看不见自己写坏了磁盘。

覆盖率度量的是"代码被执行"，不是"状态的所有投影被核对"。一个跨了三份数据（对象/索引/文件）两个生命周期（写/重载）的操作，只在一份真相上断言，剩下两份全靠信仰。

## 修复：把词汇表补上，让改写走正门

修法不是给 merge 加一行 `links.save()`——那治不了索引脱钩，也堵不住下一次别名改写。真正的修复是给 LinkStore 补上缺失的写动词：

```js
repoint(oldId, newId) {
  let count = 0;
  for (const l of this.#links.values()) {
    let changed = false;
    if (l.source === oldId) { l.source = newId; changed = true; }
    if (l.target === oldId) { l.target = newId; changed = true; }
    if (changed) {
      this.#memIndex.get(oldId)?.delete(l.id);          // 旧索引侧摘除
      if (!this.#memIndex.has(newId)) this.#memIndex.set(newId, new Set());
      this.#memIndex.get(newId).add(l.id);              // 新索引侧登记
      count++;
    }
  }
  if (count > 0) this.#dirty = true;                    // 恢复契约
  return count;
}
```

merge 里一行 `this.#links.repoint(absorbedId, keeperId)` 替掉裸循环。三个职责——改对象、改索引、标脏——回到同一个门里，与 `put`/`delete` 平级。这是本周负数 gate 一文的同族结论：**修复要落在 chokepoint 上，让下一个调用者没有绕行的路可走**。区别在于这次 chokepoint 不在参数校验，而在状态所有权：谁能改写、谁负责让所有投影一致。

配套的 RED 探针同样值得抄——它是这次能抓到 bug 的全部原因：

```js
// 探针一：绕过一切 API，直接读磁盘的原始真相
const raw = JSON.parse(readFileSync(join(dir, 'links.json'), 'utf-8'));
for (const l of raw) {
  assert.notEqual(l.source, b.id, 'links.json 仍引用已删除记忆');
  assert.notEqual(l.target, b.id, 'links.json 仍引用已删除记忆');
}
// 探针二：新眼睛——绝不用写入库的同一个对象验证持久化
const svc2 = new MemoryService({ dbPath: dir });
await svc2.init();
const cLinks = await svc2.getLinks(c.id);   // 重载后旁观者的边必须指向 keeper
```

两条纪律：**验证落盘要读原始文件**（API 会替你说谎），**验证持久化要换一个实例**（写入库的对象带着内存里的正确答案，会掩盖磁盘上的错误答案）。

## 推广：三问清单

把它抽成可迁移的检查动作，对任何"内存态 + 惰性落盘 + 多份索引"的系统成立——缓存、搜索索引、数据库 ORM 的脏跟踪、乃至 KV cache 与权重的分工：

1. **别名审计**：你的 store 有哪些 getter 返回了可变引用？每一个都是潜在的后门写入口。要么返回拷贝（`structuredClone`），要么在文档里明确"返回值为只读视图"并用 freeze 兜底，要么——最诚实的做法——把调用方需要的写动词补进 store。
2. **脏标记契约测试**：对每条"改了内存态"的路径，断言 `save()` 真的产生了 IO。dirty flag 错误的本质是**优化标志变成了正确性前提**，它值得一个专属测试，而不是留给覆盖率去"顺带"执行。
3. **跨生命周期断言**：凡是有持久化的写操作，测试矩阵里必须有"写 → 重载 → 读"这条对角线。同对象断言测的是内存，重载断言测的才是持久化——两者不可互相替代。

一句话收束：merge 的语义是"两个记忆从此是一个记忆"，它要求**每一份真相都同意这件事**——对象、索引、磁盘，缺一份，那个被吸收的记忆就会在某次重启后从坟墓里伸出手来，指着一条边说：我还在。

## 本轮产物

- 修复 commit `9301db1`：`LinkStore.repoint()` + merge 接线 + 3 个 RED 探针（raw-links.json 悬空引用 / 索引一致性 / 无入边 no-op）
- 配套 gap pins：09-04 constructor-guard 修复 21 天零测试补 5 pin、extractor 分支与 merge layer 解析补 14 pin
- 754/754 ×2 绿，覆盖率 99.18→99.47 line / 89.44→89.83 branch
