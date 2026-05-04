# 常见重构手法 · 前后对比

> 每条都给"信号 / 改前 / 改后 / 注意"。

---

## 1. 内联只有一个调用点的 helper

**信号**:`grep -r "funcName"` 只显示定义点 + 一个调用点。

**改前**:
```ts
function formatUserName(user: User): string {
  return `${user.firstName} ${user.lastName}`;
}

function renderHeader(user: User) {
  return <h1>{formatUserName(user)}</h1>;
}
```

**改后**:
```ts
function renderHeader(user: User) {
  return <h1>{`${user.firstName} ${user.lastName}`}</h1>;
}
```

**注意**:如果 `formatUserName` 这个名字本身就是好文档(替代了注释),保留。

---

## 2. 卫语句替代嵌套 if

**信号**:3 层及以上嵌套,且每层只是为了"满足条件后继续"。

**改前**:
```ts
function process(data: Input | null) {
  if (data) {
    if (data.valid) {
      if (data.items.length > 0) {
        return doWork(data.items);
      }
    }
  }
  return null;
}
```

**改后**:
```ts
function process(data: Input | null) {
  if (!data) return null;
  if (!data.valid) return null;
  if (data.items.length === 0) return null;
  return doWork(data.items);
}
```

---

## 3. 删除单实现 interface

**信号**:`interface Foo` + 唯一 class `FooImpl`,且没有为测试 mock 预留。

**改前**:
```ts
interface UserService {
  getUser(id: string): Promise<User>;
}

class UserServiceImpl implements UserService {
  async getUser(id: string) { /* ... */ }
}
```

**改后**:
```ts
class UserService {
  async getUser(id: string) { /* ... */ }
}
```

**注意**:测试里如果 mock 了 UserService,要保持 mock 仍然可用(类的 mock 也支持)。

---

## 4. 删除墓碑注释

**信号**:注释里说"以前这里有 xxx",或"为了兼容 yyy 保留"。

**改前**:
```ts
// 注:这里以前有 legacyHandler,2024-Q3 删除
// TODO(#123): 等 v2 上线后再优化
function handle(req) {
  // ...
}
```

**改后**:
```ts
function handle(req) {
  // ...
}
```

**注意**:如果 issue #123 还开着且仍有相关性,保留 TODO。

---

## 5. 删除过度防御

**信号**:internal 函数里校验"上游不可能传入"的值。

**改前**:
```ts
// internal helper
function double(n: number) {
  if (typeof n !== 'number') throw new Error('not number');
  if (isNaN(n)) throw new Error('NaN');
  return n * 2;
}
```

**改后**:
```ts
function double(n: number) {
  return n * 2;
}
```

**注意**:边界函数(收 user input、HTTP body、外部 API 响应)的检查**必须保留**。

---

## 6. 抽取重复代码

**信号**:3 段或以上结构相同的代码。

**改前**:
```ts
function audit() {
  log('start audit');
  const start = Date.now();
  const result = doAudit();
  log(`audit done in ${Date.now() - start}ms`);
  return result;
}

function migrate() {
  log('start migrate');
  const start = Date.now();
  const result = doMigrate();
  log(`migrate done in ${Date.now() - start}ms`);
  return result;
}

function backup() {
  log('start backup');
  const start = Date.now();
  const result = doBackup();
  log(`backup done in ${Date.now() - start}ms`);
  return result;
}
```

**改后**:
```ts
function timed<T>(name: string, fn: () => T): T {
  log(`start ${name}`);
  const start = Date.now();
  const result = fn();
  log(`${name} done in ${Date.now() - start}ms`);
  return result;
}

const audit = () => timed('audit', doAudit);
const migrate = () => timed('migrate', doMigrate);
const backup = () => timed('backup', doBackup);
```

**注意**:只有 2 次重复**不要抽**(YAGNI)。

---

## 7. 删除空壳包装

**信号**:函数体只有 `return f(args)`,且没改语义。

**改前**:
```ts
async function getUser(id: string) {
  return userService.getUser(id);
}
```

**改后**:直接用 `userService.getUser(id)`。

**注意**:如果包装提供了"稳定的 API 表面"(比如对外暴露,内部实现可能换),保留。

---

## 8. 收敛类型断言

**信号**:`as any`、`as unknown as Foo` 这种宽松断言。

**改前**:
```ts
const config = JSON.parse(rawConfig) as any;
const port = config.port as number;
```

**改后**:
```ts
type Config = { port: number; host: string };
const config = JSON.parse(rawConfig) as Config;
const { port } = config;
```

**注意**:边界处(JSON.parse / 网络响应)的断言要配合校验(zod / valibot 等)。本步骤只是减少 `any`,不是把校验完全省掉。

---

## 9. 合并重复的常量

**信号**:多个文件定义了同名同值常量。

**改前**:
```ts
// a.ts
const MAX_RETRIES = 3;

// b.ts
const MAX_RETRIES = 3;

// c.ts
const MAX_RETRIES = 3;
```

**改后**:
```ts
// constants.ts
export const MAX_RETRIES = 3;

// a.ts / b.ts / c.ts
import { MAX_RETRIES } from './constants';
```

**注意**:语义不同的同名常量**不要合并**(比如 a.ts 的 retries 和 b.ts 的 retries 实际是不同业务,只是巧合相同值)。

---

## 10. 删除已无调用方的 兼容垫片

**信号**:`legacyXxx`、`oldYyy`、注释 "保留兼容性"——但 grep 后发现没人调了。

**改前**:
```ts
// 兼容旧版调用方,2024-Q1 后所有调用方已迁移到 newApi
export function legacyApi(opts: OldOpts) {
  return newApi(convertOpts(opts));
}
```

**改后**:删除整个函数 + `convertOpts` helper(若也无人用)。

**注意**:如果是公共 npm 包,需走 deprecation cycle,**不要直接删**。

---

## 改动顺序建议

建议按以下顺序在一次会话里推进,每步跑一次验证:

```
1. P0.2 未使用导入       (最安全,风险最低)
2. P0.1 未使用导出       (跨文件 grep 确认)
3. P0.3 未使用参数/变量  (linter 辅助)
4. P0.4-5 死分支/死函数  (注意可能被反射调用)
5. P0.7 兼容垫片        (确认无调用方)
6. P0.8 过期注释        (纯清理)
7. P1 系列               (单实现 interface、空壳等)
8. P2 系列               (谨慎,只在确实更清晰时做)
```
