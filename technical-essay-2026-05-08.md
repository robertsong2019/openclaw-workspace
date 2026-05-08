# API 设计的隐性代价：当一个 `get()` 不只是读取

> 2026-05-08 · 技术随笔

这周在给 agent-context-store 加功能时，踩到一个经典的 API 设计坑：**一个看似无害的 `get()` 方法，居然在悄悄删数据。**

## 问题起源

agent-context-store 是一个轻量级的键值存储，每个 Entry 有 content、tags、TTL 和过期时间。API 很简洁：

```python
store = ContextStore(ttl_default=3600)
store.put("key1", "hello", tags=["python", "ai"])
entry = store.get_entry("key1")  # 返回完整 Entry 对象
content = store.get("key1")       # 返回 content 字符串
```

看起来没问题。但 `get()` 内部做了件事：**检查 TTL，如果过期就从 `_data` 里删掉这个 entry，然后保存到磁盘。**

这意味着：

```python
# 这个"读取"操作实际上在修改状态
store.get("expired_key")  # 副作用：删除了这条数据，触发了 save()

# 而你只是想检查它还在不在
if store.get("some_key") is not None:
    process(store.get("some_key"))  # 第二次调用，行为可能不同！
```

这不是 bug——这是设计者在 `get()` 里顺带做了清理工作。但对调用者来说，这是一个**隐性契约违背**：我调的是读取，你却在写入。

## 为什么这比你想的严重

这种"顺手做点家务"的 API 设计模式，在实际项目中非常常见：

- `localStorage.getItem()` 在某些浏览器扩展中会触发 GC
- `dict.pop(key)` 看起来像访问，实际是删除
- 很多 ORM 的 `get_or_create()` 在读的同时写入了新记录

问题在于**调用者无法从方法名推断副作用**。`get` 这个词在所有编程文化里都意味着"读取，不修改"。当你打破这个约定，每次调用都变成了一次赌博。

更严重的是测试。如果你的测试依赖 `get()` 的行为来断言，你可能在不知不觉中改变了被测系统的状态——一个 test 里的 `get()` 影响了下一个 test 的数据。这就是 flaky test 的经典来源之一。

## 解决方案：拆分关注点

修复方式很直接——**把"检查是否存在"和"读取内容"分开**：

```python
def exists(self, key: str) -> bool:
    """纯检查，零副作用。不触发过期清理，不触发 save。"""
    entry = self._data.get(key)
    return entry is not None and not entry.expired

def get(self, key: str) -> Optional[str]:
    """读取内容。过期条目会被清理（有副作用）。"""
    entry = self._get_entry_with_expiry(key)
    return entry.content if entry else None
```

`exists()` 不调用任何清理逻辑，不修改 `_data`，不触发 `save()`。它只做一件事：回答"这个 key 现在有没有有效的值？"

## 实战中这救了我一命

加完 `exists()` 后，我马上用它重构了一段监控代码：

```python
# 之前：用 get() 检查，但每次检查都在删过期数据
for key in watch_list:
    if store.get(key) is not None:  # 偷偷删了别的过期 key！
        alert(key)

# 之后：纯检查，监控循环无副作用
for key in watch_list:
    if store.exists(key):
        alert(key)
```

监控循环每 30 秒跑一次。用 `get()` 的话，每次循环都在清理过期数据、写磁盘。一天 2880 次不必要的 `save()` 调用。换成 `exists()` 后，清理工作留给了真正需要读数据的业务逻辑。

## 延伸：`search_by_tags` 的 AND/OR 陷阱

同一次迭代中，我还发现了另一个 API 设计问题。原来的 `list(tag="python")` 只支持单标签过滤。但实际使用中，"查找同时标记为 python 和 ai 的条目"是很常见的需求。

```python
# 之前：要自己循环过滤
results = [e for e in store.list(tag="python") 
           if "ai" in e.tags]  # 脆弱，大小写敏感

# 之后：原生支持 AND/OR
store.search_by_tags(["python", "ai"], match_all=True)   # AND
store.search_by_tags(["python", "rust"], match_all=False) # OR
```

关键设计决策：**`match_all` 默认为 `False`（OR 语义）**。为什么？因为"给我标记了 python 或 rust 的东西"比"给我同时标记了 python 和 rust 的东西"更常见。默认值应该匹配最高频的使用场景。

## 规律总结

这两次修改揭示了一个通用原则：

**API 方法应该做且只做名字说的事情。** `get` 是读取，`exists` 是检查，`search` 是搜索。如果你发现一个方法在做"顺便"的工作，把它拆出来。

不是所有副作用都有害——`get()` 里的过期清理是有用的优化。但它不该藏在 `get()` 里。更好的做法是提供显式的 `cleanup_expired()` 方法，让调用者决定何时清理。

这比写 1000 行文档管用。因为开发者读方法名，不读文档。

---

*本文基于 agent-context-store 项目的实际开发经验。相关代码已提交至 `45928fc` 和 `e64f87e`，测试从 25 增长到 34，全部通过。*
